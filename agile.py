from email.mime import message
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import datetime
from dotenv import load_dotenv
import uuid
import schedule
import time
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


load_dotenv()

email = os.getenv("USER_NAME")
password = os.getenv("PASSWORD")
from_to_mail = os.getenv("EMAIL")
from_to_mail_password = os.getenv("EMAIL_PASSWORD")


login_selector = 'input.button.button-primary'
domain_link = os.getenv("LINK")

selector_screen_shot = "body.Chrome"

def open_browser(domain_link,email,password):
    with sync_playwright() as playwright:
        chromium = playwright.firefox  # or "firefox" or "webkit".
        browser = chromium.launch(headless=False)
        context = browser.new_context(
            ignore_https_errors=True, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36")
        page = context.new_page()
        page.goto(domain_link)
        page.wait_for_load_state()
        page.wait_for_timeout(10000)
        page_content = page.content()
        soup = BeautifulSoup(page_content, 'html.parser')

        page.locator("input[name='username']").fill(email)
        page.locator("input[name='password']").fill(password)
        page.click(login_selector)
        page.wait_for_timeout(20000)
        print("Giriş Başarılı!")
        page.wait_for_timeout(10000)
        failed_check(page,soup)

def failed_check(page,soup):
    eror = soup.find('div.message.message-Error')
    if eror:
        message = "An error has been detected"
        logfile_text( message)
        file_name = failed_screen_shot(page)
        send_mail(file_name, message)
    else:
        message = "no problem"
        logfile_text(message)
        logout_agile(page,soup)

def logout_agile(page,soup):

    try:
        signout_click_selector = "span.user-actions.signout-icon"
        profil_click_selector = "img.userprofile"
        page.click(profil_click_selector)
        page.wait_for_timeout(5000)
        page.click(signout_click_selector)
        page.wait_for_timeout(5000)
    except:
        message = "An error has been detected"
        logfile_text( message)
        file_name = failed_screen_shot(page)
        send_mail(file_name, message)

def logfile_text(message):
    now_time = datetime.datetime.now()
    with open('logfile.txt', 'a') as f:
        f.write('{0} , {1} \n '.format(now_time,message))

def failed_screen_shot(page):
    area_img = page.query_selector(selector_screen_shot)
    img_uudi = str(uuid.uuid1())
    file_name = "./image/"+img_uudi+".png"
    area_img.screenshot(path=file_name)

    return file_name

def send_mail(file_name,message_text):
    send_to= ["ufukcicek199@gmail.com",'ufuk.cicek@arcelik.com']
    msg = MIMEMultipart()
    msg['From'] = from_to_mail
    msg['To'] = ', '.join(send_to)  
    msg['Subject'] = "Agile Point Failed"


    ImgFileName = file_name
    with open(file_name, 'rb') as f:
        img_data = f.read()

    part = MIMEImage(img_data, name=os.path.basename(ImgFileName))

    msg.attach(part)

    smtp = smtplib.SMTP(host="smtp.gmail.com", port= 587) 
    smtp.starttls()
    smtp.login(from_to_mail, from_to_mail_password)
    smtp.sendmail(from_to_mail, send_to, msg.as_string())
    smtp.close()

def job():
    now_time = datetime.datetime.now()
    print("I'm working...{0}".format(now_time))
    open_browser(domain_link,email,password)

schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)