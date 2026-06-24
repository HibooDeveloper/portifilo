-- Portfolio Database Initialization
-- Run automatically by MySQL Docker container on first start

CREATE DATABASE IF NOT EXISTS portfolio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE portfolio_db;

-- Grant privileges
GRANT ALL PRIVILEGES ON portfolio_db.* TO 'portfolio_user'@'%';
FLUSH PRIVILEGES;
