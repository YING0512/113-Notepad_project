import tkinter as tk
from tkinter import messagebox
import datetime
import time
from threading import Thread
from tkcalendar import DateEntry
import os

class Todo:
    def __init__(self, root, mode_day=False):
        self.root = root
        self.mode_day = mode_day
        self.tasks = []
        self.reminders = []

        # Colors
        self.white = "#ffffff"
        self.black = "#000000"
        self.darkBG1 = "#2d2f32"
        self.darkBG2 = "#3f4145"
        self.darkactive = "#4c4e52"
        self.brightBG1 ="#c0c0c0"
        self.brightBG2 ="#dfdfdf"
        self.brightactive = "#f1f0f2"

        self.current_time = datetime.datetime.now()
        self.next_minute = (self.current_time + datetime.timedelta(minutes=1)).strftime("%M")
        # Frame for the input section
        self.input_frame = tk.Frame(self.root, bg=self.darkBG2)
        self.input_frame.pack(pady=10, padx=10, fill="x")
        self.title_txt = tk.Label(self.input_frame, text="標題:", fg=self.white, bg=self.darkBG2, font=(12))
        self.title_txt.pack(side="left")

        # Entry field to add tasks
        self.txt_input = tk.Entry(self.input_frame, width=30)
        self.txt_input.pack(side="left", padx=5)
        
        # DateEntry for selecting date
        self.cal = DateEntry(self.input_frame, width=12, background='darkblue', foreground='white', borderwidth=2, year=2024, date_pattern="yyyy/mm/dd")
        self.cal.pack(side="left", padx=5)

        # Labels and Spinboxes for time selection
        self.time_pick = tk.Label(self.input_frame, text="時間:", fg=self.white, bg=self.darkBG2, font=(12))
        self.time_pick.pack(side="left")
        self.hour_spinbox = tk.Spinbox(self.input_frame, from_=1, to=12, width=2, format="%02.0f")
        self.hour_spinbox.pack(side="left", padx=5)
        self.hour_spinbox.delete(0, 'end')
        self.hour_spinbox.insert(0, (self.current_time + datetime.timedelta(minutes=1)).strftime("%I"))
        self.minute_semicolon = tk.Label(self.input_frame, text=":", fg=self.white, bg=self.darkBG2)
        self.minute_semicolon.pack(side="left")
        self.minute_spinbox = tk.Spinbox(self.input_frame, from_=0, to=59, width=2, format="%02.0f")
        self.minute_spinbox.pack(side="left", padx=5)
        self.minute_spinbox.delete(0, 'end')
        self.minute_spinbox.insert(0, self.next_minute)
        self.ampm_combobox = tk.StringVar(self.root)
        self.ampm_combobox.set(datetime.datetime.now().strftime("%p"))
        self.ampm_optionmenu = tk.OptionMenu(self.input_frame, self.ampm_combobox, "AM", "PM")
        self.ampm_optionmenu.pack(side="left", padx=5)

        # Button to add tasks and set reminders
        self.btn_add_task = tk.Button(self.input_frame, text="建立待辦事項", fg="white", bg="#6CAE75", command=self.add_task)
        self.btn_add_task.pack(side="left", padx=5)

        # Button to delete selected task
        self.btn_delete_task = tk.Button(self.input_frame, text="刪除選定事項", fg="white", bg="#EF5350", command=self.delete_task)
        self.btn_delete_task.pack(side="left", padx=5)

        # Listbox to display tasks
        self.lb_tasks = tk.Listbox(self.root, width=60, height=15)
        self.lb_tasks.pack(pady=10, padx=10, fill="both", expand=True)

        # Load tasks from file
        self.load_tasks_from_file()
        self.update_listbox()

        # Start a new thread to monitor reminders
        self.thread = Thread(target=self.check_reminders, daemon=True)
        self.thread.start()

    def toggle_mode(self, mode_day):
        # Change color
        self.mode_day = mode_day
        if self.mode_day:
            self.currentbg_color = self.darkBG2
            self.currentfg_color = self.white
            self.currentactive_color = self.darkactive
        else:
            self.currentbg_color = self.brightBG2
            self.currentfg_color = self.black
            self.currentactive_color = self.brightactive

        self.input_frame.config(bg=self.currentbg_color)
        self.minute_semicolon.config(bg=self.currentbg_color)
        self.title_txt.config(bg=self.currentbg_color, fg=self.currentfg_color)
        self.time_pick.config(bg=self.currentbg_color, fg=self.currentfg_color)
        
    # Function to update the listbox with tasks
    def update_listbox(self):
        self.lb_tasks.delete(0, "end")
        sorted_tasks = sorted(self.tasks, key=lambda x: (x['date'], x['time'], x['title']))
        for task in sorted_tasks:
            task_text = f"{task['date']} {task['time']} {task['title']}"
            self.lb_tasks.insert("end", task_text)

    # Function to add a task and set a reminder
    def add_task(self):
        task_title = self.txt_input.get()
        if task_title:
            task_date = self.cal.get_date().strftime("%Y/%m/%d")
            task_hour = int(self.hour_spinbox.get())
            if self.ampm_combobox.get() == "PM" and task_hour != 12:
                task_hour += 12
            elif self.ampm_combobox.get() == "AM" and task_hour == 12:
                task_hour = 0
            task_time = f"{task_hour:02d}:{int(self.minute_spinbox.get()):02d}"
            task = {'title': task_title, 'date': task_date, 'time': task_time}
            self.tasks.append(task)
            self.update_listbox()
            self.txt_input.delete(0, "end")
            self.save_task_to_file(task)
            self.set_reminder(task)
        else:
            messagebox.showinfo("提示", "不能輸入空白")

    # Function to set a reminder for a given task
    def set_reminder(self, task):
        reminder_time_str = f"{task['date']} {task['time']}"
        try:
            reminder_time = datetime.datetime.strptime(reminder_time_str, "%Y/%m/%d %H:%M")
        except ValueError:
            messagebox.showinfo("錯誤", "提醒時間格式不正確，請按照 YYYY/MM/DD HH:MM 格式輸入。")
            return
        current_time = datetime.datetime.now()
        if reminder_time <= current_time:
            messagebox.showinfo("錯誤", "提醒時間必須晚於當前時間。")
            return
        self.reminders.append((reminder_time, task['title']))
        messagebox.showinfo("提示", f"提醒時間設定 '{task['title']}' at {reminder_time.strftime('%Y/%m/%d %H:%M')}")

    # Function to delete a selected task
    def delete_task(self):
        selected_index = self.lb_tasks.curselection()
        if selected_index:
            selected_task_text = self.lb_tasks.get(selected_index)
            task_date, task_time, task_title = selected_task_text.split(' ', 2)
            task_to_delete = {'title': task_title, 'date': task_date, 'time': task_time}
            self.tasks.remove(task_to_delete)
            self.update_listbox()
            self.delete_task_from_file(task_to_delete)
            messagebox.showinfo("提示", f"已刪除 '{task_title}'")
    
    # Function to check reminders
    def check_reminders(self):
        while True:
            current_time = datetime.datetime.now()
            for reminder in self.reminders:
                reminder_time, task = reminder
                if current_time >= reminder_time:
                    messagebox.showinfo("提醒", f"'{task}'")
                    self.reminders.remove(reminder)
            time.sleep(1)

    # Function to save task to file
    def save_task_to_file(self, task):
        with open("tasks.txt", "a", encoding='utf-8') as file:
            file.write(f"{task['date']},{task['time']},{task['title']}\n")

    # Function to delete task from file
    def delete_task_from_file(self, task):
        if os.path.exists("tasks.txt"):
            with open("tasks.txt", "r", encoding='utf-8') as file:
                tasks = file.readlines()
            with open("tasks.txt", "w", encoding='utf-8') as file:
                for line in tasks:
                    if line.strip() != f"{task['date']},{task['time']},{task['title']}":
                        file.write(line)

    # Function to load tasks from file
    def load_tasks_from_file(self):
        if os.path.exists("tasks.txt"):
            with open("tasks.txt", "r", encoding='utf-8') as file:
                tasks = file.readlines()
            for line in tasks:
                task_date, task_time, task_title = line.strip().split(',', 2)
                task = {'title': task_title, 'date': task_date, 'time': task_time}
                self.tasks.append(task)

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = Todo(root)
#     root.mainloop()
