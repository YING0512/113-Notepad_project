import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import font, colorchooser
from PIL import Image, ImageTk
from tkinter import filedialog
import json
import os

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.last_saved_file = None  # 初始化上一次儲存的文件路徑
        self.fontSize = 12
        self.fontStyle = 'Arial'
        self.DATA_FILE = "data.json"

        # State variables for font attributes
        self.is_bold = False
        self.is_italic = False
        self.is_underline = False

        # Colors
        self.white = "#ffffff"
        self.black = "#000000"
        self.darkBG1 = "#2d2f32"
        self.darkBG2 = "#3f4145"
        self.darkBG3 = "#5c5f64"
        self.brightBG1 = "#e3e5e8"
        self.brightBG2 = "#f7f6f7"

        # Main layout container (No external padding)
        self.main_container = tk.Frame(self.root, border=0, bg=self.darkBG2)
        self.main_container.pack(fill=BOTH, expand=True, padx=0, pady=0)

        # TOP: Text Area Frame
        self.text_frame = tk.Frame(self.main_container, border=0, bg=self.darkBG2)
        self.text_frame.pack(side=TOP, fill=X, expand=False, padx=0, pady=0)

        # Title Frame
        self.labelframe = tk.Frame(self.text_frame, border=0, bg=self.darkBG2)
        self.labelframe.pack(fill=X, padx=0, pady=2)
        self.title_label = tk.Label(self.labelframe, text="標題:", font=("微軟正黑體", 12), bg=self.darkBG2, fg=self.white)
        self.title_label.pack(side=LEFT, padx=5)

        self.input_font = ("微軟正黑體", 16)
        self.text_area = Text(self.labelframe, width=20, height=1, wrap=NONE, font=self.input_font, bg=self.darkBG3, fg=self.white)
        self.text_area.pack(side=LEFT, fill=X, expand=True, padx=5)
        self.text_area.bind("<Return>", lambda event: "break")

        self.other_save_Button = tk.Button(self.labelframe, text="另存新檔", compound=LEFT, command=self.save)
        self.other_save_Button.pack(side=RIGHT, padx=5)
        
        self.saveButton = tk.Button(self.labelframe, text="存檔", compound=LEFT, command=self.save_to_other_file)
        self.saveButton.pack(side=RIGHT, padx=5)

        # Tool bar
        self.tool_bar = tk.Frame(self.text_frame, bg=self.darkBG2)
        self.tool_bar.pack(side=TOP, fill=X, padx=0, pady=0)
        self.font_families = font.families()
        self.font_family_variable = StringVar()
        self.fontfamily_Combobox = Combobox(self.tool_bar, width=30, value=self.font_families, state='readonly',
                                       textvariable=self.font_family_variable)
        self.fontfamily_Combobox.current(self.font_families.index('Arial'))
        self.fontfamily_Combobox.grid(row=0, column=0, padx=13)
        self.size_variable = IntVar()
        self.font_size_Combobox = Combobox(self.tool_bar, width=14, textvariable=self.size_variable, state='readonly',
                                      values=tuple(range(8, 81)))
        self.font_size_Combobox.current(4)
        self.font_size_Combobox.grid(row=0, column=1, padx=5)

        self.fontfamily_Combobox.bind('<<ComboboxSelected>>', self.font_style)
        self.font_size_Combobox.bind('<<ComboboxSelected>>', self.font_size)

        # Buttons for formatting
        self.bold_image = Image.open('icon/bold.png')
        self.bold_icon = ImageTk.PhotoImage(self.bold_image)
        self.boldButton = tk.Button(self.tool_bar, image=self.bold_icon, command=self.bold_text, bd=0, bg=self.darkBG2)
        self.boldButton.grid(row=0, column=3, padx=5)

        self.italic_image = Image.open('icon/italic.png')
        self.italic_icon = ImageTk.PhotoImage(self.italic_image)
        self.italicButton = tk.Button(self.tool_bar, image=self.italic_icon, command=self.italic_text, bd=0, bg=self.darkBG2)
        self.italicButton.grid(row=0, column=4, padx=5)

        self.underline_image = Image.open('icon/underline.png')
        self.underline_icon = ImageTk.PhotoImage(self.underline_image)
        self.underlineButton = tk.Button(self.tool_bar, image=self.underline_icon, command=self.underline_text, bd=0, bg=self.darkBG2)
        self.underlineButton.grid(row=0, column=5, padx=5)

        self.font_color_image = Image.open('icon/font_Color.png')
        self.font_color_icon = ImageTk.PhotoImage(self.font_color_image)
        self.fontColorButton = tk.Button(self.tool_bar, image=self.font_color_icon, command=self.color_select, bd=0, bg=self.darkBG2)
        self.fontColorButton.grid(row=0, column=6, padx=5)

        self.left_align_image = Image.open('icon/left.png')
        self.left_align_icon = ImageTk.PhotoImage(self.left_align_image)
        self.leftAlignButton = tk.Button(self.tool_bar, image=self.left_align_icon, command=self.align_left, bd=0, bg=self.darkBG2)
        self.leftAlignButton.grid(row=0, column=7, padx=5)

        self.center_align_image = Image.open('icon/center.png')
        self.center_align_icon = ImageTk.PhotoImage(self.center_align_image)
        self.centerAlignButton = tk.Button(self.tool_bar, image=self.center_align_icon, command=self.align_center, bd=0, bg=self.darkBG2)
        self.centerAlignButton.grid(row=0, column=8, padx=5)

        self.right_align_image = Image.open('icon/right.png')
        self.right_align_icon = ImageTk.PhotoImage(self.right_align_image)
        self.rightAlignButton = tk.Button(self.tool_bar, image=self.right_align_icon, command=self.align_right, bd=0, bg=self.darkBG2)
        self.rightAlignButton.grid(row=0, column=9, padx=5)

        # Content Frame
        self.contentframe = tk.Frame(self.text_frame, border=0, bg=self.darkBG2)
        self.contentframe.pack(fill=BOTH, expand=False, padx=0, pady=4)

        # Text input for content (reduced width/height to limit initial bounds)
        self.text_input = Text(self.contentframe, width=40, height=18, wrap='word', font=(self.fontStyle, self.fontSize), bg=self.darkBG3, fg=self.white)
        self.text_input.pack(fill=BOTH, expand=True, padx=5, pady=0)

        # BOTTOM: List frame for notes
        self.list_frame = tk.Frame(self.main_container, border=0, bg=self.darkBG2)
        self.list_frame.pack(side=BOTTOM, fill=BOTH, expand=True, padx=0, pady=(5, 20))

        self.list_top = tk.Frame(self.list_frame, bg=self.darkBG2)
        self.list_top.pack(fill=X)
        self.list_label = tk.Label(self.list_top, text="已存筆記", font=("微軟正黑體", 12, "bold"), fg=self.white, bg=self.darkBG2)
        self.list_label.pack(side=LEFT, padx=5)

        self.btn_delete_note = tk.Button(self.list_top, text="刪除選定筆記", fg="white", bg="#EF5350", font=("微軟正黑體", 10, "bold"), relief="flat", command=self.delete_note)
        self.btn_delete_note.pack(side=RIGHT, padx=5)

        self.notes_listbox = Listbox(self.list_frame, height=10, font=("微軟正黑體", 12), border=0, relief="flat", bg=self.darkBG3, fg=self.white, selectbackground="#6CAE75")
        self.notes_listbox.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=(5, 0))
        self.notes_listbox.bind('<<ListboxSelect>>', self.load_selected_note)

        # Change colors and mode
        self.toggle_mode(mode_day=True)

        # Load notes list
        self.load_notes_list()

        # self.root.mainloop() # Removed to prevent blocking when used as module

    def load_notes_list(self):
        self.notes_listbox.delete(0, END)
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r", encoding='utf-8') as file:
                    data = json.load(file)
                    notes = data.get('notes', [])
                    for note in notes:
                        self.notes_listbox.insert(END, note.get('title', '無標題'))
            except:
                pass

    def load_selected_note(self, event):
        selection = self.notes_listbox.curselection()
        if selection:
            selected_title = self.notes_listbox.get(selection[0])
            if os.path.exists(self.DATA_FILE):
                try:
                    with open(self.DATA_FILE, "r", encoding='utf-8') as file:
                        data = json.load(file)
                        notes = data.get('notes', [])
                        for note in notes:
                            if note.get('title') == selected_title:
                                self.text_area.delete("1.0", END)
                                self.text_area.insert("1.0", note.get('title', ''))
                                self.text_input.delete("1.0", END)
                                self.text_input.insert("1.0", note.get('content', ''))
                                break
                except:
                    pass

    def delete_note(self):
        selection = self.notes_listbox.curselection()
        if selection:
            selected_title = self.notes_listbox.get(selection[0])
            if os.path.exists(self.DATA_FILE):
                try:
                    with open(self.DATA_FILE, "r", encoding='utf-8') as file:
                        data = json.load(file)
                    
                    notes = data.get('notes', [])
                    new_notes = [note for note in notes if note.get('title') != selected_title]
                    data['notes'] = new_notes
                    
                    with open(self.DATA_FILE, "w", encoding='utf-8') as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)
                        
                    self.load_notes_list()
                    # Clear editor if deleted note was open
                    if self.text_area.get("1.0", "end-1c") == selected_title:
                        self.text_area.delete("1.0", END)
                        self.text_input.delete("1.0", END)
                except:
                    pass

    # Function to change font style
    def font_style(self, event=None):
        self.fontStyle = self.font_family_variable.get()
        self.update_font()

    # Function to change font size
    def font_size(self, event=None):
        self.fontSize = self.size_variable.get()
        self.update_font()

    # Function to update font configuration
    def update_font(self):
        font_attributes = [self.fontStyle, self.fontSize]
        if self.is_bold:
            font_attributes.append('bold')
        if self.is_italic:
            font_attributes.append('italic')
        if self.is_underline:
            font_attributes.append('underline')
        self.text_input.config(font=font_attributes)

    # Function to toggle bold
    def bold_text(self):
        self.is_bold = not self.is_bold
        self.update_font()

    # Function to toggle italic
    def italic_text(self):
        self.is_italic = not self.is_italic
        self.update_font()

    # Function to toggle underline
    def underline_text(self):
        self.is_underline = not self.is_underline
        self.update_font()

    # Function to select font color
    def color_select(self):
        color = colorchooser.askcolor()
        if color[1]:
            self.text_input.config(fg=color[1])

    # Function to align text right
    def align_right(self):
        self.text_input.tag_remove('left', '1.0', END)
        self.text_input.tag_remove('center', '1.0', END)
        self.text_input.tag_config('right', justify=RIGHT)
        self.text_input.tag_add('right', '1.0', END)

    # Function to align text left
    def align_left(self):
        self.text_input.tag_remove('center', '1.0', END)
        self.text_input.tag_remove('right', '1.0', END)
        self.text_input.tag_config('left', justify=LEFT)
        self.text_input.tag_add('left', '1.0', END)

    # Function to align text center
    def align_center(self):
        self.text_input.tag_remove('left', '1.0', END)
        self.text_input.tag_remove('right', '1.0', END)
        self.text_input.tag_config('center', justify=CENTER)
        self.text_input.tag_add('center', '1.0', END)

    def toggle_mode(self, mode_day):
        # change color
        self.mode_day = mode_day
        if self.mode_day:
            self.currentbg_color = self.darkBG2
            self.currentfg_color = self.white
            self.list_label.config(bg=self.darkBG2, fg=self.white)
            self.list_top.config(bg=self.darkBG2)
            self.notes_listbox.config(bg=self.darkBG3, fg=self.white)
            self.labelframe.config(bg=self.darkBG2)
            self.title_label.config(bg=self.darkBG2, fg=self.white)
            self.tool_bar.config(bg=self.darkBG2)
            self.contentframe.config(bg=self.darkBG2)
        else:
            self.currentbg_color = self.brightBG2
            self.currentfg_color = self.black
            self.list_label.config(bg=self.brightBG2, fg=self.black)
            self.list_top.config(bg=self.brightBG2)
            self.notes_listbox.config(bg=self.white, fg=self.black)
            self.labelframe.config(bg=self.brightBG2)
            self.title_label.config(bg=self.brightBG2, fg=self.black)
            self.tool_bar.config(bg=self.brightBG2)
            self.contentframe.config(bg=self.brightBG2)

        # Update colors
        self.text_area.config(bg=self.currentbg_color, fg=self.currentfg_color)
        self.text_input.config(bg=self.currentbg_color, fg=self.currentfg_color)

    def save(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            try:
                title_text = self.text_area.get("1.0", "end-1c")
                content_text = self.text_input.get("1.0", "end-1c")
                with open(filename, "w", encoding='utf-8') as f:
                    f.write("Title:\n")
                    f.write(title_text + "\n\n")
                    f.write("Content:\n")
                    f.write(content_text)
                
            # 更新最後一次儲存的文件路徑
                self.last_saved_file = filename
                # Also save to internal JSON storage
                self.save_note_to_json(title_text, content_text)
            except Exception as e:
                print("An error occurred while saving the file:", e)
        # self.save_note_to_file() # Removed legacy txt save

    def save_note_to_json(self, title, content):
        data = {}
        if os.path.exists(self.DATA_FILE):
             try:
                with open(self.DATA_FILE, "r", encoding='utf-8') as file:
                    data = json.load(file)
             except:
                 pass
        
        notes = data.get('notes', [])
        
        # Check if note with same title exists, update it
        updated = False
        for note in notes:
            if note.get('title') == title:
                note['content'] = content
                updated = True
                break
        
        if not updated:
            notes.append({'title': title, 'content': content})
            
        data['notes'] = notes
        
        with open(self.DATA_FILE, "w", encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        self.load_notes_list()

    def save_to_other_file(self):
        title_text = self.text_area.get("1.0", "end-1c")
        content_text = self.text_input.get("1.0", "end-1c")
        
        if self.last_saved_file:  
            filename = self.last_saved_file
            try:
                with open(filename, "w", encoding='utf-8') as f:
                    f.write("Title:\n")
                    f.write(title_text + "\n\n")
                    f.write("Content:\n")
                    f.write(content_text)
            except Exception as e:
                print("An error occurred while saving to other file:", e)
        else:
             print("No external file selected, saving implicitly to app storage.")
             
        # Always save to internal storage on "Save"
        self.save_note_to_json(title_text, content_text)


# if __name__ == "__main__":
#     root = Tk()
#     te = TextEditor(root)
#     root.mainloop()