class LoginPage:
    def __init__(self):
        pass
    
    def validateUserData(self, email, password, accounts):
        # check if the account exists in the database
        if email in accounts:
            accountPassword = accounts[email]
            # check if the passwords match
            if accountPassword == password:
                print("Logged in successfully!")
                # redirect to home page
            else:
                print("Error: Passwords do not match.")
        else:
            print("Error: Account does not exist.")
    
    def render(self):
        pass

class StudentLoginPage(LoginPage):
    def render(self):
        pass

class EmployerLoginPage(LoginPage):
    def render(self):
        pass

class AdminLoginPage(LoginPage):
    def render(self):
        pass
