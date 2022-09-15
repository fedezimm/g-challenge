class HiredEmployee(object):
    def __init__(
        self,
        id,
        name,
        datetime,
        department_id,
        job_id
    ):
        self.id = id
        self.name = name
        self.datetime = datetime
        self.department_id = department_id
        self.job_id = job_id