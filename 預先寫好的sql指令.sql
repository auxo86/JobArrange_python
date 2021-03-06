取消arrange_order的unique

ALTER TABLE member_array RENAME TO sqlitestudio_temp_table;

CREATE TABLE member_array (ID INTEGER NOT NULL PRIMARY KEY, arrange_order INTEGER, name CHAR (255) UNIQUE, by_pass INTEGER, discount INTEGER);

INSERT INTO member_array (ID, arrange_order, name, by_pass, discount) SELECT ID, arrange_order, name, by_pass, discount FROM sqlitestudio_temp_table;

DROP TABLE sqlitestudio_temp_table;
---------------------------------------------------------------------
恢復arrange_order的unique

ALTER TABLE member_array RENAME TO sqlitestudio_temp_table;

CREATE TABLE member_array (ID INTEGER NOT NULL PRIMARY KEY, arrange_order INTEGER UNIQUE, name CHAR (255) UNIQUE, by_pass INTEGER, discount INTEGER);

INSERT INTO member_array (ID, arrange_order, name, by_pass, discount) SELECT ID, arrange_order, name, by_pass, discount FROM sqlitestudio_temp_table;

DROP TABLE sqlitestudio_temp_table;
---------------------------------------------------------------------
把某人之後的arrange_order都加一
update member_array set arrange_order = arrange_order + 1 where arrange_order > 某號
---------------------------------------------------------------------
插人的sql
insert into member_array values (null, 21, 'Robot1', 0, 1);
---------------------------------------------------------------------
產生新的ForArrange
drop table if exists MemberWithoutByPass;
drop table if exists MemberWithoutByPassAndWithoutDiscount;
create table MemberWithoutByPass as select name from member_array where by_pass = 0 order by arrange_order;
create table MemberWithoutByPassAndWithoutDiscount as select name from member_array where by_pass = 0 and discount = 0 order by arrange_order;
delete from ForArrange;
vacuum;
insert into ForArrange (name) select name from (select * from MemberWithoutByPass union all select * from MemberWithoutByPassAndWithoutDiscount);
---------------------------------------------------------------------
產生MemberChange表
CREATE TABLE if not exists MemberChange (date DATETIME NOT NULL, MemberId INTEGER NOT NULL, flagChange INTEGER NOT NULL, ArrangeOrder INTEGER);
---------------------------------------------------------------------
產生JobHistory表
CREATE TABLE if not exists JobHistory (ID STRING PRIMARY KEY, date DATE, JobName STRING, OwnerName STRING);