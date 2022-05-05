import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from func import *
from graph import *

st.set_page_config(page_title="Lipstick RGB", page_icon="💋")

corner_step = 5
# initialize
if 'hex_color' not in st.session_state:
    st.session_state['hex_color'] = '#ffffff'
if 'rgb_corner' not in st.session_state:
    st.session_state['rgb_corner'] = (255, 255, 255)
    
st.title('Lipstick RGB')
# Left-> more muted, Right-> more vibrant
# Higher-> Higher, Lower-> Darker
st.write('You can use this to find a lipstick color that you like, available at Sephora. Choose a starting lipstick or color, then run Altair to choose a lighter, darker, or more/less vibrant color!')

df = pd.read_csv("df.csv")

with st.expander("Choose a color", expanded=True):
    st.write("Choose a brand and color swatch of a lipstick you already like! If you don't have one, choose a color from the HEX color picker instead.")
    prod = st.selectbox('Brand', np.append(['Select'], df['brand'].unique()))
    if prod!='Select':
        df_prod = df.loc[df['brand']==prod]
        swatch = st.selectbox('Swatch', np.append(['Select'], df_prod['color'].unique()))
        # return index
        if swatch!='Select':
            lipstick_chooser(df, prod, swatch)
            # Color should change when a lipstick is picked
    color = st.color_picker('Or a HEX color', value = st.session_state['hex_color'] )
    # replace with rgb bottom?
    st.session_state['hex_color'] = color
    st.session_state['rgb_corner']=rgb_corner(hex_to_rgb(st.session_state['hex_color']))
      
if st.button('Run Altair graphs for your chosen color to find your next lipstick!'):
    df_filtered = df.loc[(df['r0']>st.session_state['rgb_corner'][0]-corner_step)
                         &(df['r0']<st.session_state['rgb_corner'][0]+corner_step)]
    df_filtered = df_filtered.loc[(df_filtered['g0']>st.session_state['rgb_corner'][1]-corner_step)
                                  &(df_filtered['g0']<st.session_state['rgb_corner'][1]+corner_step)]    
    df_filtered = df_filtered.loc[(df_filtered['b0']>st.session_state['rgb_corner'][2]-corner_step)
                                  &(df_filtered['b0']<st.session_state['rgb_corner'][2]+corner_step)] 
    get_rgb_top(st.session_state['hex_color'], st.session_state['rgb_corner'], df_filtered)
    get_rgb_bottom(st.session_state['rgb_corner'])
    st.write(df_filtered[['brand', 'product', 'color']])
