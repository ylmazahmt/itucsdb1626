Parts Implemented by Buğra Ekuklu
================================

User, post and related entities

Throughout the tutorial, you may initialize the database by clicking the
button.

The main route will redirect you to feed of the 2nd user. Normally, this
screen will show the feed of the user logged in. However, since we did
not implemented authentication/authorization logic yet, there will be no
login action. Instead, you may checkout pages without logging in with
different credentials.

This wiki will guide you how to navigate in our website.

This is the home page. Currently, as it has been said before, it
redirects to the feed of the second user. If it does not exist, it will
bring you back a 404.

|Create Post| Here, we can create a new post. The 'Where did you eat?'
section, which is the first text input of the form, has autocomplete
logic built with jQuery UI. For instance, when you type 'Mc' there, it
will list you search results which contains that keyword.

.. figure:: https://github.com/itucsdb1626/itucsdb1626/raw/master/docs/img/chatatata-wiki/autocomplete.png
   :alt: AutocompleteDropdown

   AutocompleteDropdown
To create the post properly, you need to select a field from this
autocomplete dropdown.

Secondly, you may rate your meal from 0 to 10 inclusively with maximum 1
decimal precision. '5', '7.2' and '10' are examplery values.

Thirdly, you should say what did you eat.

At fourth, you need to specify an amount of money. Note that, you should
write an integer amount without any currency.

Lastly, you should provide some information about your experience. Neat.

After that, tap 'enter' button in order to create the post. If nothing's
happened, you might not have selected the place from the dropdown menu.

You may see the created post after page has been reloaded.

You may like your post by clicking like button. If you liked it before,
it will highlight and in case of click, it will delike.

Sadly, comment and share functions are not implemented yet.

.. figure:: https://github.com/itucsdb1626/itucsdb1626/raw/master/docs/img/chatatata-wiki/name.png
   :alt: Name

   Name
To go to profile page of a user, you may click his/her name located in
top of a post callout.

.. figure:: https://github.com/itucsdb1626/itucsdb1626/raw/master/docs/img/chatatata-wiki/profile_page.png
   :alt: Profile Page

   Profile Page
Here is the profile page of a user.

You may do some actions from the lower-left menu. At the right-hand
side, you will see the posts of the user.

If the user hasn't activated yet, you may activate it by clicking
'Activate User'.

Let's do one example.

.. figure:: https://github.com/itucsdb1626/itucsdb1626/raw/master/docs/img/chatatata-wiki/activation.png
   :alt: Activate

   Activate
Copy the activation key from the top and paste it to the label.
Normally, this key is sent via email. This is not the case, though.

.. figure:: https://github.com/itucsdb1626/itucsdb1626/raw/master/docs/img/chatatata-wiki/input_box_act_key.png
   :alt: ACtKey

   ACtKey
Click 'Activate user' button. It will activate and go back to the
profile page.

.. figure:: https://github.com/itucsdb1626/itucsdb1626/raw/master/docs/img/chatatata-wiki/activation_has_gone.png
   :alt: acthasgone

   acthasgone
Notice activation button has gone. This is because user is already
activated.

--------------

Editing user
~~~~~~~~~~~~

Let's edit the user. Click the 'Edit User' button at the bottom.

.. figure:: https://github.com/itucsdb1626/itucsdb1626/raw/master/docs/img/chatatata-wiki/profile_card.png
   :alt: ProfileCard

   ProfileCard
You will see the enlargened profile card of the user.

You may edit the URL of the users image, label and username by clicking
to these labels.

.. figure:: https://github.com/itucsdb1626/itucsdb1626/raw/master/docs/img/chatatata-wiki/edited_user.png
   :alt: EditedUser

   EditedUser
I've edited mine as follows.

You should know that if you write an existing username right there, the
whole transaction will rollback. The user image will not be changed.

Click save button to persist changes.

You will get redirected to the edited user. Mine has changed like below.
|Changed user|

--------------

Editing post
~~~~~~~~~~~~

Let's edit some post. At the right side, click to 'Edit post' button of
a post. You'll be redirected to a page with a bigger callout.

In this page, you may change the title, cost, score and body. You need
to know that the things we said in the beginning of this wiki about cost
and score, same thing applies here. Edit the post however you want. I
edited it as follows:

.. figure:: https://github.com/itucsdb1626/itucsdb1626/raw/master/docs/img/chatatata-wiki/edited_post.png
   :alt: Edited Post

   Edited Post
Click 'Save changes'. It will redirect you to the user profile you came
from.

.. figure:: https://github.com/itucsdb1626/itucsdb1626/raw/master/docs/img/chatatata-wiki/changed_post.png
   :alt: Changed Post

   Changed Post
Everything works great. The post looks yummy.

Let's delete this post. Click 'Delete post'.

.. figure:: https://github.com/itucsdb1626/itucsdb1626/raw/master/docs/img/chatatata-wiki/no_post.png
   :alt: No post

   No post
Boom. Post became deleted. The message, literally, tells us there is no
post of the user. Joke of mine, by the way. Marvellous.

.. figure:: https://github.com/itucsdb1626/itucsdb1626/raw/master/docs/img/chatatata-wiki/delete_user.png
   :alt: Delete user

   Delete user
We have nothing to do with the 'Space Guy'. Delete the user anyways. It
will redirect you to users list.

--------------

Search bar
~~~~~~~~~~

.. figure:: https://github.com/itucsdb1626/itucsdb1626/raw/master/docs/img/chatatata-wiki/search.png
   :alt: Search

   Search
We have a powerful search bar. You may search for 'Sarah Hyland'. She is
a great artist. The search bar will search users, places and more by you
type. Click to the shown search result.

.. figure:: https://github.com/itucsdb1626/itucsdb1626/raw/master/docs/img/chatatata-wiki/sarah_no_post.png
   :alt: Sarah No Post

   Sarah No Post
She doesn't have a post.

Let's go to the feed. She's more like reader than writer.

Emma has posted something there. Like it. |Like|

Oops, we remembered we're unlawful with Emma. Let's unlike this swiftly.
Click to like button again. |Unlike|

And initialize the database at the end. |Initialize DB|

That's all. Thank you.

Buğra Ekuklu

.. |Create Post| image:: https://github.com/itucsdb1626/itucsdb1626/raw/master/docs/img/chatatata-wiki/createPost.png
.. |Changed user| image:: https://github.com/itucsdb1626/itucsdb1626/raw/master/docs/img/chatatata-wiki/changed_user.png
.. |Like| image:: https://github.com/itucsdb1626/itucsdb1626/raw/master/docs/img/chatatata-wiki/like.png
.. |Unlike| image:: https://github.com/itucsdb1626/itucsdb1626/raw/master/docs/img/chatatata-wiki/like_un.png
.. |Initialize DB| image:: https://github.com/itucsdb1626/itucsdb1626/raw/master/docs/img/chatatata-wiki/initialize_db.png
