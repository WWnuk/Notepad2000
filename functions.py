import classes
import tkinter

def get_file_name_from_windows_path(path):
    if path != None:
        parts = path.split("/")
        filename = parts[len(parts)-1]
        return filename
    else:
        return "Untitled document"


def load_text_file(filepath, encoding="utf8"):
    with open(filepath) as f:
        lines = f.read()
        return lines


def restore_editor_window(database, editor_window, login_window):
    entered_username = login_window.login_entry_var.get()
    entered_password = login_window.password_entry_var.get()

    login_query=database.execute_query("SELECT Username,Password,Admin,Name,Surname,Office_Location FROM tLoginInformation "
                                 "JOIN tPersonalInformation ON tLoginInformation.Worker_ID=tPersonalInformation.Worker_ID "
                                 "WHERE Username = '"+entered_username+"' AND Password = '"+entered_password+"';")
    print(login_query)
    if len(login_query) > 0:
        print("Username is:" + login_query[0][0])
        print("Password is:" + login_query[0][1])
        editor_window.title("Hello "+login_query[0][3]+" "+login_query[0][4]+" !")
        admin_menu_droplist_container = tkinter.Menu(editor_window.menu_bar, tearoff=0)

        if login_query[0][2] == 1:
            editor_window.menu_bar.add_cascade(label="Admin", menu=admin_menu_droplist_container)
            admin_menu_droplist_container.add_command(label="Admin Panel", command=editor_window.open_admin_panel_window)
            editor_window.config(menu=editor_window.menu_bar)

        editor_window.deiconify()
        login_window.withdraw()
    else:
        login_window.bad_login()


def restore_editor_window_wrapper(database, editor_window, login_window):
    login_window.login_button.configure(command=lambda: restore_editor_window(database, editor_window, login_window))


def configure_close_option_for_editor_window_wrapper(windows_container, editor_window):
    editor_window.destroy()
    windows_container.destroy()


def configure_close_option_for_editor_window(windows_container, editor_window):
    editor_window.protocol("WM_DELETE_WINDOW",
                           lambda: configure_close_option_for_editor_window_wrapper(windows_container, editor_window))

def configure_close_option_for_login_window_wrapper(windows_container, login_window):
    login_window.destroy()
    windows_container.destroy()


def configure_close_option_for_login_window(windows_container, login_window):
    login_window.protocol("WM_DELETE_WINDOW",
                           lambda: configure_close_option_for_login_window_wrapper(windows_container, login_window))
