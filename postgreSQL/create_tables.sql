/*
  Creates a role (user) named 'test_user' if it doesn't already exist.
  The role is created with login privileges and a password of 'password'.
  Additionally, the role is granted the ability to create databases.
*/
-- Create the role (user) if it doesn't already exist
DO
$$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'test_user') THEN
        CREATE ROLE test_user WITH LOGIN PASSWORD 'password';
        ALTER ROLE test_user CREATEDB;
    END IF;
END
$$;

-- Grant privileges to the role
GRANT ALL PRIVILEGES ON DATABASE task_manager_db TO test_user;

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  fullname VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE status (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  title VARCHAR(100) NOT NULL,
  description TEXT,
  status_id INTEGER REFERENCES status(id),
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);
