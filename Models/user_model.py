class UserModel:
    _instance = None  # Class variable to keep the instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(UserModel, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.username = None
            self.password = None
            self.name = None
            self.email = None
            self.initialized = True