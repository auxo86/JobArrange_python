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
    conn.execute('delete from MemberChange')
    c.execute('vacuum;')
    conn.commit()
    return listMemberChange

def RecordNamesAndPattern(listMemberForArrange, intStartMemberId):
    listNowAndNextMemberNamesAndPattern = []
    #迴圈跑十次，保留十個人名
    for i in range(0,10,1):
		#先看看排到的這個人在listMemberForArrange中出現幾次
        listIdsAndNames = list(filter(lambda Names: Names[1] == listMemberForArrange[intStartMemberId - 1][1], listMemberForArrange))
		#如果抓出來的list中有兩個元素，從第一個元素開始，如果ID = 現在排到的人的ID，則把listPattern的list塞入一個1。當然另外一個就是塞入0，如果抓出的元素只有一個，那麼listPattern只會有一個1。這可以告訴我們，如果是明旭，是前面的明旭還是後面的明旭，也就是製造pattern
        listPattern=[]
        for IDandName in listIdsAndNames:
            if IDandName[0] == intStartMemberId:
                listPattern.append(1)
            else:
                listPattern.append(0)
        listNowAndNextMemberNamesAndPattern.append((listMemberForArrange[intStartMemberId - 1][1],) + (listPattern,))
        intStartMemberId += 1
        if intStartMemberId > len(listMemberForArrange):
            intStartMemberId = 1
    #listNowAndNextMemberNamesAndPattern裡面大概是這樣 [('明旭', [1,0]), ('慧枚', [1,0])....]
    return listNowAndNextMemberNamesAndPattern

def CheckPattern(listZipped):
    #為了避免這個問題 -> 就是萬一這個人本來沒有折扣，如果pattern是[0,1]那就ok。但是萬一他在listMemberForArrange加加減減的過程中變成有折扣，這時候如果pattern還是[0,1]，這就糟了。zip後可能會產生[0, (145, '詠馨')]....於是在下面的程式碼中，就變成最後回傳的intStartMemberId == 0
    if (len(listZipped) == 1 and listZipped[0][0] == 0) or len(listZipped) == 0:
        return 0
    else:
        return 1

def GetBackStarterID(listNowAndNextMemberNamesAndPattern, listMemberForArrange):
    listIdsAndNames = []
    i = 0
    listZipped = []
    #有保留十個人名，萬一一個個被抽走，還可以有十個機會。如果超過十個就會出現錯誤
    #為了避免這個問題 -> 就是萬一這個人本來沒有折扣，如果pattern是[0,1]那就ok。但是萬一他在listMemberForArrange加加減減的過程中變成有折扣，這時候如果pattern還是[0,1]，這就糟了。zip後可能會產生[0, (145, '詠馨')]....於是在下面的程式碼中，就變成最後回傳的intStartMemberId == 0
    while len(listIdsAndNames) == 0 or CheckPattern(listZipped) == 0:
        listIdsAndNames = list(filter(lambda Names: Names[1] == listNowAndNextMemberNamesAndPattern[i][0], listMemberForArrange))
        listZipped = list(zip(listNowAndNextMemberNamesAndPattern[i][1], listIdsAndNames))
        i += 1
    intStartMemberId = 0
    for item in listZipped:
        if item[0] == 1:
            intStartMemberId = item[1][0]
    return intStartMemberId