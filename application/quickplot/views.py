from application.fit.callback import fit_callback, remove_functions, save_callback
from dearpygui.simple import *
from utils.callback import on_close_callback
from .callback import *

app_menu_name = 'Tools'
app_menu_item_name = 'quickplot'
pnum = 1


def start_app(sender, data):
    global app_name
    global pnum
    global plot_ID
    global data_button
    global To_fit
    global Lpanel_name
    global Rpanel_name
    global fit_it
    global clear_it
    global save_it
    global sliderd
    global stop_render

    for i in range(pnum):
        app_name = "plot" + f"{i}"
        plot_ID = "Iplot" + f"{i}"
        data_button = "Plot data " + f"{i}"
        To_fit = f"To fit{i}"
        fit_it = f"fit_it{i}"
        clear_it = f"clear_it{i}"
        Lpanel_name = f"Left_Panel{i}"
        Rpanel_name = f"Right_Panel{i}"
        save_it = f"Save{i}"
        sliderd = f"sliderd{i}"
        stop_render = f"render{i}"
        if not is_item_shown(app_name):
            add_app_interface()
            dict = {
                'model': [],
                'prefix': [], 
                'number': 0, 
                'HNP': {'name':'havriliak_negami_permittivity', 'num': 0, 'serial': [], 'pars': ['de', 'logtau0', 'a', 'b', 'einf'], 'pmin': [0, -np.inf, 0, 0, 0], 'pmax': [np.inf, np.inf, 1, 1, np.inf], 'vary': [True, True, True, True, True]},
                'HNC': {'name':'havriliak_negami_conductivity', 'num': 0, 'serial': [], 'pars': ['de', 'logtau0', 'a', 'b', 'einf'], 'pmin': [0, -np.inf, 0, 0, 0], 'pmax': [np.inf, np.inf, 1, 1, np.inf], 'vary': [True, True, True, True, True]},
                'RBMC': {'name':'random_barrier_model_conductivity', 'num': 0, 'serial': [], 'pars': ['logsigma', 'logtau0'], 'pmin': [-np.inf, -np.inf], 'pmax': [np.inf, np.inf], 'vary': [True, True]},
                'RBMPA': {'name':'random_barrier_model_permittivityA', 'num': 0, 'serial': [], 'pars': ['logsigma', 'logtau0'], 'pmin': [-np.inf, -np.inf], 'pmax': [np.inf, np.inf], 'vary': [True, True]},
                'RBMPB': {'name':'random_barrier_model_permittivityB', 'num': 0, 'serial': [], 'pars': ['logsigma', 'logtau0'], 'pmin': [-np.inf, -np.inf], 'pmax': [np.inf, np.inf], 'vary': [True, True]},
                'KWW': {'name':'KWW_modulus', 'num': 0, 'serial':[], 'pars': ['logomega0', 'b', 'height'], 'pmin': [0, 0.4, 0], 'pmax': [np.inf, 1, np.inf], 'vary': [True, True, True]},
                'OZ': {'name':'OZ_formula', 'num': 0, 'serial':[], 'pars': ['I0', 'kesai'], 'pmin': [0, 40], 'pmax': [np.inf, 200], 'vary': [True, True]},
                'WLF': {'name':'WLF_function', 'num': 0, 'serial':[], 'pars': ['C1', 'C2', 'Tr'], 'pmin': [0, 0, 0], 'pmax': [np.inf, np.inf, np.inf], 'vary': [True, True, True]}
                }
            add_data(f"stored_dict{i}", dict)
            pnum = pnum + 1
            

def add_app_interface():
    with tab(f"{app_name}", parent = "PlotTabBar"):
        with group(Lpanel_name, width=200):
            add_button(data_button, label="Plot data", callback=plot_callback)
            add_checkbox(To_fit, label="To fit", default_value=False, callback=update_tofit)
            add_button(fit_it, label="Fit", callback=fit_callback)
            add_button(clear_it, label="Clear functions", callback=remove_functions)
            add_button(save_it, label="Save", callback=save_callback)
            add_button(stop_render, callback=renderstop_callback, label="Render")
            add_spacing(count=5)
        
        add_same_line()

        with group(Rpanel_name):
            add_text("Tips")
            add_text("Double click plot to scale to data", bullet=True)
            add_text("Right click and drag to zoom to an area", bullet=True)
            add_text("Right click to open settings", bullet=True)
            add_text("Toggle data sets on the legend to hide them", bullet=True)
            add_text("Click and drag in the plot area to pan", bullet=True)
            add_text("Scroll mouse wheel in the plot area to zoom", bullet=True)
            add_text("Click and drag on an axs to just pan that dimension", bullet=True)
            add_text("Scroll mouse wheel on an axis to just scale that dimension", bullet=True)
            add_plot(plot_ID, label=app_name, height=-1, xaxis_log_scale=True, yaxis_log_scale=True)
            
def update_tofit(sender, data):
    # select the plot that you want to deal with
    my_var = get_value(sender)
    if my_var == True:
        strs = get_item_parent(sender)
        current_i = strs[10:]
        for j in range(pnum):
            if f"To fit{j}" != sender:
                set_value(f"To fit{j}", False)
    else:
        current_i = None
    add_data("stored_i", current_i)
    log_debug(current_i)

