from dearpygui.core import *
from dearpygui.simple import*
import numpy as np

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
            add_data(self.stored_name, self.dict)
    
    def add_widgets(self):
        with group(self.si + f"{self.dict['prefix'][-1]}", parent=self.panel_name):
            add_text(f"{self.dict['prefix'][-1]}")
            for i in range(self.num):
                add_checkbox("##"+ self.si + f"lock{self.dict['prefix'][-1]}" + self.dict['HN']['pars'][i], default_value=True)
                add_same_line()
                add_input_float(
                    self.si + self.dict['prefix'][-1] + self.dict['HN']['pars'][i], label=f"{self.dict['HN']['pars'][i]}", default_value=self.po[i])

    def plot_unfitted_curves(self):
        origin_data = get_data("stored_data" + self.si)
        x = origin_data[:, 0]
        if get_data("col_num") == 3:
            str = f'{self.name}' + '( x, ' + ','.join(self.po) +')'
            fit = eval(str)
            fit2 = -fit.imag
            x_float = x.astype(np.float64)
            x_list = x_float.tolist()
            fit2 = fit2.astype(np.float64)
            fit2 = fit2.tolist()
            add_line_series("Iplot" + self.si, f"{self.dict['prefix'][-1]}"+ 'component', x_list, fit2, update_bounds=False)
        if get_data("col_num") == 2:
            str = f'{self.name}' + '( x, ' + ','.join(self.po) +')'
            fit = eval(str)
            x_float = x.astype(np.float64)
            x_list = x_float.tolist()
            fit = fit.astype(np.float64)
            fit = fit.tolist()
            add_line_series("Iplot" + self.si, f"{self.dict['prefix'][-1]}"+ 'component', x_list, fit, update_bounds=False)
        add_data("frame_count", 1)

def havriliak_negami_permittivity(x, logtau0, de, a, b, einf):
    """2-d HNP: HNP(x, logtau0, de, a, b, einf)"""
    return de / ( 1 + ( 1j * x * 10**logtau0 )**a )**b + einf

def KWW_modulus(x,logomega0, b, height):
    """1-d KWW: KWW(x, logomega0, b, height)"""
    return height / ((1 - b) + (b / (1 + b)) * (b * (10**logomega0 / x) + (x / 10**logomega0)**b))

def HNP_callback(sender,data):
    HNP = fun_callback([100,-2,1,1,1], 'HNP', 5, 'havriliak_negami_permittivity')
    HNP.add_item()
    HNP.add_widgets()
    HNP.plot_unfitted_curves()

def KWW_callback(sender,data):
    KWW = fun_callback([1,1,1], 'KWW', 3, 'KWW_modulus')
    KWW.add_item()
    KWW.add_widgets()
    KWW.plot_unfitted_curves