# ADAPTED FROM: https://stackoverflow.com/a/26369282

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .gmail_secret import GMAIL_APP_PW
from .email_body import get_email_body
from .constants import EMAIL_FROM


def send_failure_email(resp):
    obj_type = "Workbook" if "Workbook" in resp["event_type"] else "Datasource"

    # me == my email address
    # you == recipient's email address
    me = EMAIL_FROM
    you = resp["owner_email"]

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Tableau Extract Refresh Failure"
    msg["From"] = me
    msg["To"] = you

    # Create the body of the message (a plain-text and an HTML version).
    text = ""
    html = get_email_body(obj_type, resp["resource_name"], resp["webpage_url"])

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    # Send the message via local SMTP server.
    mail = smtplib.SMTP("smtp.gmail.com", 587)

    mail.ehlo()

    mail.starttls()

    mail.login(EMAIL_FROM, GMAIL_APP_PW)
    mail.sendmail(me, you, msg.as_string())
    mail.quit()
