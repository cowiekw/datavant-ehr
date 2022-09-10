class Patient:
    """ A patient class"""
    def __init__(self, first_name, last_name, birthday, address, city, state):
        self.first_name = first_name # patient legal name
        self.last_name = last_name
        self.birthday = birthday
        self.address = address
        self.city  = city
        self.state = state

    def __repr__(self):
        return "Entity:'{}', '{}', {}".format(self.first_name, self.last_name, self.state)
