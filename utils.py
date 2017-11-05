import logging
import smtplib
from email.mime.text import MIMEText



def setup_logger(name, log_file, formatter, level=logging.INFO):
    """Function setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


def sendmail(action, message):
    fromaddr = 'madhiker123@gmail.com'
    toaddrs  = 'danieltidus@gmail.com'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('madhiker123','$735136$')
    msg = MIMEText(message)

    msg['Subject'] = "WhiteBird Action: " + str(action)
    msg['From'] = fromaddr
    msg['To'] = toaddrs
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()