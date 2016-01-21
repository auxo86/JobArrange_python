import datetime

class JobObj:
    def __init_(self, JobDate, JobName, JobOwner):
        self.JobDate = datetime.date(JobDate)
        self.JobName = JobName
        self.JobOwner = JobOwner


