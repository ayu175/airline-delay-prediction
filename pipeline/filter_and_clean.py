# import packages
import pandas as pd

# import the import_and_format.csv into a data frame
df = pd.read_csv('import_and_format.csv')

# filter data frame to only New York, NY: John F. Kennedy International - Airport ID: 12478
jfk_df = df[df['ORG_AIRPORT'] == 12478].copy()

# data cleaning part 1: check for missing values and remove rows with missing values
jfk_df.isnull().sum()
jfk_df.dropna(inplace=True)

# data cleaning part 2: change data types from float to integer and integer to string
jfk_df = jfk_df.astype({
    'ORG_AIRPORT': str,
    'DEST_AIRPORT': str,
    'DEPARTURE_TIME': int,
    'DEPARTURE_DELAY': int,
    'ARRIVAL_TIME': int,
    'ARRIVAL_DELAY': int})

# export csv for model
jfk_df.to_csv('filter_and_clean.csv', index=False)