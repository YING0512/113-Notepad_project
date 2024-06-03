import calendar
import tkinter as tk
from datetime import datetime, timedelta
from PIL import Image, ImageTk

class CalendarFM:
    def __init__(self, parent, mode_day=False, action1=None, action2=None):
        self.parent = parent
        self.mainframe = tk.Frame(self.parent, bg="#3f4145")
        self.mainframe.pack(pady=40)
        self.selected_cell_label = None
        self.action1 = action1
        self.action2 = action2
        
        # Colors
        self.white = "#ffffff"
        self.black = "#000000"
        self.darkBG1 = "#2d2f32"
        self.darkBG2 = "#3f4145"
        self.darkactive = "#4c4e52"
        self.brightBG1 ="#c0c0c0"
        self.brightBG2 ="#dfdfdf"
        self.brightactive = "#f1f0f2"
        self.currentbg_color = self.darkBG2  # Add this line
        self.currentfg_color = self.white 
        # Get current date
        now = datetime.now()
        self.year = tk.IntVar(value=now.year)
        self.month = tk.IntVar(value=now.month)
        self.day = tk.IntVar(value=(now + timedelta(days=1)).day)
        self.calendar_frame = None

        # Image settings
        self.off_off_image_path = "icon/off-off_image.png"
        self.off_on_image_path = "icon/off-on_image.png"
        self.on_off_image_path = "icon/on-off_image.png"
        self.on_on_image_path = "icon/on-on_image.png"
        self.woff_off_image_path = "icon/woff-off_image.png"
        self.woff_on_image_path = "icon/woff-on_image.png"
        self.won_off_image_path = "icon/won-off_image.png"
        self.won_on_image_path = "icon/won-on_image.png"
        self.off_off_image = self.resize_image(self.off_off_image_path, 48, 19)
        self.off_on_image = self.resize_image(self.off_on_image_path, 48, 19)
        self.on_off_image = self.resize_image(self.on_off_image_path, 48, 19)
        self.on_on_image = self.resize_image(self.on_on_image_path, 48, 19)
        self.woff_off_image = self.resize_image(self.off_off_image_path, 48, 19)
        self.woff_on_image = self.resize_image(self.off_on_image_path, 48, 19)
        self.won_off_image = self.resize_image(self.on_off_image_path, 48, 19)
        self.won_on_image = self.resize_image(self.on_on_image_path, 48, 19)

        # Load tasks
        self.tasks = self.load_tasks("tasks.txt")

        # Initialize interface
        self.create_widgets()

    def resize_image(self, image_path, width, height):
        image = Image.open(image_path)
        image = image.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(image)

    def load_tasks(self, filename):
        tasks = {}
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                date, time, task = line.strip().split(',')
                if date in tasks:
                    tasks[date].append((time, task))
                else:
                    tasks[date] = [(time, task)]
        return tasks

    def toggle_mode(self, mode_day):
        self.mode_day = mode_day
        if self.mode_day:
            self.currentbg_color = self.darkBG2
            self.currentfg_color = self.white
            self.currentactive_color = self.darkactive
            # self.off_offimage = self.woff_off_image
            # self.off_onimage = self.woff_off_image
            # self.on_offimage = self.woff_off_image
            # self.on_onimage = self.woff_off_image
        else:
            self.currentbg_color = self.brightBG2
            self.currentfg_color = self.black
            self.currentactive_color = self.brightactive
            # self.off_offimage = self.off_off_image
            # self.off_onimage = self.off_off_image
            # self.on_offimage = self.off_off_image
            # self.on_onimage = self.off_off_image

        self.mainframe.config(bg=self.currentbg_color)
        self.year_month_frame.config(bg=self.currentbg_color)
        self.year_label.config(bg=self.currentbg_color, fg=self.currentfg_color)
        self.month_label.config(bg=self.currentbg_color, fg=self.currentfg_color)
        self.calendar_frame.config(bg=self.currentbg_color)
        
        for label in self.weekday_labels:
            label.config(bg=self.currentbg_color, fg=self.currentfg_color)
        for row_labels in self.calendar_grid:
            for cell_label in row_labels:
                if cell_label.cget('text') != "":
                    cell_label.config(bg=self.currentbg_color, fg=self.currentfg_color,
                                      activebackground=self.currentactive_color, activeforeground=self.currentfg_color)
                else:
                    cell_label.config(bg=self.currentbg_color, activebackground=self.currentactive_color)

    def create_widgets(self):
        self.year_month_frame = tk.Frame(self.mainframe, bg=self.darkBG2)
        self.year_month_frame.grid(row=0, column=0, columnspan=7, pady=(0, 10))

        self.year_label = tk.Label(self.year_month_frame, text="Year:", font=(16), bg=self.darkBG2, fg=self.white)
        self.year_label.grid(row=0, column=0, padx=5, pady=5, sticky="ne")

        self.year_spinbox = tk.Spinbox(self.year_month_frame, from_=1900, to=2100, textvariable=self.year, command=self.update_calendar)
        self.year_spinbox.grid(row=0, column=1, padx=5, pady=5)

        self.month_label = tk.Label(self.year_month_frame, text="Month:", font=(16), bg=self.darkBG2, fg=self.white)
        self.month_label.grid(row=0, column=2, padx=5, pady=5, sticky="ne")

        self.month_spinbox = tk.Spinbox(self.year_month_frame, from_=1, to=12, textvariable=self.month, command=self.update_calendar)
        self.month_spinbox.grid(row=0, column=3, padx=5, pady=5)

        self.calendar_frame = tk.Frame(self.mainframe, bg=self.darkBG2)
        self.calendar_frame.grid(row=1, column=0, columnspan=7, sticky="n")

        weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        self.weekday_labels = []
        for i, day in enumerate(weekdays):
            label = tk.Label(self.calendar_frame, text=day, bg=self.darkBG2, fg=self.white, font=('Helvetica', 12))
            label.grid(row=0, column=i, padx=0, pady=0)
            self.weekday_labels.append(label)

        self.calendar_grid = []
        self.create_calendar_grid(self.calendar_frame)

        self.button_frame = tk.Frame(self.mainframe, bg=self.darkBG2)
        self.button_frame.grid(row=2, column=0, columnspan=7, pady=10)

    def create_calendar_grid(self, frame):
        for row in self.calendar_grid:
            for label in row:
                label.destroy()
        self.calendar_grid.clear()

        year = self.year.get()
        month = self.month.get()
        cal = calendar.monthcalendar(year, month)
        mycalendar = [[0 for i in range(8)] for j in range(7)]
        for i, week in enumerate(cal):
            for j, day in enumerate(week):
                if day != 0:
                    weekday = (calendar.weekday(year, month, day) + 1) % 7
                    if weekday == 0:
                        i += 1
                        mycalendar[i][weekday] = day
                        break
                    else:
                        mycalendar[i][weekday] = day

        cnt = 0
        for i in range(7):
            for j in range(7):
                if mycalendar[i][j] == 0:
                    cnt += 1
            mycalendar[i][7] = cnt
            cnt = 0
            if mycalendar[0][7] == 7:
                del mycalendar[0]
                mycalendar.append([0] * len(mycalendar[0]))

        for i in range(6):
            row_labels = []
            for j in range(7):
                if mycalendar[i][j] != 0:
                    day = mycalendar[i][j]
                    formatted_date = "{}/{:02d}/{:02d}".format(self.year.get(), self.month.get(), day)
                    self.image = self.off_on_image if formatted_date in self.tasks else self.off_off_image
                    cell_label = tk.Label(frame, text=day, bg=self.currentbg_color, fg=self.currentfg_color, image=self.image, compound="bottom",
                                          activebackground="#4c4e52", activeforeground=self.white, relief="ridge",
                                          width=94, height=97, bd=1, font=('Helvetica', 16, 'bold'))
                    cell_label.grid(row=i+1, column=j, padx=0, pady=0)
                    cell_label.bind("<Button-1>", lambda event, day=day: self.calendar_btnclick(day, event))
                    row_labels.append(cell_label)
                else:
                    if mycalendar[i][7] != 7:
                        cell_label = tk.Button(frame, text="", bg=self.currentbg_color, fg=self.currentfg_color, activebackground=self.darkBG2,
                                               activeforeground=self.white, relief="ridge", width=10, height=5, bd=1,
                                               font=('Helvetica', 12))
                        cell_label.grid(row=i+1, column=j, padx=0, pady=0)
                        row_labels.append(cell_label)
            i += 1
            self.calendar_grid.append(row_labels)

    def calendar_btnclick(self, date, event):
        formatted_date = "{}/{:02d}/{:02d}".format(self.year.get(), self.month.get(), date)
        print("Button clicked for date:", formatted_date)

        # 清除之前选中的cell_label上的按钮
        if self.selected_cell_label:
            for widget in self.selected_cell_label.winfo_children():
                widget.destroy()

        def action1():
            print("Action 1 for", formatted_date)

        def action2():
            print("Action 2 for", formatted_date)

        # 将按钮放在当前选中的cell_label上
        btn1 = tk.Button(event.widget, text="記事本", width=5, height=1, command=self.action1)
        btn1.place(x=2, y=73)

        btn2 = tk.Button(event.widget, text="備忘錄", width=5, height=1, command=self.action2)
        btn2.place(x=48, y=73)

        # 更新当前选中的cell_label
        self.selected_cell_label = event.widget


    def update_calendar(self):
        for row_labels in self.calendar_grid:
            for cell_label in row_labels:
                if cell_label.cget('text') != "":
                    cell_label.config(bg=self.darkBG2, fg=self.white, compound="bottom",
                                    activebackground="#4c4e52", activeforeground=self.white, relief="ridge",
                                    width=94, height=97, bd=1, font=('Helvetica', 16, 'bold'))
                else:
                    cell_label.config(bg=self.darkBG2, fg=self.white, activebackground=self.darkBG2,
                                    activeforeground=self.white, relief="ridge", width=10, height=5, bd=1,
                                    font=('Helvetica', 12))

        # Update tasks
        self.tasks = self.load_tasks("tasks.txt")

        # Destroy existing buttons
        for row in self.calendar_grid:
            for button in row:
                button.destroy()

        # Recreate weekday labels
        weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        self.weekday_labels = []
        for i, day in enumerate(weekdays):
            label = tk.Label(self.calendar_frame, text=day, bg=self.currentbg_color, fg=self.currentfg_color, font=('Helvetica', 12))
            label.grid(row=0, column=i, padx=0, pady=0)
            self.weekday_labels.append(label)

        # Recreate date grid
        self.create_calendar_grid(self.calendar_frame)
        self.calendar_frame.grid(row=1, column=0, columnspan=7)


# if __name__ == "__main__":
#     root = tk.Tk()
#     app = CalendarFM(root)
#     root.mainloop()
