from . import CURSOR, CONN

class Department:
    all = {}

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS departments;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def __init__(self, name):
        self.id = None
        self.name = name

    def save(self):
        if self.id is None:
            sql = """
                INSERT INTO departments (name)
                VALUES (?)
            """
            CURSOR.execute(sql, (self.name,))
            CONN.commit()
            self.id = CURSOR.lastrowid
            type(self).all[self.id] = self
        else:
            sql = """
                UPDATE departments
                SET name = ?
                WHERE id = ?
            """
            CURSOR.execute(sql, (self.name, self.id))
            CONN.commit()

    @classmethod
    def create(cls, name):
        department = cls(name)
        department.save()
        return department

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM departments
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        if row:
            department = cls(row[1])
            department.id = row[0]
            cls.all[row[0]] = department
            return department
        else:
            return None