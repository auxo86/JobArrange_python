# -*- coding: utf8 -*-
""" 下面是用來取得一天有幾個班的函數 """
def CountJobQuantityInOneDay(c):
    c.execute('select count(job_name) from job where enable = 1')
    intJobQuantity = c.fetchall()[0][0]
    return intJobQuantity

def ShowAndReturnMemberTable(c):
    c.execute('select * from ForArrange')
    listMemberForArrange = c.fetchall()
    i = 0
    for tupleMember in listMemberForArrange:
        print(tupleMember, end = '\t')
        if i % 4 == 3:
            print()
        i += 1
    print()
    return listMemberForArrange