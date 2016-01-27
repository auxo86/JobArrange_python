# -*- coding: utf8 -*-
""" 下面是用來取得一天有幾個班的函數 """
def CountJobQuantityInOneDay(c):
    c.execute('select count(job_name) from job where enable = 1')
    intJobQuantity = c.fetchall()[0][0]
    return intJobQuantity

def ReturnJobsList(c):
    c.execute('select * from job where enable = 1 order by job_order')
    listJobsInOneDay = c.fetchall()
    return listJobsInOneDay

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

def ReturnRegularMemberName(c, intMemberId):
    c.execute('select name from member_array where ID = ' + str(intMemberId))
    strMemberName = c.fetchall()[0][0]
    return strMemberName