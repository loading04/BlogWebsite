import smtplib

from routes import *


def send_email(username, email, phone, message):
    MY_EMAIL = OWN_EMAIL
    TO_EMAIL = OWN_EMAIL
    My_PASSWORD = OWN_PASSWORD

    msg = f"\nName: {username}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"

    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(MY_EMAIL, My_PASSWORD)
    mail.sendmail(MY_EMAIL, TO_EMAIL, msg)
    mail.quit()


if __name__ == "__main__":
    app.run(debug=True)
