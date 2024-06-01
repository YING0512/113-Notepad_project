import tkinter
import tkinter.messagebox
import random
import datetime
import time
from threading import Thread
from tkcalendar import DateEntry

class Todo:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        root.resizable(False, False)
        self.tasks = []
        self.reminders = []

        #color
        self.white="#ffffff"
        self.black="#000000"
        self.darkBG1="#2d2f32"
        self.darkBG2="#3f4145"
        
        # Frame for the input section
        self.input_frame = tkinter.Frame(self.root, bg=self.white)
        self.input_frame.pack(pady=10, padx=10, fill="x")
        tkinter.Label(self.input_frame, text="標題:",fg= self.black, bg=self.white, font=(12)).pack(side="left")
        self.txt_input = tkinter.Entry(self.input_frame, width=30)
        self.txt_input.pack(side="left", padx=5)

        # Button to add tasks
        self.btn_add_task = tkinter.Button(self.input_frame, text="增加待辦事項", fg="white", bg="#6CAE75", command=self.add_task)
        self.btn_add_task.pack(side="left", padx=5)

        # Button to delete all tasks
        self.btn_del_all = tkinter.Button(self.input_frame, text="刪除全部", fg="white", bg="#EF5350", command=self.del_all_tasks)
        self.btn_del_all.pack(side="left", padx=5)

        # Frame for time selection
        self.time_frame = tkinter.Frame(self.root, bg=self.white)
        self.time_frame.pack(pady=5, padx=10, fill="x")

        # Labels and Spinboxes for time selection
        tkinter.Label(self.time_frame, text="時間:",fg= self.black, bg=self.white, font=(12)).pack(side="left")
        self.hour_spinbox = tkinter.Spinbox(self.time_frame, from_=1, to=12, width=2)
        self.hour_spinbox.pack(side="left", padx=5)
        self.hour_spinbox.delete(0, 'end')
        self.hour_spinbox.insert(0, datetime.datetime.now().strftime("%I"))
        tkinter.Label(self.time_frame, text=":", bg=self.white).pack(side="left")
        self.minute_spinbox = tkinter.Spinbox(self.time_frame, from_=0, to=59, width=2)
        self.minute_spinbox.pack(side="left", padx=5)
        self.minute_spinbox.delete(0, 'end')
        self.minute_spinbox.insert(0, datetime.datetime.now().strftime("%M"))
        tkinter.Label(self.time_frame, text=":", bg=self.white).pack(side="left")
        self.second_spinbox = tkinter.Spinbox(self.time_frame, from_=0, to=59, width=2)
        self.second_spinbox.pack(side="left", padx=5)
        self.second_spinbox.delete(0, 'end')
        self.second_spinbox.insert(0, datetime.datetime.now().strftime("%S"))
        self.ampm_combobox = tkinter.StringVar(self.root)
        self.ampm_combobox.set(datetime.datetime.now().strftime("%p"))
        self.ampm_optionmenu = tkinter.OptionMenu(self.time_frame, self.ampm_combobox, "AM", "PM")
        self.ampm_optionmenu.pack(side="left", padx=5)

        # DateEntry for selecting date
        self.cal = DateEntry(self.time_frame, width=12, background='darkblue', foreground='white', borderwidth=2, year=2024)
        self.cal.pack(side="left", padx=5)

        # Button to set reminder
        self.btn_reminder = tkinter.Button(self.root, text="設定提醒", fg="white", bg="#6CAE75", command=self.set_reminder)
        self.btn_reminder.pack(pady=5, padx=10, fill="x")

        # Button to cancel reminder
        self.btn_cancel_reminder = tkinter.Button(self.root, text="取消提醒", fg="white", bg="#EF5350", command=self.cancel_reminder)
        self.btn_cancel_reminder.pack(pady=5, padx=10, fill="x")

        # Listbox to display tasks
        self.lb_tasks = tkinter.Listbox(self.root, width=60, height=15)
        self.lb_tasks.pack(pady=10, padx=10, fill="both", expand=True)

        # Button to delete a selected task
        self.btn_delete_one = tkinter.Button(self.root, text="刪除選定事項", fg="white", bg="#EF5350", command=self.delete_one_task)
        self.btn_delete_one.pack(pady=5, padx=10, fill="x")

    # Function to update the listbox with tasks
    def update_listbox(self):
        self.clear_listbox()
        for task in self.tasks:
            self.lb_tasks.insert("end", task)

    # Function to clear the listbox
    def clear_listbox(self):
        self.lb_tasks.delete(0, "end")

    # Function to add a task
    def add_task(self):
        task = self.txt_input.get()
        if task != "":
            self.tasks.append(task)
            self.update_listbox()
        else:
            tkinter.messagebox.showinfo("錯誤", "標題不能空白")
        self.txt_input.delete(0, "end")

    # Function to delete all tasks
    def del_all_tasks(self):
        self.tasks = []
        self.update_listbox()

    # Function to delete a selected task
    def delete_one_task(self):
        task = self.lb_tasks.get("active")
        if task in self.tasks:
            self.tasks.remove(task)
        self.update_listbox()

    # Function to set a reminder for a selected task
    def set_reminder(self):
        task = self.lb_tasks.get("active")
        if task in self.tasks:
            reminder_time_str = f"{self.cal.get_date()} {self.hour_spinbox.get()}:{self.minute_spinbox.get()}:{self.second_spinbox.get()} {self.ampm_combobox.get()}"
            try:
                reminder_time = datetime.datetime.strptime(reminder_time_str, "%Y-%m-%d %I:%M:%S %p")
            except ValueError:
                tkinter.messagebox.showinfo("錯誤", "提醒時間格式不正確，請按照 YYYY-MM-DD hh:mm:ss AM/PM 格式輸入。")
                return
            current_time = datetime.datetime.now()
            if reminder_time <= current_time:
                tkinter.messagebox.showinfo("錯誤", "提醒時間必須晚於當前時間。")
                return
            self.reminders.append((reminder_time, task))
            tkinter.messagebox.showinfo("提醒", f"提醒時間設定 '{task}' at {reminder_time.strftime('%Y-%m-%d %I:%M:%S %p')}")
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
            for reminder in self.reminders:
                reminder_time, task = reminder
                if current_time >= reminder_time:
                    tkinter.messagebox.showinfo("提醒", f"注意事項 '{task}'!")
                    self.reminders.remove(reminder)
            time.sleep(1)

# Create an instance of the Todo class to run the application
def main():
    root =tkinter.Tk()  # 創建主視窗
    app = Todo(root)  #
    root.mainloop()  # 進入主事件循環，等待用戶交互操作

if __name__ == "__main__":
    root =tkinter.Tk()  # 創建主視窗
    app = Todo(root)  #
    root.mainloop()