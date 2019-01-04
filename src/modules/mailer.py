import smtplib
import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import modules.logger as logger

COMMASPACE = ', '

class Mailer(object):
    def __init__(self, sender_address, recipient_list, subject, host, port, message, file=''):
        sender = sender_address
        self.logger = logger.Logger()
        recipients = recipient_list.split(',')
        outer = MIMEMultipart()
        outer['Subject'] = subject
        outer['To'] = COMMASPACE.join(recipients)
        outer['From'] = sender
        outer.attach(MIMEText(message, 'plain'))
        if file != '':
            attachments = [file]

            for file in attachments:
                try:
                    with open(file, 'rb') as fp:
                        msg = MIMEBase('application/excel', 'octect-stream')
                        msg.set_payload(fp.read())
                    encoders.encode_base64(msg)
                    msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
                    outer.attach(msg)
                except Exception as e:
                    self.logger.exception('Unable to open  attachment: {}'.format(e))
        
        composed = outer.as_string()
        try:
            with smtplib.SMTP(host, port) as mail:
                mail.ehlo()
                mail.starttls()
                mail.ehlo()
                mail.sendmail(sender, recipients, composed)
                mail.close()
            self.logger.info('Email sent!')
        except Exception as e:
            self.logger.error('Error sending message: {}'.format(e))