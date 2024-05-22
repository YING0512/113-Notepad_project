import tkinter as tk
from tkinter import messagebox
import datetime
import time
from threading import Thread
from tkcalendar import DateEntry

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
        self.brightBG1 = "#e3e5e8"
        self.brightBG2 = "#f7f6f7"
        self.brightactive = "#f1f0f2"

        # Frame for the input section
        self.input_frame = tk.Frame(self.root, bg=self.darkBG2)
        self.input_frame.pack(pady=10, padx=10, fill="x")
        self.title_txt = tk.Label(self.input_frame, text="標題:", fg=self.white, bg=self.darkBG2, font=(12))
        self.title_txt.pack(side="left")

        # Entry field to add tasks
        self.txt_input = tk.Entry(self.input_frame, width=30)
        self.txt_input.pack(side="left", padx=5)
        
        # Frame for time selection
        self.time_frame = tk.Frame(self.root, bg=self.darkBG2)
        self.time_frame.pack(pady=5, padx=10, fill="x")
        
        # DateEntry for selecting date
        self.cal = DateEntry(self.input_frame, width=12, background='darkblue', foreground='white', borderwidth=2, year=2024)
        self.cal.pack(side="left", padx=5)

        # Labels and Spinboxes for time selection
        self.time_pick = tk.Label(self.input_frame, text="時間:", fg=self.white, bg=self.darkBG2, font=(12))
        self.time_pick.pack(side="left")
        self.hour_spinbox = tk.Spinbox(self.input_frame, from_=1, to=12, width=2)
        self.hour_spinbox.pack(side="left", padx=5)
        self.hour_spinbox.delete(0, 'end')
        self.hour_spinbox.insert(0, datetime.datetime.now().strftime("%I"))
        self.minute_semicolon = tk.Label(self.input_frame, text=":", fg=self.white, bg=self.darkBG2)
        self.minute_semicolon.pack(side="left")
        self.minute_spinbox = tk.Spinbox(self.input_frame, from_=0, to=59, width=2)
        self.minute_spinbox.pack(side="left", padx=5)
        self.minute_spinbox.delete(0, 'end')
        self.minute_spinbox.insert(0, datetime.datetime.now().strftime("%M"))
        self.ampm_combobox = tk.StringVar(self.root)
        self.ampm_combobox.set(datetime.datetime.now().strftime("%p"))
        self.ampm_optionmenu = tk.OptionMenu(self.input_frame, self.ampm_combobox, "AM", "PM")
        self.ampm_optionmenu.pack(side="left", padx=5)

        # Button to add tasks and set reminders
        self.btn_add_task = tk.Button(self.input_frame, text="增加待辦事項並設定提醒", fg="white", bg="#6CAE75", command=self.add_task)
        self.btn_add_task.pack(side="left", padx=5)

        # Button to delete selected task
        self.btn_delete_task = tk.Button(self.input_frame, text="刪除選定事項", fg="white", bg="#EF5350", command=self.delete_task)
        self.btn_delete_task.pack(side="left", padx=5)

        # Listbox to display tasks
        self.lb_tasks = tk.Listbox(self.root, width=60, height=15)
        self.lb_tasks.pack(pady=10, padx=10, fill="both", expand=True)

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
        self.time_frame.config(bg=self.currentbg_color)
        self.minute_semicolon.config(bg=self.currentbg_color)
        self.title_txt.config(bg=self.currentbg_color, fg=self.currentfg_color)
        self.time_pick.config(bg=self.currentbg_color, fg=self.currentfg_color)
        
    # Function to update the listbox with tasks
    def update_listbox(self):
        self.lb_tasks.delete(0, "end")
        for task in self.tasks:
            self.lb_tasks.insert("end", task)

    # Function to add a task and set a reminder
    def add_task(self):
        task = self.txt_input.get()
        if task:
            self.tasks.append(task)
            self.update_listbox()
            self.txt_input.delete(0, "end")
            self.set_reminder(task)
        else:
            messagebox.showinfo("提示", "不能輸入空白")

    # Function to set a reminder for a given task
    def set_reminder(self, task):
        reminder_time_str = f"{self.cal.get_date()} {self.hour_spinbox.get()}:{self.minute_spinbox.get()} {self.ampm_combobox.get()}"
        try:
            reminder_time = datetime.datetime.strptime(reminder_time_str, "%Y-%m-%d %I:%M %p")
        except ValueError:
            messagebox.showinfo("錯誤", "提醒時間格式不正確，請按照 YYYY-MM-DD hh:mm AM/PM 格式輸入。")
            return
        current_time = datetime.datetime.now()
        if reminder_time <= current_time:
            messagebox.showinfo("錯誤", "提醒時間必須晚於當前時間。")
            return
        self.reminders.append((reminder_time, task))
        messagebox.showinfo("提示", f"提醒時間設定 '{task}' at {reminder_time.strftime('%Y-%m-%d %I:%M:%S %p')}")

    # Function to delete a selected task
    def delete_task(self):
        selected_index = self.lb_tasks.curselection()
        if selected_index:
            selected_task = self.lb_tasks.get(selected_index)
            self.tasks.remove(selected_task)
            self.update_listbox()
            messagebox.showinfo("提示", f"已刪除 '{selected_task}'")
    
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


if __name__ == "__main__":
    root = tk.Tk()
    app = Todo(root)
    root.mainloop()
