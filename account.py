from post import Post

class Account:
    def __init__(self, username, password, posts = None, following = None):
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
        
