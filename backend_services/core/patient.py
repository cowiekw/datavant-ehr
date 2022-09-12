class Patient:
    """ A patient class"""
    def __init__(self, first_name, last_name, age, city, state, email):
        self.first_name = first_name # patient legal name
        self.last_name = last_name
        self.age = age
        self.city  = city
        self.state = state
        self.email = email

    def __repr__(self):
        return "Entity:'{}', '{}', {}".format(self.first_name, self.last_name, self.state)
