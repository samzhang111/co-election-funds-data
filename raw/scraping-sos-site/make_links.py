base = 'http://tracer.sos.colorado.gov/PublicSite/SearchPages/CommitteeDetail.aspx?OrgID={}\n'
base_cand = 'http://tracer.sos.colorado.gov/PublicSite/SearchPages/CandidateDetail.aspx?SeqID={}\n'

with open('committee_urls.txt', 'w') as out:
    for i in range(1, 34035):
        url = base.format(i)
        out.write(url)

with open('candidate_urls.txt', 'w') as out:
    for i in range(40432, 0, -1):
        url = base_cand.format(i)
        out.write(url)
