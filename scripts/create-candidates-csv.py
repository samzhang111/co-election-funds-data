import pandas as pd
import sys

contributions_csv = sys.argv[1]
candidates_csv = sys.argv[2]
df = pd.read_csv(contributions_csv, encoding='iso-8859-1')
df_candidates = pd.read_csv(candidates_csv)

df['person'] = df['FirstName'] + ' ' + df['LastName'] + ' ' + df['Address1'] + ' ' + df['City']

i = 0

# We're counting each unlisted contributor as a "unique" person.
def fill_row(p):
    global i
    if not pd.isna(p):
        return p

    i += 1
    return 'Unlisted {}'.format(i)

df['person'] = df['person'].apply(fill_row)
df['colorado'] = df.State == 'CO'

campaign_person_total = df.groupby(['CO_ID', 'person']).ContributionAmount.sum()
mean_by_campaign = campaign_person_total.mean(level=0)
donors_by_campaign = campaign_person_total.count(level=0)
donations_by_campaign = df.groupby('CO_ID').Jurisdiction.count()

df_campaign = pd.merge(donors_by_campaign.to_frame(), mean_by_campaign.to_frame(), how='left', left_index=True, right_index=True).rename(columns={
    'ContributionAmount_x': 'donors',
    'ContributionAmount_y': 'mean'
    }).fillna(0)

df_campaign = df_campaign.join(donations_by_campaign).rename(columns={
    'Jurisdiction': 'donations'
})

# donations from in vs. out of state
in_state_donors_by_campaign = df[df.colorado].groupby('CO_ID').person.nunique()
df_campaign = df_campaign.join(in_state_donors_by_campaign).rename(columns={
    'person': 'in_state_donors_count'
})

df_campaign['oo_state_donors_count'] = df_campaign['donors'] - df_campaign['in_state_donors_count']

campaign_contribs_by_colorado = df.groupby(['CO_ID', 'person', 'colorado']).ContributionAmount.sum().mean(level=[0, 2]).reset_index(level=1)

df_campaign = pd.merge(df_campaign, campaign_contribs_by_colorado[campaign_contribs_by_colorado.colorado], left_index=True, right_index=True).rename(columns={
    'ContributionAmount': 'in_state_donations_amt'
})

df_campaign = pd.merge(df_campaign, campaign_contribs_by_colorado[~campaign_contribs_by_colorado.colorado], left_index=True, right_index=True).rename(columns={
    'ContributionAmount': 'oo_state_donations_amt'
})

df_campaign.drop(['colorado_x', 'colorado_y'], inplace=True, axis=1)

# merging in candidate data

df_campaign = pd.merge(df_campaign, df_candidates[[
    'name', 'org_id', 'office', 'district', 'committee_id',
    'party', 'jurisdiction', 'race_id', 'declared_year'
    ]].rename(columns={'committee_id': 'CO_ID'}), left_index=True, right_on='CO_ID')

df_campaign = df_campaign[df_campaign.declared_year >= 2016]

df_campaign.to_csv('campaigns.csv', index=False)
