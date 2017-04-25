import logging

from commons.connect import DBConnect
states = """
AK
AL
AZ
AR
CA
CO
CT
DE
FL
GA
HI
ID
IL
IN
IA
KS
KY
LA
ME
MD
MA
MI
MN
MS
MO
MT
NE
NV
NH
NJ
NM
NY
NC
ND
OH
OK
OR
PA
RI
SC
SD
TN
TX
UT
VT
VA
WA
WV
WI
WY
"""

connect = DBConnect()
states = states.split('\n')
overall = 0
for s in states:
    if s == "":
        continue

    sql = "SELECT count(CompanyAddress) as count FROM ScrapedCompany WHERE CompanyAddress LIKE '% " + s + " %' AND ScrapingSourceID=1;"
    result = connect.cursor.execute(sql)

    total = result.fetchall()[0][0]
    overall += total
    print(s + " : " + str(total))

print overall