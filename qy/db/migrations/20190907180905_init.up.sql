-- https://tnishimura.github.io/articles/queues-in-postgresql/

CREATE TABLE qy_jobs (
    id              BIGSERIAL PRIMARY KEY,
    qname           VARCHAR NOT NULL,
    retries         INTEGER NOT NULL DEFAULT 3,
    queued          TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    scheduled       TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    data            JSON NOT NULL DEFAULT '{}'
);
CREATE INDEX qy_jobs_queued ON qy_jobs(queued);
CREATE INDEX qy_jobs_qname ON qy_jobs(qname);
CREATE INDEX qy_jobs_retries ON qy_jobs(retries);
