import sys
from login import *

ADMIN_EMAIL = "admin@mail.umw.edu"

def getAccountType(email):        
    accountType = None;
    if email.endswith("@mail.umw.edu"):
        if email == ADMIN_EMAIL:
            accountType = "admin"
        else:
            accountType = "student"
    else:
        accountType = "employer"
    return accountType

def simulateUserInput(email, password):
    print("Enter your email: " + email)
    print("Enter your password: " + password)

def main(args):
    if len(args) != 2:
        return
    testEmail = args[0]
    testPassword = args[1]
 
    # these will be replaced by databases
    studentAccounts = {}
    employerAccounts = {}
    adminAccount = {}
    studentAccounts["student@mail.umw.edu"] = "password"
    employerAccounts["employer@gmail.com"] = "password"
    adminAccount["admin@mail.umw.edu"] = "password"

    accountType = getAccountType(testEmail);
    loginPage = None
    if accountType == "student":
        loginPage = StudentLoginPage()
        simulateUserInput(testEmail, testPassword)
        loginPage.validateUserData(testEmail, testPassword, studentAccounts)
    elif accountType == "employer":
        loginPage = EmployerLoginPage()
        simulateUserInput(testEmail, testPassword)
        loginPage.validateUserData(testEmail, testPassword, employerAccounts)
    elif accountType == "admin":
        loginPage = AdminLoginPage()
        simulateUserInput(testEmail, testPassword)
        loginPage.validateUserData(testEmail, testPassword, adminAccount)

# pass in command line arguments
main(sys.argv[1:])
