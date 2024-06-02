import tkinter as tk
from PIL import Image, ImageTk
from notecalendarFM import CalendarFM
from notetodoFM import Todo
from notetextFM import TextEditor
import os

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Note")
        self.root.geometry("1200x768")
        root.resizable(False, False)
        self.menu_expanded = False
        self.mode_day = False
        self.last_modification_time = None
        self.root.after(1000, self.check_file_changes)
        
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
      
        # Menu Frame
        self.title_icon_path = "icon/feather-pen.png"
        self.menu_icon_path = "icon/menu-burger.png"
        self.title_icon = self.resize_image(self.title_icon_path, 30, 30)
        self.menu_icon = self.resize_image(self.menu_icon_path, 30, 30)
        self.menu_frame = tk.Frame(self.root, bd=2, bg=self.darkBG1)
        self.menu_frame.place(x=0, y=40, width=50, height=660)
        self.title_frame = tk.Frame(self.root, bg=self.darkBG3)
        self.title_frame.place(x=0, y=0, width=1200, height=40)
        self.title_button = tk.Button(self.title_frame, image=self.title_icon, bd=0,  cursor="hand2",)
        self.title_button.place(x=47, y=2, width=32, height=32)
        
        
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
        self.calendar_app = CalendarFM(self.content_frame, mode_day=self.mode_day, action1=self.text_click, action2=self.todo_click)
        self.calendarr = True
        
        # Information Frame
        self.information_frame = tk.Frame(self.root, bd=0, bg=self.darkBG1)
        self.information_frame.place(x=940, y=40, width=300, height=728)
        self.DoList = tk.Frame(self.information_frame, bg=self.darkBG1)
        self.DoList.place(x=0, y=0, width=300, height=364)
        self.NoteList= tk.Frame(self.information_frame, bg=self.darkBG1 ,bd=1)
        self.NoteList.place(x=0, y=404, width=300, height=364)

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
        self.calender_btn = tk.Button(self.menu_frame, text=" 日　歷", compound=tk.LEFT, font=('宋體', 11 , 'bold'), image=self.calender_icon, bd=0, cursor="hand2",command=self.calendar_click)
        self.calender_btn.image = self.calender_icon_path
        self.calender_btn.place(x=7, y=7, width=90, height=32)
        self.menu_buttons.append(self.calender_btn)

        self.text_btn = tk.Button(self.menu_frame, text=" 記事本", compound=tk.LEFT, font=('宋體', 11 , 'bold'), image=self.text_icon, bd=0, cursor="hand2",command=self.text_click)
        self.text_btn.image = self.text_icon_path
        self.text_btn.place(x=7, y=47, width=90, height=32)
        self.menu_buttons.append(self.text_btn)

        self.todo_btn = tk.Button(self.menu_frame, text=" 備忘錄", compound=tk.LEFT, font=('宋體', 11 , 'bold'), image=self.todo_icon, bd=0, cursor="hand2",command=self.todo_click)
        self.todo_btn.image = self.todo_icon_path
        self.todo_btn.place(x=7, y=87, width=90, height=32)
        self.menu_buttons.append(self.todo_btn)
            
        if self.mode_day:
            self.modetext =" 暗色模式"
        else:
            self.modetext =" 亮色模式"
        self.mode_button.config(text=self.modetext,compound=tk.LEFT, font=('宋體', 11 , 'bold'),command=self.toggle_mode)
        self.mode_button.place(x=7, y=7, width=100, height=32)
# 
    def toggle_menu(self):  #menu size change
        if self.menu_expanded:  # Hide menu buttons
            for button in self.menu_buttons:
                button.destroy()
            # Restore default frame proportions
            self.menu_frame.place(x=0, y=40, width=50, height=660)
            self.set_frame.place(x=0, y=700, width=50, height=660)
            self.content_frame.place(x=50, y=40, width=890, height=728)
            self.information_frame.place(x=940, y=40, width=300, height=728)
            if self.mode_day:
                self.modetext =" 亮色模式"
            else:
                self.modetext =" 暗色模式"
                self.mode_button.config(text=self.modetext)
            self.menu_expanded = False
        else:
            # Adjust frame proportions
            self.menu_frame.place(x=0, y=40, width=120, height=680)
            self.set_frame.place(x=0, y=700, width=120, height=660)
            self.content_frame.place(x=120, y=40, width=820, height=768)
            self.mode_button.config(text="")
            self.menu_expanded = True
        # Recreate menu buttons
        self.create_menu_buttons()
#   
    def toggle_mode(self):
        if self.mode_day:
            self.mode_button.config(image=self.setting_dayicon)
            self.menu_frame.config(bg=self.darkBG1)
            self.set_frame.config(bg=self.darkBG1)
            self.content_frame.config(bg=self.darkBG2)
            self.information_frame.config(bg=self.darkBG1)
            self.DoList.config(bg=self.darkBG1)
            self.title_frame.config(bg=self.darkBG3)
            if self.menu_expanded:
                self.mode_button.config(text=" 亮色模式")
        else:
            self.mode_button.config(image=self.setting_nighticon)
            self.menu_frame.config(bg=self.brightBG1)
            self.set_frame.config(bg=self.brightBG1)
            self.content_frame.config(bg=self.brightBG2)
            self.information_frame.config(bg=self.brightBG1)
            self.DoList.config(bg=self.brightBG1)
            self.title_frame.config(bg=self.brightBG3)
            if self.menu_expanded:
                self.mode_button.config(text=" 暗色模式")

        # Update mode_day in other methods
        for widget in self.content_frame.winfo_children():
            if isinstance(widget, (CalendarFM, Todo)):
                widget.toggle_mode(self.mode_day)

            # Destroy old widgets and create new ones
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        if self.calendarr:
            self.calendar_app = CalendarFM(self.content_frame, mode_day=self.mode_day)
            self.calendar_app.toggle_mode(self.mode_day)
        elif self.todo:
            self.todo_app = Todo(self.content_frame, mode_day=self.mode_day)
            self.todo_app.toggle_mode(self.mode_day)
        else:
            self.mode_day = not self.mode_day
            self.text_app = TextEditor(self.content_frame)
            


        self.mode_day = not self.mode_day

    def calendar_click(self):
        self.calendarr = True
        self.text = False
        self.todo = False
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.calendar_app = CalendarFM(self.content_frame, mode_day=self.mode_day, action1=self.text_click, action2=self.todo_click)
        self.calendar_app.toggle_mode(not self.mode_day)

    def text_click(self):
        self.calendarr = False
        self.text = True
        self.todo = False
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        if self.text:
            self.text_app = TextEditor(self.content_frame)  
        # self.text_app.toggle_mode(not self.mode_day)

    def todo_click(self):
        self.calendarr = False
        self.text = False
        self.todo = True
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.todo_app = Todo(self.content_frame, mode_day=self.mode_day)
        self.todo_app.toggle_mode(not self.mode_day)
        print(self.mode_day)

    def check_file_changes(self):
        # 检查文件是否存在
        if os.path.exists("tasks.txt"):
            # 获取文件的最后修改时间
            current_modification_time = os.path.getmtime("tasks.txt")

            # 比较最后修改时间是否有变化
            if current_modification_time != self.last_modification_time:
                # 重新加载任务数据
                self.load_tasks()
                # 更新最后修改时间
                self.last_modification_time = current_modification_time
        if os.path.exists("notes.txt"):
            # 获取文件的最后修改时间
            current_modification_time = os.path.getmtime("notes.txt")

            # 比较最后修改时间是否有变化
            if current_modification_time != self.last_modification_time:
                # 重新加载任务数据
                self.load_notes()
                # 更新最后修改时间
                self.last_modification_time = current_modification_time

        # 重新注册定时器
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
                    task_text = f"{task[0]} {task[1]} {task[2]}"
                    label = tk.Label(self.DoList, text=task_text, bg="#696969", fg=self.white, font=("宋體", 18))
                    label.grid(row=i, column=0, sticky="w", padx=10, pady=10)
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
                    note_text = f"{note[0]} {note[1]}"
                    label = tk.Label(self.NoteList, text=note_text, bg="#696969", fg=self.white, font=("宋體", 18))
                    label.grid(row=i, column=0, sticky="w", padx=10, pady=10)
        except FileNotFoundError:
            print("找不到檔案")

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
