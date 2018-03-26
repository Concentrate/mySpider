import smtplib
from email.mime.text import MIMEText
from email.header import Header

mail_host = "smtp.163.com"
mail_user = "qq1098014590@163.com"
mail_passwd = "ldy19941007"
sender = mail_user


def sendNotifiedMessage(msg, subject):
    receivers = ["1098014590@qq.com", ]
    message = MIMEText(msg, 'plain', 'utf8')
    message['From'] = sender
    message["To"] = receivers[0]
    message["Subject"] = Header(subject, "utf8")
    try:
    	smtpObj = smtplib.SMTP()
    	smtpObj.connect(mail_host, 25)
    	smtpObj.login(mail_user, mail_passwd)
    	smtpObj.sendmail(sender, receivers, message.as_string())
    	print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(e)
