from commons.connect import DBConnect
from data.us_states import states_list

connect = DBConnect()
states = states_list.split('\n')
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