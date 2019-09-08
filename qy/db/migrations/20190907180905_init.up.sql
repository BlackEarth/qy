-- https://tnishimura.github.io/articles/queues-in-postgresql/

CREATE TABLE qy_queue (
    id              BIGSERIAL PRIMARY KEY,
    retries         INTEGER NOT NULL DEFAULT 3,
    created         TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    scheduled       TIMESTAMPTZ NOT NULL DEFAULT current_timestamp,
    data            JSON NOT NULL DEFAULT '{}'
);
CREATE INDEX qy_queue_created ON qy_queue(created);
CREATE INDEX qy_queue_retries ON qy_queue(retries);
