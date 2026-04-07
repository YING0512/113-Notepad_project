import tkinter as tk    #pip install tk
from PIL import Image, ImageTk  #pip install pillow
from notecalendarFM import CalendarFM
from notetodoFM import Todo
from notetextFM import TextEditor

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Note")
        self.root.geometry("1200x768")
        root.resizable(False, False)
        self.menu_expanded = False
        self.mode_day = True
        
        #color
        self.white="#ffffff"
        self.black="#000000"
        self.darkBG1="#2d2f32"
        self.darkBG2="#3f4145"
      
        # Menu Frame
        self.menu_frame = tk.Frame(self.root, bd=2, bg=self.darkBG1)
        self.menu_frame.place(x=0, y=0, width=50, height=700)
        
        #Setting frame
        self.setting_dayicon_path = "icon/brightness.png"
        self.setting_nighticon_path = "icon/moon.png"
        self.setting_dayicon = self.resize_image(self.setting_dayicon_path, 20, 20)
        self.setting_nighticon = self.resize_image(self.setting_nighticon_path, 20, 20)
        self.set_frame = tk.Frame(self.root, bd=1, bg=self.darkBG1)
        self.set_frame.place(x=0, y=700, width=50, height=68)
        self.mode_button = tk.Button(self.set_frame, cursor="hand2", bd=1, fg=self.black, bg=self.white, image=self.setting_dayicon, command=self.toggle_mode)
        self.mode_button.place(x=7, y=0, width=32, height=40)
        
        # Content Frame
        self.content_frame = tk.Frame(self.root, bd=1, bg=self.darkBG2)
        self.content_frame.place(x=50, y=0, width=850, height=768)
        self.calendar_app = CalendarFM(self.content_frame)
        
        # Information Frame
        self.information_frame = tk.Frame(self.root, bd=2, bg=self.darkBG1)
        self.information_frame.place(x=900, y=0, width=300, height=768)
        
        # Icon location
        self.calender_icon_path = Image.open("icon/daily-calendar (1).png").resize((20, 20))
        self.calender_icon = ImageTk.PhotoImage(self.calender_icon_path)
        self.text_icon_path = Image.open("icon/edit.png").resize((20, 20))
        self.text_icon = ImageTk.PhotoImage(self.text_icon_path)
        self.todo_icon_path = Image.open("icon/list-check.png").resize((20, 20))
        self.todo_icon = ImageTk.PhotoImage(self.todo_icon_path)

        self.menu_icon_path = "icon/menu-burger.png"
        
        # Create menu buttons
        self.create_menu_buttons()  # Start with closed menu buttons

        # Menu Button
        self.menu_icon = self.resize_image(self.menu_icon_path, 20, 20)
        self.menu_btn = tk.Button(self.menu_frame,text="menu",fg=self.black, image=self.menu_icon, bd=0, cursor="hand2", command=self.toggle_menu)
        self.menu_btn.image = self.menu_icon
        self.menu_btn.place(x=7, y=7, width=32, height=32)
# 
    def create_menu_buttons(self):
        self.menu_buttons = []
        button_func = self.create_menu_buttons_expanded if self.menu_expanded else self.create_menu_buttons_closed
        button_func()
# 
    def create_menu_buttons_closed(self):#menu closed
        # Create buttons individually
        self.calender_btn = tk.Button(self.menu_frame, image=self.calender_icon, fg=self.black, bd=0, cursor="hand2",command=self.calendar_click)
        self.calender_btn.image = self.calender_icon_path
        self.calender_btn.place(x=7, y=47, width=32, height=32)
        self.menu_buttons.append(self.calender_btn)

        self.text_btn = tk.Button(self.menu_frame, image=self.text_icon, fg=self.black, bd=0, cursor="hand2",command=self.text_click)
        self.text_btn.image = self.text_icon_path
        self.text_btn.place(x=7, y=87, width=32, height=32)
        self.menu_buttons.append(self.text_btn)

        self.todo_btn = tk.Button(self.menu_frame, image=self.todo_icon, fg=self.black, bd=0, cursor="hand2",command=self.todo_click)
        self.todo_btn.image = self.todo_icon_path
        self.todo_btn.place(x=7, y=127, width=32, height=32)
        self.menu_buttons.append(self.todo_btn)
        self.mode_button.config(text="",command=self.toggle_mode)
        self.mode_button.place(x=7, y=7, width=32, height=32)
# 
    def create_menu_buttons_expanded(self):#menu expanded
        self.calender_btn = tk.Button(self.menu_frame, text=" 日　歷", compound=tk.LEFT, font=('宋體', 11 , 'bold'), image=self.calender_icon, fg=self.black, bd=0, cursor="hand2",command=self.calendar_click)
        self.calender_btn.image = self.calender_icon_path
        self.calender_btn.place(x=7, y=47, width=90, height=32)
        self.menu_buttons.append(self.calender_btn)

        self.text_btn = tk.Button(self.menu_frame, text=" 記事本", compound=tk.LEFT, font=('宋體', 11 , 'bold'), image=self.text_icon, fg=self.black, bd=0, cursor="hand2",command=self.text_click)
        self.text_btn.image = self.text_icon_path
        self.text_btn.place(x=7, y=87, width=90, height=32)
        self.menu_buttons.append(self.text_btn)

        self.todo_btn = tk.Button(self.menu_frame, text=" 提　醒", compound=tk.LEFT, font=('宋體', 11 , 'bold'), image=self.todo_icon, fg=self.black, bd=0, cursor="hand2",command=self.todo_click)
        self.todo_btn.image = self.todo_icon_path
        self.todo_btn.place(x=7, y=127, width=90, height=32)
        self.menu_buttons.append(self.todo_btn)
            
        self.mode_button.config(text=" 亮色模式", compound=tk.LEFT, font=('宋體', 11 , 'bold'),command=self.toggle_mode)
        self.mode_button.place(x=7, y=7, width=100, height=32)
# 
    def toggle_menu(self):  #menu size change
        if self.menu_expanded:  # Hide menu buttons
            for button in self.menu_buttons:
                button.destroy()
            # Restore default frame proportions
            self.menu_frame.place(x=0, y=0, width=50, height=700)
            self.set_frame.place(x=0, y=700, width=50, height=68)
            self.content_frame.place(x=50, y=0, width=850, height=768)
            self.information_frame.place(x=900, y=0, width=300, height=768)
            self.menu_expanded = False
        else:
            # Adjust frame proportions
            self.menu_frame.place(x=0, y=0, width=120, height=700)
            self.set_frame.place(x=0, y=700, width=120, height=68)
            self.content_frame.place(x=120, y=0, width=780, height=768)
            self.menu_expanded = True
        # Recreate menu buttons
        self.create_menu_buttons()
#   
    def toggle_mode(self):  #background   
        if self.mode_day:
            self.mode_button.config(image=self.setting_nighticon)
            self.mode_button_text = " 暗色模式"
        else:
            self.mode_button.config(image=self.setting_dayicon)
            self.mode_button_text = " 亮色模式"
        self.mode_button.config(text=self.mode_button_text)
        self.mode_day = not self.mode_day
# 
    def show_info(self, button_text):   #check button content
        print(f"Button clicked: {button_text}")
# 
    def resize_image(self, image_path, width, height):  #input con&setting size
        image = Image.open(image_path)
        image = image.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(image)
# 
    def calendar_click(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()          
        self.calendar_app = CalendarFM(self.content_frame)
    
    def text_click(self):    
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.text_app = TextEditor(self.content_frame)
    
    def todo_click(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.todo_app = Todo(self.content_frame)
        
    
if __name__ == "__main__":
    root = tk.Tk()
    app = NoteApp(root)
    root.mainloop()
