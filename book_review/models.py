from django.db import models
import re
import bcrypt
class UserManager(models.Manager): 
    def Registration_Validator(self, postData): 
        errors = {} 
        if len(postData['name']) < 2: 
            errors['name'] = " name must be 2 characters or more" 
            if len(postData['alias']) < 2: 
                errors['alisa'] = " Alias name must be 2 characters or more" 
                user_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
                if not user_regex.match(postData['email']): 
                    errors['email'] = "You must enter in a valid email" 
                    check_email = User.objects.filter(email=postData['email']) 
                    if len(check_email) > 0: 
                        errors['emailExists'] = "Already a user with this email in our database" 
                    if len(postData['password']) < 8: 
                        errors['password'] = "Password must be at least 8 characters long" 
                    if postData['password'] != postData['passwordC']: 
                        errors['passwordC'] = "Your password and confirm password do not match" 
        return errors

    def Login_Validator(self, postData): 
        errors = {} 
        login_user = User.objects.filter(email=postData['email']) 
        if len(login_user) > 0: 
            if bcrypt.checkpw(postData['password'].encode(), login_user[0].password.encode()): 
                print("Password matches") 
            else: errors['password'] = "Password does not match!" 
        else: 
            errors['email'] = "There is no user with that email" 
        return errors

class User(models.Model): 
    name=models.CharField(max_length=30) 
    alias=models.CharField(max_length=30) 
    email = models.CharField(max_length=80) 
    password = models.CharField(max_length=32) 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    objects = UserManager()

class Author(models.Model): 
    name = models.CharField(max_length=30) 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model): 
    title = models.CharField(max_length=30) 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    author = models.ForeignKey(Author, related_name="book", on_delete= models.CASCADE)

class Review(models.Model): 
    description = models.CharField(max_length=30) 
    rating = models.IntegerField() 
    user = models.ForeignKey(User, related_name ="reviewers", on_delete= models.CASCADE) 
    book = models.ForeignKey(Book, related_name="reviews", on_delete = models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)









