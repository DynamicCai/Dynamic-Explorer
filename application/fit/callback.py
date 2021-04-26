from dearpygui.core import *
from dearpygui.simple import*
import numpy as np
from lmfit import Model, Parameters
from numpy.lib.function_base import delete

class fun_callback():
    #方程回调类
    def __init__(self, po, abb, num, name):
        self.si = get_data('stored_i')
        self.panel_name = 'Left_Panel' + self.si
        self.stored_name = 'stored_dict' + self.si
        self.dict = get_data(self.stored_name)
        self.po = po
        self.abb = abb
        self.num = num
        self.name = name
    
    # Update
    def add_item(self):
        self.dict[self.abb]['num'] = self.dict[self.abb]['num'] + 1
        if not self.dict[self.abb]['serial']:
            self.dict[self.abb]['serial'] = [1]
        else:
            if max(self.dict[self.abb]['serial']) >= self.dict[self.abb]['num']:
                i = 0
                while i < max(self.dict[self.abb]['serial']):
                    i += 1
                    if self.dict[self.abb]['serial'].count(i) > 0:
                        continue
                    else:
                        self.dict[self.abb]['serial'].append(i)
                        break
            else:
                self.dict[self.abb]['serial'].append(self.dict[self.abb]['num'])
        self.dict['prefix'].append(f"{self.abb}{self.dict[self.abb]['serial'][-1]}_")
        self.dict['model'].append(self.abb)
        print(self.dict)
        add_data(self.stored_name, self.dict)
    
    def add_widgets(self):
        with group(self.si + f"{self.dict['prefix'][-1]}", parent=self.panel_name):
            add_text(f"{self.dict['prefix'][-1]}")
            for i in range(self.num):
                add_checkbox("##"+ self.si + f"lock{self.dict['prefix'][-1]}" + self.dict[self.abb]['pars'][i], default_value=True)
                add_same_line()
                add_input_float(
                    self.si + self.dict['prefix'][-1] + self.dict[self.abb]['pars'][i], label=f"{self.dict[self.abb]['pars'][i]}", default_value=self.po[i])
        
    def plot_unfitted_curves(self):
        origin_data = get_data("stored_data" + self.si)
        x = origin_data[:, 0]
        po = [str(i) for i in self.po]
        if get_data("col_num") == 3:
            strfun = f'{self.name}' + '( x, ' + ','.join(po) +')'
            fit = eval(strfun)
            fit1 = fit.real
            fit2 = -fit.imag
            x_float = x.astype(np.float64)
            x_list = x_float.tolist()
            fit2 = fit2.astype(np.float64)
            fit2 = fit2.tolist()
            fit1 = fit1.astype(np.float64).tolist()
            add_line_series("Iplot" + self.si, f"{self.dict['prefix'][-1]}"+ 'component', x_list, fit2, update_bounds=False)
        if get_data("col_num") == 2:
            strfun = f'{self.name}' + '( x, ' + ','.join(po) +')'
            fit = eval(strfun)
            x_float = x.astype(np.float64)
            x_list = x_float.tolist()
            fit = fit.astype(np.float64)
            fit = fit.tolist()
            add_line_series("Iplot" + self.si, f"{self.dict['prefix'][-1]}"+ 'component', x_list, fit, update_bounds=False)
        add_data("frame_count", 1)
        set_render_callback(dynamic_callback)

def havriliak_negami_permittivity(x, de, logtau0, a, b, einf):
    """2-d HNP: HNP(x, logtau0, de, a, b, einf)"""
    return de / ( 1 + ( 1j * x * 10**logtau0 )**a )**b + einf

def havriliak_negami_conductivity(x, de, logtau0, a, b, einf):
    """2-d HNC: HNC(x, logtau0, de, a, b, einf)"""
    return ( de / ( 1 + ( 1j * x * 10**logtau0 )**a )**b + einf ) * ( 1j * x * 8.854187817 * 10**(-12) )

def random_barrier_model_permittivityA(x, logsigma, logtau0):
    """2-d RBMPA: RBMPA(x, sigma, logtau0)"""
    return 10**logsigma * 10**logtau0 / ( np.log(1 + 1j * x * 10**logtau0) * (8.854187817 * 10**(-12)) )

def random_barrier_model_permittivityB(x, logsigma, logtau0):
    """2-d RBMPB: RBMPB(x, sigma, logtau0)"""
    return 10**logsigma * 10**logtau0 / np.log(1 + 1j * x * 10**logtau0) / (8.854187817 * 10**(-12)) - 10**logsigma / ( 1j * x * 8.854187817 * 10**(-12) )

def random_barrier_model_conductivity(x, logsigma, logtau0):
    """2-d RBMC: RBMC(x, sigma, logtau0)"""
    return 10**logsigma * ( 1j * x * 10**logtau0 / np.log(1 + 1j * x * 10**logtau0) )

def KWW_modulus(x, logomega0, b, height):
    """1-d KWW: KWW(x, logomega0, b, height)"""
    return height / ((1 - b) + (b / (1 + b)) * (b * (10**logomega0 / x) + (x / 10**logomega0)**b))

def OZ_formula(x, I0, kesai):
    return I0 / ( 1 + x**2 * kesai**2)

def WLF_function(x, C1, C2, Tr):
    return - C1 * ( x - Tr ) / ( C2 + ( x - Tr ) )

def HNP_callback(sender,data):
    HNP = fun_callback([100,-2,1,1,1], 'HNP', 5, 'havriliak_negami_permittivity')
    HNP.add_item()
    HNP.add_widgets()
    HNP.plot_unfitted_curves()

def HNC_callback(sender,data):
    HNC = fun_callback([100,-2,1,1,1], 'HNC', 5, 'havriliak_negami_conductivity')
    HNC.add_item()
    HNC.add_widgets()
    HNC.plot_unfitted_curves()

def RBMPA_callback(sender,data):
    RBMPA = fun_callback([-10,-2], 'RBMPA', 2, 'random_barrier_model_permittivityA')
    RBMPA.add_item()
    RBMPA.add_widgets()
    RBMPA.plot_unfitted_curves()

def RBMPB_callback(sender,data):
    RBMPB = fun_callback([-10,-2], 'RBMPB', 2, 'random_barrier_model_permittivityB')
    RBMPB.add_item()
    RBMPB.add_widgets()
    RBMPB.plot_unfitted_curves()

def RBMC_callback(sender,data):
    RBMC = fun_callback([-10,-2], 'RBMC', 2, 'random_barrier_model_conductivity')
    RBMC.add_item()
    RBMC.add_widgets()
    RBMC.plot_unfitted_curves()

def KWW_callback(sender,data):
    KWW = fun_callback([2,1,0.015], 'KWW', 3, 'KWW_modulus')
    KWW.add_item()
    KWW.add_widgets()
    KWW.plot_unfitted_curves()

def OZ_callback(sender,data):
    OZ = fun_callback([1,40], 'OZ', 2, 'OZ_formula')
    OZ.add_item()
    OZ.add_widgets()
    OZ.plot_unfitted_curves()

def WLF_callback(sender,data):
    WLF = fun_callback([1,1,273], 'WLF', 3, 'WLF_function')
    WLF.add_item()
    WLF.add_widgets()
    WLF.plot_unfitted_curves()

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
        y1_float = y1_fit.astype(np.float64)
        x_list = x_float.tolist()
        y1_list = y1_float.tolist()
        delete_series("Iplot" + si, "fitted")
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
            fitted1 = comps[prefix].real
            fitted1 = fitted1.astype(np.float64)
            fitted1_list = fitted1.tolist()
            fitted2 = -comps[prefix].imag
            fitted2 = fitted2.astype(np.float64)
            fitted2_list = fitted2.tolist()
            add_line_series("Iplot" + si, prefix + 'component', x_list, fitted2_list, update_bounds=False)
        add_data("fitted_data" + si, fitted_data)
        add_data("fitted_param" + si, result.best_values)
        add_data("frame_count", 1)
    
    if get_data("col_num") == 2:
        dict = get_data(stored_name)
        # Generate data
        range_data = get_data("range_data" + si)
        x_dat = range_data[:, 0]
        y = range_data[:, 1]
        # Fitting
        pars = Parameters()
        for model, prefix in zip(dict['model'], dict['prefix']):
            exec(f"{prefix}mod = Model({dict[model]['name']}, prefix='{prefix}')", globals())
            for k, par in enumerate(dict[model]['pars']):
                current_data = get_value(si + prefix + par)
                dict[model]['vary'][k] = get_value("##"+si+f"lock{prefix}"+par)
                pars.add(f"{prefix}{dict[model]['pars'][k]}", value=current_data, min=dict[model]['pmin'][k], max=dict[model]['pmax'][k], vary=dict[model]['vary'][k])  
        add_data(stored_name, dict)
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
        for model, prefix in zip(dict['model'], dict['prefix']):
            for par in dict[model]['pars']: 
                set_value(si + prefix + par, result.best_values[prefix + par])
        #plot components
        comps = result.eval_components()
        for prefix in dict['prefix']:
            delete_series("Iplot" + si, prefix + 'component')
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
    pars = Parameters()
    
    if frame_count == 0 or si == None:
        frame_count = 0
    else:
        # Initialize
        stored_name = "stored_dict" + si
        dict = get_data(stored_name)
        p = Parameters()
        # updating plot data and plotting new data
        for model, prefix in zip(dict['model'], dict['prefix']):
            exec(f"{prefix}mod = Model({dict[model]['name']}, prefix='{prefix}')", globals())
            for k, par in enumerate(dict[model]['pars']):
                current_data = get_value(si + prefix + par)
                dict[model]['vary'][k] = get_value("##"+si+f"lock{prefix}"+par)
                pars.add(f"{prefix}{dict[model]['pars'][k]}", value=current_data, min=dict[model]['pmin'][k], max=dict[model]['pmax'][k], vary=dict[model]['vary'][k])
                p.add(f"{prefix}{dict[model]['pars'][k]}", value=current_data, min=dict[model]['pmin'][k], max=dict[model]['pmax'][k], vary=False) 
        add_data(stored_name, dict)
        try:
            if pars != get_data("previous_pars"):
                origin_data = get_data("stored_data" + si)
                x = origin_data[:, 0]
                y = x
                x_float = x.astype(np.float64)
                x_list = x_float.tolist()
                prefix_= [a+'mod' for a in dict['prefix']]
                exec("mod = " + "+".join(prefix_), globals())
                fresult = mod.fit(y, p, x=x)
                comps = fresult.eval_components()
                if np.size(origin_data,1) == 3:
                    for prefix in dict['prefix']:
                        delete_series("Iplot" + si, prefix + 'component')
                        fitted1 = comps[prefix].real
                        fitted1 = fitted1.astype(np.float64).tolist()
                        fitted2 = -comps[prefix].imag
                        fitted2 = fitted2.astype(np.float64).tolist()
                        add_line_series("Iplot" + si, prefix + 'component', x_list, fitted2, update_bounds=False)
                if np.size(origin_data,1) == 2:
                    for prefix in dict['prefix']:
                        delete_series("Iplot" + si, prefix + 'component')
                        fitted2 = comps[prefix]
                        fitted2= fitted2.astype(np.float64).tolist()
                        add_line_series("Iplot" + si, prefix + 'component', x_list, fitted2, update_bounds=False)
                add_data("previous_pars", pars)
                frame_count += 1
        except SystemError:
            add_data("previous_pars", pars)
            frame_count += 1
        # update frame
    add_data("frame_count", frame_count)

def remove_functions(sender, data):
    # Track of current panel
    si = get_data("stored_i")
    stored_name = "stored_dict" + si
    dict = get_data(stored_name)
    add_data("frame_count", 0)
    delete_series("Iplot" + si, "fitted")
    for prefix in dict['prefix']:
        delete_series("Iplot" + si, prefix + 'component')
        delete_item(si + f"{dict['prefix'][-1]}")
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
    add_data(f"stored_dict" + si, dict)

def save_callback(sender, data):
    # Track of current panel
    si = get_data("stored_i")
    pi = int(si)
    fitted_data = get_data("fitted_data" + si)
    np.savetxt(f"data\plot{pi}", fitted_data)

