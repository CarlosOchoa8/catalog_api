-- migrate:up
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(50) NOT NULL UNIQUE,
    price DECIMAL(12,4) NOT NULL,
    brand VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- migrate:down
DROP TABLE IF EXISTS products;
