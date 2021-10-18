#Super class for account creation
class account:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    account = account("email", "password")


#Admin child class for account
class Admin(account):
    def __init__(self, email, password):
        super().__init__(email, password)

#Employer child class for account   
class Employer(account):
    def __init__(self, email, password):
        super().__init__(email, password)

#Student child class for account
class Student(account):
    def __init__(self, email, password, date):
        super().__init__(email, password)
        self.graduationDate = date