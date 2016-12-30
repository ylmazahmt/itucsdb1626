Parts Implemented by Buğra Ekuklu
=================================

:User, post and related entities:

Features
********

1. `Home Page`_
2. `Feed`_
3. `Search Bar`_

Home page
*********

The main route will redirect you to feed of the 2nd user. Normally, this
screen will show the feed of the user logged in. However, since we did
not implemented authentication/authorization logic yet, there will be no
login action. Instead, you may checkout pages without logging in with
different credentials.

*This wiki will guide you how to navigate in our website.*

This is the home page. Currently, as it has been said before, it
redirects to the feed of the second user. If it does not exist, it will
bring you back a *404*.

  .. raw:: latex
      \newpage

Creating a new post
-------------------

  .. figure:: member1images/createPost.png
    :scale: 50%
    :alt: Create a new post

Here, we can create a new post. The *'Where did you eat?'* section, which is the first text input of the form, has autocomplete logic built with jQuery UI. For instance, when you type 'Mc' there, it will list you search results which contains that keyword.



  .. figure:: member1images/autocomplete.png
    :scale: 50%
    :alt: AutocompleteDropdown

To create the post properly, you need to select a field from this autocomplete dropdown.

Secondly, you may rate your meal from 0 to 10 inclusively with maximum 1 decimal precision. '5', '7.2' and '10' are sample values.

Thirdly, you should say what did you eat.

At fourth, you need to specify an amount of money. Note that, you should write an integer amount without any currency.

Lastly, you should provide some information about your experience. Neat.

After that, tap 'enter' button in order to create the post. If nothing's happened, you might not have selected the place from the dropdown menu.

You may see the created post after page has been reloaded.

  .. raw:: latex
      \clearpage

User Profile Page
-----------------

  .. figure:: member1images/name.png
    :scale: 50%
    :alt: Name

To go to profile page of a user, you may click his/her name located in
top of a post callout.

  .. figure:: member1images/profile_page.png
    :scale: 50%
    :alt: Profile Page

Here is the profile page of a user.

You may do some actions from the lower-left menu. At the right-hand side, you will see the posts of the user.

If the user hasn't activated yet, you may activate it by clicking 'Activate User'.

Let's do one example.

  .. figure:: member1images/activation.png
    :scale: 50 %
    :alt: Activation Panel

Copy the activation key from the top and paste it to the label. Normally, this key is sent via email. This is not the case, though.

  .. figure:: member1images/input_box_act_key.png
    :scale: 50 %
    :alt: Activation Key

Click 'Activate user' button. It will activate and go back to the
profile page.

  .. figure:: member1images/activation_has_gone.png
    :scale: 50 %
    :alt: Activation has been completed

Notice activation button has gone. This is because user is already
activated.

  .. raw:: latex
    \clearpage

:Editing user:

Let's edit the user. Click the 'Edit User' button at the bottom.

  .. figure:: member1images/profile_card.png
    :scale: 25 %
    :alt: ProfileCard

You will see the enlargened profile card of the user.

You may edit the URL of the users image, label and username by clicking to these labels.

  .. figure:: member1images/edited_user.png
    :scale: 25 %
    :alt: EditedUser

I've edited mine as follows.

You should know that if you write an existing username right there, the whole transaction will rollback. The user image will not be changed.

  *Click save button to persist changes.*

You will get redirected to the edited user. Mine has changed like below.

  .. figure:: member1images/changed_user.png
    :scale: 25%
    :alt: Changed User

  .. raw:: latex
      \clearpage


Feed
****

Editing post
------------

Let's edit some post. At the right side, click to 'Edit post' button of a post. You'll be redirected to a page with a bigger callout.

In this page, you may change the title, cost, score and body. You need to know that the things we said in the beginning of this wiki about cost and score, same thing applies here. Edit the post however you want. I edited it as follows:

  .. figure:: member1images/edited_post.png
    :scale: 25%
    :alt: Edited Post

Click 'Save changes'. It will redirect you to the user profile you came from.

  .. figure:: member1images/changed_post.png
    :scale: 25%
    :alt: Changed Post

Everything works great. The post looks yummy.

  .. raw:: latex
      \clearpage

Deleting post
-------------

Let's delete this post. Click 'Delete post'.

  .. figure:: member1images/no_post.png
    :scale: 50%
    :alt: No post

Boom. Post became deleted. The message, literally, tells us there is no
post of the user. Joke of mine, by the way. Marvellous.

Deleting user
-------------

  .. figure:: member1images/delete_user.png
    :scale: 25 %
    :alt: Delete user

We have nothing to do with the 'Space Guy'. Delete the user anyways. It
will redirect you to users list.

  .. raw:: latex
      \newpage

Search bar
**********

  .. figure:: member1images/search.png
    :scale: 25 %
    :alt: Search

We have a powerful search bar. You may search for 'Sarah Hyland'. She is a great artist. The search bar will search users, places and more by you type. Click to the shown search result.

  .. figure:: member1images/sarah_no_post.png
    :scale: 50%
    :alt: Sarah No Post

She doesn't have a post.
