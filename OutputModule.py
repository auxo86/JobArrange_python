# -*- coding: utf8 -*-
def PrintJobTable(listDaysArray, listJobsTable):
    file = open(str(listDaysArray[0][0].JobDate.date()) + '~' + str(listDaysArray[len(listDaysArray)-1][0].JobDate.date()) + '的班表.html', 'w', encoding = 'UTF-8')
    #列印頁首
    file.write('<html>\n')
    file.write('<head>\n')
    file.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n')
    file.write('<title>' + str(listDaysArray[0][0].JobDate.date()) + '~' + str(listDaysArray[len(listDaysArray)-1][0].JobDate.date()) + '的班表' + '</title>\n')
    file.write('</head>\n')
    file.write('<body>\n')
    #列印內容
    file.write('<font size = "5" color = "blue" align = "left">' + str(listDaysArray[0][0].JobDate.date()) + '~' + str(listDaysArray[len(listDaysArray)-1][0].JobDate.date()) + '的班表' + '</font>\n')
    file.write('<table border="1" cellspacing="0" cellpadding ="5">\n')
    #列印班別
    file.write('<tr>' + '<th>日期</th><th>班別</th>')
    for JobItem in listJobsTable:
        file.write('<th>' + JobItem[2] +'</th>')
    file.write('</tr>\n\n')
    dictWeekDay = {1:"一", 2:"二", 3:"三", 4:"四", 5:"五", 6:"六", 7:"日"}
    for Day in listDaysArray:
        file.write('<tr><th>'+str(Day[0].JobDate.date()) + '</th>')
        file.write('<th>'+dictWeekDay[Day[0].JobDate.isoweekday()] + '</th>')
        for Job in Day:
            file.write('<td>'+Job.JobOwner + '</td>')
        file.write('</tr>\n')
    file.write('</body>\n')
    file.write('</html>')

#def PrintJobTable(listDaysArray, listJobsTable):
#    #列印頁首
#    print(str(listDaysArray[0][0].JobDate.date()) + '~' + str(listDaysArray[len(listDaysArray)-1][0].JobDate.date()) + '的班表')
#    print()
#    #列印內容
#    print(',,', end = '')
#    for JobItem in listJobsTable:
#        print(JobItem[2] +',', end = '')
#    print()

#    dictWeekDay = {1:"一", 2:"二", 3:"三", 4:"四", 5:"五", 6:"六", 7:"日"}
#    for Day in listDaysArray:
#        print(str(Day[0].JobDate.date()) + ',', end = '')
#        print(dictWeekDay[Day[0].JobDate.isoweekday()] + ',', end = '')
#        for Job in Day:
#            print(Job.JobOwner + ',', end = '')
#        print()