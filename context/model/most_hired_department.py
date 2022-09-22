class MostHiredDepartment(object):
    def __init__(self, department_id, department_name, hired):
        self.department_id = department_id
        self.department_name = department_name
        self.hired = hired
    
class MostHiredDepartmentRepository(object):
    def __init__(self, db_sink):
        self.db_sink = db_sink

    def list(self):
        query = """
            WITH base AS
            (SELECT d.id, d.department, count(*) AS hired
             FROM hired_employees he
                  INNER JOIN departments d ON d.id = he.department_id
             WHERE YEAR(datetime) = 2021
             GROUP BY d.id, d.department),
            m AS
            (SELECT AVG(hired) AS mean
             FROM base)
            SELECT id, department, hired
            FROM base
            WHERE hired > (SELECT mean FROM m)
            ORDER BY hired DESC
        """
        objects = self.db_sink.query(query)
        results = []

        for row in objects:
            obj = MostHiredDepartment(
                department_id = int(row.id),
                department_name = str(row.department),
                hired = int(row.hired)
            )
            results.append(obj)
        
        return results
