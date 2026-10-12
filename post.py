class Post:

    # Constructor
    def __init__(self, title, text, poster):
        self.title = title
        self.text = text
        self.poster = poster

    def __str__(self):
        return f"{self.poster}'s Post:\nTitle: {self.title}\n{self.text}\n"

    def to_dict(self):
        return {"title": self.title, "text": self.text, "poster": self.poster}

