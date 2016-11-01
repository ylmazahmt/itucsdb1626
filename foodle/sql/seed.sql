INSERT INTO users (username, password_digest)
VALUES ('test', '$2b$12$N/fbLZ21CmeFVH9yHvlZxuqpOTo96698ZKes5jpfGihkNo4M3EEya');

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
