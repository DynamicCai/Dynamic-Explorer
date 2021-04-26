from dearpygui.core import *
from dearpygui.simple import *
from utils.widgets import add_themes_and_help_menu, auto_add_application_to_menu

with window("Main window"):
    with menu_bar('Main Menu Bar'):
        auto_add_application_to_menu(sender='Main Menu Bar', data=None)
        add_themes_and_help_menu(sender='Main Menu Bar', data=None)
    with group('Main Window Cover', horizontal=True):
        pass
    with tab_bar("PlotTabBar"):
        pass

if __name__ == "__main__":
    set_main_window_title('Dynamic Explorer')
    start_dearpygui(primary_window="Main window")
