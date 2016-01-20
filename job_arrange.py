from openpyxl import Workbook
import sqlite3
conn = sqlite3.connect('job_arrange.db')
c = conn.cursor()
for row in c.execute("select * from member_array"):
    print(row)
conn.close()