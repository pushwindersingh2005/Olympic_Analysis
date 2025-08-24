import pandas as pd

def preprocess():
    # Load datasets inside function
    df = pd.read_csv('athlete_events.csv')
    region_df = pd.read_csv('noc_regions.csv')

    # Only Summer Olympics
    df = df[df['Season'] == 'Summer']

    # Merge to get region column
    df = df.merge(region_df[['NOC', 'region']], on='NOC', how='left')

    # Drop duplicate rows
    df.drop_duplicates(inplace=True)

    # Add medal dummy columns (safe handling NaN)
    medal_dummies = pd.get_dummies(df['Medal'])
    df = pd.concat([df, medal_dummies], axis=1)

    return df
