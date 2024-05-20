import tkinter as tk
import tkinter.messagebox
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
        self.title_txt_input = tk.Entry(self.input_frame, width=30)
        self.title_txt_input.pack(side="left", padx=5)

        # Button to add tasks
        self.btn_add_task = tk.Button(self.input_frame, text="增加待辦事項", fg="white", bg="#6CAE75", command=self.add_task)
        self.btn_add_task.pack(side="left", padx=5)

        # Button to delete all tasks
        self.btn_del_all = tk.Button(self.input_frame, text="刪除全部", fg="white", bg="#EF5350", command=self.del_all_tasks)
        self.btn_del_all.pack(side="left", padx=5)

        # Frame for time selection
        self.time_frame = tk.Frame(self.root, bg=self.darkBG2)
        self.time_frame.pack(pady=5, padx=10, fill="x")

        # Labels and Spinboxes for time selection
        self.time_pick = tk.Label(self.time_frame, text="時間:", fg=self.white, bg=self.darkBG2, font=(12))
        self.time_pick.pack(side="left")
        self.hour_spinbox = tk.Spinbox(self.time_frame, from_=1, to=12, width=2)
        self.hour_spinbox.pack(side="left", padx=5)
        self.hour_spinbox.delete(0, 'end')
        self.hour_spinbox.insert(0, datetime.datetime.now().strftime("%I"))
        self.minute_semicolon = tk.Label(self.time_frame, text=":", fg=self.white, bg=self.darkBG2)
        self.minute_semicolon.pack(side="left")
        self.minute_spinbox = tk.Spinbox(self.time_frame, from_=0, to=59, width=2)
        self.minute_spinbox.pack(side="left", padx=5)
        self.minute_spinbox.delete(0, 'end')
        self.minute_spinbox.insert(0, datetime.datetime.now().strftime("%M"))
        self.ampm_combobox = tk.StringVar(self.root)
        self.ampm_combobox.set(datetime.datetime.now().strftime("%p"))
        self.ampm_optionmenu = tk.OptionMenu(self.time_frame, self.ampm_combobox, "AM", "PM")
        self.ampm_optionmenu.pack(side="left", padx=5)

        # DateEntry for selecting date
        self.cal = DateEntry(self.time_frame, width=12, background='darkblue', foreground='white', borderwidth=2, year=2024)
        self.cal.pack(side="left", padx=5)

        # Button to set reminder
        self.btn_reminder = tk.Button(self.root, text="設定提醒", fg="white", bg="#6CAE75", command=self.set_reminder)
        self.btn_reminder.pack(pady=5, padx=10, fill="x")

        # Button to cancel reminder
        self.btn_cancel_reminder = tk.Button(self.root, text="取消提醒", fg="white", bg="#EF5350", command=self.cancel_reminder)
        self.btn_cancel_reminder.pack(pady=5, padx=10, fill="x")

        # Listbox to display tasks
        self.lb_tasks = tk.Listbox(self.root, width=60, height=15)
        self.lb_tasks.pack(pady=10, padx=10, fill="both", expand=True)

        # Button to delete a selected task
        self.btn_delete_one = tk.Button(self.root, text="刪除選定事項", fg="white", bg="#EF5350", command=self.delete_one_task)
        self.btn_delete_one.pack(pady=5, padx=10, fill="x")

        # Bind listbox selection event to update reminder button state
        self.lb_tasks.bind("<<ListboxSelect>>", self.update_reminder_button_state)

        # Load tasks from file on initialization
        self.load_tasks()

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
        self.clear_listbox()
        for task in self.tasks:
            self.lb_tasks.insert("end", self.format_task_display(task))

    # Function to format task for display in listbox
    def format_task_display(self, task):
        task_parts = task.split(",")
        if len(task_parts) >= 3:
            date_time_str = task_parts[0] + "," + task_parts[1]
            return date_time_str + "," + task_parts[2]
        else:
            return task

    # Function to check if a task has a reminder
    def has_reminder(self, task):
        for reminder in self.reminders:
            _, reminder_task = reminder
            if reminder_task == task:
                return True
        return False

    # Function to add a task
    def add_task(self):
        task_title = self.title_txt_input.get()
        if task_title != "":
            # Get date and time from the widgets
            task_date = self.cal.get_date()
            hour = int(self.hour_spinbox.get())
            minute = int(self.minute_spinbox.get())
            ampm = self.ampm_combobox.get()
            if ampm == "PM" and hour != 12:
                hour += 12
            elif ampm == "AM" and hour == 12:
                hour = 0
            task_time = datetime.time(hour, minute)
            task_datetime = datetime.datetime.combine(task_date, task_time)

            # Format task as string
            task_str = f"{task_datetime.strftime('%Y/%m/%d,%H:%M')},{task_title}"
            self.tasks.append(task_str)
            self.update_listbox()
            self.save_task(task_str)
        else:
            tkinter.messagebox.showinfo("錯誤", "標題不能空白")
        self.title_txt_input.delete(0, "end")

        # Function to delete a selected task
    def delete_one_task(self):
        task = self.lb_tasks.get("active")
        if task in self.tasks:
            # Check if the task has a reminder, if so, remove it
            for reminder in self.reminders:
                reminder_time, reminder_task = reminder
                if reminder_task == task:
                    self.reminders.remove(reminder)
                    break
            self.tasks.remove(task)
            self.update_listbox()  # Update the listbox after deleting a task
            self.save_all_tasks()
            self.load_tasks()  # Add this line to reload all tasks after deleting a task


    # Function to set a reminder for a selected task
    def set_reminder(self):
        task = self.lb_tasks.get("active")
        if task in self.tasks:
            reminder_time_str = f"{self.cal.get_date()} {self.hour_spinbox.get()}:{self.minute_spinbox.get()} {self.ampm_combobox.get()}"
            try:
                reminder_time = datetime.datetime.strptime(reminder_time_str, "%Y-%m-%d %I:%M %p")
            except ValueError:
                tkinter.messagebox.showinfo("錯誤", "提醒時間格式不正確，請按照 YYYY-MM-DD hh:mm:ss AM/PM 格式輸入。")
                return
            current_time = datetime.datetime.now()
            if reminder_time <= current_time:
                tkinter.messagebox.showinfo("錯誤", "提醒時間必須晚於當前時間。")
                return
            self.reminders.append((reminder_time, task))
            tkinter.messagebox.showinfo("提醒", f"提醒時間設定 '{task}' at {reminder_time.strftime('%Y-%m-%d %I:%M %p')}")
            # Start a new thread to monitor reminders
            thread = Thread(target=self.check_reminders)
            thread.start()

    # Function to cancel reminder for a selected task
    def cancel_reminder(self):
        task = self.lb_tasks.get("active")
        for reminder in self.reminders:
            reminder_time, reminder_task = reminder
            if reminder_task == task:
                self.reminders.remove(reminder)
                tkinter.messagebox.showinfo("提醒", f"已取消 '{task}' 的提醒")
                break

    # Function to check reminders
    def check_reminders(self):
        while True:
            current_time = datetime.datetime.now()
            for reminder in self.reminders[:]:  # Use a copy of reminders to iterate    
                reminder_time, task = reminder
                if current_time >= reminder_time:
                    tkinter.messagebox.showinfo("提醒", f"注意事項 '{task}'!")
                    self.reminders.remove(reminder)
                    self.update_listbox()  # Update the listbox after removing a reminder
            time.sleep(1)

    # Function to update reminder button state based on selection
    def update_reminder_button_state(self, event):
        task = self.lb_tasks.get("active")
        if task in self.tasks and not self.has_reminder(task):
            self.btn_reminder.config(state="normal")
        else:
            self.btn_reminder.config(state="disabled")

    # Function to clear the listbox
    def clear_listbox(self):
        self.lb_tasks.delete(0, "end")

    # Function to save a task to file
    def save_task(self, task):
        try:
            with open("tasks.txt", "a", encoding='utf-8') as file:
                file.write(task + "\n")
        except Exception as e:
            tkinter.messagebox.showerror("錯誤", f"寫入檔案時發生錯誤: {e}")

    # Function to delete all tasks
    def del_all_tasks(self):
        self.tasks = []
        self.update_listbox()
        try:
            open("tasks.txt", "w").close()  # 清空文件内容
        except Exception as e:
            tkinter.messagebox.showerror("錯誤", f"清空檔案時發生錯誤: {e}")

    # Function to save all tasks to file (used after deleting a task)
    def save_all_tasks(self):
        try:
            with open("tasks.txt", "w", encoding='utf-8') as file:
                for task in self.tasks:
                    file.write(task + "\n")
        except Exception as e:
            tkinter.messagebox.showerror("錯誤", f"保存檔案時發生錯誤: {e}")

        # Function to load tasks from file and display in listbox
    def load_tasks(self):
        try:
            with open("tasks.txt", "r", encoding='utf-8') as file:
                tasks = file.readlines()
                for task in tasks:
                    self.lb_tasks.insert("end", task.strip())
        except FileNotFoundError:
            print("找不到檔案")
        except Exception as e:
            tkinter.messagebox.showerror("錯誤", f"讀取檔案時發生錯誤: {e}")


