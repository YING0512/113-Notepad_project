import calendar
import tkinter as tk
from datetime import datetime, timedelta
from PIL import Image, ImageTk

class CalendarFM:
    def __init__(self, parent, mode_day=False):  # 新增mode_day參數，默認為False
        self.parent = parent
        self.mainframe = tk.Frame(self.parent, bg="#3f4145")
        self.mainframe.pack(pady=40)

        # Colors
        self.white = "#ffffff"
        self.black = "#000000"
        self.darkBG1 = "#2d2f32"
        self.darkBG2 = "#3f4145"
        self.darkactive = "#4c4e52"
        self.brightBG1 = "#e3e5e8"
        self.brightBG2 = "#f7f6f7"
        self.brightactive = "#f1f0f2"

        # Get current date
        now = datetime.now()
        self.year = tk.IntVar(value=now.year)  # Initialize year variable, set to current year
        self.month = tk.IntVar(value=now.month)  # Initialize month variable, set to current month
        self.day = tk.IntVar(value=(now + timedelta(days=1)).day)  # Initialize date variable, set to tomorrow's date
        self.calendar_frame = None

        # Image settings
        self.off_off_image_path = "icon/off-off_image.png"
        self.off_on_image_path = "icon/off-on_image.png"
        self.on_off_image_path = "icon/on-off_image.png"
        self.on_on_image_path = "icon/on-on_image.png"
        self.off_off_image = self.resize_image(self.off_off_image_path, 20, 20)
        self.off_on_image = self.resize_image(self.off_on_image_path, 20, 20)
        self.on_off_image = self.resize_image(self.on_off_image_path, 20, 20)
        self.on_on_image = self.resize_image(self.on_on_image_path, 20, 20)

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
        # change color
        self.mode_day = mode_day
        if self.mode_day:
            self.currentbg_color = self.darkBG2
            self.currentfg_color = self.white
            self.currentactive_color = self.darkactive
        else:
            self.currentbg_color = self.brightBG2
            self.currentfg_color = self.black
            self.currentactive_color = self.brightactive

        self.mainframe.config(bg=self.currentbg_color)
        self.year_month_frame.config(bg=self.currentbg_color)
        self.year_label.config(bg=self.currentbg_color, fg=self.currentfg_color)
        self.month_label.config(bg=self.currentbg_color, fg=self.currentfg_color)
        self.calendar_frame.config(bg=self.currentbg_color)
        for label in self.weekday_labels:
            label.config(bg=self.currentbg_color, fg=self.currentfg_color)
        for row_labels in self.calendar_grid:
            for cell_label in row_labels:
                if cell_label.cget('text') != "":  # .cget() Get the current value of a specific widget attribute.
                    cell_label.config(bg=self.currentbg_color, fg=self.currentfg_color,
                                      activebackground=self.currentactive_color, activeforeground=self.currentfg_color)
                else:
                    cell_label.config(bg=self.currentbg_color, activebackground=self.currentactive_color)

    def create_widgets(self):
        # Year and month layout
        self.year_month_frame = tk.Frame(self.mainframe, bg=self.darkBG2)
        self.year_month_frame.grid(row=0, column=0, columnspan=7, pady=(0, 10))

        # Year selection
        self.year_label = tk.Label(self.year_month_frame, text="Year:", font=(16), bg=self.darkBG2, fg=self.white)
        self.year_label.grid(row=0, column=0, padx=5, pady=5, sticky="ne")

        self.year_spinbox = tk.Spinbox(self.year_month_frame, from_=1900, to=2100, textvariable=self.year, command=self.update_calendar)
        self.year_spinbox.grid(row=0, column=1, padx=5, pady=5)

        # Month selection
        self.month_label = tk.Label(self.year_month_frame, text="Month:", font=(16), bg=self.darkBG2, fg=self.white)
        self.month_label.grid(row=0, column=2, padx=5, pady=5, sticky="ne")

        self.month_spinbox = tk.Spinbox(self.year_month_frame, from_=1, to=12, textvariable=self.month, command=self.update_calendar)
        self.month_spinbox.grid(row=0, column=3, padx=5, pady=5)

        # Create week label and date grid layout
        self.calendar_frame = tk.Frame(self.mainframe, bg=self.darkBG2)
        self.calendar_frame.grid(row=1, column=0, columnspan=7, sticky="n")

        weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        self.weekday_labels = []  # 用於保存星期標籤的列表
        for i, day in enumerate(weekdays):
            label = tk.Label(self.calendar_frame, text=day, bg=self.darkBG2, fg=self.white, font=('Helvetica', 12))
            label.grid(row=0, column=i, padx=0, pady=0)
            self.weekday_labels.append(label)  # 將每個標籤添加到列表中

        # Create date grid
        self.calendar_grid = []
        self.create_calendar_grid(self.calendar_frame)

    def create_calendar_grid(self, frame):
        # Clear existing date grid
        for row in self.calendar_grid:
            for label in row:
                label.destroy()
        self.calendar_grid.clear()

        # Get calendar for selected date
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
            row_labels = []  # Initialize list of labels for each row
            for j in range(7):
                if mycalendar[i][j] != 0:
                    day = mycalendar[i][j]
                    formatted_date = "{}/{:02d}/{:02d}".format(self.year.get(), self.month.get(), day)
                    # Check if the date has tasks and select the appropriate image
                    image = self.off_on_image if formatted_date in self.tasks else self.off_off_image
                    # Create a button with command to call calendar_btnclick with the clicked date
                    cell_label = tk.Button(frame, text=day, bg=self.darkBG2, fg=self.white, image="image", compound="bottom",
                                           activebackground="#4c4e52", activeforeground=self.white, relief="ridge",
                                           width=92, height=97, bd=1, font=('Helvetica', 14),
                                           command=lambda day=day: self.calendar_btnclick(day))
                    cell_label.grid(row=i+1, column=j, padx=0, pady=0)
                    row_labels.append(cell_label)
                else:
                    if mycalendar[i][7] != 7:
                        # Create an empty button
                        cell_label = tk.Button(frame, text="", bg=self.darkBG2, fg=self.white, activebackground="#4c4e52",
                                               activeforeground=self.white, relief="ridge", width=10, height=5, bd=1,
                                               font=('Helvetica', 12))
                        cell_label.grid(row=i+1, column=j, padx=0, pady=0)
                        row_labels.append(cell_label)
                j += 1
            i += 1
            self.calendar_grid.append(row_labels)

    def calendar_btnclick(self, date):
        # This method is called when a button in the calendar is clicked
        formatted_date = "{}/{:02d}/{:02d}".format(self.year.get(), self.month.get(), date)
        print("Button clicked for date:", formatted_date)
        return formatted_date

    def update_calendar(self):  # Update date grid
        for row_labels in self.calendar_grid:
            for cell_label in row_labels:
                if cell_label.cget('text') != "":  # .cget() Get the current value of a specific widget attribute.
                    cell_label.config(bg=self.currentbg_color, fg=self.currentfg_color,
                                      activebackground=self.currentactive_color, activeforeground=self.currentfg_color)
                else:
                    cell_label.config(bg=self.currentbg_color, activebackground=self.currentactive_color)
        for row in self.calendar_grid:
            for button in row:
                button.destroy()

        weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        self.weekday_labels = []  # 用於保存星期標籤的列表
        for i, day in enumerate(weekdays):
            label = tk.Label(self.calendar_frame, text=day, bg=self.darkBG2, fg=self.white, font=('Helvetica', 12))
            label.grid(row=0, column=i, padx=0, pady=0)
            self.weekday_labels.append(label)  # 將每個標籤添加到列表中

        # Create date grid
        self.calendar_grid = []
        calendar_frame = self.calendar_frame
        self.create_calendar_grid(calendar_frame)
        calendar_frame.grid(row=1, column=0, columnspan=7)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarFM(root)
    root.mainloop()
