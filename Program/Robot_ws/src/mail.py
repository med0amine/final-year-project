#! /usr/bin/env python3

__author__ = "Mohamed Amine Ben Ammar"
__date__ = "20/03/2022"

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

fromEmail = 'slividrobot@gmail.com'
Password = 'AMINE@amine.medamine'

toEmail = 'med52969142@gmail.com'

def sendEmail(image):
	msgRoot = MIMEMultipart('related')
	msgRoot['Subject'] = 'Security Alret'
	msgRoot['From'] = fromEmail
	msgRoot['To'] = toEmail
	msgRoot.preamble = 'Robot Security upadte'

	msgAlternative = MIMEMultipart('alternative')
	msgRoot.attach(msgAlternative)
	msgText = MIMEText('Robot found person')
	msgAlternative.attach(msgText)

	msgText = MIMEText('<img src="cid:image1">', 'html')
	msgAlternative.attach(msgText)

	msgImage = MIMEImage(image)
	msgImage.add_header('Content-ID', '<image1>')
	msgRoot.attach(msgImage)

	smtp = smtplib.SMTP('smtp.gmail.com', 587)
	smtp.starttls()
	smtp.login(fromEmail, Password)
	smtp.sendmail(fromEmail, toEmail, msgRoot.as_string())
	smtp.quit()