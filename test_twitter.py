import pytest
from twitter import Twitter, SameUsernameError, LoginError
from account import Account, SameTitleError, NoTitledPostError, AlreadyFollowingError, SelfFollowError
from post import Post


# Gives each test Twitter with two accounts already created
@pytest.fixture
def twitter():
    t = Twitter()
    t.create_account("lucas", "pass1")
    t.create_account("dylan", "pass2")
    return t


# check_username checks
def test_check_username_available(twitter):
    # A new username should not raise anything
    twitter.check_username("riley")

def test_check_username_taken(twitter):
    with pytest.raises(SameUsernameError):
        twitter.check_username("lucas")

def test_check_username_case_sensitive(twitter):
    # Lucas should be different than lucas
    twitter.check_username("Lucas")


# create_account checks
def test_create_account_adds_account():
    t = Twitter()
    t.create_account("riley", "pw")
    assert len(t.accounts) == 1
    assert t.accounts[0].username == "riley"
    assert t.accounts[0].password == "pw"

def test_create_account_starts_empty():
    t = Twitter()
    t.create_account("riley", "pw")
    assert t.accounts[0].posts == []
    assert t.accounts[0].following == []


# login checks
def test_login_success(twitter):
    account = twitter.login("lucas", "pass1")
    assert account.username == "lucas"

def test_login_returns_same_object(twitter):
    # login must return the stored account, not a copy
    assert twitter.login("lucas", "pass1") is twitter.accounts[0]

def test_login_wrong_password(twitter):
    with pytest.raises(LoginError):
        twitter.login("lucas", "wrong")

def test_login_unknown_user(twitter):
    with pytest.raises(LoginError):
        twitter.login("nobody", "pass1")

def test_login_other_users_password(twitter):
    with pytest.raises(LoginError):
        twitter.login("lucas", "pass2")

# show_feed checks
# capsys captures what gets printed so it can be checked
def test_show_feed_not_following(twitter, capsys):
    alice = twitter.login("lucas", "pass1")
    twitter.show_feed(alice)
    output = capsys.readouterr().out
    assert "You haven't followed anyone" in output

def test_show_feed_shows_followed_posts(twitter, capsys):
    lucas = twitter.login("lucas", "pass1")
    dylan = twitter.login("dylan", "pass2")
    dylan.create_post("Hello", "First post")
    lucas.follow(dylan)

    twitter.show_feed(lucas)
    output = capsys.readouterr().out
    assert "dylan's Post:" in output
    assert "Title: Hello" in output
    assert "First post" in output

def test_show_feed_excludes_own_posts(twitter, capsys):
    lucas = twitter.login("lucas", "pass1")
    dylan = twitter.login("dylan", "pass2")
    lucas.create_post("Mine", "Should not appear")
    lucas.follow(dylan)

    twitter.show_feed(lucas)
    output = capsys.readouterr().out
    assert "Should not appear" not in output

def test_show_feed_sees_new_posts_after_follow(twitter, capsys):
    lucas = twitter.login("lucas", "pass1")
    dylan = twitter.login("dylan", "pass2")
    lucas.follow(dylan)
    dylan.create_post("Later", "Posted after the follow")

    twitter.show_feed(lucas)
    assert "Posted after the follow" in capsys.readouterr().out


# follow_account checks
def test_follow_account_success(twitter, capsys):
    lucas = twitter.login("lucas", "pass1")
    twitter.follow_account(lucas, "dylan")
    assert lucas.following == [twitter.accounts[1]]
    assert "Successfully followed dylan" in capsys.readouterr().out

def test_follow_account_not_found(twitter, capsys):
    lucas = twitter.login("lucas", "pass1")
    twitter.follow_account(lucas, "nobody")
    assert lucas.following == []
    assert "Account not found" in capsys.readouterr().out

def test_follow_account_twice(twitter):
    lucas = twitter.login("lucas", "pass1")
    twitter.follow_account(lucas, "dylan")
    with pytest.raises(AlreadyFollowingError):
        twitter.follow_account(lucas, "dylan")

def test_follow_account_self(twitter):
    lucas = twitter.login("lucas", "pass1")
    with pytest.raises(SelfFollowError):
        twitter.follow_account(lucas, "lucas")
    assert lucas.following == []


# Account post checks
def test_create_post():
    lucas = Account("lucas", "pw")
    lucas.create_post("T", "body")
    assert len(lucas.posts) == 1
    assert lucas.posts[0].title == "T"
    assert lucas.posts[0].poster == "lucas"

def test_create_post_same_title():
    lucas = Account("lucas", "pw")
    lucas.create_post("T", "one")
    with pytest.raises(SameTitleError):
        lucas.create_post("T", "two")
    assert len(lucas.posts) == 1

def test_delete_post():
    lucas = Account("lucas", "pw")
    lucas.create_post("T", "body")
    lucas.delete_post("T")
    assert lucas.posts == []

def test_delete_missing_post():
    lucas = Account("lucas", "pw")
    with pytest.raises(NoTitledPostError):
        lucas.delete_post("nope")


# Post checks
def test_post_str():
    p = Post("T", "body", "lucas")
    assert str(p) == "lucas's Post:\nTitle: T\nbody\n"

def test_post_to_dict():
    p = Post("T", "body", "lucas")
    assert p.to_dict() == {"title": "T", "text": "body", "poster": "lucas"}