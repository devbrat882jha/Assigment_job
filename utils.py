from passlib.context import CryptContext
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_function(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

MAILTRAP_USERNAME = "8770088b9e81bd"
MAILTRAP_PASSWORD = "c242bbaf71abb1"
MAILTRAP_SERVER = "smtp.mailtrap.io"
MAILTRAP_PORT = 587

def send_email(subject: str, body: str, to_email: str, from_email: str = "noreply@jobportal.com"):
    try:
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(MAILTRAP_SERVER, MAILTRAP_PORT) as server:
            server.login(MAILTRAP_USERNAME, MAILTRAP_PASSWORD)
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)
            print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
