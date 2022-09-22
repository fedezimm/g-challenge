class DepartmentJobQuarterCount(object):
    def __init__(self, department, job, q1, q2, q3, q4):
        self.department = department
        self.job = job
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3
        self.q4 = q4
    
class DepartmentJobQuarterCountRepository(object):
    def __init__(self, db_sink):
        self.db_sink = db_sink

    def list(self):
        query = """
            WITH t1 as
            (SELECT a.department, a.job, hired_quarter = 1 AS q1, hired_quarter = 2 AS q2, hired_quarter = 3 AS q3, hired_quarter = 4 AS q4
             FROM (SELECT d.department, j.job, QUARTER(datetime) AS hired_quarter
                   FROM hired_employees he
                        INNER JOIN jobs j ON he.job_id = j.id
                        INNER JOIN departments d ON he.department_id = d.id
                   WHERE YEAR(datetime) = 2021) AS a)
            SELECT department, job, sum(q1) AS q1, sum(q2) AS q2, sum(q3) AS q3, sum(q4) AS q4
            FROM t1
            GROUP BY department, job
            ORDER BY department, job
        """
        objects = self.db_sink.query(query)
        results = []

        for row in objects:
            obj = DepartmentJobQuarterCount(
                department = str(row.department),
                job = str(row.job),
                q1 = int(row.q1),
                q2 = int(row.q2),
                q3 = int(row.q3),
                q4 = int(row.q4)
            )
            results.append(obj)
        
        return results
