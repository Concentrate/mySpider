from scrapy.mail import MailSender
if __name__=="__main__":
    mailsender=MailSender(mailfrom="smartguy@ok.com")
    mailsender.send(to="1098014590@qq.com",subject="test mail sender",body="that is cool")
