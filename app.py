import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from nav_eda import *
from nav_stat import *
from functions.data_functions import *
from functions.stats_functions import *

##############################################
#                                            #
#                  SETTINGS                  #
#                                            #
##############################################

page_title = '6 Nations 2024 - Analyse Séquences de Jeu'
page_icon = 'Logo_Six_Nations.png'
st.set_page_config(layout='wide', initial_sidebar_state='expanded', page_icon=page_icon, page_title=page_title)

##################################################
#                                                #
#                  INOFS & DATA                  #
#                                                #
##################################################

teams_colors = {'France': 'blue',
                'England': 'lightgrey',
                'Scotland': '#2a3f88',
                'Ireland': '#00c8a9',
                'Wales': 'red',
                'Italia': '#2267e8'}

teams_img = {'France': 'img/France.png',
             'England': 'img/England.png',
             'Scotland': 'img/Scotland.png',
             'Ireland': 'img/Ireland.png',
             'Wales': 'img/Wales.png',
             'Italia': 'img/Italia.png'}

games_scores = {'France': {'Ireland': '17 - 38', 'Scotland': '16 - 20', 'Italia': '13 - 13', 'Wales': '24 - 45', 'England': '33 - 31'},
                'England': {'Italia': '24 - 27', 'Wales': '16 - 14', 'Scotland': '30 - 21', 'Ireland': '23 - 22', 'France': '33 - 31'},
                'Scotland': {'Wales': '26 - 27', 'France': '16 - 20', 'England': '30 - 21', 'Italia': '31 - 29', 'Ireland': '17 - 13'},
                'Ireland': {'France': '17 - 38', 'Italia': '36 - 0', 'Wales': '31 - 7', 'England': '23 - 22', 'Scotland': '17 - 13'},
                'Wales': {'Scotland': '26 - 27', 'England': '16 - 14', 'Ireland': '31 - 7', 'France': '24 - 45', 'Italia': '21 - 24'},
                'Italia': {'England': '24 - 27', 'Ireland': '36 - 0', 'France': '13 - 13', 'Scotland': '31 - 29', 'Wales': '21 - 24'}}

games_results = {'France': {'Ireland': 'D', 'Scotland': 'V', 'Italia': 'N', 'Wales': 'V', 'England': 'V'},
                 'England': {'Italia': 'V', 'Wales': 'V', 'Scotland': 'D', 'Ireland': 'V', 'France': 'D'},
                 'Scotland': {'Wales': 'V', 'France': 'D', 'England': 'V', 'Italia': 'D', 'Ireland': 'D'},
                 'Ireland': {'France': 'V', 'Italia': 'V', 'Wales': 'V', 'England': 'D', 'Scotland': 'V'},
                 'Wales': {'Scotland': 'D', 'England': 'D', 'Ireland': 'D', 'France': 'D', 'Italia': 'D'},
                 'Italia': {'England': 'D', 'Ireland': 'D', 'France': 'N', 'Scotland': 'V', 'Wales': 'V'}}

@st.cache_data
def get_data():
    return load_data()

data_6nations = get_data()

@st.cache_data
def desc_tbl_full():
    return descriptive_tbl_full(data_6nations)

tbl_desc_full = desc_tbl_full()

@st.cache_data
def desc_tbl_period():
    return descriptive_tbl_period(data_6nations)

tbl_desc_period = desc_tbl_period()

@st.cache_data
def ttest_tbl():
    return stat_report_ttest(data_6nations)

tbl_ttest = ttest_tbl()

@st.cache_data
def ttest_tbl_period():
    return stat_report_ttest_period(data_6nations)

tbl_ttest_period = ttest_tbl_period()

@st.cache_data
def anova_game():
    return stat_report_anova_game(data_6nations)

tbl_anova = anova_game()

@st.cache_data
def anova_period():
    return stat_report_anova_period(data_6nations)

tbl_anova_period = anova_period()

#############################################
#                                           #
#                  SIDEBAR                  #
#                                           #
#############################################

with st.sidebar:
    st.image('Logo_Six_Nations.png')
    ''
    ''
    menu = option_menu(menu_title='Menu',
                       menu_icon='list',
                       options=['Statistiques descriptives', 'Statistiques inférentielles'],
                       icons=['bar-chart-line-fill', 'sliders2-vertical'],
                       default_index=0)
    
##########################################
#                                        #
#                  MAIN                  #
#                                        #
##########################################
    
if menu == 'Statistiques descriptives':
    eda_navigation(data_6nations, teams_img, games_scores, games_results, tbl_desc_full, tbl_desc_period)
elif menu == 'Statistiques inférentielles':
    stat_navigation(data_6nations, teams_img, games_scores, games_results, tbl_ttest, tbl_ttest_period, tbl_anova, tbl_anova_period)