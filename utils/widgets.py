import os  # 添加的代码
from dearpygui.core import *
from dearpygui.simple import *

def auto_add_application_to_menu(sender, data):  # 添加的方法
    
    application_dirs = []
    
    for file in os.listdir('application\\'):
        application_dirs.append(file)
    
    application_menu = {}
    
    for application in application_dirs:
        exec(f'import application.{application}.views as {application}')
        exec(f'application_menu[{application}.app_menu_name]=[]')
    
    for application in application_dirs:
        exec(
            'application_menu[' + application + '.app_menu_name].append({"app":' + application + ',"name":' + application + '.app_menu_item_name})')
    
    for menu_k, menu_v in application_menu.items():
        with menu(f'{menu_k}##Main Menu', parent=sender):
            for _item in menu_v: 
                add_menu_item(f'{_item["name"]}##Main Menu Item', callback=_item['app'].start_app)

def add_themes_and_help_menu(sender, data):
    with menu('Themes', parent=sender):
        add_menu_item("Dark", label='Dark (default)', callback=lambda sender, data: set_theme(sender), check=True)
        add_menu_item("Light", callback=lambda sender, data: set_theme(sender), check=True)
        add_menu_item("Classic", callback=lambda sender, data: set_theme(sender), check=True)
        add_menu_item("Dark 2", callback=lambda sender, data: set_theme(sender), check=True)
        add_menu_item("Grey", callback=lambda sender, data: set_theme(sender), check=True)
        add_menu_item("Dark Grey", callback=lambda sender, data: set_theme(sender), check=True)
        add_menu_item("Cherry", callback=lambda sender, data: set_theme(sender), check=True)
        add_menu_item("Purple", callback=lambda sender, data: set_theme(sender), check=True)
        add_menu_item("Gold", callback=lambda sender, data: set_theme(sender), check=True)
        add_menu_item("Red", callback=lambda sender, data: set_theme(sender), check=True)
    with menu('Help', parent=sender):
        add_menu_item('Show Logger', callback=show_logger)
        add_menu_item('Show About', callback=show_about)
        add_menu_item('Show Metrics', callback=show_metrics)
        add_menu_item('Show Documentation', callback=show_documentation)
        add_menu_item('Show Debug', callback=show_debug)
        add_menu_item('Show Style Editor', callback=show_style_editor)
