# -*- coding: utf8 -*-

#使用本程式請注意設定以下條件：
#1.誰下大夜
#2.誰上大夜
#3.是否有新人進入排班
#4.是否有新人去ipd或是兒科training第一周
#5.是否有人離職
#6.是否有人出臨床
#7.是否有人入臨床
#8.是否有人外派
#9.是否有人新包班
#10.是否有人不包了
#11.本月是否有休假日

import sqlite3
import datetime
from ClassInJobArrange import JobObj
from SourceReader import CountJobQuantityInOneDay, ReturnJobsList, ReturnRegularMemberName, ReturnMemberChange, RecordNamesAndPattern, GetBackStarterID, GetBackStarterID, ShowForArrangeMemberTable, ReturnHolidays
from copy import deepcopy
from OutputModule import PrintJobTable
from DatabaseOperation import DoMemberDiscount, InsertMember, DisableMember, UpdateForArrange, DisableMemberDiscount

def main():
    conn = sqlite3.connect('job_arrange.db')
    c = conn.cursor()
    #動態更動班後要重新算過
    intJobQuantity = CountJobQuantityInOneDay(c)
    dateStartDate = datetime.datetime.strptime(input('請輸入排班起始日期(西元年-月-日)：'),'%Y-%m-%d')  
    intDays = int(input('請輸入天數：'))
    #回傳資料庫中的班別表格
    #動態更動班後要重新算過
    listJobsTable = ReturnJobsList(c)
    listMemberForArrange = UpdateForArrange(conn)
    listHolidays = ReturnHolidays(c)
    ShowForArrangeMemberTable(listMemberForArrange)
    #把動態更動排班人員的需求載入
    listMemberChange = ReturnMemberChange(conn)
    intStartMemberId = int(input('請輸入排班起始人員的Order ID：'))
    #todo: 產生排班計畫。例如是否於某日加減人員，或是某日加減班。然後依據日期一天天形成班別或是人員條件改變list。然後依據日期去檢查是否有改變的班或是人員，先檢查班，確定有多少班後檢查人員。
    #製造一天中要填班的陣列
    listJobObjsInOneDay = [JobObj() for i in range(0, intJobQuantity, 1)]
    listDaysArray = [deepcopy(listJobObjsInOneDay) for i in range(0, intDays,1)]
    #進入排班流程
    for JobsInOneDay in listDaysArray:
        #確定排到誰了,紀錄現在排到的人名，還有下一位即將排到的人名，以便在陣列重組後可以找到從哪開始排
        listNowAndNextMemberNamesAndPattern = RecordNamesAndPattern(listMemberForArrange, intStartMemberId)
        #todo: 先挑出日期，判斷是否有班別數量更動。
        #todo: 然後判斷是否有人員更動。原則是要先確定班別再確定人員。
        #使用當天日期來判斷是否有在listMemberChange中，如果有，就抓給listMemberChangeToday
        listMemberChangeToday = list(filter(lambda listMC: listMC[0] == str(dateStartDate.date()), listMemberChange))
        if len(listMemberChangeToday) > 0: 
            '''
            判斷人員更動的旗標組合結果如下：
            4:加人
            2:抽人
            1:折扣
            3:先設定有折扣，但是目前人先抽走
            5:加人並設定其折扣
            6:加人但目前不列入排班
            7:加人並設定好折扣但目前不列入排班
            8:取消折扣
            '''
            funcMC = {
                        4: InsertMember,
                        2: DisableMember,
                        1: DoMemberDiscount,
                        #3: print,
                        #5: print,
                        #6: print,
                        #7: print
                        8: DisableMemberDiscount
                     }
            #MC = ('日期', ID, 執行的動作代碼, ArrangeOrder, name, by_pass, discount)
            for MC in listMemberChangeToday:
                listMemberForArrange = funcMC[MC[2]](MC, conn)
            #從記錄下的人名找出下一個要排的人，並且設定好intStartMemberId
            intStartMemberId = GetBackStarterID(listNowAndNextMemberNamesAndPattern,listMemberForArrange)
        if dateStartDate.isoweekday() < 6 and (str(dateStartDate.date()) not in listHolidays):
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

        #for Job in JobsInOneDay:
        #    print(str(Job.JobDate.date()) + ':' + Job.JobName + ":" + Job.JobOwner + "\n")

    PrintJobTable(listDaysArray, listJobsTable) #產生EXCEL或是任何可以產生粗體的文件格式

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

