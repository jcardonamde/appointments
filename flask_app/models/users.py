from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data ['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        result = connectToMySQL('esquema_appointments').query_db(query, formulario)
        return result
    
    @classmethod
    def get_by_email(cls, formulario):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('esquema_appointments').query_db(query, formulario)
        if len(result) < 1:
            return False
        else:
            user = cls(result[0])
            return user
    
    @classmethod
    def get_by_id(cls, formulario):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL('esquema_appointments').query_db(query, formulario)
        user = cls(result[0])
        return user
    
    @staticmethod
    def validate_user(formulario):
        is_valid = True
        
        if len(formulario['first_name']) < 3:
            flash('Name must have at least 3 characters', 'registro')
            is_valid = False
            
        if len(formulario['last_name']) < 3:
            flash('Last Name must have at least 3 characters', 'registro')
            is_valid = False
        
        # Valid email address with regular expressions
        if not EMAIL_REGEX.match(formulario['email']):
            flash('Invalid email, please verify that the email entered is correct', 'registro')
            is_valid = False
        
        # Check if password at least 8 characters
        if len(formulario['password']) < 8:
            flash('Password must have at least 8 characters', 'registro')
            is_valid = False
        
        # Check if the password matches with Password Confirmation field
        if formulario['password'] != formulario['confirm_password']:
            flash('Passwords do not match', 'registro')
            is_valid = False
            
        #Check if the Email address not already in database
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('esquema_appointments').query_db(query, formulario)
        if len(results) >= 1:
            flash('Email registrado previamente', 'registro')
            is_valid = False
            
        return is_valid