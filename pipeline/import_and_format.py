# import packages
import pandas as pd

# import downloaded csv file into a data frame
df = pd.read_csv('T_ONTIME_REPORTING.csv')

# change header names as instructed in the model description
df = df.rename(columns={'DAY_OF_MONTH': 'DAY', 'ORIGIN_AIRPORT_ID': 'ORG_AIRPORT', 'DEST_AIRPORT_ID': 'DEST_AIRPORT',
                        'CRS_DEP_TIME': 'SCHEDULED_DEPARTURE', 'DEP_TIME': 'DEPARTURE_TIME', 'DEP_DELAY': 'DEPARTURE_DELAY',
                        'CRS_ARR_TIME': 'SCHEDULED_ARRIVAL', 'ARR_TIME': 'ARRIVAL_TIME', 'ARR_DELAY': 'ARRIVAL_DELAY'})

# export csv to prepare for data cleaning script
df.to_csv('import_and_format.csv', index=False)