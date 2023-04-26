#!/usr/bin/python3

import hashlib
import os
import sys
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

if __name__ == "__main__":
    filepath = Path(sys.argv[1])
    filename = filepath.name

    sha256_hash = hashlib.sha256()
    with filepath.open('rb') as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload((attachment).read())
        for byte_block in iter(lambda: attachment.read(4096),b""):
            sha256_hash.update(byte_block)
    
    checksum = sha256_hash.hexdigest()
    
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    
    subject = "A new file has been generated by motioncore"
    body = f"<h2><style='color:red'>Motion detected!</style></h2><br><h3>Motion has been detected.<br>Sha256sum checksum of attachment is {checksum}</h3>"

    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = "jamesstewartmiller@gmail.com"
    message['To'] = "jamesstewartmiller@gmail.com"
    html_part = MIMEText(body, 'html')
    message.attach(html_part)
    message.attach(part)

    sslcontext = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.gmail.com", "465", context=sslcontext)
    server.login("jamesstewartmiller@gmail.com", "enxfpsraifydwkhp")
    server.sendmail("jamesstewartmiller@gmail.com", "jamesstewartmiller@gmail.com", message.as_string())
    server.quit()