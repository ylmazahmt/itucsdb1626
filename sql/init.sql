
--  Drop cascade the `main` schema
DROP SCHEMA main CASCADE;

--  Reinitialize a schema with name `main`
CREATE SCHEMA main;

--  Recall `uuid-ossp` extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

--  Create `users` table
CREATE TABLE users(
    id serial PRIMARY KEY,
    username character varying(255) UNIQUE NOT NULL,
    password_digest character varying(255) NOT NULL,
    email character varying(255) UNIQUE NOT NULL,
    activation_key uuid DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    inserted_at timestamp DEFAULT now() NOT NULL
);

--  Create `user_activations` table
CREATE TABLE user_activations(
    user_id integer PRIMARY KEY,
    inserted_at timestamp DEFAULT now() NOT NULL,
    FOREIGN KEY ("user_id") REFERENCES users(id)
);

--  Create `user_images` table
CREATE TABLE user_images(
    user_id integer PRIMARY KEY,
    data bytea NOT NULL,
    inserted_at timestamp DEFAULT now() NOT NULL,
    FOREIGN KEY ("user_id") REFERENCES users(id)
);

-- Create `places` table
CREATE TABLE places(
    id serial PRIMARY KEY,
    name character varying(255) UNIQUE NOT NULL,
    description text NOT NULL,
    user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    inserted_at timestamp DEFAULT now() NOT NULL
);

-- Create `places.user_id` index

CREATE INDEX places_user_id_idx ON places(user_id);
