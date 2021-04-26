from dearpygui.core import *
from dearpygui.simple import *
import numpy as np
from numpy import pi

# callbacks

def plot_callback(sender, data):
    # Track of current plot
    si = sender[10:]
    plot_name = "Iplot" + si
    origin_data = get_data("custom_data")
    # Get X Y col
    x_col = get_data("x_col")
    y_col = get_data("y_col")
    if len(y_col) == 2:
        origin_data = np.column_stack((origin_data[:,x_col]*2*np.pi, origin_data[:,y_col[0]], origin_data[:,y_col[1]]))
        log_debug(origin_data)
        float_data = origin_data.astype(np.float64)
        datax = float_data[:,0]
        datay2 = float_data[:,2]
        datax_list = datax.tolist()
        datay2_list = datay2.tolist()
        add_scatter_series(plot_name, "Original_Data", datax_list, datay2_list)
    
    if len(y_col) == 1:
        origin_data = np.column_stack((origin_data[:,x_col]*2*np.pi, origin_data[:,y_col[0]]))
        log_debug(origin_data)
        float_data = origin_data.astype(np.float64)
        datax = float_data[:,0]
        datay = float_data[:,1]
        datax_list = datax.tolist()
        datay_list = datay.tolist()
        add_scatter_series(plot_name, "Original_Data", datax_list, datay_list)
    
    add_data("stored_data" + si, origin_data)
    add_data("range_data" + si, origin_data)
    add_data("col_num", np.size(origin_data,1))
    with group(f"slider" + si, parent=f"Rpanel_name" + si, before=f"Iplot" + si):
        add_same_line()
        add_dummy(width=200)
        add_same_line()
        add_drag_int2(
            f"range" + si, default_value=[0, np.size(origin_data,0)-1], max_value=np.size(origin_data,0)-1, label="range", width=300, callback=range_callback)

def range_callback(sender, data):
    # Track of current plot
    si = sender[5:]
    range_data = get_data("range_data" + si)
    ranges = get_value("range" + si)
    minv = ranges[0]
    maxv = ranges[1]
    range_data = range_data[minv:maxv+1,:].astype(np.float64)
    x_list = range_data[:,0].tolist()
    if np.size(range_data,1) == 3:
        y2_list = range_data[:,2].tolist()
        delete_series("Iplot" + si, "Original_Data")
        add_scatter_series("Iplot" + si, "Original_Data", x_list, y2_list, update_bounds=False)
    if np.size(range_data,1) == 2:
        y_list = range_data[:,1].tolist()
        delete_series("Iplot" + si, "Original_Data")
        add_scatter_series("Iplot" + si, "Original_Data", x_list, y_list, update_bounds=False)

def renderstop_callback(sender,data):
    frame_count = get_data("frame_count")
    if frame_count != 0:
        add_data("frame_count", 0)
    else:
        add_data("frame_count", 1)
    
