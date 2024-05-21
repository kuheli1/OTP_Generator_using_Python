
from email.message import EmailMessage
import re,os,sys,smtplib,random as r
from dotenv import load_dotenv

# Load environment variables from .env file into the current environment
load_dotenv()


def get_app_specific_info():
    """
    Retrieves application-specific information such as password and sender from environment variables.
    Returns: password and sender retrieved from environment variables.
    """
    password = os.getenv('passcode')
    sender = os.getenv('sender')
    return password, sender


def otpgen():
    """function to generate a 6 digit random number"""
    otp = ''
    digit = 6
    for i in range(digit):
        otp = otp + str(r.randint(1, 9))
    return otp


def is_email_valid(recipient):
    """Function to validate if the email address is in valid format"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$'
    return re.match(pattern, recipient)


def connecting_email(recipient, code):
    """Function to simulate sending the OTP to the user's email address"""
    try:
        password, sender = get_app_specific_info()

        msg = EmailMessage()
        msg['from'] = sender
        msg['to'] = recipient
        msg['subject'] = "Here's your OTP "
        msg.set_content("hello there, find your OTP " + code)
        print(f"Sending OTP to {recipient}...")

        with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipient, msg.as_string())
            smtp_server.quit()

    except smtplib.SMTPAuthenticationError:
        print("Authentication Failed. Please check Sender email address and Password")
        sys.exit(1)
    except:
        print("An Error Occurred")
        sys.exit(1)


def verifyUser(code):
    """Function to prompt the user to enter the OTP received in their email and then verifies if the entered OTP matches the generated OTP"""
    for attempt in range(3):
        userotp = input('Enter your OTP: ')
        if userotp == code:
            print('Your OTP is Verified')
            break
        else:
            print('Wrong OTP Entered')
            if attempt < 2:
                print(f'You have {2-attempt} attempts remaining')
            else:
                print('Sorry! You have lost all 3 attempts. Bye')      

# Main Function to execute OTP generation,sending and verification
def main():
    for attempt in range(3):
        recipient = input('Enter your email address: ')
        is_email_valid(recipient)
        if is_email_valid(recipient):
            code = otpgen()
            connecting_email(recipient, code)
            verifyUser(code)
            break
        else:
            print("Email id not valid.")
            if attempt < 2:
                print(f'Please Try again, you have {2-attempt} attempts left')
    else:
        print('Sorry! you dont have any more attempts')


if __name__ == '__main__':
    main()

