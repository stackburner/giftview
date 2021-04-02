import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


class Mail:

    def __init__(self, server, port, user, pw, to, sub, msg):
        self.User = user
        self.PW = pw
        self.Server = smtplib.SMTP_SSL(server, port)
        self.To = to.split(',')
        self.Sub = sub
        self.Body = msg
        self.Msg = self._construct()


    def _construct(self):
        msg = MIMEMultipart()
        msg['Subject'] = Header(self.Sub, 'utf-8')
        msg['From'] = self.User
        msg['To'] = ', '.join(self.To)
        msg.attach(MIMEText(self.Body, 'plain'))

        return msg.as_string()


    def send(self):
        self.Server.login(self.User, self.PW)
        self.Server.sendmail(self.User, self.To, self.Msg)
        self.Server.quit()
