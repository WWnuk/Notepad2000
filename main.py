import classes
import functions
import tkinter
import sql_statements

database = classes.Database()
windows_container = classes.WindowsContainer()
# Some additional config
functions.restore_editor_window_wrapper(database, windows_container.editor_window, windows_container.login_window)
functions.configure_close_option_for_editor_window(windows_container, windows_container.editor_window)
functions.configure_close_option_for_login_window(windows_container, windows_container.login_window)
###############################
windows_container.mainloop()