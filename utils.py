import logging
import smtplib
from email.mime.text import MIMEText
import ConfigParser




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

def addState(ex1, ex2, id, currencyPair, spreadExit):
    config = ConfigParser.RawConfigParser()
    state_file = "botstate_" + str(ex1) + "_" + str(ex2) + ".cfg"
    config.read(state_file)

    config.add_section(str(id))
    config.set(str(id), 'currencyPair', str(currencyPair))
    config.set(str(id), 'spreadExit', str(spreadExit))

    with open(state_file, 'w') as configfile:
        config.write(configfile)


def removeState(ex1, ex2, id):
    config = ConfigParser.RawConfigParser()
    state_file = "botstate_" + str(ex1) + "_" + str(ex2) + ".cfg"
    config.read(state_file)

    config.remove_section(str(id))
    with open(state_file, 'w') as configfile:
        config.write(configfile)


def updateStateofCounters(ex1, ex2, combinations, profitCount):
    config = ConfigParser.RawConfigParser()
    state_file = "botstate_" + str(ex1) + "_" + str(ex2) + ".cfg"
    config.read(state_file)

    config.remove_section('profitCount')
    config.add_section('profitCount')
    for c in combinations:
        config.set('profitCount', str(c["id"]), str(profitCount[c["id"]]))


    with open(state_file, 'w') as configfile:
        config.write(configfile)

def loadStateSpread(ex1, ex2):
    config = ConfigParser.RawConfigParser()
    state_file = "botstate_" + str(ex1) + "_" + str(ex2) + ".cfg"
    config.read(state_file)

    spreadExit = {}
    for each_section in config.sections():
        if each_section != 'profitCount':
            spreadExit[int(each_section)] = float(config.get(each_section, 'spreadExit'))
            pass
    return spreadExit

def loadProfitCount(ex1, ex2):
    profitCount = {}
    try:
        config = ConfigParser.RawConfigParser()
        state_file = "botstate_" + str(ex1) + "_" + str(ex2) + ".cfg"
        config.read(state_file)

        for (each_key, each_val) in config.items('profitCount'):
            profitCount[int(each_key)] = int(each_val)
        pass
    except Exception, error:
        print("Info: Mo  profit count state stored! Initializing from zero...")
    return profitCount

def hasSavedState(ex1, ex2):
    try:
        config = ConfigParser.RawConfigParser()
        state_file = "botstate_" + str(ex1) + "_" + str(ex2) + ".cfg"
        config.read(state_file)
        if len(config.sections()) != 0:
            return True
        else:
            return False
    except Exception:
        return False
