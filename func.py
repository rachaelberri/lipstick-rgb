import pandas as pd
import streamlit as st
import math

def lipstick_chooser(df, prod, swatch):
    st.session_state['hex_color'] = df.loc[(df['brand']==prod)&(df['color']==swatch)]['hex'].values[0]
    
def rgb_corner(rgb):
    # takes rgb values as a tuple and returns the top right color (what is chosen at the bottom of the RGB picker)
    min_rgb, max_rgb = rgb.index(min(rgb)), rgb.index(max(rgb)) # actually the index value, not the rgb value
    ind = [0, 1, 2]
    if min_rgb == max_rgb:
        return (0,0,0) # not top right corner....
    else:
        ind.remove(min_rgb)
        ind.remove(max_rgb)
        mid_rgb = ind[0]
        new_rgb = [0, 0, 0]
        new_rgb[min_rgb] = 0
        new_rgb[max_rgb] = 255
        # math time!
        x = 255-(255*rgb[min_rgb]/rgb[max_rgb])
        new_rgb[mid_rgb]=round(255-255*(255-255*rgb[mid_rgb]/rgb[max_rgb])/x)
        return tuple(new_rgb)

def rgb_xy(x, y, rgb):
    # takes xy values and calculates the rgb value in that location
    return int((255-((255-rgb)*x/255))*(y/255))

def xy_rgb(rgb):
    # takes rgb values as a tuple and calculates the xy
    y = max(rgb)
    x = 255-(255*min(rgb)/y)
    return x,y

#def rgb_round(rgb, step):
#    #take each of r, g, b and round by step
#    return round(r/step)*step

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

#def rgb_to_hex(rgb):
#    return '#%02x%02x%02x' % rgb

def get_df_top(rgb_corner):
    # df with x, y coordinates
    granularity_top = 5
    x = list(range(0, 256, granularity_top))*math.ceil(256/5)
    y = []
    for i in range(0, 256, granularity_top):
        for j in range(math.ceil(256/granularity_top)):
            y.append(i)
    rgb_top = pd.DataFrame({'x': x , 'y': y})
    rgb_top[['r', 'g', 'b', 'hex']]=[0, 0, 0, '']
    for i in rgb_top.index:
        rgb_top.loc[i, 'r'] = rgb_xy(rgb_top.loc[i, 'x'], rgb_top.loc[i, 'y'], rgb_corner[0])
        rgb_top.loc[i, 'g'] = rgb_xy(rgb_top.loc[i, 'x'], rgb_top.loc[i, 'y'], rgb_corner[1])
        rgb_top.loc[i, 'b'] = rgb_xy(rgb_top.loc[i, 'x'], rgb_top.loc[i, 'y'], rgb_corner[2])
        rgb_top.loc[i, 'hex'] = '#%02x%02x%02x' % (rgb_top['r'][i], rgb_top['g'][i], rgb_top['b'][i])
    return rgb_top

