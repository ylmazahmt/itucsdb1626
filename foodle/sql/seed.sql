INSERT INTO users (username, password_digest, ip_address)
VALUES ('test', '$2b$12$N/fbLZ21CmeFVH9yHvlZxuqpOTo96698ZKes5jpfGihkNo4M3EEya', '0.0.0.0');

INSERT INTO users (username, password_digest, ip_address)
VALUES ('test22', '$s5jpfGihkNo4M3EEya', '0.0.0.0');

INSERT INTO users (username, password_digest, ip_address)
VALUES ('test23', '$2b$123N/fbLZ21CmTo96698ZKes5jpfGihkNo4M3EEya', '0.0.0.0');

INSERT INTO user_emails (user_id, email)
VALUES (2, 'test@mail.com');

INSERT INTO user_images (user_id, data)
VALUES (1, '00000');

INSERT INTO places (name, description, user_id)
VALUES ('McDonalds', 'The worst burger place in the world. Seriously.', 1);

INSERT INTO check_ins (user_id, place_id)
VALUES (1, 1);

INSERT INTO user_activations (user_id)
VALUES (2);

INSERT INTO posts (body, user_id)
VALUES('Great place to eat and spent time', 2);

INSERT INTO post_images (post_id, link)
VALUES (1,'http://www.yukle.tc/galeri/images/7446muz_buyuk.jpg');

INSERT INTO posts (body, user_id)
VALUES('Great place to eat and spent time', 3);

INSERT INTO post_comments (user_id, post_id, body)
VALUES(1,1,'First comment for testing did i say that this is the first comment for testing');

INSERT INTO post_comments (user_id, post_id, body)
VALUES(2,2,'Another comment for testing for html positions');

INSERT INTO users (username, password_digest, ip_address)
VALUES ('gugar', '$2b$12$N/fbLZ21CmeFVH9yHvlZxuqpOTo96698ZKes5jpfGihkNo4M3EEya', '0.0.0.0');

INSERT INTO user_emails (user_id, email)
VALUES (3, 'gugar@mail.com');

INSERT INTO users (username, password_digest, ip_address)
VALUES ('test1', '$2b$12$N/fbLZ21CmeFVH9yHvlZxuqpOTo96698ZKes5jpfGihkNo4M3EEya', '0.0.0.0');

INSERT INTO user_emails (user_id, email)
VALUES (4, 'test1@mail.com');

INSERT INTO users (username, password_digest, ip_address)
VALUES ('test2', '$2b$12$N/fbLZ21CmeFVH9yHvlZxuqpOTo96698ZKes5jpfGihkNo4M3EEya', '0.0.0.0');

INSERT INTO user_emails (user_id, email)
VALUES (5, 'test2@mail.com');

INSERT INTO user_friends(user_id, friend_id, is_friend)
VALUES (1,2,'FALSE');

INSERT INTO user_friends(user_id, friend_id, is_friend)
VALUES (3,2,'TRUE');

INSERT INTO user_friends(user_id, friend_id, is_friend)
VALUES (2,3,'TRUE');

INSERT INTO user_friends(user_id, friend_id, is_friend)
VALUES (4,2,'TRUE');

INSERT INTO user_friends(user_id, friend_id, is_friend)
VALUES (2,4,'TRUE');

INSERT INTO user_friends(user_id, friend_id, is_friend)
VALUES (5,2,'FALSE');

INSERT INTO place_instances (user_id, place_id, name, capacity)
VALUES ('1', '1','Suadiye Mc', '200');
