from django.db import models

# databases
class AccountDatabase:#(models.Model)
    def __init__(self):
        self.accounts = {}
        self.primaryKey = 0
    def size(self):
        return len(self.accounts)
    def getTable(self):
        return self.accounts
    def getAccounts(self):
        return self.accounts.values()
    def getAccountByEmail(self, email):
        return self.accounts.get(email, None)
    def addAccount(self, account):
        self.accounts[account.getEmail()] = account
        self.primaryKey += 1
    def removeAccount(self, account):
        self.accounts.pop(account.getEmail())
        self.primaryKey -= 1
    def updateAccountStatus(self, account, status):
        account.setStatus(status)
        self.accounts[account.getEmail()] = account

class PostDatabase:#(models.Model)
    def __init__(self):
        self.posts = {}
        self.primaryKey = 0
        self.searchFuncs = {"title": self.searchByTitle,
                            "job type": self.searchByJobType,
                            "description": self.searchByDescription}
    def size(self):
        return len(self.posts)
    def getTable(self):
        return self.posts
    def getPosts(self):
        return self.posts.values()
    def getPostById(self, postId):
        return self.posts.get(postId, None)
    def getPostByAuthor(self, author):
        for post in getPosts():
            if post.getAuthor() == author:
                return post
        return None
    def addPost(self, post):
        post.setId(self.primaryKey)
        self.posts[post.getId()] = post
        self.primaryKey += 1
    def removePost(self, post):
        self.posts.pop(post.getId())
        self.primaryKey -= 1
    def search(self, currentFilter, searchString):
        return self.searchFuncs[currentFilter](searchString.lower())
    def searchByTitle(self, searchString):
        posts = []
        for post in self.getPosts():
            if searchString in post.getTitle().lower():
                posts.append(post)
        return posts
    def searchByJobType(self, searchString):
        posts = []
        for post in self.getPosts():
            if searchString in post.getJobType().lower():
                posts.append(post)
        return posts
    def searchByDescription(self, searchString):
        posts = []
        for post in self.getPosts():
            if searchString in post.getDescription().lower():
                posts.append(post)
        return posts

# accounts
class Account:#(models.Model)
    def __init__(self, email, password, accountType):
        self.email = email
        self.password = password
        self.accountType = accountType
        self.status = "unblocked"
    def getEmail(self):
        return self.email
    def getPassword(self):
        return self.password
    def getAccountType(self):
        return self.accountType
    def getStatus(self):
        return self.status
    def setEmail(self, email):
        self.email = email
    def setPassword(password):
        self.password = password
    def setAccountType(self, accountType):
        self.accountType = accountType
    def setStatus(self, status):
        self.status = status

class StudentAccount(Account):#(models.Model):
    def __init__(self, email, password):
        super().__init__(email, password, "student")

class EmployerAccount(Account):#(models.Model):
    def __init__(self, email, password):
        super().__init__(email, password, "employer")

class AdminAccount(Account):#(models.Model):
    def __init__(self, email, password):
        super().__init__(email, password, "admin")

# job post
class Post:#(models.Model)
    def __init__(self, author, title, jobType, description):
        self.id = 0
        self.author = author
        self.title = title
        self.jobType = jobType
        self.description = description
        self.status = "active"
    def getId(self):
        return self.id
    def getAuthor(self):
        return self.author
    def getTitle(self):
        return self.title
    def getJobType(self):
        return self.jobType
    def getDescription(self):
        return self.description
    def getStatus(self):
        return self.status
    def setId(self, id):
        self.id = id
    def setAuthor(self, author):
        self.author = author
    def setTitle(self, title):
        self.title = title
    def setJobType(self, jobType):
        self.jobType = jobType
    def setDescription(self, description):
        self.description = description
    def setStatus(self, status):
        self.status = status

class AccountFactory:#(models.Manager):
    def __init__(self):
        pass
    def create(self, accountType, email, password):
        account = None
        if accountType == "student":
            account = StudentAccount(email, password)
        elif accountType == "employer":
            account = EmployerAccount(email, password)
        elif accountType == "admin":
            account = AdminAccount(email, password)
        return account
