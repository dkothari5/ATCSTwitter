class Post:

    # Constructor
    def __init__(self, title, text, hashtags = None):
        self.title = title
        self.text = text
        if hashtags is None:
            self.hashtags = []
        else:
            self.hashtags = hashtags

    def __str__(self):
        return f"{self.title}\n{self.text}"
