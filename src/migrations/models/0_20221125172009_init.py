from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "applicant" (
    "identifier" UUID NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(255),
    "is_active" BOOL NOT NULL  DEFAULT True
);
CREATE TABLE IF NOT EXISTS "application" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "identifier" UUID NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "flow_name" VARCHAR(128) NOT NULL,
    "applicant_id" UUID REFERENCES "applicant" ("identifier") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_application_identif_421e13" ON "application" ("identifier");
CREATE TABLE IF NOT EXISTS "flow" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "flow_type" VARCHAR(128) NOT NULL,
    "flow_name" VARCHAR(128) NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "applicant_id" UUID REFERENCES "applicant" ("identifier") ON DELETE CASCADE,
    "application_id" INT  UNIQUE REFERENCES "application" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "flow"."flow_type" IS 'MAIN: MAIN\nPUBLIC: PUBLIC';
CREATE TABLE IF NOT EXISTS "step" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "is_first_step" BOOL NOT NULL  DEFAULT False,
    "step" VARCHAR(128) NOT NULL,
    "status" VARCHAR(128),
    "reason" VARCHAR(1024),
    "retry_period" INT NOT NULL  DEFAULT 1800,
    "description" VARCHAR(1024),
    "application_id" INT REFERENCES "application" ("id") ON DELETE CASCADE,
    "flow_id" INT REFERENCES "flow" ("id") ON DELETE CASCADE,
    "next_step_id" INT REFERENCES "step" ("id") ON DELETE CASCADE,
    "next_step_if_error_id" INT REFERENCES "step" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "step"."status" IS 'IN_PROGRESS: IN_PROGRESS\nFINISH: FINISH\nFAILED: FAILED';
COMMENT ON TABLE "step" IS 'retry period: cast to seconds';
CREATE TABLE IF NOT EXISTS "event" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "event" VARCHAR(1024),
    "step_id" INT REFERENCES "step" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
