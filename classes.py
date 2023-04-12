import tkinter
from tkinter import messagebox
from tkinter import filedialog
import functions
import sqlite3
import os
from sqlite3 import Error


dirname = os.path.dirname(__file__)
notepad_icon = os.path.join(dirname, 'pictures\\notepad.png')
terms_of_use = os.path.join(dirname, 'Terms of use.txt')
database_file = os.path.join(dirname, 'database.sqlite')
login_icon = os.path.join(dirname, 'pictures\\login_button.png')

class WindowsContainer(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.geometry("400x400")
        self.iconphoto(True, tkinter.PhotoImage(file=notepad_icon))
        self.title("Notepad2000")
        self.resizable(width=0, height=0)
        self.login_window = LoginWindow()
        self.editor_window = EditorWindow()
        self.terms_window = TermsWindow()
        self.font_selection_window = FontSelectionWindow()
        self.editor_window.withdraw()
        self.terms_window.withdraw()
        self.font_selection_window.withdraw()
        self.withdraw()





class EditorWindow(tkinter.Toplevel):

    def __init__(self, *args, **kwargs):
        tkinter.Toplevel.__init__(self, *args, **kwargs)
        self.reference_file = None
        self.reference_file_path = None
        self.was_file_saved_or_opened_previously = None
        self.previously_saved_or_opened_filepath = None
        self.font_selection_window = None
        self.saved_font = 'Segoe UI'
        self.saved_font_size = 14

        self.geometry("400x400")
        self.iconphoto(True, tkinter.PhotoImage(file=notepad_icon))
        self.title("Notepad2000")
        self.resizable(width=0, height=0)

        ## Adding frame to force text field to be fixed size ##
        self.text_frame = tkinter.Frame(self,
                                        width=400,
                                        height=370)

        self.initial_font= ("Segoe UI", 14)
        self.text_field = tkinter.Text(master=self.text_frame,
                                  font=self.initial_font,
                                       height=16)
        self.scroll_bar = tkinter.Scrollbar(self, orient="vertical", command=self.text_field.yview)
        self.text_field.configure(yscrollcommand=self.scroll_bar.set)

        self.scroll_bar.pack(side="right", fill="y")
        self.text_frame.pack()
        self.text_field.place(x=0, y=0, width=385, height=370)

        ## Adding menubar ##
        self.menu_bar = tkinter.Menu(self)
        file_menu_droplist_container = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu_droplist_container)
        file_menu_droplist_container.add_command(label="New", command=self.open_new_document_window)
        file_menu_droplist_container.add_command(label="Open", command=self.open_open_file_window)
        file_menu_droplist_container.add_command(label="Save", command=self.save_file_no_window)
        file_menu_droplist_container.add_command(label="Save As...", command=self.open_save_file_window)
        file_menu_droplist_container.add_separator()
        file_menu_droplist_container.add_command(label="Exit", command=self.quit)

        edit_menu_droplist_container = tkinter.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu_droplist_container)
        edit_menu_droplist_container.add_command(label="Font", command=self.open_font_selection_window)
        edit_menu_droplist_container.add_command(label="Clear All", command=self.clear_all)
        self.config(menu=self.menu_bar)

        self.bottom_bar_frame = tkinter.Frame(self)
        self.display_font_label = tkinter.Label(self.bottom_bar_frame, text=self.initial_font[0] +"  "+ str(self.initial_font[1]), font=("Arial", 10))
        self.display_file_name_label = tkinter.Label(self.bottom_bar_frame, text="Untitled document", font=("Arial", 10))
        self.bottom_bar_frame.pack(side="bottom")
        self.display_font_label.grid(row=0, column=0, sticky='w')
        self.display_file_name_label.grid(row=0, column=2, sticky='e')




    def open_font_selection_window(self):
        self.font_selection_window = FontSelectionWindow()
        self.font_selection_window.group_font.set(self.saved_font)
        self.font_selection_window.group_size.set(self.saved_font_size)
        self.font_selection_window.save_button.configure(command=self.save_font_settings)

    def save_font_settings(self):
        self.saved_font = self.font_selection_window.group_font.get()
        self.saved_font_size = self.font_selection_window.group_size.get()
        self.text_field.configure(font=(self.saved_font, self.saved_font_size))
        self.display_font_label.configure(text=self.saved_font + "  " + str(self.saved_font_size), font=("Arial", 10))
        self.font_selection_window.destroy()

    def open_save_file_window(self):
        file_to_be_saved_to = tkinter.filedialog.asksaveasfile(defaultextension='.txt', filetypes=[("Plain Text File", ".txt"),
                                                                                                   ("HTML File",".html")])
        print(file_to_be_saved_to)
        if str(file_to_be_saved_to) != "None":
            self.reference_file_path = str(file_to_be_saved_to.name)
            self.reference_file = True
            self.was_file_saved_or_opened_previously = True
            self.previously_saved_or_opened_filepath = self.reference_file_path

            self.display_file_name_label.configure(text=functions.get_file_name_from_windows_path(self.previously_saved_or_opened_filepath))
            text_field_content = str(self.text_field.get(1.0, tkinter.END))
            file_to_be_saved_to.write(text_field_content)
            file_to_be_saved_to.close()
        else:
            self.display_file_name_label.configure(text=functions.get_file_name_from_windows_path(self.previously_saved_or_opened_filepath))
            self.reference_file = False
            self.reference_file_path = None

    def open_open_file_window(self):
        file_to_be_opened = tkinter.filedialog.askopenfile()

        if str(file_to_be_opened) != "None":
            self.reference_file = True
            self.reference_file_path = str(file_to_be_opened.name)
            self.was_file_saved_or_opened_previously = True
            self.previously_saved_or_opened_filepath = self.reference_file_path

            self.display_file_name_label.configure(text=functions.get_file_name_from_windows_path(self.previously_saved_or_opened_filepath))
            opened_file_content = file_to_be_opened.read()
            self.text_field.delete(1.0, tkinter.END)
            self.text_field.insert(1.0, opened_file_content)
            file_to_be_opened.close()
        else:
            self.display_file_name_label.configure(text=functions.get_file_name_from_windows_path(self.previously_saved_or_opened_filepath))
            self.reference_file = False
            self.reference_file_path = None

    def save_file_no_window(self):
        if self.reference_file == True:
            file = open(self.reference_file_path, "w")
            text_field_content = str(self.text_field.get(1.0, tkinter.END))
            file.write(text_field_content)
            file.close()

    def clear_all(self):
        self.text_field.delete(1.0, tkinter.END)

    def open_new_document_window(self):
        self.text_field.delete(1.0, tkinter.END)
        file_to_be_saved_to = tkinter.filedialog.asksaveasfile(defaultextension='.txt', filetypes=[("Plain Text File", ".txt"),
                                                                                                   ("HTML File",".html")])
        print(file_to_be_saved_to)
        if str(file_to_be_saved_to) != "None":
            self.reference_file_path = str(file_to_be_saved_to.name)
            self.reference_file = True
            self.was_file_saved_or_opened_previously = True
            self.previously_saved_or_opened_filepath = self.reference_file_path

            self.display_file_name_label.configure(text=functions.get_file_name_from_windows_path(self.previously_saved_or_opened_filepath))
            text_field_content = str(self.text_field.get(1.0, tkinter.END))
            file_to_be_saved_to.write(text_field_content)
            file_to_be_saved_to.close()
        else:
            self.display_file_name_label.configure(text=functions.get_file_name_from_windows_path(self.previously_saved_or_opened_filepath))
            self.reference_file = False
            self.reference_file_path = None

    def open_admin_panel_window(self):
        print("Admin panel opened")
        AdminPanelWindow()





class AdminPanelWindow(tkinter.Toplevel):
    def __init__(self, *args, **kwargs):
        tkinter.Toplevel.__init__(self, *args, **kwargs)
        self.database = Database()
        self.admin_checkbox_value = tkinter.IntVar()
        self.search_query = None
        self.search_results_number = 0
        self.search_results_label_list = []
        self.geometry("900x550")
        self.iconphoto(True,tkinter.PhotoImage(file=notepad_icon))
        self.title("Notepad2000")
        self.resizable(width=0, height=0)
        self.username_entry_var = tkinter.StringVar()
        self.surname_entry_var = tkinter.StringVar()


        # Search for user
        self.search_user_frame = tkinter.LabelFrame(self, text="Search for users", width=450, height=240)
        self.search_user_frame.grid_propagate(0)
        self.username_entry = tkinter.Entry(self.search_user_frame, font=("Arial", 14),
                                         foreground="black",
                                         textvariable=self.username_entry_var)
        self.surname_entry = tkinter.Entry(self.search_user_frame, font=("Arial", 14),
                                            foreground="black",
                                            textvariable=self.surname_entry_var)
        self.username_label = tkinter.Label(self.search_user_frame, text="Username", font=("Arial",14))
        self.surname_label = tkinter.Label(self.search_user_frame, text="Surname", font=("Arial",14))
        self.search_button = tkinter.Button(self.search_user_frame, text="Search", font=("Arial",14), command=self.display_search_results)

        self.username_label.grid(row=0, column=0, sticky='w')
        self.username_entry.grid(row=0, column=1)
        self.surname_label.grid(row=1, column=0, sticky='w')
        self.surname_entry.grid(row=1, column=1)
        self.search_button.grid(row=2, column=0, columnspan=2)
        self.search_user_frame.grid(row=0, column=0)

        # Bottom frame to display labels with search results

        self.search_result_frame = tkinter.LabelFrame(self,
                                        width=450,
                                        height=350)
        self.search_result_frame.grid_propagate(0)

        # Create 5 labels for column names
        self.column_username = tkinter.Label(self.search_result_frame, text="Username", font=("Arial", 10, "bold"), relief="solid")
        self.column_admin = tkinter.Label(self.search_result_frame, text="Admin?", font=("Arial", 10, "bold"), relief="solid")
        self.column_name = tkinter.Label(self.search_result_frame, text="Name", font=("Arial", 10, "bold"), relief="solid")
        self.column_surname = tkinter.Label(self.search_result_frame, text="Surname", font=("Arial", 10, "bold"), relief="solid")
        self.column_office_location = tkinter.Label(self.search_result_frame, text="Office Location", font=("Arial", 10, "bold"), relief="solid")

        self.column_username.grid(row=0, column=0, padx=7)
        self.column_admin.grid(row=0, column=1, padx=7)
        self.column_name.grid(row=0, column=2, padx=7)
        self.column_surname.grid(row=0, column=3, padx=7)
        self.column_office_location.grid(row=0, column=4, padx=7)

        self.search_result_frame.grid(row=1, column=0)

        # Right side of the window, add new user to database

        self.add_user_frame = tkinter.LabelFrame(self, text="Add user", width=450, height=240)
        self.add_user_frame.grid_propagate(0)
        self.add_user_username_entry = tkinter.Entry(self.add_user_frame, font=("Arial", 14),
                                         foreground="black")
        self.add_user_name_entry = tkinter.Entry(self.add_user_frame, font=("Arial", 14),
                                            foreground="black")
        self.add_user_username_label = tkinter.Label(self.add_user_frame, text="Username", font=("Arial",14))
        self.add_user_name_label = tkinter.Label(self.add_user_frame, text="Name", font=("Arial",14))
        self.add_user_surname_entry = tkinter.Entry(self.add_user_frame, font=("Arial", 14),
                                                     foreground="black")
        self.add_user_office_entry = tkinter.Entry(self.add_user_frame, font=("Arial", 14),
                                                    foreground="black")
        self.add_user_surname_label = tkinter.Label(self.add_user_frame, text="Surname", font=("Arial", 14))
        self.add_user_office_label = tkinter.Label(self.add_user_frame, text="Office", font=("Arial", 14))
        self.add_user_password_entry = tkinter.Entry(self.add_user_frame, font=("Arial", 14),
                                                     foreground="black", show="*")
        self.add_user_password_label = tkinter.Label(self.add_user_frame, text="Password", font=("Arial", 14))
        self.add_user_admin_checkbox = tkinter.Checkbutton(self.add_user_frame,
                                                  onvalue=1,
                                                  offvalue=0,
                                                  variable=self.admin_checkbox_value, text="Make user an Admin!")


        self.add_user_create_button = tkinter.Button(self.add_user_frame,
                                                     text="Create user!",
                                                     font=("Arial", 14),
                                                     command=self.add_new_user)



        self.add_user_username_label.grid(row=0, column=0, sticky='w')
        self.add_user_username_entry.grid(row=0, column=1)
        self.add_user_name_label.grid(row=1, column=0, sticky='w')
        self.add_user_name_entry.grid(row=1, column=1)
        self.add_user_surname_label.grid(row=2, column=0, sticky='w')
        self.add_user_surname_entry.grid(row=2, column=1)
        self.add_user_office_label.grid(row=3, column=0, sticky='w')
        self.add_user_office_entry.grid(row=3, column=1)
        self.add_user_password_label.grid(row=4, column=0, sticky='w')
        self.add_user_password_entry.grid(row=4, column=1)
        self.add_user_admin_checkbox.grid(row=5, column=0)
        self.add_user_create_button.grid(row=6, column=1, columnspan=2)

        self.add_user_frame.grid(row=0, column=1)





    def display_search_results(self):
        # remove results from previous search
        if self.search_results_number > 0:
            for label in self.search_results_label_list:
                label.destroy()
        self.search_results_number = 0
        if len(self.username_entry.get()) > 0 and len(self.surname_entry.get()) == 0:
            self.search_query = self.database.execute_query(
                "SELECT Username,Admin,Name,Surname,Office_Location FROM tLoginInformation "
                "JOIN tPersonalInformation ON tLoginInformation.Worker_ID=tPersonalInformation.Worker_ID "
                "WHERE Username = '" + self.username_entry.get() + "';")
        elif len(self.username_entry.get()) == 0 and len(self.surname_entry.get()) > 0:
            self.search_query = self.database.execute_query(
                "SELECT Username,Admin,Name,Surname,Office_Location FROM tLoginInformation "
                "JOIN tPersonalInformation ON tLoginInformation.Worker_ID=tPersonalInformation.Worker_ID "
                "WHERE Surname = '" + self.surname_entry.get() + "';")
        else:
            self.search_query = self.database.execute_query(
                "SELECT Username,Admin,Name,Surname,Office_Location FROM tLoginInformation "
                "JOIN tPersonalInformation ON tLoginInformation.Worker_ID=tPersonalInformation.Worker_ID "
                "WHERE Username = '" + self.username_entry.get() + "' AND Surname= '" + self.surname_entry.get() + "';")


        print("Username length: "+ str(len(self.username_entry.get())))
        print("Surname length: " + str(len(self.surname_entry.get())))

        columns = 5
        rows = 0
        for tuple in self.search_query:
            rows = rows+1
            self.search_results_number = self.search_results_number + 1
        print(rows)


        arr = []
        for i in range(rows):
            col = []
            for j in range(columns):
                col.append(self.search_query[i][j])
                label = tkinter.Label(self.search_result_frame,
                              text=self.search_query[i][j],
                              font=("Arial", 10))
                label.grid(row=i+1, column=j)
                self.search_results_label_list.append(label)
            arr.append(col)
        print(arr)

    def add_new_user(self):
        if len(self.add_user_username_entry.get()) > 0 and len(self.add_user_password_entry.get()) > 0:
            row=(self.add_user_username_entry.get(), self.add_user_password_entry.get(), self.admin_checkbox_value.get())
            self.database.insert_row(
                "INSERT INTO tLoginInformation (Username,Password,Admin)"
                "VALUES (?,?,?);", row)
            last_inserted_worker_id = self.database.execute_query(
                "SELECT Worker_ID From tLoginInformation WHERE ROWID=last_insert_rowid();")
            if len(last_inserted_worker_id) != 0:
                row = (last_inserted_worker_id[0][0],
                       self.add_user_name_entry.get(),
                       self.add_user_surname_entry.get(),
                       self.add_user_office_entry.get())
                self.database.insert_row(
                    "INSERT INTO tPersonalInformation(Worker_ID,Name,Surname,Office_Location)"
                    "VALUES (?,?,?,?);", row)
        else:
            messagebox.showerror("User creation failed", "At least Username and Password must be specified!")





class LoginWindow(tkinter.Toplevel):

    def open_terms_window(self, event):
        TermsWindow()

    def check_login_empty(self):
        print(self.login_entry_var.get())
        if len(self.login_entry_var.get()) != 0:
            self.enable_login_button()
        if len(self.login_entry_var.get()) == 0:
            self.disable_login_button()
        return True

    def check_password_empty(self):
        print(self.password_entry_var.get())
        if len(self.password_entry_var.get()) != 0:
            self.enable_login_button()
        if len(self.password_entry_var.get()) == 0:
            self.disable_login_button()
        return True

    def enable_disable_login_button_activator(self):
        self.enable_login_button()
        self.disable_login_button()

    def __init__(self, *args, **kwargs):
        tkinter.Toplevel.__init__(self, *args, **kwargs)
        self.terms_checkbox_value = tkinter.IntVar()
        self.geometry("400x400")
        self.iconphoto(True,tkinter.PhotoImage(file=notepad_icon))
        self.title("Notepad2000")
        self.resizable(width=0, height=0)
        self.login_frame = tkinter.Frame(self)
        self.bottom_frame = tkinter.Frame(self)

        self.login_entry_var = tkinter.StringVar()
        self.password_entry_var = tkinter.StringVar()
        self.login_entry = tkinter.Entry(self.login_frame, font=("Arial", 20),
                                         foreground="black",
                                         validate="focusout",
                                         textvariable=self.login_entry_var,
                                         validatecommand=self.check_login_empty)
        self.password_entry = tkinter.Entry(self.login_frame, font=("Arial", 20),
                                            foreground="black",
                                            show="*",
                                            validate="focusout",
                                            textvariable=self.password_entry_var,
                                            validatecommand=self.check_password_empty)
        self.login_label = tkinter.Label(self.login_frame, text="Username: ", font=("Arial",16))
        self.password_label = tkinter.Label(self.login_frame, text="Password: ", font=("Arial",16))
        self.terms_checkbox = tkinter.Checkbutton(self.bottom_frame,
                                                  onvalue=1,
                                                  offvalue=0,
                                                  variable=self.terms_checkbox_value,
                                                  command=self.enable_disable_login_button_activator)
        self.login_image=tkinter.PhotoImage(file=login_icon)
        self.login_button = tkinter.Button(self,
                                           text="Login",
                                           font=("Arial",16),
                                           image=self.login_image,
                                           compound="left",
                                           state="disabled")
        self.terms_checkbox_label = tkinter.Label(self.bottom_frame,
                                                  text="I accept the terms",
                                                  font=("Arial", 16),
                                                  cursor="hand2",
                                                  fg="blue")

        self.login_frame.pack(side="top", fill="both")
        self.login_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)
        self.login_label.grid(row=0, column=0)
        self.password_label.grid(row=1, column=0)

        self.bottom_frame.pack(side="bottom", fill="both")
        self.terms_checkbox.grid(row=0, column=0, columnspan=1, ipadx=0)
        self.terms_checkbox_label.grid(row=0, column=3)
        self.terms_checkbox_label.bind("<Button-1>", self.open_terms_window)

        self.login_button.pack(side="bottom")
    def bad_login(self):
        messagebox.showerror("Login error", "Invalid username or password!")

    def enable_login_button(self):
        if len(self.login_entry_var.get()) > 0:
            if len(self.password_entry_var.get()) > 0:
                if self.terms_checkbox_value.get() == 1:
                    self.login_button.configure(state="active")

    def disable_login_button(self):
        print(len(self.login_entry_var.get()))
        print(len(self.password_entry_var.get()))
        print(self.terms_checkbox_value.get())
        if len(self.login_entry_var.get()) == 0 or len(self.password_entry_var.get()) == 0 or self.terms_checkbox_value.get() == 0:
            self.login_button.configure(state="disabled")


class TermsWindow(tkinter.Toplevel):
    def __init__(self, *args, **kwargs):
        tkinter.Toplevel.__init__(self, *args, **kwargs)
        self.geometry("400x400")
        self.resizable(width=0, height=0)
        self.title("Terms")
        self.iconphoto(True, tkinter.PhotoImage(file=notepad_icon))
        self.focus_force()
        self.text_field = tkinter.Text(self, width=54, height=100, font=("Arial", 10))
        self.scroll_bar = tkinter.Scrollbar(self, orient="vertical", command=self.text_field.yview)
        self.text_field.pack(side="left")
        self.text_field.insert(tkinter.END, functions.load_text_file(terms_of_use))
        self.text_field.configure(state="disabled", yscrollcommand=self.scroll_bar.set)

        self.scroll_bar.pack(side="right", fill="y")

class Database:
    def __init__(self):
        self.database_filepath = database_file
        self.connection = self.create_connection(self.database_filepath)
    def create_connection(self, database_filepath):
        connection = None
        try:
            connection = sqlite3.connect(database_filepath)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")
        return connection

    def execute_query(self, query):
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute(query)
            self.connection.commit()
            result = cursor.fetchall()
            print("Query commited successfully")
            return result
        except Error as e:
            print(f"The error '{e}' occurred")

    def insert_row(self, query, row):
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute(query, row)
            self.connection.commit()
            result = cursor.fetchall()
            print("Query commited successfully")
            return result
        except Error as e:
            messagebox.showerror("User creation failed", f"Error message: '{e}'")


    def print_table(self, table_name):
        data = self.execute_query("SELECT * FROM "+str(table_name))
        for d in data:
            print(d)


class FontSelectionWindow(tkinter.Toplevel):

    def __init__(self, *args, **kwargs):
        tkinter.Toplevel.__init__(self, *args, **kwargs)
        self.geometry("400x200")
        self.resizable(width=0, height=0)
        self.title("Font Selection")
        self.iconphoto(True, tkinter.PhotoImage(file=notepad_icon))


        self.group_font = tkinter.StringVar()
        self.group_size = tkinter.IntVar()
        self.font_frame = tkinter.LabelFrame(self, text="Font")
        self.font_frame.grid(row=0, column=0, padx=50)
        self.size_frame = tkinter.LabelFrame(self, text="Size")
        self.size_frame.grid(row=0, column=1)

        tkinter.Radiobutton(self.font_frame, text='Segoe UI', variable=self.group_font, value='Segoe UI').pack(anchor='w')
        tkinter.Radiobutton(self.font_frame, text='Calibri', variable=self.group_font, value='Calibri').pack(anchor='w')
        tkinter.Radiobutton(self.font_frame, text='Times New Roman', variable=self.group_font, value='Times New Roman').pack()
        tkinter.Radiobutton(self.font_frame, text='Comic Sans', variable=self.group_font, value='Comic Sans').pack(anchor='w')

        tkinter.Radiobutton(self.size_frame, text='12', variable=self.group_size, value=12).grid(row=0, column=0)
        tkinter.Radiobutton(self.size_frame, text='14', variable=self.group_size, value=14).grid(row=0, column=1)
        tkinter.Radiobutton(self.size_frame, text='16', variable=self.group_size, value=16).grid(row=1, column=0)
        tkinter.Radiobutton(self.size_frame, text='18', variable=self.group_size, value=18).grid(row=1, column=1)
        tkinter.Radiobutton(self.size_frame, text='20', variable=self.group_size, value=20).grid(row=2, column=0)
        tkinter.Radiobutton(self.size_frame, text='22', variable=self.group_size, value=22).grid(row=2, column=1)
        tkinter.Radiobutton(self.size_frame, text='24', variable=self.group_size, value=24).grid(row=3, column=0)
        tkinter.Radiobutton(self.size_frame, text='26', variable=self.group_size, value=26).grid(row=3, column=1)

        self.save_button = tkinter.Button(self,
                                           text="Save",
                                           font=("Arial",12))
        self.cancel_button = tkinter.Button(self,
                                           text="Cancel",
                                           font=("Arial",12),
                                           command=self.destroy)
        self.save_button.grid(row=1, column=0, pady=30)
        self.cancel_button.grid(row=1, column=1, pady=30)




        self.focus_force()