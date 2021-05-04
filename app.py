# imports
from lxml import html
from bs4 import BeautifulSoup
import requests
from time import sleep
import time
import smtplib
import os
from os.path import join, dirname
from dotenv import load_dotenv

# take environment variables from .env.
load_dotenv()

# recipient email address
recipientEmail = os.environ.get("RECIPIENT_EMAIL")

# gmail send credentials
send_user = os.environ.get("GMAIL_USERNAME")
send_pass = os.environ.get("GMAIL_PASSWORD")

# global arr to store info extracted from page to use elsewhere
info = []

# urls to check
urls = ["https://www.amazon.com/ASUS-GeForce-Graphics-DisplayPort-Bearings/dp/B08HH5WF97?ref_= ast_sto_dp", "https://www.amazon.com/ASUS-Graphics-DisplayPort-Military-Grade-Certification/dp/B08HHDP9DW?ref_ = ast_sto_dp", "https://www.amazon.com/PNY-GeForce-Gaming-EPIC-X-Graphics/dp/B08HBR7QBM?ref_ = ast_sto_dp",
        "https://www.amazon.com/PNY-GeForce-Gaming-UPRISING-Graphics/dp/B08HBTJMLJ?ref_ = ast_sto_dp", "https://www.amazon.com/MSI-GeForce-320-Bit-Architecture-Graphics/dp/B08HR5SXPS?ref_ = ast_sto_dp", "https://www.amazon.com/MSI-GeForce-Tri-Frozr-Architecture-Graphics/dp/B08HR7SV3M?ref_ = ast_sto_dp", "https://www.amazon.com/EVGA-10G-P5-3897-KR-GeForce-Technology-Backplate/dp/B08HR3Y5GQ?ref_ = ast_sto_dp", "https://www.amazon.com/dp/B08J6F174Z?tag=nismain-20&linkCode=ogi&th=1&psc=1", "https://www.amazon.com/dp/B08KGZVKXM?tag=nismain-20&linkCode=ogi&th=1&psc=1", ]

# get the title of the item


def get_title(soup):
    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id": 'productTitle'})

        # Inner NavigableString Object
        title_value = title.string

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string

# Get price of item


def get_price(soup):

    try:
        price = soup.find(
            "span", attrs={'id': 'priceblock_ourprice'}).string.strip()

    except AttributeError:
        price = ""

    return price

# Get price of item


def get_rating(soup):

    try:
        rating = soup.find(
            "i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()

    except AttributeError:

        try:
            rating = soup.find(
                "span", attrs={'class': 'a-icon-alt'}).string.strip()
        except:
            rating = ""

    return rating

# Get number of reviews


def get_review_count(soup):
    try:
        review_count = soup.find(
            "span", attrs={'id': 'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""

    return review_count

# Get current availability


def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id': 'availability'})
        available = available.find("span").string.strip()

    except AttributeError:
        available = ""

    return available

# main function to run checks


def check(url):
    # Headers for request
    HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})

    # HTTP Request
    webpage = requests.get(url, headers=HEADERS)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "lxml")

    # Function calls to get all needed product information
    info.append(get_title(soup))
    info.append(get_price(soup))
    info.append(get_rating(soup))
    info.append(get_review_count(soup))
    info.append(get_availability(soup))

    # print out the info
    print("Product Title =", get_title(soup))
    print("Product Price =", get_price(soup))
    print("Product Rating =", get_rating(soup))
    print("Number of Product Reviews =", get_review_count(soup))
    print("Availability =", get_availability(soup))

    return get_availability(soup)

# send an email if in stock


def sendmail(ans, product, url):
    recipient = recipientEmail
    body_of_email = ans + "\n" + url
    email_subject = product + ' product availability'

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(send_user, send_pass)

    # message to be sent
    headers = "\r\n".join(["from: " + send_user,
                           "subject: " + email_subject,
                           "to: " + recipient,
                           "mime-version: 1.0",
                           "content-type: text/html"])

    content = headers + "\r\n\r\n" + body_of_email
    s.sendmail(send_user, recipient, content)
    s.quit()

# main function


def read(url):
    print("Processing")
    ans = check(url)

    if "In Stock" in ans:
        print("sending email")

        # sending email
        sendmail(ans, info[0], url)
    print()
    print()


def job():
    # the product ID to track
    for url in urls:
        read(url)


while True:
    job()

    # sleep for 10 secs
    time.sleep(10)
