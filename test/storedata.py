from dearpygui.core import *
from dearpygui.simple import *

def store_data(sender, data):
    custom_data = {
        "Radio Button": get_value("Radio Button"),
        "Checkbox": get_value("Checkbox"),
        "Text Input": get_value("Text Input"),
    }
    add_data("stored_data", custom_data)

def print_data(sender, data):
    log_debug(get_data("stored_data"))

show_logger()
show_debug()

with window("Tutorial"):
    add_radio_button("Radio Button", items=["item1", "item2"])
    add_checkbox("Checkbox")
    add_input_text("Text Input")
    add_button("Store Data", callback=store_data)
    add_button("Print Data", callback=print_data)

start_dearpygui()