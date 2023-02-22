from fileinput import filename
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email import encoders
from os.path import basename
import os

def send_mail(send_from: str, subject: str, text: str, 
send_to: list):

    path_image = "./image"
    files = os.listdir(path_image)

    send_to= default_address if not send_to else send_to

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = ', '.join(send_to)  
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for filename in os.listdir(path_image):
        print(filename,"------------")
        with open(filename, 'rb') as f:
            img_data = f.read()

    part = MIMEImage(img_data, name=os.path.basename(filename))

    msg.attach(part)

    smtp = smtplib.SMTP(host="smtp.gmail.com", port= 587) 
    smtp.starttls()
    smtp.login('ufukcicek987@gmail.com','civyytsdkzzsppek')
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


send_mail("ufukcicek987@gmail.com","agile point","Agile point hata",["ufukcicek199@gmail.com"])