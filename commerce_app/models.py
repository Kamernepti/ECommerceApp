from django.db import models
from django import forms
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Model):
    def reg_validation(self, form):
        errors={}
        if len(form['fname']) < 1:
            errors['fname'] = 'First Name must have at least 1 character'
        if len(form['lname'])<1:
            errors['lname'] = 'Last Name must have at least 1 character'
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = "Invalid Email format"
        email_check = self.filter(email=form['email'])
        if email_check:
            errors['email'] = 'Email already in use'
        if len(form['password']) < 7:
            errors['password'] = 'Password must contain at least 7 characters'
        if (form['password'] != ['confirmpw']):
            errors['password'] = 'Passwords do not match'
        return errors
    def log_validation(self, email, password):
        users = User.objects.filter(email=email)
        if not users:
            return False
        user=users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

class User(models.Model):
    first_name= models.CharField(max_length= 45)
    last_name=models.CharField(max_length=45)
    email = models.CharField(max_length=255)
    password= models.CharField(max_length=150)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    objects=UserManager()

class Product(model.Models):
    description= models.CharField(max_length=200)
    price= models.DecimalField(decimal_place=2, max_digits=5)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

class Order(model.Models):
    quantity_ordered= models.IntegerField()
    total_price=models.DecimalField(decimal_places=2, max_digits=6)
    purchaser= models.ForeignKey (User, on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)