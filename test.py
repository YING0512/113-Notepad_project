import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from tkcalendar import DateEntry

root = tk.Tk()
root.configure(bg="#F0F0F0")
root.title("待辦事項")
root.geometry("800x600")

tasks = []
reminders = []
DELETE_DELAY = 30 * 24 * 60 * 60  # 設定過期事件在30天後自動刪除（30天的秒數）

# Function to update the listbox with tasks
def update_listbox():
    lb_tasks.delete(0, "end")
    for task in tasks:
        lb_tasks.insert("end", task)

# Function to add a task and set a reminder
def add_task():
    task = txt_input.get()
    if task:
        tasks.append(task)
        update_listbox()
        txt_input.delete(0, "end")
        set_reminder(task)
    else:
        lbl_display["text"] = "不能輸入空白"

# Function to set a reminder for a given task
def set_reminder(task):
    reminder_time_str = f"{cal.get_date()} {hour_spinbox.get()}:{minute_spinbox.get()} {ampm_combobox.get()}"
    try:
        reminder_time = datetime.datetime.strptime(reminder_time_str, "%Y-%m-%d %I:%M %p")
    except ValueError:
        lbl_display["text"] = "提醒時間格式不正確，請按照 YYYY-MM-DD hh:mm AM/PM 格式輸入。"
        return
    current_time = datetime.datetime.now()
    if reminder_time <= current_time:
        lbl_display["text"] = "提醒時間必須晚於當前時間。"
        return
    reminders.append((reminder_time, task))
    print(f"提醒時間設定 '{task}' at {reminder_time.strftime('%Y-%m-%d %I:%M:%S %p')}")

# Function to delete a selected task
def delete_task():
    selected_index = lb_tasks.curselection()
    if selected_index:
        selected_task = lb_tasks.get(selected_index)
        tasks.remove(selected_task)
        update_listbox()
        lbl_display["text"] = f"已刪除 '{selected_task}'"

# Function to mark task as expired
def mark_task_expired(task):
    index = tasks.index(task)
    tasks[index] = f"~{task}~"
    update_listbox()

# Function to check reminders and handle expired tasks
def check_reminders():
    current_time = datetime.datetime.now()
    expired_reminders = []
    for reminder in reminders:
        reminder_time, task = reminder
        if current_time >= reminder_time:
            messagebox.showinfo("提醒", f"注意事項 '{task}'!")
            expired_reminders.append(reminder)
            mark_task_expired(task)
            # 設定一段時間後自動刪除
            root.after(DELETE_DELAY * 1000, lambda t=task: delete_task_by_name(t))
    for reminder in expired_reminders:
        reminders.remove(reminder)
    root.after(1000, check_reminders)  # 每秒檢查一次提醒

# Function to delete a task by its name
def delete_task_by_name(task):
    task_with_strike = f"~{task}~"
    if task_with_strike in tasks:
        tasks.remove(task_with_strike)
        update_listbox()
        lbl_display["text"] = f"已自動刪除過期事項 '{task}'"

# Frame for the input section
input_frame = tk.Frame(root, bg="#F0F0F0")
input_frame.pack(pady=10, padx=10, fill="x")

# Entry field to add tasks
txt_input = tk.Entry(input_frame, width=30)
txt_input.pack(side="left", padx=5)

# DateEntry for selecting date
cal = DateEntry(input_frame, width=12, background='darkblue', foreground='white', borderwidth=2, year=2024)
cal.pack(side="left", padx=5)

# Labels and Spinboxes for time selection
tk.Label(input_frame, text="時間:", bg="#F0F0F0").pack(side="left")
hour_spinbox = tk.Spinbox(input_frame, from_=1, to=12, width=2)
hour_spinbox.pack(side="left", padx=5)
hour_spinbox.delete(0, 'end')
hour_spinbox.insert(0, datetime.datetime.now().strftime("%I"))
tk.Label(input_frame, text=":", bg="#F0F0F0").pack(side="left")
minute_spinbox = tk.Spinbox(input_frame, from_=0, to=59, width=2)
minute_spinbox.pack(side="left", padx=5)
minute_spinbox.delete(0, 'end')
minute_spinbox.insert(0, datetime.datetime.now().strftime("%M"))
ampm_combobox = tk.StringVar(root)
ampm_combobox.set(datetime.datetime.now().strftime("%p"))
ampm_optionmenu = tk.OptionMenu(input_frame, ampm_combobox, "AM", "PM")
ampm_optionmenu.pack(side="left", padx=5)

# Button to add tasks and set reminders
btn_add_task = tk.Button(input_frame, text="增加待辦事項並設定提醒", fg="white", bg="#6CAE75", command=add_task)
btn_add_task.pack(side="left", padx=5)

# Button to delete selected task
btn_delete_task = tk.Button(input_frame, text="刪除選定事項", fg="white", bg="#EF5350", command=delete_task)
btn_delete_task.pack(side="left", padx=5)

# Listbox to display tasks
lb_frame = tk.Frame(root)
lb_frame.pack(pady=10, padx=10, fill="both", expand=True)
lb_tasks = tk.Listbox(lb_frame, width=60, height=15)
lb_tasks.pack(side="left", fill="both", expand=True)

# Scrollbar for the listbox
scrollbar = tk.Scrollbar(lb_frame)
scrollbar.pack(side="right", fill="y")
lb_tasks.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=lb_tasks.yview)

# Label to display status
lbl_display = tk.Label(root, text="", bg="#F0F0F0", font=("Arial", 12))
lbl_display.pack(pady=5, fill="x")

# Information about automatic deletion
lbl_info = tk.Label(root, text=f"過期事項將在 {DELETE_DELAY // (24 * 60 * 60)} 天後自動刪除", bg="#F0F0F0", font=("Arial", 10))
lbl_info.pack(pady=5, fill="x")

# Start checking reminders
check_reminders()

root.mainloop()