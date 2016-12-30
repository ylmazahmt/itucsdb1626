Parts Implemented by Ahmet Yılmaz
================================

This documentation aims to guide user through simple application features and how to use them

In this application I implemented three features which have their own entities:

Features
********

1. `Friendship Relations`_
2. `Check-In Comments`_
3. `Place Ratings`_

Friendship Relations
********************

Index Page
----------

    .. figure:: /docs/img/ylmazahmt-doc/Friends-Index.png
        :scale: 125 %
        :alt: friends_index_page
        :align: center

        **Friends Index Page**


* Friends Page: This page is the index page for the friends, friend requests etc... In order to access this page you can click friend hyperlink in any user page. (7)

* 'Remove Friend' button under user card removes this user from friends of owner. (4)

* In this page also previously sent friend requests from owner to other users can be seen in the bottom of the page. (6)

* 'Cancel Friend Request' button remove previosly sent friend request from database. (5)

* 'Add New Friend' button in index page directs into a page where a total strangers for session owners listed. (2)

* Pending friend requests can be accessed through clicking to button "go to friend requests" in index page. (1)

* A search bar place in index page used for searching in currently friends or previously sent friend requests. (3)


Add New Friend Page
-------------------

    .. figure:: /docs/img/ylmazahmt-doc/new_friend.png
        :scale: 100 %
        :alt: new_friend_page
        :align: center

        **New Friend Page**
* total strangers for session owners listed. (1)

* 'Send Friend Request' button in user cards sends a friend request to related user from current session owner. Afterwards the friend request just sent is listed in the index page in sent friend requests page. (2)

Pending Requests Page
--------------------

    .. figure:: /docs/img/ylmazahmt-doc/friend_requests.png
        :scale: 100 %
        :alt: pending_requests_page
        :align: center

        **Friend Requests Page**

* Friend Requests page lists the friend requests that has been received by owner from other users. (1)

* 'Accept Friend Request' button accepts received friend request by th user shown in user card. Afterwards new friend listed int friends page. (2)

Search Bar
----------

    .. figure:: /docs/img/ylmazahmt-doc/search_bar.png
        :scale: 100 %
        :alt: search_page
        :align: center

        **Search Feature**

* An example for keyword "emm" used for search seen above. (1)

* Found users listed. (2)


Check-In Comments
*****************

Index Page
----------

    .. figure:: /docs/img/ylmazahmt-doc/check_in_comments_index.png
        :scale: 125 %
        :alt: check_in_comments_index_page
        :align: center

        **Index Page**


* 'Add New Comment' Button goes into new comment page. (1)
* 'Delete' button deletes comment from database. (2)
* Comment Content also a hyperlink which directs into show page. (3)
* All available check-in comments in database listed here.


New Comment Page
-------------------

    .. figure:: /docs/img/ylmazahmt-doc/check_in_comments_new.png
        :scale: 100 %
        :alt: new_comment_page
        :align: center

        **New Page**
* New comment box. (5)
* Comment Content goes here. (1)
* Select Box for user to comment as. (2)
* Select Box for check-ins to comment at. (3)
* 'Add Comment' button adds comment to database. (4)

Show Page
--------------------

    .. figure:: /docs/img/ylmazahmt-doc/check_in_comments_show.png
        :scale: 100 %
        :alt: check_in_comments_show_page
        :align: center

        **Show Page**

* Comment content shown. (1)
* 'Edit' button directs to edit page for comment. (2)
Edit Page
----------

    .. figure:: /docs/img/ylmazahmt-doc/check_in_comments_edit.png
        :scale: 100 %
        :alt: check_in_comments_edit_page
        :align: center

        **Edit Page**

* New comment content to for changing old one. (1)

* 'Submit Changes' button submit changes to database. (2)

Place Ratings
*************

Index Page
----------

    .. figure:: /docs/img/ylmazahmt-doc/place_ratings_index.png
        :scale: 125 %
        :alt: place_ratings_index_page
        :align: center

        **Index Page**


* 'Add New rating' Button goes into new rating page. (1)
* 'Delete' button deletes rating from database. (2)
* Rating value is  also a hyperlink which directs into show page. (3)
* All available place ratings in database listed here.


New Rating Page
-------------------

    .. figure:: /docs/img/ylmazahmt-doc/place_ratings_new.png
        :scale: 100 %
        :alt: new_rating_page
        :align: center

        **New Page**
* New rating box. (5)
* Rating vale selected from selection box as 1-10. (1)
* Select Box for user to rate as. (2)
* Select Box for places to rate at. (3)
* 'Add Rating' button adds rating to database. (4)

Show Page
--------------------

    .. figure:: /docs/img/ylmazahmt-doc/place_ratings_show.png
        :scale: 100 %
        :alt: place_ratings_show_page
        :align: center

        **Show Page**

* Rating value shown. (1)
* 'Edit' button directs to edit page for rating. (2)

Edit Page
----------

    .. figure:: /docs/img/ylmazahmt-doc/place_ratings_edit.png
        :scale: 100 %
        :alt: place_ratings_edit_page
        :align: center

        **Edit Page**

* New rating value selected through selection box as 1-10. (1)

* 'Submit Changes' button submit changes to database. (2)

