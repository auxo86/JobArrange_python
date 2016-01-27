# -*- coding: utf8 -*-

#使用本程式請注意設定以下條件：
#1.誰下大夜
#2.誰上大夜
#3.是否有新人進入排班
#4.是否有新人去ipd或是兒科training
#5.是否有人離職
#6.是否有人出臨床
#7.是否有人入臨床
#8.是否有人外派

import sqlite3
import datetime
from ClassInJobArrange import JobObj
from SourceReader import CountJobQuantityInOneDay, ShowAndReturnMemberTable, ReturnJobsList, ReturnRegularMemberName
from copy import deepcopy

def main():
    conn = sqlite3.connect('job_arrange.db')
    c = conn.cursor()
    intJobQuantity = CountJobQuantityInOneDay(c)
    dateStartDate = datetime.datetime.strptime(input('請輸入排班起始日期(西元年-月-日)：'),'%Y-%m-%d')  
    intDays = int(input('請輸入天數：'))
    #回傳資料庫中的班別表格
    listJobsTable = ReturnJobsList(c)
    listMemberForArrange = ShowAndReturnMemberTable(c)
    intStartMemberId = int(input('請輸入排班起始人員的Order ID：'))
    #製造一天中要填班的陣列
    listJobObjsInOneDay = [JobObj() for i in range(0, intJobQuantity, 1)]
    listDaysArray = [deepcopy(listJobObjsInOneDay) for i in range(0, intDays,1)]
    for JobsInOneDay in listDaysArray:
        if dateStartDate.isoweekday() < 6:
            iJobIndex = 0
            for Job in JobsInOneDay:
                #填入日期
                Job.JobDate = dateStartDate
                #填入工作點字串
                Job.JobName = listJobsTable[iJobIndex][2]
                #填入人員。不過要先判斷是否有包班。
                if listJobsTable[iJobIndex][(dateStartDate.isoweekday() + 5)] == 1: #如果這天有這個班
                    if listJobsTable[iJobIndex][4] == 1: #看看是否有包班
                        Job.JobOwner = ReturnRegularMemberName(c, listJobsTable[iJobIndex][5]) #取得包班人員名字
                    else:
                        Job.JobOwner = listMemberForArrange[intStartMemberId - 1][1] #從待排人員陣列中抓一個來排
                        #排了人就往下一位加一，沒有排就不用
                        intStartMemberId += 1
                else:
                    #如果當天沒有這個工作，人名不填
                    Job.JobOwner = ""
                #如果要排的ID到了大於人員陣列的情況，就從頭開始排
                if intStartMemberId > len(listMemberForArrange):
                    intStartMemberId = 1
                iJobIndex += 1 #推往下一個班
        else:
            for Job in JobsInOneDay:
                Job.JobDate = dateStartDate
                Job.JobName = ""
                Job.JobOwner = ""
        dateStartDate = dateStartDate + datetime.timedelta(days = 1)

        for Job in JobsInOneDay:
            print(str(Job.JobDate.date()) + ':' + Job.JobName + ":" + Job.JobOwner + "\n")

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

