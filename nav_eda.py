import streamlit as st

from functions.data_functions import *

# @st.partial
def eda_navigation(data_6nations, teams_img, games_scores, games_results, tbl_desc_full, tbl_desc_period):
    c1, _, c2 = st.columns([.2, .05, .75])
    with c1:
        st.write('')
        team_sel = st.selectbox('Sélectionner une équipe', sorted(list(teams_img.keys())))
        data_team = data_6nations[data_6nations['Match'].str.contains(team_sel)].reset_index(drop=True).copy()
        _, c11 = st.columns([.25, .75])
        with c11:
            st.image(teams_img[team_sel])
    
    with c2:
        st.title('Résultats')
        c22= st.columns(5)
        for (g, s), c in zip(games_scores[team_sel].items(), c22):
            c.markdown(g)
            if games_results[team_sel][g] == 'V':
                c.markdown(f':green[{s}]')
            elif games_results[team_sel][g] == 'D':
                c.markdown(f':red[{s}]')
            else:
                c.markdown(f':orange[{s}]')
    st.write('---')

    st.header('Timelines de match')
    c_timeline = [column for row in [st.columns(2) for _ in range(2)] for column in row]
    for i, r in enumerate(['J1', 'J2', 'J3', 'J4']):
        with c_timeline[i]:
            data_team_r = data_team[data_team['Round']==r].reset_index(drop=True).copy()
            game_ = data_team_r['Match'].unique()[0]
            st.image(f'eda_timeline/{r}_{game_}.png')
    c_r5 = st.columns([.2, .6, .2])
    with c_r5[1]:
        data_team_r5 = data_team[data_team['Round']=='J5'].reset_index(drop=True).copy()
        game_ = data_team_r5['Match'].unique()[0]
        st.image(f'eda_timeline/J5_{game_}.png')

    st.write('')

    st.header('Distributions')
    st.subheader('Boxplots (sans valeur aberrante)')
    c_box = [column for row in [st.columns(3) for _ in range(3)] for column in row]
    for i, m in enumerate(['Durée', 'Phases', 'Ratio Rucks-Passes', 'Avancée +', 'Ratio Avancée', 'Progression Zones']):
        with c_box[i]:
            st.image(f'eda_boxplots/{team_sel}_{m}.png')
    st.write('')

    st.subheader('Tables descriptives')
    with st.expander('**:blue[Matchs complets]**'):
        for m in ['Durée', 'Phases', 'Ratio Rucks-Passes', 'Avancée +', 'Ratio Avancée', 'Progression Zones']:
            st.caption(m)
            st.dataframe(tbl_desc_full[(tbl_desc_full['game'].str.contains(team_sel)) 
                                       & (tbl_desc_full['metric']==m)].drop(columns=['game', 'metric']), use_container_width=True)
    with st.expander('**:blue[Matchs complets par période de 20min]**'):
        for m in ['Durée', 'Phases', 'Ratio Rucks-Passes', 'Avancée +', 'Ratio Avancée', 'Progression Zones']:
            st.caption(m)
            st.dataframe(tbl_desc_period[(tbl_desc_period['game'].str.contains(team_sel)) 
                                         & (tbl_desc_period['metric']==m)].drop(columns=['game', 'metric']), use_container_width=True)
    st.write('')
    st.write('---')
    
    st.header('Progression (médiane du nb de zones) selon zone de départ des séquences')
    
    data_team_r1 = data_team[data_team['Round']=='J1'].reset_index(drop=True).copy()
    data_team_r2 = data_team[data_team['Round']=='J2'].reset_index(drop=True).copy()
    data_team_r3 = data_team[data_team['Round']=='J3'].reset_index(drop=True).copy()
    data_team_r4 = data_team[data_team['Round']=='J4'].reset_index(drop=True).copy()
    data_team_r5 = data_team[data_team['Round']=='J5'].reset_index(drop=True).copy()

    game_r1 = data_team_r1['Match'].unique()[0]
    game_r2 = data_team_r2['Match'].unique()[0]
    game_r3 = data_team_r3['Match'].unique()[0]
    game_r4 = data_team_r4['Match'].unique()[0]
    game_r5 = data_team_r4['Match'].unique()[0]

    st.subheader(f'**:blue[{game_r1}]**')
    c_field = st.columns(2)
    with c_field[0]:
        st.write(game_r1.split(' - ')[0])
        st.image(f"eda_fields/J1_{game_r1.split(' - ')[0]}.png")
        c01, c02 = st.columns(2)
        with c01:
            st.caption("0'-20'")
            st.image(f"eda_fields/J1_0'-20'_{game_r1.split(' - ')[0]}.png")
            st.caption("40'-60'")
            st.image(f"eda_fields/J1_40'-60'_{game_r1.split(' - ')[0]}.png")
        with c02:
            st.caption("20'-40'")
            st.image(f"eda_fields/J1_20'-40'_{game_r1.split(' - ')[0]}.png")
            st.caption("60'-80'")
            st.image(f"eda_fields/J1_60'-80'_{game_r1.split(' - ')[0]}.png")
    with c_field[1]:
        st.write(game_r1.split(' - ')[1])
        st.image(f"eda_fields/J1_{game_r1.split(' - ')[1]}.png")
        c11, c12 = st.columns(2)
        with c11:
            st.caption("0'-20'")
            st.image(f"eda_fields/J1_0'-20'_{game_r1.split(' - ')[1]}.png")
            st.caption("40'-60'")
            st.image(f"eda_fields/J1_40'-60'_{game_r1.split(' - ')[1]}.png")
        with c12:
            st.caption("20'-40'")
            st.image(f"eda_fields/J1_20'-40'_{game_r1.split(' - ')[1]}.png")
            st.caption("60'-80'")
            st.image(f"eda_fields/J1_60'-80'_{game_r1.split(' - ')[1]}.png")

    st.subheader(f'**:blue[{game_r2}]**')
    c_field = st.columns(2)
    with c_field[0]:
        st.write(game_r2.split(' - ')[0])
        st.image(f"eda_fields/J2_{game_r2.split(' - ')[0]}.png")
        c01, c02 = st.columns(2)
        with c01:
            st.caption("0'-20'")
            st.image(f"eda_fields/J2_0'-20'_{game_r2.split(' - ')[0]}.png")
            st.caption("40'-60'")
            st.image(f"eda_fields/J2_40'-60'_{game_r2.split(' - ')[0]}.png")
        with c02:
            st.caption("20'-40'")
            st.image(f"eda_fields/J2_20'-40'_{game_r2.split(' - ')[0]}.png")
            st.caption("60'-80'")
            st.image(f"eda_fields/J2_60'-80'_{game_r2.split(' - ')[0]}.png")
    with c_field[1]:
        st.write(game_r2.split(' - ')[1])
        st.image(f"eda_fields/J2_{game_r2.split(' - ')[1]}.png")
        c11, c12 = st.columns(2)
        with c11:
            st.caption("0'-20'")
            st.image(f"eda_fields/J2_0'-20'_{game_r2.split(' - ')[1]}.png")
            st.caption("40'-60'")
            st.image(f"eda_fields/J2_40'-60'_{game_r2.split(' - ')[1]}.png")
        with c12:
            st.caption("20'-40'")
            st.image(f"eda_fields/J2_20'-40'_{game_r2.split(' - ')[1]}.png")
            st.caption("60'-80'")
            st.image(f"eda_fields/J2_60'-80'_{game_r3.split(' - ')[1]}.png")

    st.subheader(f'**:blue[{game_r3}]**')
    c_field = st.columns(2)
    with c_field[0]:
        st.write(game_r3.split(' - ')[0])
        st.image(f"eda_fields/J3_{game_r3.split(' - ')[0]}.png")
        c01, c02 = st.columns(2)
        with c01:
            st.caption("0'-20'")
            st.image(f"eda_fields/J3_0'-20'_{game_r3.split(' - ')[0]}.png")
            st.caption("40'-60'")
            st.image(f"eda_fields/J3_40'-60'_{game_r3.split(' - ')[0]}.png")
        with c02:
            st.caption("20'-40'")
            st.image(f"eda_fields/J3_20'-40'_{game_r3.split(' - ')[0]}.png")
            st.caption("60'-80'")
            st.image(f"eda_fields/J3_60'-80'_{game_r3.split(' - ')[0]}.png")
    with c_field[1]:
        st.write(game_r3.split(' - ')[1])
        st.image(f"eda_fields/J3_{game_r3.split(' - ')[1]}.png")
        c11, c12 = st.columns(2)
        with c11:
            st.caption("0'-20'")
            st.image(f"eda_fields/J3_0'-20'_{game_r3.split(' - ')[1]}.png")
            st.caption("40'-60'")
            st.image(f"eda_fields/J3_40'-60'_{game_r3.split(' - ')[1]}.png")
        with c12:
            st.caption("20'-40'")
            st.image(f"eda_fields/J3_20'-40'_{game_r3.split(' - ')[1]}.png")
            st.caption("60'-80'")
            st.image(f"eda_fields/J3_60'-80'_{game_r3.split(' - ')[1]}.png")
            
    st.subheader(f'**:blue[{game_r4}]**')
    c_field = st.columns(2)
    with c_field[0]:
        st.write(game_r4.split(' - ')[0])
        st.image(f"eda_fields/J4_{game_r4.split(' - ')[0]}.png")
        c01, c02 = st.columns(2)
        with c01:
            st.caption("0'-20'")
            st.image(f"eda_fields/J4_0'-20'_{game_r4.split(' - ')[0]}.png")
            st.caption("40'-60'")
            st.image(f"eda_fields/J4_40'-60'_{game_r4.split(' - ')[0]}.png")
        with c02:
            st.caption("20'-40'")
            st.image(f"eda_fields/J4_20'-40'_{game_r4.split(' - ')[0]}.png")
            st.caption("60'-80'")
            st.image(f"eda_fields/J4_60'-80'_{game_r4.split(' - ')[0]}.png")
    with c_field[1]:
        st.write(game_r4.split(' - ')[1])
        st.image(f"eda_fields/J4_{game_r4.split(' - ')[1]}.png")
        c11, c12 = st.columns(2)
        with c11:
            st.caption("0'-20'")
            st.image(f"eda_fields/J4_0'-20'_{game_r4.split(' - ')[1]}.png")
            st.caption("40'-60'")
            st.image(f"eda_fields/J4_40'-60'_{game_r4.split(' - ')[1]}.png")
        with c12:
            st.caption("20'-40'")
            st.image(f"eda_fields/J4_20'-40'_{game_r4.split(' - ')[1]}.png")
            st.caption("60'-80'")
            st.image(f"eda_fields/J4_60'-80'_{game_r4.split(' - ')[1]}.png")

    st.subheader(f'**:blue[{game_r5}]**')
    c_field = st.columns(2)
    with c_field[0]:
        st.write(game_r5.split(' - ')[0])
        st.image(f"eda_fields/J5_{game_r5.split(' - ')[0]}.png")
        c01, c02 = st.columns(2)
        with c01:
            st.caption("0'-20'")
            st.image(f"eda_fields/J5_0'-20'_{game_r5.split(' - ')[0]}.png")
            st.caption("40'-60'")
            st.image(f"eda_fields/J5_40'-60'_{game_r5.split(' - ')[0]}.png")
        with c02:
            st.caption("20'-40'")
            st.image(f"eda_fields/J5_20'-40'_{game_r5.split(' - ')[0]}.png")
            st.caption("60'-80'")
            st.image(f"eda_fields/J5_60'-80'_{game_r5.split(' - ')[0]}.png")
    with c_field[1]:
        st.write(game_r4.split(' - ')[1])
        st.image(f"eda_fields/J5_{game_r5.split(' - ')[1]}.png")
        c11, c12 = st.columns(2)
        with c11:
            st.caption("0'-20'")
            st.image(f"eda_fields/J5_0'-20'_{game_r5.split(' - ')[1]}.png")
            st.caption("40'-60'")
            st.image(f"eda_fields/J5_40'-60'_{game_r5.split(' - ')[1]}.png")
        with c12:
            st.caption("20'-40'")
            st.image(f"eda_fields/J5_20'-40'_{game_r5.split(' - ')[1]}.png")
            st.caption("60'-80'")
            st.image(f"eda_fields/J5_60'-80'_{game_r5.split(' - ')[1]}.png")