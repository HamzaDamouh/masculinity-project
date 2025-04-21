#!/usr/bin/env python3
# src/data_preparation.py

import pandas as pd
import os
from pathlib import Path

# 1) Paths
BASE       = Path(__file__).resolve().parent.parent
RAW_CSV    = BASE / 'data' / 'raw'       / 'masculinity.csv'
OUT_DIR    = BASE / 'data' / 'processed'
CLEAN_CSV  = OUT_DIR / 'masculinity_clean.csv'
OUT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    # 2) Load & drop non‑responders to Q1
    df = pd.read_csv(RAW_CSV)
    df = df.dropna(subset=['q0001'])

    # 3) Rename only columns that exist
    rename_map = {
        'q0001': 'self_masculinity',            # Q1
        'q0002': 'importance_seen_masculine',   # Q2
        'q0005': 'pressure_unhealthy',          # Q5
        'q0014': 'metoo_awareness',             # Q14
        'q0015': 'metoo_behavior_work',         # Q15
        'q0017': 'expect_first_move',           # Q17
        'q0018': 'date_payment_freq',           # Q18
        'q0022': 'rel_behavior_change',         # Q22
        'q0009': 'employment_status',           # Q9
        'q0024': 'marital_status',              # Q24
        'kids':   'children_status',            # Q25
        'orientation': 'orientation',           # Q26
        'age3':   'age_bracket',                # Q27
        'q0028': 'age_exact',                   # Q27 exact
        'race2':  'race_group',                 # Q28 broad
        'racethn4':'ethnicity',                 # Q28 detail
        'educ3':  'education_detail',           # Q29 detail
        'educ4':  'education',                  # Q29 main
        'q0034': 'income_bracket',              # income (from q0034)
        'q0035': 'region',                      # Q30
        'q0036': 'device_type',                 # device info
        'weight': 'survey_weight'               # sample weight
    }
    # Keep only existing keys
    rename_map = {old: new for old,new in rename_map.items() if old in df.columns}
    df = df.rename(columns=rename_map)

    # 4) Order all single‑select categoricals
    if 'self_masculinity' in df:
        df['self_masculinity'] = pd.Categorical(
            df['self_masculinity'],
            categories=[
                'Not at all masculine',
                'Not very masculine',
                'Somewhat masculine',
                'Very masculine'
            ], ordered=True
        )
    if 'importance_seen_masculine' in df:
        df['importance_seen_masculine'] = pd.Categorical(
            df['importance_seen_masculine'],
            categories=[
                'Not at all important',
                'Not too important',
                'Somewhat important',
                'Very important'
            ], ordered=True
        )
    if 'pressure_unhealthy' in df:
        df['pressure_unhealthy'] = df['pressure_unhealthy'].map({'Yes':1, 'No':0}).astype('Int64')
    if 'metoo_awareness' in df:
        df['metoo_awareness'] = pd.Categorical(
            df['metoo_awareness'],
            categories=['Nothing at all','Only a little','Some','A lot'],
            ordered=True
        )
    if 'metoo_behavior_work' in df:
        df['metoo_behavior_work'] = df['metoo_behavior_work'].map({'Yes':1,'No':0}).astype('Int64')
    if 'expect_first_move' in df:
        df['expect_first_move'] = df['expect_first_move'].map({'Yes':1,'No':0}).astype('Int64')
    if 'date_payment_freq' in df:
        df['date_payment_freq'] = pd.Categorical(
            df['date_payment_freq'],
            categories=['Never','Rarely','Sometimes','Often','Always'],
            ordered=True
        )
    if 'rel_behavior_change' in df:
        df['rel_behavior_change'] = df['rel_behavior_change'].map({'Yes':1,'No':0}).astype('Int64')

    # Demographics ordering
    if 'children_status' in df:
        df['children_status'] = pd.Categorical(
            df['children_status'],
            categories=[
                'No children',
                'Yes, one or more children under 18',
                'Yes, one or more children 18 or older'
            ], ordered=True
        )
    if 'orientation' in df:
        df['orientation'] = pd.Categorical(
            df['orientation'],
            categories=['Straight','Gay','Bisexual','Other']
        )
    if 'age_bracket' in df:
        df['age_bracket'] = pd.Categorical(
            df['age_bracket'],
            categories=['18 - 34','35 - 64','65+'], ordered=True
        )
    if 'race_group' in df:
        df['race_group'] = pd.Categorical(
            df['race_group'],
            categories=['White','Non-white']
        )
    if 'education' in df:
        df['education'] = pd.Categorical(
            df['education'],
            categories=[
                'Did not complete high school',
                'High school or G.E.D.',
                'Associate’s degree',
                'Some college',
                'College graduate',
                'Post graduate degree'
            ], ordered=True
        )

    # 5) Convert every multi‑select block to 0/1 flags
    multi_prefixes = ['q0004_', 'q0007_', 'q0008_', 'q0010_', 'q0011_', 'q0012_', 'q0019_', 'q0020_', 'q0021_']
    for pref in multi_prefixes:
        cols = [c for c in df.columns if c.startswith(pref)]
        if cols:
            df[cols] = df[cols].ne('Not selected').astype(int)

    # 6) Save clean dataset
    df.to_csv(CLEAN_CSV, index=False)
    print("✅ Cleaned data written to:", CLEAN_CSV)

if __name__ == '__main__':
    main()
