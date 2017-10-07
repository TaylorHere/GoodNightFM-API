from test import *
from random_data import random_data as ran


class User(Test):

    def __init__(self):
        self.telephone = ran().telephoe()
        self.nickname = ran().people_name()
