from post import Post

class NoTitledPostError(Exception):
    pass

class Account:
    def __init__(self, username, password, posts=None, following=None):
        self.username = username
        self.password = password

        if posts is None:
            self.posts = []
        else:
            self.posts = posts

        if following is None:
            self.following = []
        else:
            self.following = following

    def create_post(self, title, text):
        post = Post(title, text)
        self.posts.append(post)

    def delete_post(self, title):
        for post in self.posts:
            if title == post.title:
                self.posts.remove(post)
                return
        raise NoTitledPostError(f"No post titled '{title}'")

            
