import numpy as np
import pandas as pd

print("Loaded helper.py")

def fetch_medal_tally(df, year='Overall', country='Overall'):
    temp_df = df.copy()

    # Apply filters
    if year != 'Overall' and country != 'Overall':
        temp_df = temp_df[(temp_df['Year'] == int(year)) & (temp_df['region'] == country)]
    elif year != 'Overall':
        temp_df = temp_df[temp_df['Year'] == int(year)]
    elif country != 'Overall':
        temp_df = temp_df[temp_df['region'] == country]

    # Create numeric medal columns
    temp_df['Gold']   = (temp_df['Medal'] == 'Gold').astype(int)
    temp_df['Silver'] = (temp_df['Medal'] == 'Silver').astype(int)
    temp_df['Bronze'] = (temp_df['Medal'] == 'Bronze').astype(int)

    # Group and sum
    x = (
        temp_df.groupby('region')[['Gold','Silver','Bronze']]
        .sum()
        .sort_values('Gold', ascending=False)
        .reset_index()
    )

    # Add total
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x



def medal_tally(df):
    # Remove duplicate rows
    medal_tally = df.drop_duplicates(
        subset=['Team','NOC','Games','Year','City','Sport','Event','Medal']
    )

    # Create numeric medal columns
    medal_tally['Gold']   = (medal_tally['Medal'] == 'Gold').astype(int)
    medal_tally['Silver'] = (medal_tally['Medal'] == 'Silver').astype(int)
    medal_tally['Bronze'] = (medal_tally['Medal'] == 'Bronze').astype(int)

    # Group by region and sum
    medal_tally = (
        medal_tally.groupby('region')[['Gold', 'Silver', 'Bronze']]
        .sum()
        .sort_values('Gold', ascending=False)
        .reset_index()
    )

    # Add total medals
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years, country

def data_over_time(df, col):
    out = (
        df.drop_duplicates(['Year', col])
          .groupby('Year')[col]
          .count()
          .reset_index()
          .rename(columns={col: 'count'})
    )
    return out

def most_successful(df, sport='Overall'):
    # Filter only medal winners
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Count medals by athlete
    x = (temp_df.groupby(['Name', 'region'])
                .count()['Medal']
                .reset_index()
                .sort_values('Medal', ascending=False)
                .head(15))

    return x

def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df