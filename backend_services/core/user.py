class User:
    """ A user class"""
    def __init__(self, id, name, email):
        self.id = id # patient legal name
        self.name = name
        self.email = email

    def __repr__(self):
        return "Entity:'{}', '{}', {}".format(self.name, self.email)
