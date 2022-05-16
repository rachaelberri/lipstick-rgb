import altair as alt
import pandas as pd
import numpy as np
import streamlit as st
import math
from func import *

#df = pd.read_csv("df_rgb.csv")
df = pd.read_csv('df_rgb.csv', converters={"rgb": eval, "rgb0": eval})
df_bottom = pd.read_csv('rgb_bottom.csv', converters={"rgb": eval})

def get_rgb_top(hex_color, rgb_corner, df_filtered):
    rgb_top = get_df_top(rgb_corner)
    step = 5
    colorlist = rgb_top['hex'].unique().tolist()
    graph = alt.Chart(rgb_top).mark_rect().encode(
        x=alt.X('x', bin=alt.Bin(extent=[0, 255], step=step), axis = None),  # 
        y=alt.Y('y', bin=alt.Bin(extent=[0, 255], step=step), axis = None), 
        color=alt.Color('hex', scale = alt.Scale(domain=colorlist, range=colorlist), legend = None),
        opacity = alt.value(1),
    ).properties(width = 600,height = 600, )
    graph_lipsticks = alt.Chart(df_filtered).mark_circle(opacity = 1).encode(
        x=alt.X('x', bin=alt.Bin(extent=[0, 255], step=step), axis = None),  # 
        y=alt.Y('y', bin=alt.Bin(extent=[0, 255], step=step), axis = None), 
        color=alt.value('white'),
        size = alt.value(250),
        tooltip = [alt.Tooltip('brand', title='Brand'), 
                   alt.Tooltip('product', title='Product'),
                   alt.Tooltip('color', title='Swatch')]
    )
    x_selected, y_selected = xy_rgb(hex_to_rgb(hex_color))
    graph_selected = alt.Chart(pd.DataFrame({'x':[x_selected], 'y':[y_selected]})).mark_circle().encode(
        x=alt.X('x', bin=alt.Bin(extent=[0, 255], step=step), axis = None),  # 
        y=alt.Y('y', bin=alt.Bin(extent=[0, 255], step=step), axis = None), 
        color=alt.value('white'),
        size = alt.value(600),
    ).properties(width = 600,height = 600, )
    return st.altair_chart((graph+graph_selected+graph_lipsticks))

def get_rgb_bottom(rgb_corner):
    step=10
    colorlist_bottom = df_bottom['hex'].tolist()
    df_selected = df_bottom.loc[(df_bottom['r']==rgb_corner[0])&(df_bottom['g']==rgb_corner[1])&(df_bottom['b']==rgb_corner[2])]
    df_selected['x'] = df_selected['x'] 
    graph = alt.Chart(df_bottom.loc[:, df_bottom.columns!='rgb']).mark_rect().encode(
        x=alt.X('x', bin=alt.Bin(extent=[0, 255*6], step=step), axis = None),  # 
        y=alt.Y('y', axis = None), 
        color=alt.Color('hex', scale=alt.Scale(domain=colorlist_bottom, range=colorlist_bottom), legend = None),
        opacity=alt.value(0.3) #opacity = alt.condition(selector, alt.value(1), alt.value(0.05)),
    ).properties(width = 625, height = 50,)
    graph_selected = alt.Chart(df_selected).mark_rule(width=5).encode(
        x=alt.X('x', axis = None),  # 
        color=alt.value('black')
        #opacity = alt.condition(selector, alt.value(1), alt.value(0.05)),
    ).properties(width = 600, height = 50,)
    return st.altair_chart((graph+graph_selected).configure_view(strokeWidth=0))
