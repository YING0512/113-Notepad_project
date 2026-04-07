import tkinter as tk
import os
import json

class Home:
    def __init__(self, root, mode_day=False):
        self.root = root
        self.mainframe = tk.Frame(self.root, bg="#3f4145",bd=0)
        self.mainframe.place(x=0, y=0, width=1180, height=768)
        self.DATA_FILE = "data.json"

        # Colors
        self.white = "#ffffff"
        self.black = "#000000"
        self.darkBG1 = "#2d2f32"
        self.darkBG2 = "#3f4145"
        self.darkactive = "#4c4e52"
        self.brightBG1 = "#c0c0c0"
        self.brightBG2 = "#dfdfdf"
        self.brightactive = "#f1f0f2"
        self.currentbg_color = self.darkBG2
        self.currentfg_color = self.white
        self.currentactive_color = self.darkactive

        # Adjusted Positions and Sizes
        self.DoListTitle = tk.Label(self.mainframe, text="提醒", bg=self.darkBG1, fg=self.white, bd=1, font=("微軟正黑體", 20, "bold","underline"))
        self.DoListTitle.place(x=0, y=0, width=1180, height=50)
        self.DoList = tk.Frame(self.mainframe, bg=self.currentbg_color)
        self.DoList.place(x=0, y=50, width=1180, height=359)
        
        self.NoteListTitle = tk.Label(self.mainframe, text="記事本", bg=self.darkBG1, fg=self.white, bd=1, font=("微軟正黑體", 20, "bold","underline"))
        self.NoteListTitle.place(x=0, y=409, width=1180, height=50)
        self.NoteList = tk.Frame(self.mainframe, bg=self.currentbg_color)
        self.NoteList.place(x=0, y=459, width=1180, height=309)
        
        self.mode_day = mode_day
        self.last_modification_time = 0
        self.check_file_changes()
        
    def toggle_mode(self, mode_day):
        # Change color
        self.mode_day = mode_day
        if self.mode_day:
            self.currentbg_color = self.darkBG2
            self.currentfg_color = self.white
            self.currentactive_color = self.darkactive
            self.DoListTitle.config(bg=self.darkBG1, fg=self.currentfg_color)
            self.NoteListTitle.config(bg=self.darkBG1, fg=self.currentfg_color)
        else:
            self.currentbg_color = self.brightBG2
            self.currentfg_color = self.black
            self.currentactive_color = self.brightactive
            self.DoListTitle.config(bg=self.brightBG1, fg=self.currentfg_color)
            self.NoteListTitle.config(bg=self.brightBG1, fg=self.currentfg_color)

        # Update the background color of DoList and NoteList
        self.DoList.config(bg=self.currentbg_color)
        self.NoteList.config(bg=self.currentbg_color)

        # Update the background color of all labels in DoList and NoteList
        for widget in self.DoList.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg=self.currentbg_color, fg=self.currentfg_color)
        for widget in self.NoteList.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg=self.currentbg_color, fg=self.currentfg_color)

    def check_file_changes(self):
        if os.path.exists(self.DATA_FILE):
            try:
                current_modification_time = os.path.getmtime(self.DATA_FILE)
                if current_modification_time != self.last_modification_time:
                    self.load_tasks()
                    self.load_notes()
                    self.last_modification_time = current_modification_time
            except Exception as e:
                print(f"Error checking file changes: {e}")

        # Schedule the next check
        # Use a longer delay here to reduce CPU usage if needed, but 1000 is fine
        self.mainframe.after(1000, self.check_file_changes)

    def load_tasks(self):
        if not self.DoList.winfo_exists():
            return
        for widget in self.DoList.winfo_children():
            widget.destroy()
        try:
            if os.path.exists(self.DATA_FILE):
                with open(self.DATA_FILE, "r", encoding='utf-8') as file:
                    data = json.load(file)
                    tasks = data.get('tasks', [])
                    
                # Fix: Sort or cleanup
                for i, task in enumerate(tasks):
                    if task.get('status') == 'expired':
                         continue # Skip expired on home
                         
                    task_text = f"{task['date']}\n{task['time']}\n{task['title']}"
                    label = tk.Label(self.DoList, text=task_text, bg=self.currentactive_color, fg=self.currentfg_color, font=("微軟正黑體", 18), width=10, height=5)
                    row, col = divmod(i, 4)
                    label.grid(row=row, column=col, padx=10, pady=10)
        except Exception as e:
            print(f"Load tasks error: {e}")

    def load_notes(self):
        if not self.NoteList.winfo_exists():
            return
        for widget in self.NoteList.winfo_children():
            widget.destroy()
        try:
             if os.path.exists(self.DATA_FILE):
                with open(self.DATA_FILE, "r", encoding='utf-8') as file:
                    data = json.load(file)
                    notes = data.get('notes', [])
                    
                for i, note in enumerate(notes):
                    # Truncate content for display
                    content_preview = note['content'][:20] + "..." if len(note['content']) > 20 else note['content']
                    note_text = f"{note['title']}\n{content_preview}"
                    label = tk.Label(self.NoteList, text=note_text, bg=self.currentactive_color, fg=self.currentfg_color, font=("微軟正黑體", 18), width=10, height=5)
                    row, col = divmod(i, 4)
                    label.grid(row=row, column=col, padx=10, pady=10)
        except Exception as e:
            print(f"Load notes error: {e}")

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = Home(root)
#     root.mainloop()
