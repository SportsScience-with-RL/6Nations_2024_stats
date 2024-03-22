import pandas as pd
import numpy as np
from scipy import stats
import time
import glob

def load_data():
    data = pd.DataFrame()
    all_files = glob.glob('data/*.csv')
    
    for file in all_files:
        round_ = file.split('_')[0][-2:]
        csv_file = pd.read_csv(file, encoding='latin1')
        csv_file['Round'] = round_
        data = pd.concat([data, csv_file], ignore_index=True)

    data = data[data['Résultat']!='Supprimer']

    data['Dur.'] = [e-s for s, e in zip(data['Start_time'], data['End_time'])]
    data.loc[368, 'Dur.'] = 49.96
    data.loc[242, 'Dur.'] = 16.78
    data['Durée'] = [((time.localtime(t).tm_min*60) + time.localtime(t).tm_sec) if t>0 else 0 for t  in data['Dur.']]
    data = data[data['Durée']>0]
    data['Durée_timeline'] = [(-d) if p==m.split(' - ')[1] else d for d, p, m in zip(data['Durée'], data['Possession'], data['Match'])]

    data.loc[data['End_zone']=='En-but', 'End_zone_value'] = 12

    data['Phases'] = data['Ruck'] + data['Ruck +']

    data['Ratio Rucks-Passes'] = round(data['Phases']
                                    / (data['Passe']+data['Offload']+data['Offload +']), 2)
    data['Ratio Rucks-Passes'] = data['Ratio Rucks-Passes'].fillna(0)
    data.loc[data['Passe']==0, 'Ratio Rucks-Passes'] = 0

    data['Jeu debout'] = data['Passe'] + data['Offload'] + data['Offload +']
    data['Utilisation Pied'] = data['Dégagement'] + data['Jeu au pied']
    data['Avancée +'] = data['Ruck +'] + data['Offload +']

    data['Ratio Avancée'] = round(data['Avancée +'] / (data['Ruck']+data['Offload']), 2)
    data['Ratio Avancée'] = data['Ratio Avancée'].fillna(0)
    data.loc[data['Ratio Avancée']==np.inf, 'Ratio Avancée'] = 0

    data['Progression Zones'] = data['End_zone_value'] - data['Start_zone_value']

    return(data)

def descriptive_tbl_full(data):
    full_tbl = pd.DataFrame()
    for g in data['Match'].unique():
        df_g = data[data['Match']==g].copy()  
        for m in ['Durée', 'Phases', 'Ratio Rucks-Passes', 'Avancée +', 'Ratio Avancée', 'Progression Zones']:
            agg_func = {
                m: ['count', lambda x: f"{int(stats.variation(x)*100)}%" if np.mean(x) > 0 else '0%', 'mean', 'min',
                    lambda x: x.quantile(.25), 'median', lambda x: x.quantile(.75), 'max']
                    }
            
            tbl = df_g.groupby(['Round', 'Possession']).agg(agg_func).round(1)
            tbl = tbl.rename(columns={'count':'Nb', '<lambda_0>': 'Coef. Var.', 'mean': 'Moy.',
                                    'min': 'Min.', '<lambda_1>': 'Q1', 'median': 'Méd.',
                                    '<lambda_2>': 'Q3', 'max': 'Max.'})
            tbl.columns = tbl.columns.droplevel()
            tbl['game'] = g
            tbl['metric'] = m

            full_tbl = pd.concat([full_tbl, tbl])

    return full_tbl

def descriptive_tbl_period(data):
    full_tbl = pd.DataFrame()
    for g in data['Match'].unique():
        df_g = data[data['Match']==g].copy()  
        for m in ['Durée', 'Phases', 'Ratio Rucks-Passes', 'Avancée +', 'Ratio Avancée', 'Progression Zones']:
            agg_func = {
                m: ['count', lambda x: f"{int(stats.variation(x)*100)}%" if np.mean(x) > 0 else '0%', 'mean', 'min',
                    lambda x: x.quantile(.25), 'median', lambda x: x.quantile(.75), 'max']
                    }
            
            tbl = df_g.groupby(['Round', 'Chrono', 'Possession']).agg(agg_func).round(1)
            tbl = tbl.rename(columns={'count':'Nb', '<lambda_0>': 'Coef. Var.', 'mean': 'Moy.',
                                    'min': 'Min.', '<lambda_1>': 'Q1', 'median': 'Méd.',
                                    '<lambda_2>': 'Q3', 'max': 'Max.'})
            tbl.columns = tbl.columns.droplevel()
            tbl['game'] = g
            tbl['metric'] = m

            full_tbl = pd.concat([full_tbl, tbl])
    
    return full_tbl