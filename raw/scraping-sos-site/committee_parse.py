import os
import sys

import pandas as pd
from pyquery import PyQuery as pq

def parse_html(contents):
    doc = pq(contents)
    name = doc('#_ctl0_Content_lblCommName').text()
    addr1 = doc('#_ctl0_Content_lblPhysAddress1').text()
    addr1_citystate = doc('#_ctl0_Content_lblPhysCityStateZip').text()
    addr2 = doc('#_ctl0_Content_lblMailAddress1').text()
    addr2_citystate = doc('#__ctl0_Content_lblMailCityStateZip').text()
    phone = doc('#_ctl0_Content_lblCommPhone').text()
    fax = doc('#_ctl0_Content_lblCommFax').text()
    purpose = doc('#_ctl0_Content_lblCommPurpose').text()
    registered_agent = doc('#_ctl0_Content_lblRegisteredAgent').text()
    agent_phone = doc('#_ctl0_Content_lblAgentPhone').text()
    agent_email = doc('#_ctl0_Content_lnkAgentEmail').text()
    website = doc('#_ctl0_Content_lnkCommWebAddress').attr.href
    if website == 'http://':
        website = ''
    committee_id = doc('#_ctl0_Content_lblCommitteeID').text()
    committee_type = doc('#_ctl0_Content_lblCommitteeType').text()
    committee_status = doc('#_ctl0_Content_lblCommStatus').text()
    date_organized = doc('#_ctl0_Content_lblCommDateOrganized').text()
    date_terminated = doc('#_ctl0_Content_lblCommDateTerminated').text()
    jurisdiction = doc('#_ctl0_Content_lblJurisdiction').text()
    party = doc('#_ctl0_Content_lblCommParty').text()
    has_complaints = len(doc('#_ctl0_Content_lblNoComplaints')) == 0

    return dict(
        name = name,
        addr1 = addr1,
        addr1_citystate = addr1_citystate,
        addr2 = addr2,
        addr2_citystate = addr2_citystate,
        phone = phone,
        fax = fax,
        purpose = purpose,
        registered_agent = registered_agent,
        agent_phone = agent_phone,
        agent_email = agent_email,
        website = website,
        committee_id = committee_id,
        committee_type = committee_type,
        committee_status = committee_status,
        date_organized = date_organized,
        date_terminated = date_terminated,
        jurisdiction = jurisdiction,
        party = party,
        has_complaints = has_complaints
    )

results = []

for i, dir_entry in enumerate(os.scandir(sys.argv[1])):
    if i % 1000 == 0:
        print('.', end='')
        sys.stdout.flush()
    org_id = dir_entry.name.split('=')[-1]
    with open(dir_entry.path) as f:
        contents = f.read()

    data = parse_html(contents)
    data['org_id'] = org_id
    results.append(data)

df = pd.DataFrame(results)
df.to_csv('./committees.csv', index=False)
