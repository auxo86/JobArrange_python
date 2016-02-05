# -*- coding: utf8 -*-
import sqlite3

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


