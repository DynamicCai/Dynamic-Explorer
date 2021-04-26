from dearpygui.simple import *
from utils.callback import on_close_callback
from .callback import *

app_menu_name = 'Tools'
app_menu_item_name = 'file picker'
app_name = 'file picker'

def start_app(sender, data):
    if not is_item_shown(app_name):
        add_app_window()

def add_app_window():
    with window(app_name, on_close = on_close_callback):
        add_button("Directory Selector", callback=file_picker)
        add_text("Directory Path: ")
        add_same_line()
        add_label_text("##dir", source="directory", color=[255, 0, 0])
        add_text("File: ")
        add_same_line()
        add_label_text("##file", source="file", color=[255, 0, 0])
        add_text("File Path: ")
        add_same_line()
        add_label_text("##filepath", source="file_path", color=[255, 0, 0])
        add_button("Print Data", callback=print_data)