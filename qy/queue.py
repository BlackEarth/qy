import logging
from datetime import datetime

from pydantic import BaseModel, Field
from sqly.dialect import Dialect

logger = logging.getLogger(__name__)


class Job(BaseModel):
    qname: str = Field()
    id: int = Field(default=None)
    retries: int = Field(default=3)
    queued: datetime = Field(default=None)
    scheduled: datetime = Field(default=None)
    data: dict = Field(default_factory=dict)


class Queue(BaseModel):
    qname: str
    dialect: Dialect

    def __post_init__(self):
        logger.info('Queue initialized: %r' % self)

    def put(self, data, retries=3, scheduled=None):
        job = Job(qname=self.qname, data=data, retries=retries, scheduled=scheduled)
        return self.dialect.render(
            """
            INSERT INTO qy_jobs (qname, retries, scheduled, data) 
            VALUES (:qname, :retries, :scheduled, :data)
            RETURNING *
            """,
            job.dict(),
        )

    def get(self):
        return self.dialect.render(
            """
            UPDATE qy_jobs q1 SET retries = retries - 1
            WHERE q1.id = ( 
                SELECT q2.id FROM qy_jobs q2 
                WHERE q2.qname=:qname
                AND q2.retries > 0
                AND q2.scheduled <= now()
                ORDER BY q2.queued 
                FOR UPDATE SKIP LOCKED LIMIT 1 
            )
            RETURNING q1.*;
            """,
            {'qname': self.qname}
        )

    def delete(self, job):
        return self.dialect.render(
            """
            DELETE FROM qy_jobs WHERE id=:id
            """,
            {'id': job.id},
        )
