from post import Post

# Custom Exceptions
class SameTitleError(Exception):
    pass

class NoTitledPostError(Exception):
    pass

class Account:

    # Constructor
    def __init__(self, username, password, posts=None, following=None):
        self.username = username
        self.password = password

        # So when you deserialize it will have all of the posts and followed accounts saved but if it is a new account everything is blank
        if posts is None:
            self.posts = []
        else:
            self.posts = posts

        if following is None:
            self.following = []
        else:
            self.following = following

    def create_post(self, title, text):
        # Checks to make sure there isn't another post with the same title
        for post in self.posts:
            if title == post.title:
                raise SameTitleError(f"Already a post titled '{title}'")

        # Creates the post and adds the post to all of the account's posts
        post = Post(title, text)
        self.posts.append(post)

    def delete_post(self, title):
        # Goes through all the account's posts and checks for the exact title to delete
        for post in self.posts:
            if title == post.title:
                self.posts.remove(post)
                return

        # If not that exact title will throw an error
        raise NoTitledPostError(f"No post titled '{title}'")

            
