from dearpygui.core import *
from dearpygui.simple import *

with window("Main Window"):
    with node_editor("Node Editor"):

        with node("Node 1"):

            with node_attribute("Node A1"):
                add_input_float("F1", width=150)

            with node_attribute("Node A2", output=True):
                add_input_float("F2", width=150)

        with node("Node 2##demo"):

            with node_attribute("Node A3"):
                add_input_float("F3", width=200)

            with node_attribute("Node A4", output=True):
                add_input_float("F4", width=200)

start_dearpygui(primary_window="Main Window")