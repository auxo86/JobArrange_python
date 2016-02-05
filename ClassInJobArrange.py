import datetime

class JobObj:
    def __init__(self, JobDate = datetime.datetime.strptime('2016-01-22', '%Y-%m-%d'), JobName = '兩頭一', JobOwner = '明旭'):
        self.JobDate = JobDate
        self.JobName = JobName
        self.JobOwner = JobOwner