from __future__ import unicode_literals
from django.db import models
import bcrypt, re

class QuoteManager(models.Manager):
    def add(self, postData):
        print "Entering Quote add"
        error_list = []
        back_to_register_page = False
        quote = postData['quote'].lower().strip()
        quoted_by = postData['quoted_by'].lower().strip()
        quote_list = Quote.objects.filter(quote_text=quote)
        user_name = User.objects.get(id=postData['user_id']).first_name
        if quote_list:
            error_list.append('This quote message already exists!')
            back_to_register_page = True
        elif len(quote) < 10:
            error_list.append('Quote message cannot be less than 10 chars!')
            back_to_register_page = True
            if len(quoted_by) < 3:
                error_list.append("Quoted By' cannot be less than 3 chars!")
                back_to_register_page = True

        if back_to_register_page:
            ret_data = {
                'success': False,
                'msg_list': error_list
            }
        else:
            # All validations passed. Data can be added into DB
            print "Creating quote object "
            Quote.objects.create(quote_text=quote, quoted_by=user_name)
            ret_data = {
                'success': True,
                'msg_list': []
            }
        return ret_data

class Quote(models.Model):
    quote_text = models.CharField(max_length=300)
    posted_by = models.CharField(max_length=45)
    quoted_by = models.CharField(max_length=45)
    objects = QuoteManager()

class FavoriteManager(models.Manager):
    def add_fav(self, postData):
        print "Entering Favorite add"
        error_list = []
        back_to_register_page = False
        user_id = postData['user_id']
        print user_id
        quote = Quote.objects.get(id=postData['quote_id'])
        user = User.objects.get(id=user_id)
        favorites_list = user.favorites.all()
        if quote in favorites_list:
            ret_data = {
                'success': False,
                'msg_list': list("This quote is already in your Favorites list!")
            }
        else:
            print "Adding favorite object "
            new_fav = Favorite.objects.create(quote_id=quote)
            user.favorites.add(new_fav)
            # Favorite.objects.add(quote_id=postData['quote_id'])
            ret_data = {
                'success': True,
                'msg_list': []
            }

class Favorite(models.Model):
    quote_id = models.ForeignKey(Quote)
    objects = FavoriteManager()

class UserManager(models.Manager):
    def login(self, postData):
        def is_valid_email(email):
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.(com|net|org)+$')
            ret_val = True
            if len(email) < 1:
                error_list.append('Email cannot be blank!')
                ret_val = False
            elif not EMAIL_REGEX.match(email):
                error_list.append('Invalid email address!')
                ret_val = False
            return ret_val
        print "Entered login"
        # Initializations
        error_list = []
        back_to_index_page = False
        email = postData['email'].lower().strip()
        password = postData['password'].strip()

        # Check if user is registered (i.e. email is in DB)
        user_list = User.objects.filter(email=email)
        if not email:
            error_list.append('Email cannot be blank!')
            back_to_index_page = True
        elif not user_list:
            error_list.append('Unknown email! Please register first.')
            back_to_index_page = True
        elif not is_valid_email(email):
            back_to_index_page = True

        if len(password) < 8:
            error_list.append('Password should be at least 8 chars!')
            back_to_index_page = True

        if back_to_index_page:
            ret_data = {
                'success': False,
                'msg_list': error_list
            }
        else:
            # Authenticate the user (password check)
            passwd_db = user_list[0].password
            if bcrypt.hashpw(password.encode(), passwd_db.encode()) == passwd_db:
                # Authentication successful
                ret_data = {
                    'success': True,
                    'msg_list': []
                }
            else:
                ret_data = {
                    'success': False,
                    'msg_list': ['Incorrect password!']
                }
        return ret_data

    def register(self, postData):
        def is_valid_name(name, txt):
            NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
            ret_val = True
            if len(name) < 2:
                error_list.append(txt + ' name should be at least 2 chars!')
                ret_val = False
            if not NAME_REGEX.match(name):
                error_list.append(txt + ' name should be alphabetic chars')
                ret_val = False
            return ret_val
        def is_valid_password(pw, cpw):
            PASSWD_REGEX = re.compile(r'^[a-zA-Z0-9@#$%^&+=]+$')
            ret_val = True
            if pw != cpw:
                error_list.append("Passwords don't match")
                ret_val = False
            if len(pw) < 8:
                error_list.append('Password should be at least 8 chars!')
                ret_val = False
            if not PASSWD_REGEX.match(pw):
                error_list.append('Invalid char(s) in password. Valid chars = Alphanumeric chars and \'@#$%^&+=\'')
                ret_val = False
            return ret_val
        def is_valid_email(email):
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.(com|net|org)+$')
            ret_val = True
            if len(email) < 1:
                error_list.append('Email cannot be blank!')
                ret_val = False
            elif not EMAIL_REGEX.match(email):
                error_list.append('Invalid email address!')
                ret_val = False
            return ret_val
        print "Registration process"
        error_list = []
        back_to_register_page = False
        first_name = postData['first_name'].lower().strip()
        last_name = postData['last_name'].lower().strip()
        email = postData['email'].lower().strip()
        password = postData['password'].strip()
        conf_pwd = postData['conf_pwd'].strip()
        #Validate first_name
        if not is_valid_name(first_name, 'First'):
            back_to_register_page = True

        #Validate last_name
        if not is_valid_name(last_name, 'Last'):
            back_to_register_page = True

        # Check if user is already registered (email is in DB)
        user_list = User.objects.filter(email=email)
        if user_list:
            error_list.append('This email is already registered!')
            back_to_register_page = True
        elif not is_valid_email(email):
            back_to_register_page = True

        # Validate password
        if not is_valid_password(password, conf_pwd):
            back_to_register_page = True

        if back_to_register_page:
            ret_data = {
                'success': False,
                'msg_list': error_list
            }
        else:
            # All validations passed. Data can be added into DB
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=pw_hash
            )
            ret_data = {
                'success': True,
                'msg_list': []
            }
        return ret_data

class User(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    favorites = models.ManyToManyField(Favorite)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
