from dearpygui.core import *
from dearpygui.simple import *
from numpy.__config__ import show
from utils.callback import on_close_callback
import numpy as np

def file_picker(sender, data):
    open_file_dialog(callback=apply_selected_file, extensions=".*,.txt")

def apply_selected_file(sender, data):
    directory = data[0]
    file = data[1]
    set_value("directory", directory)
    set_value("file", file)
    set_value("file_path", f"{directory}\\{file}")
    custom_data = np.genfromtxt(f"{directory}\{file}", delimiter="\t", skip_header=3)
    add_data("custom_data", custom_data)
    select_data_window()

def select_data_window():
    column_num = np.size(get_data("custom_data"),1)
    add_data("column_num", column_num)
    with window('Choose X Y', height=220, on_close = on_close_callback):
        with child('X Column', width=80,height=160):
            for i in range(column_num):
                add_selectable(f"xc{i}", callback=update_select)
        add_same_line()
        with child('Y Column', width=80,height=160):
            for i in range(column_num):
                add_selectable(f"yc{i}")
        add_button("OK", callback=OK_callback)

def update_select(sender, data):
    my_var = get_value(sender)
    if my_var == True:
        for j in range(get_data("column_num")):
            if f"xc{j}" != sender:
                set_value(f"xc{j}", False)

def OK_callback(sender, data):
    x_col = 0
    y_col = []
    for j in range(get_data("column_num")):
        if get_value(f"xc{j}") == True:
            x_col = j
        if get_value(f'yc{j}') == True:
            y_col.append(j)
    add_data("x_col", x_col)
    add_data("y_col", y_col)
    delete_item('Choose X Y')
    delete_item('file picker')

def print_data(sender, data):
    log_debug(get_data("custom_data"))