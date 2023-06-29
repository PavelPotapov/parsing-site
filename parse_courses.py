
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
#from seleniumwire import webdriver
from proxy_auth_data import *
import time

#fake useragent
useragent = UserAgent()

#options
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={useragent.random}")

#set proxy

proxy_url = f"{login}:{password}@{domain}:{port}"

proxy_options = {
    "proxy": {
            "http": "http://" + proxy_url,
            "https": "https://" + proxy_url,
            "no_proxy": "localhost,127.0.0.1",
        }
}

'''
PROXY="neP9ve:uQEEm4@217.29.53.67:11168"
webdriver.DesiredCapabilities.CHROME['proxy'] = {
    "httpProxy": PROXY,
    "ftpProxy": PROXY,
    "sslProxy": PROXY,
    "proxyType": "MANUAL",

}
webdriver.DesiredCapabilities.CHROME['acceptSslCerts']=True
'''


urls_cources = [f'https://backoffice.algoritmika.org/course?page={i+1}' for i in range(5)]
main_url = 'https://backoffice.algoritmika.org/auth/v3/login' #"https://2ip.ru"#'https://www.whatismybrowser.com/detect/what-is-my-user-agent/' 


driver = webdriver.Chrome(
    executable_path=r"C:\Users\Admin\Desktop\python\парсинг сайта\chromedriver\chromedriver.exe",
    options=options
)

#получаем ссылки на все курсы

try:
    driver.get(url=main_url)
    login = driver.find_element(by=By.ID, value='login')
    login.clear()
    login.send_keys('popov123')
    time.sleep(2)
    button = driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/div/div[2]/form/div[2]/button').click()
    time.sleep(2)
    password_for_log = driver.find_element(by=By.ID, value='password')
    password_for_log.clear()
    password_for_log.send_keys('1234567')
    button = driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/div/div[2]/form/div[3]/button').click()
    time.sleep(2)
    for i in urls_cources:
        driver.get(i)
        elements = driver.find_elements(by=By.TAG_NAME, value='a')
        for elem in elements:
            print(type(elem.get_attribute('href')))
            if elem.get_attribute('href').find('view') != -1:
                with open("cources.txt", mode='a') as file_handler:
                    file_handler.write(elem.get_attribute('href'))
                    file_handler.write('\n')
        
    time.sleep(2)
                         
        

except Exception as ex:
    print(ex)
finally:
    driver.close()
