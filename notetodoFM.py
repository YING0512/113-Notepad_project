import tkinter as tk
from tkinter import messagebox
import datetime
import time
from tkcalendar import DateEntry
import os
import json

class Todo:
    def __init__(self, root, mode_day=False):
        self.root = root
        self.mode_day = mode_day
        self.tasks = []
        # self.reminders = [] # No longer needed here, handled by main.py
        self.DELETE_DELAY = 30 * 24 * 60 * 60  # 設定過期事件在30天後自動刪除（30天的秒數）
        self.DATA_FILE = "data.json"
        self.last_modification_time = 0

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
        self.lb_frame = tk.Frame(root)
        self.lb_frame.pack(pady=10, padx=10, fill="both", expand=True)
        self.lb_tasks = tk.Listbox(self.lb_frame, width=60, height=15)
        self.lb_tasks.pack(side="left", fill="both", expand=True)

        # Scrollbar for the listbox
        self.scrollbar = tk.Scrollbar(self.lb_frame)
        self.scrollbar.pack(side="right", fill="y")
        self.lb_tasks.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lb_tasks.yview)

        # Load tasks from file
        self.load_tasks_from_file()
        self.update_listbox()

        
        # Information about automatic deletion
        lbl_info = tk.Label(root, text=f"過期事項將在 {self.DELETE_DELAY // (24 * 60 * 60)} 天後自動刪除", bg="#F0F0F0", font=("Arial", 10))
        lbl_info.pack(pady=5, fill="x")

        # Start checking file changes instead of local reminders
        self.check_file_changes()

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
        if not self.lb_tasks.winfo_exists():
            return
        self.lb_tasks.delete(0, "end")
        # Filter out tasks that are marked for deletion (temporary visual effect if needed)
        # For now just show all
        sorted_tasks = sorted(self.tasks, key=lambda x: (x.get('date', ''), x.get('time', ''), x.get('title', '')))
        for task in sorted_tasks:
            status_mark = "~" if task.get('status') == 'expired' else ""
            task_text = f"{status_mark}{task.get('date')} {task.get('time')} {task.get('title')}{status_mark}"
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
            task = {'title': task_title, 'date': task_date, 'time': task_time, 'status': 'active'}
            self.tasks.append(task)
            self.update_listbox()
            self.txt_input.delete(0, "end")
            self.save_data()
            # self.set_reminder(task) # Handled by main.py
        else:
            messagebox.showinfo("提示", "不能輸入空白")

    # set_reminder removed - handled by main.py

    # Function to delete a selected task
    def delete_task(self):
        selected_index = self.lb_tasks.curselection()
        if selected_index:
            selected_text = self.lb_tasks.get(selected_index)
            # This parsing relies on the format in update_listbox
            # Improve: Find actual task object corresponding to selection index
            # Since we sort in display, we must sort here too to find matching index
            sorted_tasks = sorted(self.tasks, key=lambda x: (x.get('date', ''), x.get('time', ''), x.get('title', '')))
            
            if selected_index[0] < len(sorted_tasks):
                task_to_delete = sorted_tasks[selected_index[0]]
                if task_to_delete in self.tasks:
                    self.tasks.remove(task_to_delete)
                    self.update_listbox()
                    self.save_data()
                    messagebox.showinfo("提示", f"已刪除 '{task_to_delete['title']}'")
    
    # Function to mark task as expired
    def mark_task_expired(self, task):
        if task in self.tasks:
            task['status'] = 'expired'
            self.update_listbox()
            self.save_data()

    # check_reminders removed - handled by main.py
    
    def check_file_changes(self):
        if os.path.exists(self.DATA_FILE):
             try:
                # 获取文件的最后修改时间
                current_modification_time = os.path.getmtime(self.DATA_FILE)

                # 比较最后修改时间是否有变化
                if current_modification_time != self.last_modification_time:
                    # 重新加载任务数据 (if modification time > initial load time)
                    # We need to be careful not to overwrite Unsaved changes if any?
                    # But here we interact directly with file.
                    # Ideally we should reload if file changed externally.
                    if self.last_modification_time != 0: # Skip first check or ensure it works
                         self.load_tasks_from_file()
                         self.update_listbox()
                    
                    self.last_modification_time = current_modification_time
             except Exception as e:
                print(f"File check error: {e}")

        # 重新注册定时器
        self.root.after(1000, self.check_file_changes)

    # Function to save data (Global JSON)
    def save_data(self):
        data = {}
        if os.path.exists(self.DATA_FILE):
             try:
                with open(self.DATA_FILE, "r", encoding='utf-8') as file:
                    data = json.load(file)
             except:
                 pass
        
        data['tasks'] = self.tasks
        
        with open(self.DATA_FILE, "w", encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            # Update last modification time to avoid reloading own changes immediately (though it's fine if we do)
            self.last_modification_time = os.path.getmtime(self.DATA_FILE)

    # Function to load tasks from file
    def load_tasks_from_file(self):
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r", encoding='utf-8') as file:
                    data = json.load(file)
                    self.tasks = data.get('tasks', [])
                    
            except Exception as e:
                print(f"Load error: {e}")
                self.tasks = []

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = Todo(root)
#     root.mainloop()
