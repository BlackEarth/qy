from dataclasses import dataclass, field
from datetime import datetime
from datamodels import Model
from sqly import SQL, Dialects
from sqly.lib import run


@dataclass
class Job(Model):
    PK = ['id']

    id: int = field(default=None)
    retries: int = field(default=3)
    created: datetime = field(default=None)
    scheduled: datetime = field(default=None)
    data: dict = field(default_factory=dict)


@dataclass
class Queue(Model):
    dialect: Dialects

    def put(self, conn, job):
        query = SQL(
            """
            INSERT INTO qy_queue ({fields}) values ({params})
            RETURNING *
            """,
            dialect=self.dialect,
        )
        sql, values = query.render({k: v for k, v in job.items() if v})
        row = run(conn.fetchrow(sql, *values))
        return Job.from_data(row)

    def get(self, conn):
        query = SQL(
            """
            UPDATE qy_queue q1 SET retries = retries - 1
            WHERE q1.id = ( 
                SELECT q2.id FROM qy_queue q2 
                WHERE q2.retries > 0
                AND q2.scheduled <= now()
                ORDER BY q2.created FOR UPDATE SKIP LOCKED LIMIT 1 
            )
            RETURNING q1.*;
            """.rstrip(),
            dialect=self.dialect,
        )
        sql = str(query)
        row = run(conn.fetchrow(sql))
        return Job.from_data(row)

    def delete(self, conn, job):
        query = SQL(
            """
            DELETE FROM qy_queue WHERE id=:id
            """.rstrip(),
            dialect=self.dialect,
        )
        sql, values = query.render({'id': job.id})
        run(conn.execute(sql, *values))
