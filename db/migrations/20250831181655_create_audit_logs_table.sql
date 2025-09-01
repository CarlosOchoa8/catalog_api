-- migrate:up
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    action_performed varchar(20) NOT NULL,
    affected_module varchar(100) NOT NULL,
    ip_address varchar(50) NOT NULL,
    user_agent varchar(255) NOT NULL,

    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    CONSTRAINT fk_user_id FOREIGN KEY(user_id) REFERENCES "users"(id) ON DELETE CASCADE
);

-- migrate:down
DROP TABLE IF EXISTS audit_logs;
