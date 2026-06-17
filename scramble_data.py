"""
scramble_data.py — Anonymise processed CRM data for public showcase

What it does:
    - Scales all EUR financial values by a fixed hidden multiplier (preserves distributions)
    - Re-maps Patient.id and Doctor.id to anonymous tokens (P-0001, D-0001, etc.)
    - Shifts all dates by a fixed random offset (preserves trends and seasonality)
    - Leaves all categorical columns untouched (service type, specialty, stage, currency)

Usage:
    cd medical-platform-financial-analysis/
    python scramble_data.py

Output:
    data/processed/crm_stage_finished.xlsx        (overwritten with scrambled version)
    data/processed/crm_selected_translated_column.xlsx  (overwritten with scrambled version)

Run ONCE locally before pushing the showcase repo. Never commit the originals.
"""

import sys
import pandas as pd
import numpy as np
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# ---- Config ----
SEED       = 42
SCALE      = 0.73          # hidden multiplier applied to all EUR amounts
DATE_SHIFT = pd.Timedelta(days=47)   # shift all dates forward by N days

BASE_DIR      = Path(__file__).resolve().parent
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'

np.random.seed(SEED)

EUR_COLS = [
    'Patient Price, EUR',
    'Patient payment , EUR',
    'Doctor cost, EUR',
    'Gross profit',
    'Unit Gross profit',
    'Doctor payment 1 FX',
    'Doctor Payment Amount 1',
    'Patient Payment Amount',
]

DATE_COLS = ['Created Date']

# Backend keys and columns no chart uses — drop before publishing
DROP_COLS = [
    'Insurance ID',
    'Insurance Program',
    'Patient Revenue, EUR',
    'Doctor Revenue, EUR',
    'Clinic Service Amount',
    'Clinic Service, EUR',
    'Clinic Service FX',
    'Created Time',
    'Service Close Date',
    'Payment Patient Date',
    'Doctor Payment Date 1',
    'Doctor payment FX',
    'Doctor payment 1, EUR',
    'Doctor Cost',
    'Patient payment FX',
    'Other Service Cost',
]

# ---- Helpers ----

def scramble_ids(series, prefix):
    """Replace real IDs with sequential tokens (P-00001, D-00001, ...)."""
    unique_ids = series.dropna().unique()
    mapping = {v: f'{prefix}-{i+1:05d}' for i, v in enumerate(np.random.permutation(unique_ids))}
    return series.map(mapping)


def scramble_df(df: pd.DataFrame, label: str) -> pd.DataFrame:
    df = df.copy()

    # Drop unused / sensitive columns
    drop = [c for c in DROP_COLS if c in df.columns]
    if drop:
        df = df.drop(columns=drop)
        for c in drop:
            print(f'  [{label}] dropped  {c}')

    # Scale EUR columns
    for col in EUR_COLS:
        if col in df.columns:
            df[col] = (df[col] * SCALE).round(2)
            print(f'  [{label}] scaled  {col}')

    # Shift dates
    for col in DATE_COLS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col]) + DATE_SHIFT
            print(f'  [{label}] shifted {col}')

    # Anonymise IDs
    if 'Patient.id' in df.columns:
        df['Patient.id'] = scramble_ids(df['Patient.id'], 'P')
        print(f'  [{label}] anonymised Patient.id')
    if 'Doctor.id' in df.columns:
        df['Doctor.id'] = scramble_ids(df['Doctor.id'], 'D')
        print(f'  [{label}] anonymised Doctor.id')
    if 'Record Id' in df.columns:
        df['Record Id'] = scramble_ids(df['Record Id'], 'REC')
        print(f'  [{label}] anonymised Record Id')

    return df


# ---- Load, scramble, save ----

files = {
    'crm_stage_finished.xlsx':               'df_done',
    'crm_selected_translated_column.xlsx':   'df_all',
}

for filename, label in files.items():
    path = PROCESSED_DIR / filename
    if not path.exists():
        print(f'SKIP — not found: {path}')
        continue

    print(f'\nLoading {filename} ...')
    df = pd.read_excel(path)
    print(f'  {len(df):,} rows, {len(df.columns)} columns')

    df_scrambled = scramble_df(df, label)
    df_scrambled.to_excel(path, index=False)
    print(f'  Saved → {path}')

print('\nDone. Push the scrambled files to the showcase repo.')
print('Do NOT push the originals.')
