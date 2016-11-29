INSERT INTO users (username, display_name, password_digest, ip_address)
VALUES ('test', 'Emma Roberts', '$2b$12$N/fbLZ21CmeFVH9yHvlZxuqpOTo96698ZKes5jpfGihkNo4M3EEya', '0.0.0.0');

INSERT INTO users (username, display_name, password_digest, ip_address)
VALUES ('rossum', 'Emmy Rossum', '$2b$12$N/fbLZ21CmeFVH9yHvlZxuqpOTo96698ZKes5jpfGihkNo4M3EEya', '0.0.0.0');

INSERT INTO users (username, display_name, password_digest, ip_address)
VALUES ('hyland', 'Sarah Hyland', '$2b$12$N/fbLZ21CmeFVH9yHvlZxuqpOTo96698ZKes5jpfGihkNo4M3EEya', '0.0.0.0');

INSERT INTO user_emails (user_id, email)
VALUES (2, 'test@mail.com');

INSERT INTO user_emails (user_id, email)
VALUES (3, 'rossum@blabla.com');

INSERT INTO user_emails (user_id, email)
VALUES (4, 'hyland@blabla.com');

INSERT INTO user_emails (user_id, email)
VALUES (4, 'hyland_new@blabla.com');

INSERT INTO user_images (user_id, url)
VALUES (1, 'https://static.vidivodo.com/vidivodo-videos/uploads/2016/6/17/7/287D60B81F0DAD36/1466150234gTh61226267-620x410jpg.jpg');

INSERT INTO user_images (user_id, url)
VALUES (2, 'https://images5.alphacoders.com/294/294527.jpg');

INSERT INTO user_images (user_id, url)
VALUES (3, 'https://pbs.twimg.com/profile_images/588377578240544769/v39jWDt6.jpg');

INSERT INTO user_images (user_id, url)
VALUES (4, 'http://67.media.tumblr.com/bf99f4153d636e33f5b1243065831c19/tumblr_mvg887oJjq1s88ss5o1_r1_1280.jpg');

INSERT INTO places (name, description, user_id)
VALUES ('McDonalds', 'The worst burger place in the world. Seriously.', 1);

INSERT INTO place_images (place_id, url)
VALUES (1, 'https://pbs.twimg.com/profile_images/658746945565954048/Zrf2h3RD_400x400.jpg');

INSERT INTO places (name, description, user_id)
VALUES ('Burger King', 'You may eat something disgusting like that.', 1);

INSERT INTO place_images (place_id, url)
VALUES (2, 'https://pbs.twimg.com/profile_images/694921357864386563/p0nF8Bj8.jpg');

INSERT INTO places (name, description, user_id)
VALUES ('Good Chinese Guys', 'Eel and stuff to eat.', 1);

INSERT INTO place_images (place_id, url)
VALUES (3, 'http://previews.123rf.com/images/bluezace/bluezace1212/bluezace121200021/16899861-Cartoon-of-Chinese-Boy-Girl-Stock-Vector-chinese-new-year.jpg');

INSERT INTO places (name, description, user_id)
VALUES ('The House Café', 'Eat & Drink', 1);

INSERT INTO place_images (place_id, url)
VALUES (4, 'https://menumnette.com/uploads/u_2_logo_1472987297_5460.png');

INSERT INTO check_ins (user_id, place_id)
VALUES (2, 1);

INSERT INTO check_ins (user_id, place_id)
VALUES (2, 1);

INSERT INTO user_activations (user_id)
VALUES (2);

INSERT INTO posts (title, body, cost, score, user_id, place_id)
VALUES('Full breakfast including Weisenschaffer ham mould /w butter.', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent mattis ullamcorper libero, a rutrum est feugiat feugiat. Duis facilisis velit porttitor nibh malesuada, a hendrerit eros tristique. Nullam feugiat tempor tortor at cursus. Integer egestas diam augue, quis eleifend orci lobortis ac. Etiam egestas ipsum pulvinar dignissim dignissim. Integer condimentum diam eget mattis fermentum. Cras sit amet elit felis. Duis pellentesque lorem sit amet malesuada finibus. Duis semper quam mauris, ut maximus nibh ornare quis. Sed eget tellus nec nisi pretium facilisis. Phasellus eu mauris eu est efficitur facilisis eu eget odio. Sed pulvinar est rutrum, sodales massa sit amet, aliquet arcu.', 4, 46, 2, 1);

INSERT INTO posts (title, body, cost, score, user_id, place_id)
VALUES('Peking duck /w orange dressing.', 'The duck was good flavored, melted, listened, spawned, killed and died at all. Forcefully I injected a ReactJS state container, since I hate the Flux and setState things. Redux was doing great, however, you know you are doing a component-based design, the state manipulation did not work well for me since I am using these stuff also in older browsers. Good if you are not working with that, though. I would go with either Angular 2 or Backbone b2w, yet I see Angulars MVC design is anti-paradigm.', 12, 76, 3, 3);

INSERT INTO post_images (post_id, link, ip_addr)
VALUES (1, 'http://www.istanbul7hills.com/images/break.jpg', '0.0.0.0');

INSERT INTO post_images (post_id, link, ip_addr)
VALUES (2, 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Peking_Duck_3.jpg/520px-Peking_Duck_3.jpg', '0.0.0.0');

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

INSERT INTO chat_rooms (user_id, name)
VALUES('1','Desert Chat');

INSERT INTO chat_room_messages (user_id, chat_room_id, body)
VALUES('1','1','Hi there this is a test message to see something on the screen, work hard play harder');
