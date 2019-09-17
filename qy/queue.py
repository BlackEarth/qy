from dataclasses import dataclass, field
from datetime import datetime
from datamodels import Model
from sqly import SQL, Dialects
from sqly.lib import run


@dataclass
class Job(Model):
    TABLE = 'qy_jobs'
    PK = ['id']

    id: int = field(default=None)
    retries: int = field(default=3)
    queued: datetime = field(default=None)
    scheduled: datetime = field(default=None)
    data: dict = field(default_factory=dict)


@dataclass
class Queue(Model):
    dialect: Dialects

    def put(self, data, retries=3, scheduled=None):
        query = SQL(
            """
            INSERT INTO qy_jobs ({fields}) values ({params})
            RETURNING *
            """,
            dialect=self.dialect,
        )
        job = Job(data=data, retries=retries, scheduled=scheduled)
        return query.render(job.dict(nulls=False))

    def get(self):
        query = SQL(
            """
            UPDATE qy_jobs q1 SET retries = retries - 1
            WHERE q1.id = ( 
                SELECT q2.id FROM qy_jobs q2 
                WHERE q2.retries > 0
                AND q2.scheduled <= now()
                ORDER BY q2.created FOR UPDATE SKIP LOCKED LIMIT 1 
            )
            RETURNING q1.*;
            """.rstrip(),
            dialect=self.dialect,
        )
        return str(query)

    def delete(self, job):
        query = SQL(
            """
            DELETE FROM qy_jobs WHERE id=:id
            """.rstrip(),
            dialect=self.dialect,
        )
        return query.render({'id': job.id})
