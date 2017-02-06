from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import bcrypt, re
from pytz import timezone

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
        name = postData['name'].lower().strip()
        email = postData['email'].lower().strip()
        password = postData['password'].strip()
        conf_pwd = postData['conf_pwd'].strip()
        #Validate name
        if not is_valid_name(name, 'First'):
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
                name=name,
                email=email,
                password=pw_hash
            )
            print "Created user"
            ret_data = {
                'success': True,
                'msg_list': []
            }
        return ret_data

class AppointmentManager(models.Manager):
    def add_appt(self, postData):
        print "Entering add_appt"
        error_list = []
        back_to_home_page = False
        date = postData['date'].encode()
        print "date entered: ", date
        time = postData['time'].encode()
        print "time entered: ", time
        user_id = postData['user_id']
        task = postData['task']
        print "task entered: ", task
        date_list = Appointment.objects.filter(date=date, time=time)
        user = User.objects.get(id=postData['user_id'])
        todays_date = str(datetime.now(timezone('US/Pacific')).date())
        print "todays_date",todays_date
        time_now = str(datetime.now(timezone('US/Pacific')).time()).split(':')
        seq = time_now[0], time_now[1]
        time_now = ':'.join(seq)
        print "time_now", time_now

        if date_list:
            error_list.append('This date and time already has a task!')
            back_to_home_page = True
        else:
            if len(task) < 1:
                error_list.append('Task explanation cannot be empty!')
                back_to_home_page = True
            if date < todays_date:
                print "Comparison date < todays_date is TRUE"
                error_list.append("Date cannot be in the past!")
                back_to_home_page = True
            elif date == todays_date:
                print "Comparison date == todays_date is TRUE"
                if time < time_now:
                    error_list.append("Time cannot be in the past!")
                    back_to_home_page = True

        if back_to_home_page:
            print "Add appointment failed: ", error_list
            ret_data = {
                'success': False,
                'msg_list': error_list
            }
        else:
            # All validations passed. appointment can be added into Appointment DB
            print "Creating appointment object "
            appointment = Appointment(date=date,
                                      time=time,
                                      task=task,
                                      status="Pending",
                                      user=user)
            appointment.save()
            print "Saved appointment = ", appointment.task
            ret_data = {
                'success': True,
                'msg_list': []
            }
        return ret_data

    def delete_appt(self, postData):
        appointment = Appointment.objects.get(id=postData['appt_id']).delete()

    def update_appt(self, postData):
        appointment = Appointment.objects.get(id=postData['appt_id'])
        appointment.task = postData['new_task']
        appointment.status = postData['new_status']
        appointment.date = postData['new_date']
        appointment.time = postData['new_time']
        appointment.save()

class User(models.Model):
    name = models.CharField(max_length = 45)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Appointment(models.Model):
    name = models.CharField(max_length=45)
    date = models.DateField(blank=True)
    time = models.TimeField(blank=True)
    task = models.CharField(max_length = 255, blank=True)
    status = models.CharField(max_length=45)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = AppointmentManager()
