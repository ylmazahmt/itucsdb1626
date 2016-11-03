
--  Drop cascade all tables
DROP TABLE IF EXISTS users, user_emails, user_activations, user_images, places, posts, user_friends, check_ins, place_instances   CASCADE;

--  Recall `uuid-ossp` extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

--  Create `users` table
CREATE TABLE users(
    id serial PRIMARY KEY,
    username character varying(255) UNIQUE NOT NULL,
    password_digest character varying(255) NOT NULL,
    activation_key uuid DEFAULT "public".uuid_generate_v4() UNIQUE NOT NULL,
    ip_address inet NOT NULL,
    inserted_at timestamp DEFAULT now() NOT NULL
);

--  Create `user_emails` table
CREATE TABLE user_emails(
    id serial PRIMARY KEY,
    user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    email character varying(40) NOT NULL,
    inserted_at timestamp DEFAULT now() NOT NULL
);

--  Create indexes for the `user_emails` table
CREATE INDEX user_emails_user_id_idx ON user_emails(user_id);
CREATE INDEX user_emails_email_idx ON user_emails(email);

--  Create `user_activations` table
CREATE TABLE user_activations(
    user_id integer PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    inserted_at timestamp DEFAULT now() NOT NULL
);

--  Create `user_images` table
CREATE TABLE user_images(
    user_id integer PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    data bytea NOT NULL,
    inserted_at timestamp DEFAULT now() NOT NULL
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

-- Create `posts` table
CREATE TABLE posts(
  id serial PRIMARY KEY,
  body text NOT NULL,
  user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
  inserted_at timestamp DEFAULT now() NOT NULL
);

-- Create 'user_friends' table
CREATE TABLE user_friends(
    id serial PRIMARY KEY,
    user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    friend_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    is_friend boolean NOT NULL
);

--  Create `check_ins` table
CREATE TABLE check_ins(
    id serial PRIMARY KEY,
    user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    place_id integer NOT NULL REFERENCES places(id) ON DELETE CASCADE ON UPDATE CASCADE,
    inserted_at timestamp DEFAULT now() NOT NULL
);

--  Create `place_instances` table
CREATE TABLE place_instances(
    id serial PRIMARY KEY,
    user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE,
    place_id integer NOT NULL REFERENCES places(id) ON DELETE CASCADE ON UPDATE CASCADE,
    name character varying(255) UNIQUE NOT NULL,
    capacity character varying(255) NOT NULL,
    inserted_at timestamp DEFAULT now() NOT NULL
);

CREATE INDEX check_ins_user_id_idx ON check_ins(user_id);
CREATE INDEX check_ins_place_id_idx ON check_ins(place_id);
