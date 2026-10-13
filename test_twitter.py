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
# Search by Hashtag Tests

# HAPPY PATH TESTS

def test_search_hashtag_one_post(capsys):
    twitter = Twitter()
    twitter.create_account("dylan", "1234")
    twitter.accounts[0].create_post("Tennis", "I love #tennis")

    twitter.search_hashtag("#tennis")
    captured = capsys.readouterr()

    assert "I love #tennis" in captured.out


def test_search_hashtag_multiple_posts(capsys):
    twitter = Twitter()
    twitter.create_account("dylan", "1234")
    twitter.create_account("alex", "5678")

    twitter.accounts[0].create_post("Match 1", "Playing #tennis")
    twitter.accounts[1].create_post("Match 2", "Watching #tennis")

    twitter.search_hashtag("#tennis")
    captured = capsys.readouterr()

    assert "Playing #tennis" in captured.out
    assert "Watching #tennis" in captured.out


def test_search_hashtag_excludes_other_posts(capsys):
    twitter = Twitter()
    twitter.create_account("dylan", "1234")

    twitter.accounts[0].create_post("Tennis", "I love #tennis")
    twitter.accounts[0].create_post("Soccer", "I love #soccer")

    twitter.search_hashtag("#tennis")
    captured = capsys.readouterr()

    assert "I love #tennis" in captured.out
    assert "I love #soccer" not in captured.out


def test_search_hashtag_in_title(capsys):
    twitter = Twitter()
    twitter.create_account("dylan", "1234")
    twitter.accounts[0].create_post("#tennis", "Great match today")

    twitter.search_hashtag("#tennis")
    captured = capsys.readouterr()

    assert "Great match today" in captured.out


# EDGE CASE TESTS

def test_search_hashtag_no_posts(capsys):
    twitter = Twitter()
    twitter.create_account("dylan", "1234")
    twitter.accounts[0].create_post("Tennis", "I love #tennis")

    twitter.search_hashtag("#soccer")
    captured = capsys.readouterr()

    assert "There are no posts that contain that hashtag" in captured.out
    assert "I love #tennis" not in captured.out


def test_search_hashtag_capitalization(capsys):
    twitter = Twitter()
    twitter.create_account("dylan", "1234")
    twitter.accounts[0].create_post("Tennis", "I love #TENNIS")

    twitter.search_hashtag("#tennis")
    captured = capsys.readouterr()

    assert "I love #TENNIS" in captured.out


def test_search_hashtag_punctuation(capsys):
    twitter = Twitter()
    twitter.create_account("dylan", "1234")
    twitter.accounts[0].create_post("Tennis", "I love #tennis!")

    twitter.search_hashtag("#tennis")
    captured = capsys.readouterr()

    assert "I love #tennis!" in captured.out


def test_search_hashtag_duplicate(capsys):
    twitter = Twitter()
    twitter.create_account("dylan", "1234")
    twitter.accounts[0].create_post("Tennis", "#tennis is great #tennis")

    twitter.search_hashtag("#tennis")
    captured = capsys.readouterr()

    assert captured.out.count("#tennis is great #tennis") == 1


def test_search_hashtag_empty_accounts(capsys):
    twitter = Twitter()

    twitter.search_hashtag("#tennis")
    captured = capsys.readouterr()

    assert "There are no posts that contain that hashtag" in captured.out


def test_search_hashtag_partial_match(capsys):
    twitter = Twitter()
    twitter.create_account("dylan", "1234")
    twitter.accounts[0].create_post("Tennis", "I love #tennisplayer")

    twitter.search_hashtag("#tennis")
    captured = capsys.readouterr()

    assert "I love #tennisplayer" not in captured.out


# INVALID INPUT TESTS

def test_search_hashtag_empty_input(capsys):
    twitter = Twitter()

    twitter.search_hashtag("")
    captured = capsys.readouterr()

    assert "Invalid hashtag" in captured.out


def test_search_hashtag_missing_symbol(capsys):
    twitter = Twitter()

    twitter.search_hashtag("tennis")
    captured = capsys.readouterr()

    assert "Invalid hashtag" in captured.out

# Post checks
def test_post_str():
    p = Post("T", "body", "lucas")
    assert str(p) == "lucas's Post:\nTitle: T\nbody\n"

def test_post_to_dict():
    p = Post("T", "body", "lucas")
    assert p.to_dict() == {"title": "T", "text": "body", "poster": "lucas"}