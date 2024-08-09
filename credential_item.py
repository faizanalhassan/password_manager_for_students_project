class CredentialItem:
    def __init__(self, name, username, password, category=None, notes=None):
        self.name = name
        self.username = username
        self.password = password
        self.category = category
        self.notes = notes