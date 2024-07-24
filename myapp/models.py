from django.db import models
import re
import bcrypt
from datetime import datetime

class UserManager(models.Manager):
    def validate_registration(self,postData):
        errors = {}
        if len(postData['firstname']) < 2:
            errors['firstname'] = 'First name should at least be 2 char and should be alphabitcal'

        if len(postData['lastname']) < 2 :
            errors['lastname'] = 'last name should at least be 2 char and  should be alphabitcal'
       
        if not postData['birthday']:
            errors['birthday'] = 'Birthday Is Mandatory'
        else:
            birthday = datetime.strptime(postData['birthday'], "%Y-%m-%d").date()
            today = datetime.now().date()
            age = today.year - birthday.year
            if age < 13:
                errors["birhday"] = "Age must be at least 13 years old"

        # to validate  the email  if it is already exist or it's a  non valid email 
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if User.objects.filter(email=postData['email']).exists():
            errors['email'] = "Email already in use!"
        if len(postData['password']) < 8 :
            errors['password'] = 'password must be at least 8 char'
        if len(postData['password']) != len(postData['confirm_password']):
            errors['confirm_password'] = 'passwords do not match'
    
        return errors
    # def validate_login(self,postData):
    #     errors = {}
    #     EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    #     if not EMAIL_REGEX.match(postData['email']):
    #         errors['email'] = "Invalid email address!"

    

class User(models.Model):
    firstname=models.CharField(max_length=255)
    lastname=models.CharField(max_length=255)
    email=models.CharField(max_length=255,unique=True)
    birthday = models.DateField(null=True, blank=True,auto_now=True)
    password=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

def create_user(post):
    password = post['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return User.objects.create(firstname = post['firstname'],lastname=post['lastname'],birthday = post['birthday'],email = post['email'] ,password= pw_hash)

def get_id(id):
    return User.objects.get(id = id)

def filter_email(post):
    return User.objects.filter(email = post['email'])
