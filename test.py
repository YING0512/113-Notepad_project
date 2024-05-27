from PIL import Image, ImageTk
import calendar
import tkinter as tk
from datetime import datetime, timedelta


class CalendarFM:
    def __init__(self, parent, mode_day=False):
        self.parent = parent
        self.mainframe = tk.Frame(self.parent, bg="#3f4145")
        self.mainframe.pack(pady=40)

        # Color settings
        self.darkBG2 = "#3f4145"
        self.white = "#ffffff"

        # Get current date
        now = datetime.now()
        self.year = tk.IntVar(value=now.year)
        self.month = tk.IntVar(value=now.month)
        self.day = tk.IntVar(value=(now + timedelta(days=1)).day)
        self.calendar_frame = None

        # Image paths
        self.icon_message_text_off_path = "icon/message-text off.png"
        self.icon_alarm_clock_off_path = "icon/alarm-clock off.png"
        self.icon_alarm_clock_on_path = "icon/alarm-clock on.png"

        # Load tasks
        self.tasks = self.load_tasks("tasks.txt")

        # Initialize interface
        self.create_widgets()

    def load_tasks(self, filename):
        tasks = {}
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                date, _, _ = line.strip().split(',')
                tasks[date] = True
        return tasks

    def create_widgets(self):
        # Year and month layout
        self.year_month_frame = tk.Frame(self.mainframe, bg=self.darkBG2)
        self.year_month_frame.grid(row=0, column=0, columnspan=7, pady=(0, 10))

        # Year selection
        self.year_label = tk.Label(self.year_month_frame, text="Year:", font=(16), bg=self.darkBG2, fg=self.white)
        self.year_label.grid(row=0, column=0, padx=5, pady=5, sticky="ne")
        self.year_spinbox = tk.Spinbox(self.year_month_frame, from_=1900, to=2100, textvariable=self.year,
                                        command=self.update_calendar)
        self.year_spinbox.grid(row=0, column=1, padx=5, pady=5)

        # Month selection
        self.month_label = tk.Label(self.year_month_frame, text="Month:", font=(16), bg=self.darkBG2, fg=self.white)
        self.month_label.grid(row=0, column=2, padx=5, pady=5, sticky="ne")
        self.month_spinbox = tk.Spinbox(self.year_month_frame, from_=1, to=12, textvariable=self.month,
                                         command=self.update_calendar)
        self.month_spinbox.grid(row=0, column=3, padx=5, pady=5)

        # Create week label and date grid layout
        self.calendar_frame = tk.Frame(self.mainframe, bg=self.darkBG2)
        self.calendar_frame.grid(row=1, column=0, columnspan=7, sticky="n")
        weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        for i, day in enumerate(weekdays):
            label = tk.Label(self.calendar_frame, text=day, bg=self.darkBG2, fg=self.white, font=('Helvetica', 12))
            label.grid(row=0, column=i, padx=0, pady=0)

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
                    date_str = "{}/{:02d}/{:02d}".format(year, month, mycalendar[i][j])
                    cell_label = tk.Button(frame, text=mycalendar[i][j], bg=self.darkBG2, fg=self.white,
                                           activebackground="#4c4e52", activeforeground=self.white, relief="ridge",
                                           width=10, height=5, bd=1, font=('Helvetica', 12),
                                           command=lambda date=date_str: self.calendar_btnclick(date))
                    cell_label.grid(row=i + 1, column=j, padx=0, pady=0)
                    row_labels.append(cell_label)

                    # Add image below the button if tasks exist for that date
                    if date_str in self.tasks:
                        image_path = self.icon_alarm_clock_on_path
                    else:
                        image_path = self.icon_alarm_clock_off_path
                    self.add_image_below_button(frame, i + 1, j, image_path)

                else:
                    if mycalendar[i][7] != 7:
                        # Create an empty button
                        cell_label = tk.Button(frame, text="", bg=self.darkBG2, fg=self.white,
                                               activebackground="#4c4e52", activeforeground=self.white,
                                               relief="ridge", width=10, height=5, bd=1,
                                               font=('Helvetica', 12))
                        cell_label.grid(row=i + 1, column=j, padx=0, pady=0)
                        row_labels.append(cell_label)
            self.calendar_grid.append(row_labels)

    def add_image_below_button(self, frame, row, column, image_path):
        image = Image.open(image_path)
        image = image.resize((20, 20), resample=Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(frame, image=photo, bg=self.darkBG2)
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(frame, image=photo, bg=self.darkBG2)
        label.image = photo
        label.grid(row=row + 1, column=column, padx=0, pady=0, sticky="n")

    def calendar_btnclick(self, date):
        # This method is called when a button in the calendar is clicked
        formatted_date = "{}/{}/{}".format(self.year.get(), self.month.get(), date)
        print("Button clicked for date:", formatted_date)
        return formatted_date
        #print("Button clicked for date:", formatted_date)
    
    def update_calendar(self):
        # Update date grid
        for row_labels in self.calendar_grid:
            for cell_label in row_labels:
                if cell_label.cget('text') != "":
                    cell_label.config(bg=self.darkBG2, fg=self.white, activebackground="#4c4e52",
                                      activeforeground=self.white)
                else:
                    cell_label.config(bg=self.darkBG2, activebackground="#4c4e52")

        for row in self.calendar_grid:
            for button in row:
                button.destroy()

        # Create week label and date grid layout
        weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        for i, day in enumerate(weekdays):
            label = tk.Label(self.calendar_frame, text=day, bg=self.darkBG2, fg=self.white, font=('Helvetica', 12))
            label.grid(row=0, column=i, padx=0, pady=0)

        # Create date grid
        self.create_calendar_grid(self.calendar_frame)
        self.calendar_frame.grid(row=1, column=0, columnspan=7)

# Test the program
root = tk.Tk()
app = CalendarFM(root)
root.mainloop()
