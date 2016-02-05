# -*- coding: utf8 -*-
import sqlite3
""" 下面是用來取得一天有幾個班的函數 """
def CountJobQuantityInOneDay(c):
    c.execute('select count(job_name) from job where enable = 1')
    intJobQuantity = c.fetchall()[0][0]
    return intJobQuantity

def ReturnJobsList(c):
    c.execute('select * from job where enable = 1 order by job_order')
    listJobsInOneDay = c.fetchall()
    return listJobsInOneDay

def ShowForArrangeMemberTable(listMemberForArrange):
    i = 0
    for tupleMember in listMemberForArrange:
        print(tupleMember, end = '\t')
        if i % 4 == 3:
            print()
        i += 1
    print()

def ReturnRegularMemberName(c, intMemberId):
    c.execute('select name from member_array where ID = ' + str(intMemberId))
    strMemberName = c.fetchall()[0][0]
    return strMemberName

def ReturnMemberChange(conn):
    c = conn.cursor()
    c.execute('select * from MemberChange')
    listMemberChange = c.fetchall()
    #抓完要改變的人員清單後把表格清掉
    conn.execute('drop table if exists MemberChange')
    conn.commit()
    return listMemberChange

def RecordNamesAndPattern(listMemberForArrange, intStartMemberId):
    listPattern=[]
    #先看看排到的這個人在listMemberForArrange中出現幾次
    listIdsAndNames = list(filter(lambda Names: Names[1] == listMemberForArrange[intStartMemberId - 1][1], listMemberForArrange))
    #如果抓出來的list中有兩個元素，從第一個元素開始，如果ID = 現在排到的人的ID，則把listPattern的list塞入一個1。當然另外一個就是塞入0，如果抓出的元素只有一個，那麼listPattern只會有一個1。這可以告訴我們，如果是明旭，是前面的明旭還是後面的明旭
    for IDandName in listIdsAndNames:
        if IDandName[0] == intStartMemberId:
            listPattern.append(1)
        else:
            listPattern.append(0)
    listNowAndNextMemberNamesAndPattern = [[listMemberForArrange[intStartMemberId - 1][1], listMemberForArrange[intStartMemberId][1]], listPattern]
    #listNowAndNextMemberNamesAndPattern裡面大概是這樣 [['明旭','慧枚'], [1,0]]
    return listNowAndNextMemberNamesAndPattern

def GetBackStarterID(listNowAndNextMemberNamesAndPattern, listMemberForArrange):
    listIdsAndNames = list(filter(lambda Names: Names[1] == listNowAndNextMemberNamesAndPattern[0][0], listMemberForArrange))
    #如果第一個名字沒有了，找第二個，如果第二個也沒有了....那....
    if len(listIdsAndNames) == 0:
        listIdsAndNames = list(filter(lambda Names: Names[1] == listNowAndNextMemberNamesAndPattern[0][1], listMemberForArrange))
    #zip後應該是像這樣(1, (145, '詠馨'))
    listZipped = zip(listNowAndNextMemberNamesAndPattern[1], listIdsAndNames)
    intStartMemberId = 0
    for item in listZipped:
        if item[0] == 1:
            intStartMemberId = item[1][0]
    return intStartMemberId