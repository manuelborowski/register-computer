from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import time


class RC_TEST:
    def __init__(self, ll_start=1, ll_stop=126):
        # Create a new instance of the Firefox driver
        #driver = webdriver.Firefox()
        driver = webdriver.Chrome()
        #driver = webdriver.Remote("http://192.168.0.198:5001", webdriver.DesiredCapabilities.HTMLUNIT.copy())

        # go to the google home page
        driver.get("http://192.168.0.198:5001")
        #log in
        driver.find_element_by_id("username").send_keys("admin")
        driver.find_element_by_id("password").send_keys("admin")
        s = driver.find_element_by_id("submit_button")
        s.submit()
        print('from {} till {}'.format(ll_start, ll_stop))
        # we have to wait for the page to refresh, the last thing that seems to be updated is the title
        #WebDriverWait(driver, 10).until(EC.title_contains("cheese!"))

        #ce = driver.find_element_by_id("code")
        try:
            for i in range(ll_start, ll_stop+1):
                ll_code = 'LL{:03}'.format(i)
                c_code = 'URS{:03}'.format(i)
                print('{} -> {}'.format(c_code, ll_code))
                ce = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "code")))
                ce.send_keys('{}'.format(ll_code))
                re = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "register")))
                re.click()
                #time.sleep(1)
                try:
                    WebDriverWait(driver, 30).until(EC.text_to_be_present_in_element((By.ID, "code_label"), 'Computercode:'))
                except:
                    re = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "register")))
                    re.click()
                    time.sleep(1)
                    WebDriverWait(driver, 30).until(EC.text_to_be_present_in_element((By.ID, "code_label"), 'Computercode:'))

                ce = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "code")))
                ce.send_keys('{}'.format(c_code))
                re = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "register")))
                re.click()
                #time.sleep(1)
                try:
                    WebDriverWait(driver, 30).until(EC.text_to_be_present_in_element((By.ID, "code_label"), 'Leerlingcode:'))
                except:
                    re = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "register")))
                    re.click()
                    time.sleep(1)
                    WebDriverWait(driver, 30).until(EC.text_to_be_present_in_element((By.ID, "code_label"), 'Leerlingcode:'))

        finally:
            driver.quit()

if __name__ == '__main__':
    RC_TEST()