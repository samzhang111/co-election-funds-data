import sys
import pandas as pd

candidates_csv = sys.argv[1]

df = pd.read_csv('results/candidates.csv')
df['date_declared'] = pd.to_datetime(df['date_declared'])
df['declared_year'] = df['date_declared'].apply(lambda x: x.year)
df['opponents'].fillna('', inplace=True)
df = df.dropna(subset=['committee_id'])
df['candidates'] = df.apply(lambda x: str(list(sorted(x.opponents.split('|') + [x['name']]))), axis=1)

unique_campaigns = {}
unique_campaign_id = 0
df.fillna('', inplace=True)
for i, row in df.iterrows():
    row_key = (row.jurisdiction, row.office, row.district, row.candidates)
    if row_key not in unique_campaigns:
        unique_campaigns[row_key] = unique_campaign_id
        unique_campaign_id += 1

df['race_id'] = df.apply(lambda row: unique_campaigns[(row.jurisdiction, row.office, row.district, row.candidates)], axis=1)

df_dropped = df.drop(columns=['opponents'], axis=1)
df_dropped.to_csv('candidate_races.csv', index=False)
