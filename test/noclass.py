import numpy as np
from numpy import pi
from numpy.lib.function_base import delete
from scipy.optimize import least_squares
from six import exec_
from dearpygui.core import *
from dearpygui.simple import *
from lmfit import Model, Parameters

def HNP_callback(sender, data):
    # Track of current panel
    si = get_data("stored_i")
    panel_name = "Left_Panel" + si
    stored_name = "stored_dict" + si
    if get_data("col_num") == 3:
        # Initialization
        po = [100, -2, 1, 1, 1]
        dict = get_data(stored_name)
        # Update
        dict['HNP']['num'] = dict['HNP']['num'] + 1
        if not dict['HNP']['serial']:
            dict['HNP']['serial'] = [1]
        else:
            if max(dict['HNP']['serial']) >= dict['HNP']['num']:
                i = 0
                while i < max(dict['HNP']['serial']):
                    i += 1
                    if dict['HNP']['serial'].count(i) > 0:
                        continue
                    else:
                        dict['HNP']['serial'].append(i)
                        break
            else:
                dict['HNP']['serial'].append(dict['HNP']['num'])
        dict['prefix'].append(f"HNP{dict['HNP']['serial'][-1]}_")
        dict['model'].append("HNP")
        # Add widgets
        with group(si + f"{dict['prefix'][-1]}", parent=panel_name):
            add_text(f"{dict['prefix'][-1]}")
            for i in range(5):
                add_checkbox("##"+ si + f"lock{dict['prefix'][-1]}" + dict['HNP']['pars'][i], default_value=True)
                add_same_line()
                add_input_float(
                    si + dict['prefix'][-1] + dict['HNP']['pars'][i], label=f"{dict['HNP']['pars'][i]}", default_value=po[i])
        # Update
        add_data(stored_name, dict)
        # plot unfitted curves
        origin_data = get_data("stored_data" + si)
        x = origin_data[:, 0]
        fit = po[0] / ( 1 + ( 1j * x * 10**po[1] )**po[2] )**po[3] + po[4]
        fit2 = -fit.imag
        x_float = x.astype(np.float64)
        x_list = x_float.tolist()
        fit2 = fit2.astype(np.float64)
        fit2 = fit2.tolist()
        add_line_series("Iplot" + si, f"{dict['prefix'][-1]}"+ 'component', x_list, fit2, update_bounds=False)
        add_data("frame_count", 1)

def KWW_callback(sender, data):
    # Track of current panel
    si = get_data("stored_i")
    panel_name = "Left_Panel" + si
    stored_name = "stored_dict" + si
    if get_data("col_num") == 2:
        # Initialization
        dict = get_data(stored_name)
        po = [1, 1, 1]
        # Update
        dict['KWW']['num'] = dict['KWW']['num'] + 1
        if not dict['KWW']['serial']:
            dict['KWW']['serial'] = [1]
        else:
            if max(dict['KWW']['serial']) >= dict['KWW']['num']:
                i = 0
                while i < max(dict['KWW']['serial']):
                    i += 1
                    if dict['KWW']['serial'].count(i) > 0:
                        continue
                    else:
                        dict['KWW']['serial'].append(i)
                        break
            else:
                dict['KWW']['serial'].append(dict['KWW']['num'])
        dict['prefix'].append(f"KWW{dict['KWW']['serial'][-1]}_")
        dict['model'].append("KWW")
        # Add widgets and update
        with group(si + f"{dict['prefix'][-1]}", parent=panel_name):
            add_text(f"{dict['prefix'][-1]}")
            for i in range(3):
                add_checkbox("##"+ si + f"lock{dict['prefix'][-1]}" + dict['KWW']['pars'][i])
                add_same_line()
                add_input_float(
                    si + dict['prefix'][-1] + dict['KWW']['pars'][i], label=f"{dict['KWW']['prefix'][-1]}{dict['KWW']['pars'][i]}", default_value=po[i])
        # Update
        add_data(stored_name, dict)
        # plot unfitted curves
        origin_data = get_data("stored_data" + si)
        x = origin_data[:, 0]
        fit = po[0] / ((1 - po[1]) + (po[1] / (1 + po[1])) * (po[1] * (10**po[2] / x) + (x / 10**po[2])**po[1]))
        x_float = x.astype(np.float64)
        x_list = x_float.tolist()
        fit = fit.astype(np.float64)
        fit = fit.tolist()
        add_line_series("Iplot" + si, f"{dict['KWW']['prefix'][-1]}", x_list, fit, update_bounds=False)
        add_data("frame_count", 1)

def havriliak_negami_permittivity(x, logtau0, de, a, b, einf):
    """2-d HNP: HNP(x, logtau0, de, a, b, einf)"""
    return de / ( 1 + ( 1j * x * 10**logtau0 )**a )**b + einf

def KWW_modulus(x,logomega0, b, height):
    """1-d KWW: KWW(x, logomega0, b, height)"""
    return height / ((1 - b) + (b / (1 + b)) * (b * (10**logomega0 / x) + (x / 10**logomega0)**b))

def havrilliak_negami_conductivity(x, logtau0, de, a, b, einf):
    """2-d HNC: HNC(x, logtau0, de, a, b, einf)"""
    return de / ( 1 + ( 1j * x * 10**logtau0 )**a )**b + einf / ( x * 8.854187817 * 10**(-12) )

def random_barrier_model_permittivity(x, logtau0):
    return x

def fit_callback(sender, data):
    # Track of current panel
    si = get_data("stored_i")
    stored_name = "stored_dict" + si
    pars = {}
    origin_data = get_data("stored_data" + si)
    
    if get_data("col_num") == 3:
        dict = get_data(stored_name)
        #Generate data
        range_data = get_data("range_data" + si)    
        x_dat = range_data[:, 0]
        y1_dat = range_data[:, 1]
        y2_dat = range_data[:, 2]
        y = y1_dat - 1j * y2_dat
        #Fitting
        pars = Parameters()
        for model, prefix in zip(dict['model'], dict['prefix']):
            exec(f"{prefix}mod = Model({dict[model]['name']}, prefix='{prefix}')", globals())
            for k, par in enumerate(dict[model]['pars']):
                current_data = get_value(si + prefix + par)
                dict[model]['vary'][k] = get_value("##"+si+f"lock{prefix}"+par)
                pars.add(f"{prefix}{dict[model]['pars'][k]}", value=current_data, min=dict[model]['pmin'][k], max=dict[model]['pmax'][k], vary=dict[model]['vary'][k])  
        add_data(stored_name, dict)
        prefix_= [a+'mod' for a in dict['prefix']]
        print("mod = " + "+".join(prefix_))
        exec("mod = " + "+".join(prefix_), globals())
        result = mod.fit(y, pars, x=x_dat) 
        #plotting
        x_dat = origin_data[:, 0]
        y1_dat = origin_data[:, 1]
        y2_dat = origin_data[:, 2]
        y_fit = result.best_fit
        y1_fit = y_fit.real
        y2_fit = -y_fit.imag
        fitted_data = np.column_stack((x_dat, y1_dat, y2_dat, y1_fit, y2_fit))
        x_float = x_dat.astype(np.float64)
        y2_float = y2_fit.astype(np.float64)
        x_list = x_float.tolist()
        y2_list = y2_float.tolist()
        add_line_series("Iplot" + si, "fitted", x_list, y2_list, update_bounds=False)
        #fitted parameters out
        for model, prefix in zip(dict['model'], dict['prefix']):
            for par in dict[model]['pars']: 
                set_value(si + prefix + par, result.best_values[prefix + par])
        #plot components
        comps = result.eval_components()
        for prefix in dict['prefix']:
            delete_series("Iplot" + si, prefix + 'component')
            fitted_data = np.column_stack((fitted_data, comps[prefix].real, -comps[prefix].imag))
            fitted2 = -comps[prefix].imag
            fitted2 = fitted2.astype(np.float64)
            fitted2_list = fitted2.tolist()
            add_line_series("Iplot" + si, prefix + 'component', x_list, fitted2_list, update_bounds=False)
        add_data("fitted_data" + si, fitted_data)
        add_data("fitted_param" + si, result.best_values)
        add_data("frame_count", 1)
    
    if get_data("col_num") == 2:
        dict = get_data(stored_name)
        #Get initial values
        for model, prefix in zip(dict['model'], dict['prefix']):
            exec(f"{prefix}mod = Model({dict[model]['name']}, prefix='{prefix}')", globals())
            exec(f"pars.update({prefix}mod.make_params())", globals())
            for par, k in zip(dict[model]['pars'], dict[model]['vary']):
                current_data = get_value(si + prefix + par)
                dict[model]['vary'][k] = get_value("##"+si+f"lock{prefix}"+par)
                pars[f"{prefix}{dict[model]['pars'][k]}"].set(value=current_data, min=dict[model]['pmin'][k], max=dict[model]['pmax'][k], vary=dict[model]['vary'][k])
        add_data(stored_name, dict)
        # Generate data
        range_data = get_data("range_data" + si)
        x_dat = range_data[:, 0]
        y_dat = range_data[:, 1]
        # Fitting
        prefix_= [a+'mod' for a in dict['prefix']]
        exec("mod = " + "+".join(prefix_), globals())
        result = mod.fit(y, pars, x=x_dat)
        # Plotting
        x_dat = origin_data[:, 0]
        y_dat = origin_data[:, 1]
        y_fit = result.best_fit
        fitted_data = np.column_stack((x_dat, y_dat, y_fit))
        x_float = x_dat.astype(np.float64)
        y_float = y_fit.astype(np.float64)
        x_list = x_float.tolist()
        y_list = y_float.tolist()
        add_line_series("Iplot" + si, "fitted", x_list, y_list, update_bounds=False)
        #fitted parameters out
        for model in dict['model']:
            for par in dict[model]['pars']:
                set_value(si + model + "_" + par, result.best_values[model + '_' + par])
        #plot components
        comps = result.eval_components()
        for prefix in dict['prefix']:
            fitted_data = np.column_stack((fitted_data, comps[prefix]))
            fitted_list = comps[prefix].astype(np.float64).tolist()
            add_line_series("Iplot" + si, prefix + 'component', x_list, fitted_list, update_bounds=False)
        add_data("fitted_data" + si, fitted_data)
        add_data("fitted_param" + si, result.best_values)
        add_data("frame_count", 1)

def dynamic_callback(sender, data):
    # keeping track of frames
    frame_count = get_data("frame_count")
    # Track of current panel
    si = get_data("stored_i")
    
    if frame_count == 0 or si == None:
        frame_count = 0
    else:
        # Initialize
        stored_name = "stored_dict" + si
        dict = get_data(stored_name)
        pars = {}
        # updating plot data and plotting new data
        
        for model, prefix in zip(dict['model'], dict['prefix']):
            exec(f"{prefix}mod = {dict[model]['name']}(prefix='{prefix}')", globals())
            exec(f"pars.update({prefix}mod.make_params())", globals())
            for par, k in zip(dict[model]['pars'], dict[model]['vary']):
                current_data = get_value(si + prefix + par)
                dict[model]['vary'][k] = get_value("##"+si+f"lock{prefix}"+par)
                pars[f"{prefix}{dict[model]['pars'][k]}"].set(value=current_data, min=dict[model]['pmin'][k], max=dict[model]['pmax'][k], vary=dict[model]['vary'][k])
        add_data(stored_name, dict)
        
        if pars != get_data("previous_pars"):
            origin_data = get_data("stored_data" + si)
            x = origin_data[:, 0]
            prefix_= [a+'mod' for a in dict['prefix']]
            exec("mod = " + "+".join(prefix_), globals())
            init = mod.eval(pars, x=x)
            comps = init.eval_components(x=x)
            x_float = x.astype(np.float64)
            x_list = x_float.tolist()
            
            if np.size(origin_data,1) == 3:
                for prefix in dict['prefix']:
                    delete_series("Iplot" + si, prefix + 'component')
                    fitted2 = -comps[prefix].imag
                    fitted2= fitted2.astype(np.float64).tolist()
                    add_line_series("Iplot" + si, prefix + 'component', x_list, fitted2, update_bounds=False)
            
            if np.size(origin_data,1) == 2:
                for prefix in dict['prefix']:
                    delete_series("Iplot" + si, prefix + 'component')
                    fitted2 = comps[prefix]
                    fitted2= fitted2.astype(np.float64).tolist()
                    add_line_series("Iplot" + si, prefix + 'component', x_list, fitted2, update_bounds=False)

            add_data("previous_p", pars)
            frame_count += 1
    # update frame
    add_data("frame_count", frame_count)


def remove_functions(sender, data):
    # Track of current panel
    si = get_data("stored_i")
    stored_name = "stored_dict" + si
    dict = get_data(stored_name)
    add_data("frame_count", 0)
    for prefix in dict['prefix']:
        delete_series("Iplot" + si, prefix + 'component')
        delete_item(si + f"{dict['prefix'][-1]}")
    dict = {
            'model': [],
            'prefix':[], 
            'number': 0, 
            'HNP': {'name':'havriliak_negami', 'num': 0, 'serial': [], 'pars': ['de', 'logtau0', 'a', 'b', 'einf'], 'pmin': [0, -np.inf, 0, 0, 0], 'pmax': [np.inf, np.inf, 1, 1, np.inf], 'vary': [], 'p': []}, 
            'KWW': {'name':'KWW_modulus', 'num': 0, 'serial':[], 'pars': ['d'], 'pmin': [], 'pmax': [], 'vary': []}
            }
    add_data(f"stored_dict" + si, dict)

def save_callback(sender, data):
    # Track of current panel
    si = get_data("stored_i")
    pi = int(si)
    fitted_data = get_data("fitted_data" + si)
    np.savetxt(f"data\plot{pi}", fitted_data)

    