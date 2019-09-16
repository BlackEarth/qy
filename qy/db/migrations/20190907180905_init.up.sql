-- https://tnishimura.github.io/articles/queues-in-postgresql/

CREATE TABLE qy_jobs (
    id              BIGSERIAL PRIMARY KEY,
    retries         INTEGER NOT NULL DEFAULT 3,
    created         TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    scheduled       TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    data            JSON NOT NULL DEFAULT '{}'
);
CREATE INDEX qy_jobs_created ON qy_jobs(created);
CREATE INDEX qy_jobs_retries ON qy_jobs(retries);
