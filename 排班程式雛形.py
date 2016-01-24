# -*- coding: utf8 -*-
import sqlite3
import datetime
from ClassInJobArrange import JobObj

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

def main():
    conn = sqlite3.connect('job_arrange.db')
    c = conn.cursor()
    intJobQuantity = CountJobQuantityInOneDay(c)
    dateStartDate = datetime.datetime.strptime(input('請輸入排班起始日期(西元年-月-日)：'),'%Y-%m-%d')  
    intDays = int(input('請輸入天數：'))
    listMemberForArrange = ShowAndReturnMemberTable(c)
    intStartMemberId = int(input('請輸入排班起始人員的Order ID：'))
    listJobObjsInOneDay = [JobObj() for i in range(0, intJobQuantity, 1)]
    listDaysArray = [listJobObjsInOneDay[:] for i in range(0, intDays,1)]
    print(listDaysArray)

    conn.close()

if __name__ == '__main__': main()










#c.execute('select job_name from job where monday_job = 1 order by job_order' )
#job_rec_set = c.fetchall()
##job_rec_set.append(['-------------'])
#c.execute('select name from member_array where by_pass = 0 and discount = 0 order by arrange_order')
#routine_member_rec_set = c.fetchall()
##routine_member_rec_set.append(['-------------'])
#c.execute('select name from member_array where by_pass = 0 and discount = 1 order by arrange_order')
#discount_member_rec_set = c.fetchall()
##discount_member_rec_set.append(['-------------'])
#list_array = (job_rec_set, routine_member_rec_set, discount_member_rec_set)


#for x in list_array:
#    i=0
#    for y in x:
#        print(y[0], end = '\t')
#        i+=1
#        if i%12 == 0:
#            print()
#    print()
#conn.close



##print('禮拜一的工作點:')
##for x in job_rec_set:
##    print (x[0])
##print('照排的人員:')
##for x in routine_member_rec_set:
##    print (x[0])
##print('折扣的人員:')
##for x in discount_member_rec_set:
##    print (x[0])

