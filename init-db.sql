-- Initialize Hosting Panel Database
-- This script runs when the PostgreSQL container starts for the first time

-- Create extensions if they don't exist
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create additional schemas if needed
CREATE SCHEMA IF NOT EXISTS hosting_panel;

-- Set search path
SET search_path TO hosting_panel, public;

-- Create tables (these will be created by SQLAlchemy, but we can add any custom setup here)
-- The application will handle table creation through Alembic migrations

-- Grant permissions
GRANT ALL PRIVILEGES ON SCHEMA hosting_panel TO hosting_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA hosting_panel TO hosting_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA hosting_panel TO hosting_user;

-- Set default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA hosting_panel GRANT ALL ON TABLES TO hosting_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA hosting_panel GRANT ALL ON SEQUENCES TO hosting_user;
