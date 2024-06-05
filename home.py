import tkinter as tk
import os

class HomeFM:
    def __init__(self, root):
        self.root = root
        self.DoList = tk.Frame(self.root, bg="#f0f0f0")
        self.DoList.pack(fill=tk.BOTH, expand=True)
        self.NoteList = tk.Frame(self.root, bg="#f0f0f0")
        self.NoteList.pack(fill=tk.BOTH, expand=True)
        self.white = "#FFFFFF"
        self.last_modification_time = 0
        self.check_file_changes()

    def check_file_changes(self):
        # 檢查文件是否存在
        if os.path.exists("tasks.txt"):
            # 獲取文件的最後修改時間
            current_modification_time = os.path.getmtime("tasks.txt")

            # 比較最後修改時間是否有變化
            if current_modification_time != self.last_modification_time:
                # 重新加載任務數據
                self.load_tasks()
                # 更新最後修改時間
                self.last_modification_time = current_modification_time
        if os.path.exists("notes.txt"):
            # 獲取文件的最後修改時間
            current_modification_time = os.path.getmtime("notes.txt")

            # 比較最後修改時間是否有變化
            if current_modification_time != self.last_modification_time:
                # 重新加載筆記數據
                self.load_notes()
                # 更新最後修改時間
                self.last_modification_time = current_modification_time

        # 重新註冊定時器
        self.root.after(1000, self.check_file_changes)

    def load_tasks(self):
        try:
            # 清除舊的Label
            for widget in self.DoList.winfo_children():
                widget.destroy()
            
            with open("tasks.txt", "r", encoding='utf-8') as file:
                tasks = file.readlines()
                for i, task in enumerate(tasks):
                    task = task.strip().split(",")
                    task_text = f"{task[0]}\n{task[1]}\n{task[2]}"
                    label = tk.Label(self.DoList, text=task_text, bg="#696969", fg=self.white, font=("宋體", 18), width=20, height=5)
                    row, col = divmod(i, 5)
                    label.grid(row=row, column=col, padx=10, pady=10)
        except FileNotFoundError:
            print("找不到檔案")
            
    def load_notes(self):
        try:
            # 清除舊的Label
            for widget in self.NoteList.winfo_children():
                widget.destroy()
            
            with open("notes.txt", "r", encoding='utf-8') as file:
                notes = file.readlines()
                for i, note in enumerate(notes):
                    note = note.strip().split(",")
                    note_text = f"{note[0]}\n{note[1]}"
                    label = tk.Label(self.NoteList, text=note_text, bg="#696969", fg=self.white, font=("宋體", 18), width=20, height=5)
                    row, col = divmod(i, 5)
                    label.grid(row=row, column=col, padx=10, pady=10)
        except FileNotFoundError:
            print("找不到檔案")

if __name__ == "__main__":
    root = tk.Tk()
    app = HomeFM(root)
    root.mainloop()
