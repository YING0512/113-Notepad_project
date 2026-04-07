import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from notecalendarFM import CalendarFM
from notetodoFM import Todo
from notetextFM import TextEditor
from homeFM import Home
import os
import json
import datetime

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Note")
        self.root.geometry("1200x768")
        root.resizable(False, False)
        self.menu_expanded = False
        self.mode_day = False
        self.last_modification_time = 0
        self.DATA_FILE = "data.json"
        
        # Initialize state variables to prevent AttributeError
        self.home = True
        self.calendarr = False
        self.text = False
        self.todo = False

        self.reminders = []
        self.DELETE_DELAY = 30 * 24 * 60 * 60 # 30 days

        self.root.after(1000, self.check_file_changes)
        self.root.after(1000, self.check_reminders)
        
        #color
        self.white="#ffffff"
        self.black="#000000"
        self.darkBG1="#2d2f32"
        self.darkBG2="#3f4145"
        self.darkBG3="#1F1F1F"
        self.darkactive ="#4c4e52"
        self.brightBG1 ="#c0c0c0"
        self.brightBG2 ="#dfdfdf"
        self.brightBG3 ="#6F6F6F"
        self.brightactive ="#f1f0f2"
        self.currentactive_color = self.darkactive
        self.currentfg_color = self.white
      
        # Menu Frame
        self.title_icon_path = "icon/feather-pen.png"
        self.menu_icon_path = "icon/menu-burger.png"
        self.title_icon = self.resize_image(self.title_icon_path, 30, 30)
        self.menu_icon = self.resize_image(self.menu_icon_path, 30, 30)
        self.menu_frame = tk.Frame(self.root, bd=2, bg=self.darkBG1)
        self.menu_frame.place(x=0, y=40, width=50, height=660)
        self.title_frame = tk.Frame(self.root, bg=self.darkBG3)
        self.title_frame.place(x=0, y=0, width=1200, height=40)
        self.home_button = tk.Button(self.title_frame, image=self.title_icon, bd=0,  cursor="hand2",command=self.home_click)
        self.home_button.place(x=47, y=2, width=32, height=32)
        
        
        #Setting frame
        self.setting_dayicon_path = "icon/brightness.png"
        self.setting_nighticon_path = "icon/moon.png"
        self.setting_dayicon = self.resize_image(self.setting_dayicon_path, 20, 20)
        self.setting_nighticon = self.resize_image(self.setting_nighticon_path, 20, 20)
        self.set_frame = tk.Frame(self.root, bd=0, bg=self.darkBG1)
        self.set_frame.place(x=0, y=700, width=50, height=660)
        self.mode_button = tk.Button(self.set_frame, cursor="hand2", bd=0, fg=self.black, bg=self.white, image=self.setting_dayicon, command=self.toggle_mode)
        self.mode_button.place(x=7, y=0, width=32, height=40)
        
        # Content Frame
        self.content_frame = tk.Frame(self.root, bd=1, bg=self.darkBG2)
        self.content_frame.place(x=50, y=40, width=890, height=728)
        
        
        # Information Frame
        self.information_frame = tk.Frame(self.root, bd=0, bg=self.darkBG1)
        self.information_frame.place(x=940, y=40, width=300, height=728)
        self.DoListTitle = tk.Label(self.information_frame, text="提醒", bg=self.darkBG1, fg=self.white, bd=1, font=("微軟正黑體", 20, "bold","underline"))
        self.DoListTitle.place(x=0, y=0, width=300, height=40)
        self.DoList = tk.Frame(self.information_frame, bg=self.darkBG1)
        self.DoList.place(x=0, y=40, width=300, height=324)
        self.NoteListTitle = tk.Label(self.information_frame, text="記事本", bg=self.darkBG1, fg=self.white, bd=1, font=("微軟正黑體", 20, "bold","underline"))
        self.NoteListTitle.place(x=0, y=324, width=300, height=40)
        self.NoteList= tk.Frame(self.information_frame, bg=self.darkBG1 ,bd=1)
        self.NoteList.place(x=0, y=364, width=300, height=324)

        self.load_tasks()
        self.load_notes()
        
        # Icon location
        self.calender_icon_path = Image.open("icon/daily-calendar (1).png").resize((20, 20))
        self.calender_icon = ImageTk.PhotoImage(self.calender_icon_path)
        self.text_icon_path = Image.open("icon/edit.png").resize((20, 20))
        self.text_icon = ImageTk.PhotoImage(self.text_icon_path)
        self.todo_icon_path = Image.open("icon/list-check.png").resize((20, 20))
        self.todo_icon = ImageTk.PhotoImage(self.todo_icon_path)
        
        # Create menu buttons
        self.create_menu_buttons()  # Start with closed menu buttons

        # Menu Button
        self.menu_icon = self.resize_image(self.menu_icon_path, 30, 30)
        self.menu_btn = tk.Button(self.title_frame,text="menu", image=self.menu_icon, bd=0, cursor="hand2", command=self.toggle_menu)
        self.menu_btn.image = self.menu_icon
        self.menu_btn.place(x=7, y=2, width=32, height=32)
        
        self.home_app = Home(self.content_frame, mode_day=self.mode_day)
        self.content_frame.place(x=50, y=40, width=1150, height=728)
        self.information_frame.place(x=1200, y=40, width=0, height=728)
        self.home = True
# 
    def create_menu_buttons(self):
        self.menu_buttons = []
        button_func = self.create_menu_buttons_expanded if self.menu_expanded else self.create_menu_buttons_closed
        button_func()
# 
    def create_menu_buttons_closed(self):#menu closed
        # Create buttons individually
        self.calender_btn = tk.Button(self.menu_frame, image=self.calender_icon, bd=0, cursor="hand2",command=self.calendar_click)
        self.calender_btn.image = self.calender_icon_path
        self.calender_btn.place(x=7, y=7, width=32, height=32)
        self.menu_buttons.append(self.calender_btn)

        self.text_btn = tk.Button(self.menu_frame, image=self.text_icon, bd=0, cursor="hand2",command=self.text_click)
        self.text_btn.image = self.text_icon_path
        self.text_btn.place(x=7, y=47, width=32, height=32)
        self.menu_buttons.append(self.text_btn)

        self.todo_btn = tk.Button(self.menu_frame, image=self.todo_icon, bd=0, cursor="hand2",command=self.todo_click)
        self.todo_btn.image = self.todo_icon_path
        self.todo_btn.place(x=7, y=87, width=32, height=32)
        self.menu_buttons.append(self.todo_btn)
        self.mode_button.config(text="",command=self.toggle_mode)
        self.mode_button.place(x=7, y=7, width=32, height=32)
# 
    def create_menu_buttons_expanded(self):#menu expanded
        self.calender_btn = tk.Button(self.menu_frame, text=" 日　歷", compound=tk.LEFT, font=('微軟正黑體', 11 , 'bold'), image=self.calender_icon, bd=0, cursor="hand2",command=self.calendar_click)
        self.calender_btn.image = self.calender_icon_path
        self.calender_btn.place(x=7, y=7, width=90, height=32)
        self.menu_buttons.append(self.calender_btn)

        self.text_btn = tk.Button(self.menu_frame, text=" 記事本", compound=tk.LEFT, font=('微軟正黑體', 11 , 'bold'), image=self.text_icon, bd=0, cursor="hand2",command=self.text_click)
        self.text_btn.image = self.text_icon_path
        self.text_btn.place(x=7, y=47, width=90, height=32)
        self.menu_buttons.append(self.text_btn)

        self.todo_btn = tk.Button(self.menu_frame, text=" 提　醒", compound=tk.LEFT, font=('微軟正黑體', 11 , 'bold'), image=self.todo_icon, bd=0, cursor="hand2",command=self.todo_click)
        self.todo_btn.image = self.todo_icon_path
        self.todo_btn.place(x=7, y=87, width=90, height=32)
        self.menu_buttons.append(self.todo_btn)
            
        if self.mode_day:
            self.modetext =" 暗色模式"
        else:
            self.modetext =" 亮色模式"
        self.mode_button.config(text=self.modetext,compound=tk.LEFT, font=('微軟正黑體', 11 , 'bold'),command=self.toggle_mode)
        self.mode_button.place(x=7, y=7, width=100, height=32)
# 
    def toggle_menu(self):  #menu size change
        if self.menu_expanded:  # Switch to Collapsed
            for button in self.menu_buttons:
                button.destroy()
            
            if self.mode_day:
                self.modetext =" 亮色模式"
            else:
                self.modetext =" 暗色模式"
                self.mode_button.config(text=self.modetext)
            self.menu_expanded = False
        else: # Switch to Expanded
            self.mode_button.config(text="")
            self.menu_expanded = True
            
        # Update layout after state change
        self.update_layout()
        
        # Recreate menu buttons
        self.create_menu_buttons()
    
    def update_layout(self):
        # Update Menu Frame Width
        if self.menu_expanded:
            self.menu_frame.place(x=0, y=40, width=120, height=680)
            self.set_frame.place(x=0, y=700, width=120, height=660)
            content_x = 120
        else:
            self.menu_frame.place(x=0, y=40, width=50, height=660)
            self.set_frame.place(x=0, y=700, width=50, height=660)
            content_x = 50
            
        # Update Content and Information Frame
        if self.home:
            # Home mode: full width (minus side padding maybe?) or just wider content
            content_width = 1200 - content_x
            self.content_frame.place(x=content_x, y=40, width=content_width, height=728)
            self.information_frame.place(x=1200, y=40, width=0, height=728) # Hide info frame
        else:
            # Other modes: show info frame
            info_x = 940 # Fixed position for info frame in original logic
            
            if self.menu_expanded:
                # If expanded, content starts at 120. Ends at 940.
                content_width = info_x - content_x # 940-120 = 820
            else:
                # If collapsed, content starts at 50. Ends at 940.
                content_width = info_x - content_x # 940-50 = 890
                
            self.content_frame.place(x=content_x, y=40, width=content_width, height=728)
            self.information_frame.place(x=info_x, y=40, width=300, height=728)

#   
    def toggle_mode(self):
        if self.mode_day:
            self.mode_button.config(image=self.setting_dayicon)
            self.menu_frame.config(bg=self.darkBG1)
            self.set_frame.config(bg=self.darkBG1)
            self.content_frame.config(bg=self.darkBG2)
            self.information_frame.config(bg=self.darkBG1)
            self.DoListTitle.config(bg=self.darkBG1,fg=self.white)
            self.DoList.config(bg=self.darkBG1)
            self.NoteListTitle.config(bg=self.darkBG1,fg=self.white)
            self.NoteList.config(bg=self.darkBG1)
            self.title_frame.config(bg=self.darkBG3)
            self.currentactive_color = self.darkactive
            self.currentfg_color = self.white
            if self.menu_expanded:
                self.mode_button.config(text=" 亮色模式")
        else:
            self.mode_button.config(image=self.setting_nighticon)
            self.menu_frame.config(bg=self.brightBG1)
            self.set_frame.config(bg=self.brightBG1)
            self.content_frame.config(bg=self.brightBG2)
            self.information_frame.config(bg=self.brightBG1)
            self.DoListTitle.config(bg=self.brightBG1,fg=self.black)
            self.DoList.config(bg=self.brightBG1)
            self.NoteListTitle.config(bg=self.brightBG1,fg=self.black)
            self.NoteList.config(bg=self.brightBG1)
            self.title_frame.config(bg=self.brightBG3)
            self.currentactive_color = self.brightactive
            self.currentfg_color = self.black
            if self.menu_expanded:
                self.mode_button.config(text=" 暗色模式")

        # Update mode_day in other methods
        for widget in self.content_frame.winfo_children():
            if isinstance(widget, (CalendarFM, Todo)):
                widget.toggle_mode(self.mode_day)

            # Destroy old widgets and create new ones
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        if self.home:
            self.home_app = Home(self.content_frame, mode_day=self.mode_day)
            self.home_app.toggle_mode(self.mode_day)
        elif self.calendarr:
            self.calendar_app = CalendarFM(self.content_frame, mode_day=self.mode_day)
            self.calendar_app.toggle_mode(self.mode_day)
        elif self.todo:
            self.todo_app = Todo(self.content_frame, mode_day=self.mode_day)
            self.todo_app.toggle_mode(self.mode_day)
        else:
            self.text_app = TextEditor(self.content_frame, mode_day=self.mode_day)
            
        self.mode_day = not self.mode_day
        
        # Reload side bar
        self.load_tasks()
        self.load_notes()

    def home_click(self):
        self.home = True
        self.calendarr = False
        self.text = False
        self.todo = False
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        self.home_app = Home(self.content_frame, mode_day=self.mode_day)
        self.home_app.toggle_mode(not self.mode_day)
        
        # Update Layout
        self.update_layout()

                
    def calendar_click(self):
        self.home = False
        self.calendarr = True
        self.text = False
        self.todo = False
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.calendar_app = CalendarFM(self.content_frame, mode_day=self.mode_day, action1=self.text_click, action2=self.todo_click)
        self.calendar_app.toggle_mode(not self.mode_day)
        self.update_layout()


    def text_click(self):
        self.home = False
        self.calendarr = False
        self.text = True
        self.todo = False
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        if self.text:
            self.text_app = TextEditor(self.content_frame, mode_day=not self.mode_day)  
        self.update_layout()

    def todo_click(self):
        self.home = False
        self.calendarr = False
        self.text = False
        self.todo = True
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.todo_app = Todo(self.content_frame, mode_day=self.mode_day)
        self.todo_app.toggle_mode(not self.mode_day)
        self.update_layout()
        # print(self.mode_day)

    def check_file_changes(self):
        # 检查文件是否存在
        if os.path.exists(self.DATA_FILE):
             try:
                # 获取文件的最后修改时间
                current_modification_time = os.path.getmtime(self.DATA_FILE)

                # 比较最后修改时间是否有变化
                if current_modification_time != self.last_modification_time:
                    # 重新加载任务数据
                    self.load_tasks()
                    self.load_notes()
                    # 更新最后修改时间
                    self.last_modification_time = current_modification_time
             except Exception as e:
                print(f"File check error: {e}")

        # 重新注册定时器
        self.root.after(1000, self.check_file_changes)

    def check_reminders(self):
        current_time = datetime.datetime.now()
        expired_reminders = []
        
        for reminder in self.reminders:
            reminder_time = reminder['datetime']
            task = reminder['task']
            
            # If reminder time is reached
            if current_time >= reminder_time:
                messagebox.showinfo("提醒", f"注意事項 '{task['title']}'!")
                expired_reminders.append(reminder)
                self.mark_task_expired(task)
                # Schedule auto-delete
                self.root.after(int(self.DELETE_DELAY * 1000), lambda t=task: self.delete_task_object(t))
        
        for reminder in expired_reminders:
            self.reminders.remove(reminder)
            
        self.root.after(1000, self.check_reminders)  # Check every second
        
    def mark_task_expired(self, task_to_mark):
        data = {}
        if os.path.exists(self.DATA_FILE):
             try:
                with open(self.DATA_FILE, "r", encoding='utf-8') as file:
                    data = json.load(file)
             except:
                 pass
        
        tasks = data.get('tasks', [])
        found = False
        for task in tasks:
            if task.get('title') == task_to_mark.get('title') and \
               task.get('date') == task_to_mark.get('date') and \
               task.get('time') == task_to_mark.get('time'):
                   task['status'] = 'expired'
                   found = True
                   break
        
        if found:
            with open(self.DATA_FILE, "w", encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            # This save will trigger check_file_changes -> load_tasks -> update list
            
    def delete_task_object(self, task_to_delete):
         # Implementation to delete from file
         # For simplicity, similar to mark_expired but remove from list
         pass # Implement if needed, or rely on Todo app to handle deletions

    def load_tasks(self):
        try:
            # 清除舊的Label
            for widget in self.DoList.winfo_children():
                widget.destroy()
            
            self.reminders = [] # Clear reminders to rebuild
            
            if os.path.exists(self.DATA_FILE):
                with open(self.DATA_FILE, "r", encoding='utf-8') as file:
                    data = json.load(file)
                    tasks = data.get('tasks', [])
                    
                for i, task in enumerate(tasks):
                    # Check for reminders
                    if task.get('status') == 'active':
                        try:
                           rem_dt = datetime.datetime.strptime(f"{task['date']} {task['time']}", "%Y/%m/%d %H:%M")
                           if rem_dt > datetime.datetime.now(): # Only future reminders
                               self.reminders.append({'datetime': rem_dt, 'task': task})
                           elif rem_dt >= datetime.datetime.now() - datetime.timedelta(seconds=60):
                               # If it just passed within last minute (and we might have missed it/just started app), notify?
                               # For now, stick to strictly future or equal
                               pass
                        except Exception as e:
                            print(f"Time parse error: {e}")

                    if task.get('status') == 'expired':
                         continue
                         
                    task_text = f"{task['date']} {task['time']} {task['title']}"
                    label = tk.Label(self.DoList, text=task_text, bg=self.currentactive_color, fg=self.currentfg_color, font=("宋體", 18))
                    label.grid(row=i, column=0, sticky="w", padx=10, pady=10)
        except Exception as e:
            print(f"找不到檔案 or Error: {e}")
            
    def load_notes(self):
        try:
            # 清除舊的Label
            for widget in self.NoteList.winfo_children():
                widget.destroy()
            
            if os.path.exists(self.DATA_FILE):
                with open(self.DATA_FILE, "r", encoding='utf-8') as file:
                    data = json.load(file)
                    notes = data.get('notes', [])
                    
                for i, note in enumerate(notes):
                    note_text = f"{note['title']} {note['content'][:10]}..."
                    label = tk.Label(self.NoteList, text=note_text, bg=self.currentactive_color, fg=self.currentfg_color, font=("微軟正黑體", 18))
                    label.grid(row=i, column=0, sticky="w", padx=10, pady=10)
        except Exception as e:
            print(f"找不到檔案 or Error: {e}")

# 
    def show_info(self, button_text):   #check button content
        print(f"Button clicked: {button_text}")
# 
    def resize_image(self, image_path, width, height):  #input con&setting size
        image = Image.open(image_path)
        image = image.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(image)
    
if __name__ == "__main__":
    root = tk.Tk()
    app = NoteApp(root)
    root.mainloop()
