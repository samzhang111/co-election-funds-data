import os
import sys

from pyquery import PyQuery as pq
import pandas as pd

def parse_html(contents):
    doc = pq(contents)
    doc('#_ctl0_Content_ddlOthers option[selected]').remove()
    name = doc('#_ctl0_Content_lblCandName').text()
    addr1 = doc('#_ctl0_Content_lblCandMailAddress1').text()
    addr1_citystate = doc('#_ctl0_Content_lblCandMailCityStateZip').text()
    phone = doc('#_ctl0_Content_lblCandPhone').text()
    fax = doc('#_ctl0_Content_lblCandFax').text()
    email = doc('#_ctl0_Content_lnkCandEmail').attr.href
    if email == 'mailto:':
        email = ''
    website = doc('#_ctl0_Content_lnkCandWeb').attr.href
    if website == 'http://':
        website = ''
    accepted_vol_spend_limits = doc('#_ctl0_Content_lblCandVolSpendLimit').text()
    candidate_id = doc('#_ctl0_Content_lblCandidateID').text()
    candidate_status = doc('#_ctl0_Content_lblCandStatus').text()
    campaign_status = doc('#_ctl0_Content_lblCampaignStatus').text()
    date_terminated = doc('#_ctl0_Content_lblCandTermDate').text()
    date_declared = doc('#_ctl0_Content_lblCandDateDeclared').text()
    jurisdiction = doc('#_ctl0_Content_lblCandJurisdiction').text()
    party = doc('#_ctl0_Content_lblCandParty').text()
    office = doc('#_ctl0_Content_lblCandOffice').text()
    district = doc('#_ctl0_Content_lblCandDistrict').text()
    has_penalties = len(doc('#_ctl0_Content_lblNoPenalties')) > 0
    has_complaints = len(doc('#_ctl0_Content_lblNoComplaints')) > 0
    opponents = doc('#_ctl0_Content_ddlOthers option').map(lambda i, e: pq(e).text())
    opponents_text = '|'.join(list(opponents))

    committee_id = doc('#_ctl0_Content_lblCommitteeID').text()

    data = dict(
        name = name,
        addr1 = addr1,
        addr1_citystate = addr1_citystate,
        phone = phone,
        fax = fax,
        email = email,
        website = website,
        accepted_vol_spend_limits = accepted_vol_spend_limits,
        candidate_id = candidate_id,
        candidate_status = candidate_status,
        campaign_status = campaign_status,
        date_terminated = date_terminated,
        date_declared = date_declared,
        jurisdiction = jurisdiction,
        party = party,
        office = office,
        district = district,
        has_penalties = has_penalties,
        opponents = opponents_text,
        committee_id = committee_id
    )

    return data

results = []

for dir_entry in os.scandir(sys.argv[1]):
    org_id = dir_entry.name.split('=')[-1]
    with open(dir_entry.path) as f:
        contents = f.read()

    data = parse_html(contents)
    data['org_id'] = org_id
    results.append(data)

df = pd.DataFrame(results)
df.to_csv('./candidates.csv', index=False)
