import seaborn as sns; sns.set()
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 

class Data2Plot:
    def __init__(self):
        self.static_data = {}
        self.dynamic_data = {}
        self.static_or_dynamic = {}
        self.frame_labels = []
        self.panels = 0
                
    def add_static_data(self, name, x, y, panel= 1, mode= 'markers+lines', rgb_colour= None ):
        self.static_data[name] = {}
        self.static_data[name]['type'] = 'static'
        self.static_data[name]['name'] = name
        self.static_data[name]['x'] = np.array(x)
        self.static_data[name]['y'] = np.array(y)
        self.static_data[name]['panel'] = panel
        self.static_data[name]['rgb_colour'] = rgb_colour
        self.static_data[name]['mode'] = mode
        self.static_or_dynamic[name] = 'static'
        self.panels = max(self.panels, panel)
        
        
    def get_static_data(self):
        return self.static_data
    
    def get_static_data_by_name(self, name):
        return self.static_data[name]
    
    def prepare_dynamic_data(self, name, panel= 1, mode= 'markers+lines', rgb_colour= None):
        self.dynamic_data[name] = {}
        self.dynamic_data[name]['type'] = 'dynamic'
        self.dynamic_data[name]['name'] = name
        self.dynamic_data[name]['x'] = []
        self.dynamic_data[name]['y'] = []
        self.dynamic_data[name]['panel'] = panel
        self.dynamic_data[name]['mode'] = mode
        self.dynamic_data[name]['rgb_colour'] = rgb_colour
        self.static_or_dynamic[name] = 'dynamic'
        self.panels = max(self.panels, panel)
        
        
    def feed_dynamic_data(self, name, x, y):
        self.dynamic_data[name]['x'].append(x)
        self.dynamic_data[name]['y'].append(y)
           
    def get_dynamic_data(self):
        return self.dynamic_data
         
    def get_dynamic_data_by_name(self, name):
        return self.dynamic_data[name]
    
    def get_rgba_colour_by_name(self, name, alpha):
        
        colour = None
        if name in self.static_data:
            colour = self.static_data[name]['rgb_colour']
        elif name in self.dynamic_data:
            colour = self.dynamic_data[name]['rgb_colour']
        if colour is None:
            return None
        return f'rgba({colour[0]},{colour[1]}, {colour[2]}, {alpha if len(colour)==3 else colour[3]})'
        
        
        return self.dynamic_data[name].colour
    
    def get_nr_frames(self):
        return len(self.dynamic_data[list(self.dynamic_data)[0]]['x'])
        
    def get_nr_panels(self):
        return self.panels

    def is_static(self, name):
        return self.static_or_dynamic[name] == 'static'
    
    def add_frame_label(self, label):
        self.frame_labels.append(label)
            
    def get_frame_label(self, index):
        return self.frame_labels[index] if len(self.frame_labels) > 0 else index
            
            
def create_dynamic_h_plot(data2plot, title="demo", x_axis_1=None, y_axis_1=None, x_range_1=None, y_range_1=None, **args):
    args['x_axis_1'] = x_axis_1
    args['y_axis_1'] = y_axis_1
    args['x_range_1'] = x_range_1
    args['y_range_1'] = y_range_1
    
    #------------------#
    # Define the layou #
    #------------------#
    layout = dict(            
            #-----------------#
            # Location grpahs #
            #-----------------#
            title  = title,

            #-----------------#
            # The two buttons #
            #-----------------#
            updatemenus = [{'buttons': [{'args': [list(range(data2plot.get_nr_frames())), 
                                                  {'frame': {'duration': 500.0, 'redraw': False}, 
                                                   'fromcurrent': True, 
                                                   'transition': {'duration': 0, 'easing': 'linear'}}], 
                                         'label': 'Play', 
                                         'method': 'animate'}, 
                                        {'args': [[None], 
                                                  {'frame': {'duration': 0, 'redraw': False}, 
                                                   'mode': 'immediate', 
                                                   'transition': {'duration': 0}}], 
                                         'label': 'Pause', 
                                         'method': 'animate'}], 
                            'direction': 'left', 
                            'pad': {'r': 10, 't': 85}, 
                            'showactive': True, 
                            'type': 'buttons', 
                            'x': 0.1, 
                            'y': 0, 
                            'xanchor': 'right', 
                            'yanchor': 'top'}],
            
            
            #-----------------#
            # The Slider      #
            #-----------------#
            sliders = [{'yanchor': 'top', 
                        'xanchor': 'left', 
                        'currentvalue': {'font': {'size': 16}, 'prefix': 'Frame: ', 'visible': True, 'xanchor': 'right'}, 
                        'transition': {'duration': 500.0, 'easing': 'linear'}, 
                        'pad': {'b': 10, 't': 60}, 
                        'len': 0.9, 
                        'x': 0.1, 
                        'y': 0, 
                        'steps': [{'args': [[str(i)], 
                                  {'frame': {'duration': 500.0, 
                                             'easing': 'linear', 
                                             'redraw': False}, 
                                   'transition': {'duration': 0, 
                                                  'easing': 'linear'}}], 
                                   'label': data2plot.get_frame_label(i), 
                                   'method': 'animate'} for i in range(data2plot.get_nr_frames())]
                       }
                      ]
        )

    #-------------------#
    # Create the panels #
    #-------------------#
    if data2plot.get_nr_panels() == 1:
        # If we have only 1 panel
        layout['xaxis1'] = {'domain': [0.0, 1.0], 'anchor': 'y1', 'title': x_axis_1, 'range': x_range_1}
        layout['yaxis1'] = {'domain': [0.0, 1.0], 'anchor': 'x1', 'title': y_axis_1, 'range': y_range_1}
    else:
        # calculate the panel sizes 
        space = 0.06
        panel_width = (1-(space * (data2plot.get_nr_panels()-1)))/data2plot.get_nr_panels()
        pandel_x_lim = 0.0
        for p in range(1, data2plot.get_nr_panels()+1):
            layout[f'xaxis{p}'] = {'domain': [pandel_x_lim, pandel_x_lim + panel_width], 'anchor': f'y{p}', 'title': args[f'x_axis_{p}'] if f'x_axis_{p}' in args else None, 'range': args[f'x_range_{p}'] if f'x_range_{p}' in args else None}
            layout[f'yaxis{p}'] = {'domain': [0.0, 1.0], 'anchor': f'x{p}', 'title': args[f'y_axis_{p}'] if f'y_axis_{p}' in args else None, 'range': args[f'y_range_{p}'] if f'y_range_{p}' in args else None}
            pandel_x_lim += panel_width + space

    #--------------#
    # Default data #
    #--------------#  
    data = [{    'type': 'scatter', 
                 'name': obj['name'], 
                 'x': obj['x'] if obj['type'] == 'static' else obj['x'][0], 
                 'y': obj['y'] if obj['type'] == 'static' else obj['y'][0], 
                 'hoverinfo': 'name+text', 
                 'marker': {'opacity': 0.7, 'symbol': 'circle', 'line': {'width': 0, 'color': 'rgba(50,50,50,0.8)'}}, 
                 'line': {'color': data2plot.get_rgba_colour_by_name(obj['name'], 1.)},
                 'mode': obj['mode'], 
                 'fillcolor': data2plot.get_rgba_colour_by_name(obj['name'], 0.7), 
                 'legendgroup': obj['name'],
                 'showlegend': True,
                 'xaxis': f'x{obj["panel"]}',
                 'yaxis': f'y{obj["panel"]}'} for key, obj in {**data2plot.get_static_data(), **data2plot.get_dynamic_data()}.items()]
    
    
    #-----------------#
    # Create frames   #
    #-----------------#

    # first create the empty frames
    frames = [ {'name': str(i), 'data': [] } for i in range(data2plot.get_nr_frames()) ]
    
    # Loop over the data fields which we made earlier because order is important
    for e, d_obj in enumerate(data):
        
        # if we've static data
        if data2plot.is_static(d_obj['name']):
            
            # get its object and fill in the frames
            st_obj = data2plot.get_static_data_by_name(d_obj['name'])
            for fr_obj in frames:
                fr_obj['data'].append({'type': 'scatter', 'x': st_obj['x'], 'y': st_obj['y']})
        else:
            # if we have dynamic data
            dy_obj = data2plot.get_dynamic_data_by_name(d_obj['name'])
            for fr_obj, x, y in zip(frames, dy_obj['x'], dy_obj['y']):
                fr_obj['data'].append({'type': 'scatter', 'x': x, 'y': y})
    

    #---------------#
    # create figure #
    #---------------#
    fig = dict(
        layout = layout,
        data = data,
        frames = frames
    )   
        
    return go.Figure(fig)


