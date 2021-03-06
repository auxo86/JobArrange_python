# -*- coding: utf8 -*-
import sqlite3
import uuid

#更新ForArrange(人員有新增，取消，或是折扣時)
def UpdateForArrange(conn):
    c = conn.cursor()
    c.execute('drop table if exists MemberWithoutByPass;')
    c.execute('drop table if exists MemberWithoutByPassAndWithoutDiscount;')
    c.execute('create table MemberWithoutByPass as select name from member_array where by_pass = 0 order by arrange_order;')
    c.execute('create table MemberWithoutByPassAndWithoutDiscount as select name from member_array where by_pass = 0 and discount = 0 order by arrange_order;')
    c.execute('delete from ForArrange;')
    c.execute('vacuum;')
    c.execute('insert into ForArrange (name) select name from (select * from MemberWithoutByPass union all select * from MemberWithoutByPassAndWithoutDiscount);')
    conn.commit()
    c.execute('select * from ForArrange')
    listMemberForArrange = c.fetchall()
    return listMemberForArrange

def DisableMember(MC, conn):
    conn.execute('update member_array set by_pass = 1 where ID = ' + str(MC[1]))
    conn.commit()
    return UpdateForArrange(conn)

def SaveToDB(listDaysArray, conn):
    #c = conn.cursor()
    conn.execute('CREATE TABLE if not exists JobHistory (ID STRING PRIMARY KEY, date DATE, JobName STRING, OwnerName STRING);')
    strStartDate = str(listDaysArray[0][0].JobDate.date())
    StrEndDate = str(listDaysArray[len(listDaysArray)-1][0].JobDate.date())
    conn.execute('delete from JobHistory where date >= ? and date <= ?', (strStartDate, StrEndDate))
    for day in listDaysArray:
        for job in day:
            conn.execute('insert into JobHistory values (?,?,?,?)', (str(uuid.uuid4()), str(job.JobDate.date()), job.JobName, job.JobOwner))
    conn.commit()

def CheckIDorName(MC):
    if MC[1]:
        return ['ID', MC[1]]
    else:
        return ['name', MC[4]]

def InsertMember(MC, conn):
    #先檢查member_array中是不是有這個人，如果沒有就加人。如果有但是by_pass等於1，就設定為0。MC = ('日期', ID, 執行的動作代碼, ArrangeOrder, name, by_pass, discount)
    c = conn.cursor()
    IDorName = CheckIDorName(MC)
    c.execute('select * from member_array where ' + str(IDorName[0]) + ' = \'' + str(IDorName[1]) + '\';')
    Member = c.fetchall()
    if len(Member) == 0:
        #取消arrange_order的unique
        conn.execute('ALTER TABLE member_array RENAME TO sqlitestudio_temp_table;')
        conn.commit()
        conn.execute('CREATE TABLE member_array (ID INTEGER NOT NULL PRIMARY KEY, arrange_order INTEGER, name CHAR (255) UNIQUE, by_pass INTEGER, discount INTEGER);')
        conn.commit()
        conn.execute('INSERT INTO member_array (ID, arrange_order, name, by_pass, discount) SELECT ID, arrange_order, name, by_pass, discount FROM sqlitestudio_temp_table;')
        conn.commit()
        conn.execute('DROP TABLE sqlitestudio_temp_table;')
        conn.commit()
        #把某人之後的arrange_order都加1
        c.execute('update member_array set arrange_order = arrange_order + 1 where arrange_order > ' + str(MC[3]-1) + ';')
        #然後插入這個人 (ID, arrange_order, name, by_pass, discount), 而且MC = ('日期', ID, 執行的動作代碼, ArrangeOrder, name, by_pass, discount)
        conn.execute('insert into member_array values (null, ' + str(MC[3]) + ', \'' + str(MC[4]) + '\', ' + str(MC[5]) + ', ' + str(MC[6]) + ');')
        conn.commit()
        #恢復arrange_order的unique
        conn.execute('ALTER TABLE member_array RENAME TO sqlitestudio_temp_table;')
        conn.commit()
        conn.execute('CREATE TABLE member_array (ID INTEGER NOT NULL PRIMARY KEY, arrange_order INTEGER UNIQUE, name CHAR (255) UNIQUE, by_pass INTEGER, discount INTEGER);')
        conn.commit()
        conn.execute('INSERT INTO member_array (ID, arrange_order, name, by_pass, discount) SELECT ID, arrange_order, name, by_pass, discount FROM sqlitestudio_temp_table;')
        conn.commit()
        conn.execute('DROP TABLE sqlitestudio_temp_table;')
        conn.commit()
    else:
        conn.execute('update member_array set by_pass = 0 where ID = ' + str(MC[1]))
        conn.commit()
    return UpdateForArrange(conn)

def DoMemberDiscount(MC, conn):
    #檢查member_array的discount是不是等於1， 如果不是，就設定為1。MC = ('日期', ID, 執行的動作代碼, ArrangeOrder, name, by_pass, discount)
    c = conn.cursor()
    c.execute('select * from member_array where ID = ?', (MC[1],))
    Member = c.fetchone()
    if Member[4] == 0:
        c.execute('update member_array set discount = 1 where ID = ?', (MC[1],))
    return UpdateForArrange(conn)

def DisableMemberDiscount(MC, conn):
    #todo: 檢查member_array的discount是不是等於1，如果是，則設定為0
    c = conn.cursor()
    c.execute('select * from member_array where ID = ?', (MC[1],))
    Member = c.fetchone()
    if Member[4] == 1:
        c.execute('update member_array set discount = 0 where ID = ?', (MC[1],))
    return UpdateForArrange(conn)



