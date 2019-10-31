import os
import smtplib
import mimetypes
import logging
from email.MIMEMultipart import MIMEMultipart
from email import encoders
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Create file handler
fh = logging.FileHandler('Kegs-Balances/kegsbalances.log') # PATH to file on local machine
fh.setLevel(logging.INFO)
# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Add formatter to fh
fh.setFormatter(formatter)
# Add fh to logger
logger.addHandler(fh)

class SendEmail:
	# Class for sending emails from gmail account

	def send_email(self, message, subject, emailTo, emailFrom, password, fileToSend=None):
		# Sends email with provided file as attachment from emailFrom to emailTo
		# Username and Password provided for gmail acount that sends email

		logger.info('Sending Email')

		msg = MIMEMultipart()
		msg['From'] = emailFrom
		if type(emailTo) == list:
			msg['To'] = ', '.join(emailTo)
		else:
			msg['To'] = emailTo
		msg['Reply-To'] = 'NoReplay@NoReply.com'
		msg['Subject'] = subject

		body = MIMEText(message)
		msg.attach(body)

		if fileToSend == None:
			pass
		elif type(fileToSend) == list:	# Allows for multiple attachments
			for f in fileToSend:
				
				ctype, encoding = mimetypes.guess_type(f)
				if ctype is None or encoding is not None:
					ctype = 'application/octet-stream'

				maintype, subtype = ctype.split('/', 1)

				if maintype == 'application':
					fp = open(f, 'rb')
					att = MIMEApplication(fp.read(), _subtype=subtype)
					fp.close()
				elif maintype == 'text':
					fp = open(f)
					att = MIMEText(fp.read(), _subtype=subtype)
					fp.close()
				elif maintype == 'image':
					fp = open(f, 'rb')
					att = MIMEImage(fp.read(), _subtype=subtype)
					fp.close()
				elif maintype == 'audio':
					fp = open(f, 'rb')
					att = MIMEAudio(fp.read(), _subtype=subtype)
					fp.close()
				else:
					fp = open(f, 'rb')
					att = MIMEBase(maintype, subtype)
					att.set_payload(fp.read())
					fp.close()
					encoders.encode_base64(att)

				att.add_header('content-disposition', 'attachment', filename=os.path.basename(f))
				msg.attach(att)
		else:
			ctype, encoding = mimetypes.guess_type(fileToSend)
			if ctype is None or encoding is not None:
				ctype = 'application/octet-stream'

			maintype, subtype = ctype.split('/', 1)

			if maintype == 'application':
					fp = open(fileToSend, 'rb')
					att = MIMEApplication(fp.read(), _subtype=subtype)
					fp.close()
			elif maintype == 'text':
				fp = open(fileToSend)
				att = MIMEText(fp.read(), _subtype=subtype)
				fp.close()
			elif maintype == 'image':
				fp = open(fileToSend, 'rb')
				att = MIMEImage(fp.read(), _subtype=subtype)
				fp.close()
			elif maintype == 'audio':
				fp = open(fileToSend, 'rb')
				att = MIMEAudio(fp.read(), _subtype=subtype)
				fp.close()
			else:
				fp = open(fileToSend, 'rb')
				att = MIMEBase(maintype, subtype)
				att.set_payload(fp.read())
				fp.close()
				encoders.encode_base64(att)

			att.add_header('content-disposition', 'attachment', filename=os.path.basename(fileToSend))
			msg.attach(att)

		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login(emailFrom, password)
		server.sendmail(emailFrom, emailTo, msg.as_string())
		server.quit()

		return




