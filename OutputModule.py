# -*- coding: utf8 -*-
def PrintJobTable(listDaysArray, listJobsTable):
    #列印頁首
    print(str(listDaysArray[0][0].JobDate.date()) + '~' + str(listDaysArray[len(listDaysArray)-1][0].JobDate.date()) + '的班表')
    print()
    #列印內容
    print(',,', end = '')
    for JobItem in listJobsTable:
        print(JobItem[2] +',', end = '')
    print()

    dictWeekDay = {1:"一", 2:"二", 3:"三", 4:"四", 5:"五", 6:"六", 7:"日"}
    for Day in listDaysArray:
        print(str(Day[0].JobDate.date()) + ',', end = '')
        print(dictWeekDay[Day[0].JobDate.isoweekday()] + ',', end = '')
        for Job in Day:
            print(Job.JobOwner + ',', end = '')
        print()