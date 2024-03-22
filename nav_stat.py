import streamlit as st
from streamlit_option_menu import option_menu
from io import StringIO
import pandas as pd

def stat_navigation(data_6nations, teams_img, games_scores, games_results, tbl_ttest, tbl_ttest_period, tbl_anova, tbl_anova_period):
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
            c.markdown(f'''**{g}**''')
            if games_results[team_sel][g] == 'V':
                c.markdown(f':green[{s}]')
            elif games_results[team_sel][g] == 'D':
                c.markdown(f':red[{s}]')
            else:
                c.markdown(f':orange[{s}]')
    st.write('---')
    st.write('---')
    st.header('Approche fréquentiste')
    st.write('')

    stat_menu = option_menu(menu_title='',
                            options=['Comparaison des matchs', "Comparaison d'une équipe"],
                            icons=['copy', 'person-bounding-box'],
                            default_index=0, orientation='horizontal')
    
    if stat_menu == 'Comparaison des matchs':
        with st.expander('Démarche'):
            st.subheader('**:blue[Comparaison des deux équipes sur tout le match]**')
            st.write("""Un test de Shapiro-Wilk est réalisé pour chaque équipe afin de tester l'hypothèse nulle selon laquelle les valeurs de la variable sont normalement ditribuées.
                    Un test de Levene est également réalisé afin de tester l'hypothèse nulle d'homogénéité des variances entre les deux équipes pour la variable choisie.""")
            st.write("""Pour une valeur p du test de Shapiro-Wilk inférieure au seuil de 95%, nous rejetons l'hypothèse nulle : la variable de l'équipe ne semble pas suivre une loi normale (distribution normale).
                    Pour une valeur p du test de Levene inférieure au seuil de 95%, nous rejetons l'hypothèse nulle : nous supposons l'absence d'homogénéité des variances (homoscédasticité) entre les deux équipes pour la variable choisie.""")
            st.write("Pour une valeur p > 0.05 au test de Shapiro-Wilk et test de Levene, nous réaliserons un test-t de Student pour échantillons indépendants.")
            st.write("Pour une valeur p > 0.05 au test de Shapiro-Wilk et < 0.05 au test de Levene, nous réaliserons un test de Welch.")
            st.write("Pour une valeur p < 0.05 au test de Shapiro-Wilk, nous réaliserons un test U de Mann-Whitney.")
        st.write('---')

        
        for game in data_team['Match'].unique():
            st.subheader(game)
            if st.toggle('Résultats statistiques', key=game):
                stats_tabs = st.tabs(['Match', 'Périodes 20min'])
                with stats_tabs[0]:
                    c_box = [column for row in [st.columns(3) for _ in range(2)] for column in row]

                    for i, m in enumerate(['Durée', 'Phases', 'Ratio Rucks-Passes', 'Avancée +', 'Ratio Avancée', 'Progression Zones']):
                        with c_box[i]:
                            st.image(f'stat_boxplots/{game}_{m}.png')
                            st.write(tbl_ttest.loc[(tbl_ttest['Match']==game) & (tbl_ttest['Metric']==m), 'Résultat'].unique()[0])
                            st.write('')
                with stats_tabs[1]:
                    for m in ['Durée', 'Phases', 'Ratio Rucks-Passes', 'Avancée +', 'Ratio Avancée', 'Progression Zones']:
                        st.markdown(f'**{m}**')
                        c_box = st.columns(4)
                        with c_box[0]:
                            st.caption("0'-20'")
                            st.image(f"stat_boxplots_period/{game}_0'-20'_{m}.png")
                            st.write(tbl_ttest_period.loc[(tbl_ttest_period['Match']==game) 
                                                          & (tbl_ttest_period['Chrono']=="0'-20'")
                                                          & (tbl_ttest_period['Metric']==m), 'Résultat'].unique()[0])
                        with c_box[1]:
                            st.caption("20'-40'")
                            st.image(f"stat_boxplots_period/{game}_20'-40'_{m}.png")
                            st.write(tbl_ttest_period.loc[(tbl_ttest_period['Match']==game) 
                                                          & (tbl_ttest_period['Chrono']=="20'-40'")
                                                          & (tbl_ttest_period['Metric']==m), 'Résultat'].unique()[0])
                        with c_box[2]:
                            st.caption("40'-60'")
                            st.image(f"stat_boxplots_period/{game}_40'-60'_{m}.png")
                            st.write(tbl_ttest_period.loc[(tbl_ttest_period['Match']==game) 
                                                          & (tbl_ttest_period['Chrono']=="40'-60'")
                                                          & (tbl_ttest_period['Metric']==m), 'Résultat'].unique()[0])
                        with c_box[3]:
                            st.caption("60'-80'")
                            st.image(f"stat_boxplots_period/{game}_60'-80'_{m}.png")
                            st.write(tbl_ttest_period.loc[(tbl_ttest_period['Match']==game) 
                                                          & (tbl_ttest_period['Chrono']=="60'-80'")
                                                          & (tbl_ttest_period['Metric']==m), 'Résultat'].unique()[0])
            st.write('---')

    elif stat_menu == "Comparaison d'une équipe":
        with st.expander('Démarche'):
            st.subheader('**:blue[Comparaison des matchs ainsi que des périodes de 20min de chaque équipe]**')
            st.write("""Un test de Shapiro-Wilk est réalisé pour chaque période de l'équipe afin de tester l'hypothèse nulle selon laquelle les valeurs de la variable de chaque match/période sont normalement ditribuées.
             Un test de Levene est également réalisé afin de tester l'hypothèse nulle d'homogénéité des variances entre les matchs/périodes pour la variable choisie.""")
            st.write("""Pour une valeur p du test de Shapiro-Wilk inférieure au seuil de 95%, nous rejetons l'hypothèse nulle : la variable ne semble pas suivre une loi normale (distribution normale) pour le/la match/période.
                    Pour une valeur p du test de Levene inférieure au seuil de 95%, nous rejetons l'hypothèse nulle : nous supposons l'absence d'homogénéité des variances (homoscédasticité) entre les matchs/périodes pour la variable choisie.""")
            st.write('')
            st.write("Pour une valeur p > 0.05 au test de Shapiro-Wilk et test de Levene, nous réaliserons une ANOVA à un facteur, afin de tester l'hypothèse nulle selon laquelle les moyennes de la variable des matchs/périodes sont égales.")
            st.write("Pour une valeur p < 0.05 au test de Shapiro-Wilk, nous réaliserons un test de Kruskall-Wallis, afin de tester l'hypothèse nulle selon laquelle la distribution de la variable est la même pour toutes les matchs/périodes.")
            st.write("""Pour une valeur p de l'ANOVA inférieure au seuil de 95%, nous rejetons l'hypothèse nulle : la moyenne d'au moins une période est différente de celle d'un.e autre match/période (au moins).
                    Dans ce cas un test post-hoc de Tukey est réalisé afin de tester toutes les combinaisons de comparaison des différents.es matchs/périodes. 
                    Une valeur p < 0.05 au test de Tukey suggère une différence statistiquement significative entre les deux matchs/périodes.""")
            st.write("""Pour une valeur du test de Kruskall-Wallis inférieure au seuil de 95%, nous rejetons l'hypothèse nulle : la distribution d'au moins une période est différente de celle d'un.e autre match/période (au moins).
                    Dans ce cas un test post-hoc de Conover est réalisé afin de tester toutes les combinaisons de comparaison des différents.es matchs/périodes. 
                    Une valeur p < 0.05 au test de Conover suggère une différence statistiquement significative entre les deux matchs/périodes.""")
            st.write("""Pour chaque test post-hoc significatif, le d de Cohen est calculé afin de caractériser la taille de l'effet. 
                    Plus la valeur absolue du d est grande plus la taille de l'effet est importante (la différence est grande entre les matchs/périodes).
                    Le signe du d (positif ou négatif) indique le sens de la différence entre les matchs/périodes.""")
            st.write("Pour plus d'informations sur l'interprétation du d de Cohen, se rendre au lien suivant : [https://rpsychologist.com/fr/cohend/](https://rpsychologist.com/fr/cohend/)")
        
        st.subheader('Comparaison des matchs')
        stats_tabs = st.tabs(['Match', 'Périodes 20min'])
        with stats_tabs[0]:
            c_box = [column for row in [st.columns(3) for _ in range(2)] for column in row]
            for i, m in enumerate(['Durée', 'Phases', 'Ratio Rucks-Passes', 'Avancée +', 'Ratio Avancée', 'Progression Zones']):
                with c_box[i]:
                    st.image(f'stat_anova_game/{team_sel}_{m}.png')
                    st.write('')
                    st.write(tbl_anova.loc[(tbl_anova['Team']==team_sel) & (tbl_anova['Metric']==m), 'ANOVA_res'].values[0])
                    if tbl_anova.loc[(tbl_anova['Team']==team_sel)
                                     & (tbl_anova['Metric']==m), 'Post-hoc_res'].values[0] != '':
                        st.dataframe(pd.read_json(StringIO(tbl_anova.loc[(tbl_anova['Team']==team_sel)
                                                                        & (tbl_anova['Metric']==m), 'Post-hoc_res'].values[0])))
        with stats_tabs[1]:
            for m in ['Durée', 'Phases', 'Ratio Rucks-Passes', 'Avancée +', 'Ratio Avancée', 'Progression Zones']:
                st.markdown(f'**{m}**')
                c_box = st.columns(4)
                with c_box[0]:
                    st.caption("0'-20'")
                    st.image(f"stat_anova_period/{team_sel}_0'-20'_{m}.png")
                    st.write(tbl_anova_period.loc[(tbl_anova_period['Team']==team_sel)
                                                  & (tbl_anova_period['Chrono']=="0'-20'")
                                                  & (tbl_anova_period['Metric']==m), 'ANOVA_res'].values[0])
                    if tbl_anova_period.loc[(tbl_anova_period['Team']==team_sel)
                                            & (tbl_anova_period['Chrono']=="0'-20'")
                                            & (tbl_anova_period['Metric']==m), 'Post-hoc_res'].values[0] != '':
                        st.table(pd.read_json(StringIO(tbl_anova_period.loc[(tbl_anova_period['Team']==team_sel)
                                                                            & (tbl_anova_period['Chrono']=="0'-20'")
                                                                            & (tbl_anova_period['Metric']==m), 'Post-hoc_res'].values[0])))
                with c_box[1]:
                    st.caption("20'-40'")
                    st.image(f"stat_anova_period/{team_sel}_20'-40'_{m}.png")
                    st.write(tbl_anova_period.loc[(tbl_anova_period['Team']==team_sel)
                                                  & (tbl_anova_period['Chrono']=="20'-40'")
                                                  & (tbl_anova_period['Metric']==m), 'ANOVA_res'].values[0])
                    if tbl_anova_period.loc[(tbl_anova_period['Team']==team_sel)
                                            & (tbl_anova_period['Chrono']=="20'-40'")
                                            & (tbl_anova_period['Metric']==m), 'Post-hoc_res'].values[0] != '':
                        st.table(pd.read_json(StringIO(tbl_anova_period.loc[(tbl_anova_period['Team']==team_sel)
                                                                            & (tbl_anova_period['Chrono']=="20'-40'")
                                                                            & (tbl_anova_period['Metric']==m), 'Post-hoc_res'].values[0])))
                with c_box[2]:
                    st.caption("40'-60'")
                    st.image(f"stat_anova_period/{team_sel}_40'-60'_{m}.png")
                    st.write(tbl_anova_period.loc[(tbl_anova_period['Team']==team_sel)
                                                  & (tbl_anova_period['Chrono']=="40'-60'")
                                                  & (tbl_anova_period['Metric']==m), 'ANOVA_res'].values[0])
                    if tbl_anova_period.loc[(tbl_anova_period['Team']==team_sel)
                                            & (tbl_anova_period['Chrono']=="40'-60'")
                                            & (tbl_anova_period['Metric']==m), 'Post-hoc_res'].values[0] != '':
                        st.table(pd.read_json(StringIO(tbl_anova_period.loc[(tbl_anova_period['Team']==team_sel)
                                                                            & (tbl_anova_period['Chrono']=="40'-60'")
                                                                            & (tbl_anova_period['Metric']==m), 'Post-hoc_res'].values[0])))
                with c_box[3]:
                    st.caption("60'-80'")
                    st.image(f"stat_anova_period/{team_sel}_60'-80'_{m}.png")
                    st.write(tbl_anova_period.loc[(tbl_anova_period['Team']==team_sel)
                                                  & (tbl_anova_period['Chrono']=="60'-80'")
                                                  & (tbl_anova_period['Metric']==m), 'ANOVA_res'].values[0])
                    if tbl_anova_period.loc[(tbl_anova_period['Team']==team_sel)
                                            & (tbl_anova_period['Chrono']=="60'-80'")
                                            & (tbl_anova_period['Metric']==m), 'Post-hoc_res'].values[0] != '':
                        st.table(pd.read_json(StringIO(tbl_anova_period.loc[(tbl_anova_period['Team']==team_sel)
                                                                            & (tbl_anova_period['Chrono']=="60'-80'")
                                                                            & (tbl_anova_period['Metric']==m), 'Post-hoc_res'].values[0])))