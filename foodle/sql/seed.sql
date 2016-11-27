INSERT INTO users (username, display_name, password_digest, ip_address)
VALUES ('test', 'Emma Roberts', '$2b$12$N/fbLZ21CmeFVH9yHvlZxuqpOTo96698ZKes5jpfGihkNo4M3EEya', '0.0.0.0');

INSERT INTO user_emails (user_id, email)
VALUES (2, 'test@mail.com');

INSERT INTO user_images (user_id, url)
VALUES (1, 'https://static.vidivodo.com/vidivodo-videos/uploads/2016/6/17/7/287D60B81F0DAD36/1466150234gTh61226267-620x410jpg.jpg');

INSERT INTO user_images (user_id, url)
VALUES (2, 'https://images5.alphacoders.com/294/294527.jpg');

INSERT INTO places (name, description, user_id)
VALUES ('McDonalds', 'The worst burger place in the world. Seriously.', 1);

INSERT INTO place_images (place_id, url)
VALUES (1, 'https://pbs.twimg.com/profile_images/658746945565954048/Zrf2h3RD_400x400.jpg');

INSERT INTO places (name, description, user_id)
VALUES ('Burger King', 'You may eat something disgusting like that.', 1);

INSERT INTO place_images (place_id, url)
VALUES (2, 'https://pbs.twimg.com/profile_images/694921357864386563/p0nF8Bj8.jpg');

INSERT INTO places (name, description, user_id)
VALUES ('The House Café', 'Eat & Drink', 1);

INSERT INTO place_images (place_id, url)
VALUES (3, 'https://menumnette.com/uploads/u_2_logo_1472987297_5460.png');

INSERT INTO check_ins (user_id, place_id)
VALUES (2, 1);

INSERT INTO check_ins (user_id, place_id)
VALUES (2, 1);

INSERT INTO user_activations (user_id)
VALUES (2);

INSERT INTO posts (title, body, cost, score, user_id, place_id)
VALUES('Full breakfast including Weisenschaffer ham mould /w butter.', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent mattis ullamcorper libero, a rutrum est feugiat feugiat. Duis facilisis velit porttitor nibh malesuada, a hendrerit eros tristique. Nullam feugiat tempor tortor at cursus. Integer egestas diam augue, quis eleifend orci lobortis ac. Etiam egestas ipsum pulvinar dignissim dignissim. Integer condimentum diam eget mattis fermentum. Cras sit amet elit felis. Duis pellentesque lorem sit amet malesuada finibus. Duis semper quam mauris, ut maximus nibh ornare quis. Sed eget tellus nec nisi pretium facilisis. Phasellus eu mauris eu est efficitur facilisis eu eget odio. Sed pulvinar est rutrum, sodales massa sit amet, aliquet arcu.', 4, 46, 2, 1);

INSERT INTO post_images (post_id, link, ip_addr)
VALUES (1, 'http://www.istanbul7hills.com/images/break.jpg', '0.0.0.0');

INSERT INTO post_likes (post_id, user_id)
VALUES (1,2);

INSERT INTO post_comments (user_id, post_id, body)
VALUES(1, 1, 'First comment for testing did i say that this is the first comment for testing');

INSERT INTO post_comments (user_id, post_id, body)
VALUES(1, 1, 'Another comment for testing for html positions');

INSERT INTO check_in_comments (user_id, check_in_id, body)
VALUES(2, 1, 'First comment for testing did i say that this is the first comment for testing');

INSERT INTO check_in_comments (user_id, check_in_id, body)
VALUES(2, 1, 'Another comment for testing for html positions');

INSERT INTO place_ratings (user_id, place_id, rating)
VALUES(2, 1, 5);

INSERT INTO place_ratings (user_id, place_id, rating)
VALUES(2, 1, 7);

INSERT INTO place_instances (user_id, place_id, name, capacity)
VALUES ('1', '1','Suadiye Mc', '200');
