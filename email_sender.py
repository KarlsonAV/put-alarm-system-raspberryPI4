import smtplib
import logging
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


logging.getLogger().setLevel(logging.INFO)


class EmailSender:
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_email_with_photo(self, recipient_email: str, subject: str, body: str, photo_path: str) -> None:
        # Create the MIME object for the email
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        # Attach body text
        msg.attach(MIMEText(body, 'plain'))

        # Attach photo
        with open(photo_path, 'rb') as photo_file:
            img = MIMEImage(photo_file.read())
            img.add_header('Content-Disposition', 'attachment', filename='photo.jpg')
            msg.attach(img)

        try:
            context = ssl.create_default_context()
            server = smtplib.SMTP(self.smtp_server, self.smtp_port,)
            server.starttls(context=context)
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, recipient_email, msg.as_string())
            logging.info("Email sent successfuly")
        except Exception as e:
            logging.error(f"Error while sending email: {e}")