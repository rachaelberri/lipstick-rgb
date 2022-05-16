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
    st.session_state['hex_color'] = '#c71236'
if 'rgb_corner' not in st.session_state:
    st.session_state['rgb_corner'] = (250, 0, 50)
    
st.title('Lipstick RGB')
# Left-> more muted, Right-> more vibrant
# Higher-> Higher, Lower-> Darker

df = pd.read_csv("df.csv")
#with st.expander("Choose a color", expanded=True):
prod = st.sidebar.selectbox('Brand', np.append(['Select'], df['brand'].unique()))
if prod!='Select':
    df_prod = df.loc[df['brand']==prod]
    swatch = st.sidebar.selectbox('Swatch', np.append(['Select'], df_prod['color'].unique()))
    # return index
    if swatch!='Select':
        st.session_state['hex_color'] = df.loc[(df['brand']==prod)&(df['color']==swatch)]['hex'].values[0]

# Color should change when a lipstick is picked
# replace with rgb bottom?
st.session_state['hex_color'] = st.sidebar.color_picker('Or a HEX color', value = st.session_state['hex_color'] )
st.session_state['rgb_corner']=rgb_corner(hex_to_rgb(st.session_state['hex_color']))

if not st.sidebar.button('Find a new Lipstick'):
    st.write("""You can use this to find a lipstick color that you like, available at Sephora.""")
    st.write("""First, choose a lipstick brand and color swatch, or just a color from the HEX color picker on the sidebar,
    then press the `Find a new lipstick` button to look for a new color color!""")
else:
#if st.sidebar.button('Find a new Lipstick'):

    df_filtered = df.loc[(df['r0']>st.session_state['rgb_corner'][0]-corner_step)
                         &(df['r0']<st.session_state['rgb_corner'][0]+corner_step)]
    df_filtered = df_filtered.loc[(df_filtered['g0']>st.session_state['rgb_corner'][1]-corner_step)
                                  &(df_filtered['g0']<st.session_state['rgb_corner'][1]+corner_step)]    
    df_filtered = df_filtered.loc[(df_filtered['b0']>st.session_state['rgb_corner'][2]-corner_step)
                                  &(df_filtered['b0']<st.session_state['rgb_corner'][2]+corner_step)] 
    st.write('Click the white dots to see the lipstick brand and shade')
    col1, col2 = st.columns(2)
    col1.write('Left --> more muted')
    col2.write('Right --> more vibrant')
    col1.write('Higher --> lighter')
    col2.write('Lower --> darker')
    get_rgb_top(st.session_state['hex_color'], st.session_state['rgb_corner'], df_filtered)
    get_rgb_bottom(st.session_state['rgb_corner'])
    st.write(df_filtered[['brand', 'product', 'color']])
