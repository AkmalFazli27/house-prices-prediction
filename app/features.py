import pandas as pd

DROP_COLS = [
    'YrSold', 'YearBuilt', 'YearRemodAdd',
    '1stFlrSF', '2ndFlrSF', 'BsmtFinSF1', 'BsmtFinSF2',
    'GrLivArea', 'TotalBsmtSF',
    'BsmtFullBath', 'FullBath', 'BsmtHalfBath', 'HalfBath',
    'OpenPorchSF', '3SsnPorch', 'EnclosedPorch', 'ScreenPorch',
    'WoodDeckSF', 'GarageArea'
]

def engineer_features(df: pd.DataFrame):
    df = df.copy()

    df['HouseAge'] = df['YrSold'] - df['YearBuilt']
    df['HouseRemodelAge'] = df['YrSold'] - df['YearRemodAdd']
    df['TotalSF'] = (
        df['1stFlrSF'] + df['2ndFlrSF']
        + df['BsmtFinSF1'] + df['BsmtFinSF2']
    )
    df['TotalArea'] = df['GrLivArea'] + df['TotalBsmtSF']
    df['TotalBaths'] = (
        df['BsmtFullBath'] + df['FullBath']
        + 0.5 * (df['BsmtHalfBath'] + df['HalfBath'])
    )
    df['TotalPorchSF'] = (
        df['OpenPorchSF'] + df['3SsnPorch']
        + df['EnclosedPorch'] + df['ScreenPorch']
    )

    df = df.drop(columns=DROP_COLS, errors='ignore')
    if 'Id' in df.columns:
        df = df.drop(columns=['Id'])

    return df