from dearpygui.simple import *
from utils.callback import on_close_callback
from .callback import *

app_menu_name = 'Tools'
app_menu_item_name = 'fitdata'
app_name = 'Curve Fit'


def start_app(sender, data):
    if not is_item_shown(app_name):
        add_fit_window()


def add_fit_window():
    with window(f"{app_name}", width=860, height=300, on_close = on_close_callback):
        add_text("functions")
        add_separator()
        add_button("Havrilliak_Negami_permittivity", callback=HNP_callback, width=270)
        add_same_line()
        add_button("Havrilliak_Negami_conductivity", callback=HNC_callback, width=270)
        add_same_line()
        add_button("Random_Barrier_Model_conductivity", callback=RBMC_callback, width=270)
        add_button("KWW_adaptation_modulus", callback=KWW_callback, width=270)
        add_same_line()
        add_button("Random_Barrier_Model_permittivityA", callback=RBMPA_callback, width=270)
        add_same_line()
        add_button("Random_Barrier_Model_permittivityB", callback=RBMPB_callback, width=270)
        add_separator()
        add_button("OZ_formula", callback=OZ_callback, width=270)
        add_same_line()
        add_button("WLF_function", callback=WLF_callback, width=270)
        add_button("fit", callback=fit_callback)
        add_same_line()
        add_button("curves")


    