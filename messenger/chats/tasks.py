from django.core.mail import send_mail
from application.celery import app
from application.local_settings import EMAIL_HOST_USER
from users.models import User
from django.utils import timezone
import shutil
from django.core.management import call_command


@app.task(time_limit=60)   
def send_admin_email(subject, message, email_admins):
    send_mail(
        subject=subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=email_admins
    )


@app.task(time_limit=60)
def show_params_memory():
    total, used, free = shutil.disk_usage("/")
    print("Total: %d GiB" % (total // (2**30)))
    print("Used: %d GiB" % (used // (2**30)))
    print("Free: %d GiB" % (free // (2**30)))


@app.task(time_limit=600)
def backup_db():
    try:
        call_command('dbbackup')
        return f'Successful backup at : {timezone.now()}'
    
    except Exception as error:
        return f'Unsuccessful attempt backup at: {timezone.datetime.now()}, error : {error}'


@app.task(time_limit=60)
def show_users_messenger():
    count_users = calc_users_messenger()
    count_today_logged_users = calc_logged_users_today()
    with open('log_users.txt', 'a') as file:
        str_log = str(timezone.localtime(timezone.now())) + f' - {count_users} users registered, {count_today_logged_users} users logged in today' + '\n'
        file.write(str_log)


def calc_users_messenger():
    count_users = User.objects.count()
    return count_users


def calc_logged_users_today():
    count_logged_users = User.objects.filter(last_login__startswith=timezone.now().date()).count()
    return count_logged_users




