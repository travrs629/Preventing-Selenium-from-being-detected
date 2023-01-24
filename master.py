__author__ = "Soumil Shah"
__email__ = "shahsoumil519@gmail.com"
try:

    import sys
    import os
    # Scrap roxies list from different websites and checks if one specific proxy is working.
    from fp.fp import FreeProxy
    # Scrap modern useragent and randomize the user-agent with real world statistics through useragentstring.com and w3schools.com.
    from fake_useragent import UserAgent
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from selenium.webdriver import Chrome
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    import time
    print('all module are loaded ')

except Exception as e:

    print("Error ->>>: {} ".format(e))


class Spoofer(object):

    def __init__(self, country_id=['US'], rand=True, anonym=True):
        self.country_id = country_id
        self.rand = rand
        self.anonym = anonym
        self.userAgent, self.ip = self.get()

    def get(self):
        # Gets a fake UserAgent with random browser settings in fake_useragent.
        ua = UserAgent()
        # Gets the first FreeProxy with 'US' country id, with a shuffled proxy list (not newest to oldest), and with marked anonymous.
        proxy = FreeProxy(country_id=self.country_id,
                          rand=self.rand, anonym=self.anonym).get()
        # Gets rid of the 'http://' or 'https://'.
        ip = proxy.split("://")[1]
        return ua.random, ip


class DriverOptions(object):
    # Chromeoptions Class is a concept in Selenium WebDriver for manipulating various properties of the Chrome driver.
    # About all the Chromeoptions: https://stackoverflow.com/a/38336334/14499516
    def __init__(self):
        self.options = Options()
        # Bypass the restrictions on the rights of each Chrome process (OS security model) that vary from trust levels, thus increasing vulnerability.
        # Starts the browser with the highest privileges.
        # self.options.add_argument('--no-sandbox')
        # Allows the browser to open in its maximized size (default Chrome behaviour?).
        self.options.add_argument('--start-maximized')
        # Allows the browser to open in fullscreen.
        # self.options.add_argument('--start-fullscreen')
        # Runs Chrome in a single process (but seems to be depreciated in a long time ago).
        # self.options.add_argument('--single-process')
        # Prevents docker with shared 64MB memory in /dev/shm to crash with Chrome, when the partition is too small in some VM environments.
        # IT is changed into /tmp.
        # self.options.add_argument('--disable-dev-shm-usage')
        # Presets the browser to open in incognito mode.
        # self.options.add_argument("--incognito")
        # Removes the info-bar of 'Chrome is controlled by automated software.' (and other automation records).
        # self.options.add_argument('--disable-blink-features')
        # self.options.add_argument(
        #     '--disable-blink-features=AutomationControlled')
        # However, this enables the info bar of "Chrome is being controlled by automatedtest software".
        self.options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        # Disables the driver to install other Chrome extensions, such as CaptureScreenshot.
        # Disables pop-ups like  "Disable developer mode extensions" as well.
        self.options.add_experimental_option('useAutomationExtension', False)
        # Removes the info-bar of "Chrome is being controlled by automated test software", but it seems to be depreciated.
        self.options.add_argument('disable-infobars')
        # Suppresses the 'Could not read device interface GUIDs: The system cannot find the file specified.' and 'Failed to read descriptor from node connection: A device attached to the system is not functioning.' messages.
        self.options.add_experimental_option(
            "excludeSwitches", ["enable-logging"])

        self.options.add_experimental_option('detach', True)

        # Creates the object of Spoofer.
        self.helperSpoofer = Spoofer()

        # Puts the FakeUserAgent into Options object.
        self.options.add_argument(
            'user-agent={}'.format(self.helperSpoofer.userAgent))
        # Puts the FreeProxy into Options object.
        self.options.add_argument('--proxy-server=%s' % self.helperSpoofer.ip)


class WebDriver(DriverOptions):

    def __init__(self, path=''):
        DriverOptions.__init__(self)
        self.driver_instance = self.get_driver()

    def get_driver(self):

        print("""
        IP:{}
        UserAgent: {}
        """.format(self.helperSpoofer.ip, self.helperSpoofer.userAgent))

        IP = self.helperSpoofer.ip
        # Modify the proxy for Crome in Python WebDriver.
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy": IP,
            "ftpProxy": IP,
            "sslProxy": IP,
            "noProxy": None,
            "proxyType": "MANUAL",
            "autodetect": False,
        }
        # Accepts all SSL Certificates by default.
        webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True

        os.environ['PATH'] += r"C:\Program Files (x86)"
        driver = webdriver.Chrome(service=Service(), options=self.options)
        # Disables the navigator flag in webdriver.
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source":
                "const newProto = navigator.__proto__;"
                "delete newProto.webdriver;"
                "navigator.__proto__ = newProto;"
        })

        return driver


def main():

    driver = WebDriver()
    driverinstance = driver.driver_instance
    # https://bot.sannysoft.com also seems to be a good option. 
    driverinstance.get("https://www.expressvpn.com/what-is-my-ip")
    time.sleep(5)
    user_agent_check = driverinstance.execute_script(
        "return navigator.userAgent;")
    print(user_agent_check)
    print("done")


if __name__ == "__main__":
    main()
