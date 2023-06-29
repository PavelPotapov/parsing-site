
from multiprocessing import Value
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
#from seleniumwire import webdriver
from proxy_auth_data import *
import time
import os, sys, re
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests



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



main_url = 'https://backoffice.algoritmika.org/auth/v3/login' #"https://2ip.ru"#'https://www.whatismybrowser.com/detect/what-is-my-user-agent/' 
main_domen = 'https://backoffice.algoritmika.org'
#curse_url = 'https://backoffice.algoritmika.org/course/view/686'
#curse_urles = ['https://backoffice.algoritmika.org/course/view/686']
curse_urles = []

driver = webdriver.Chrome(
    executable_path=r"C:\Users\Admin\Desktop\python\парсинг сайта\chromedriver\chromedriver.exe",
    options=options
)

def zapret_s(s):
    zapret = ["'", '"', ':', '?', '>', '<', '*', '|']
    for i in zapret:
        if i in s:
            s = s.replace(i,'')
    return s


def savePage(url, pagepath='page'):
    def savenRename(soup, pagefolder, session, url, tag, inner):
        if not os.path.exists(pagefolder): # create only once
            os.mkdir(pagefolder)
        for res in soup.findAll(tag):   # images, css, etc..
            if res.has_attr(inner): # check inner tag (file object) MUST exists  
                try:
                    filename, ext = os.path.splitext(os.path.basename(res[inner])) # get name and extension
                    filename = re.sub('\W+', '', filename) + ext # clean special chars from name
                    fileurl = urljoin(url, res.get(inner))
                    filepath = os.path.join(pagefolder, filename)
                    # rename html ref so can move html and folder of files anywhere
                    res[inner] = os.path.join(os.path.basename(pagefolder), filename)
                    if not os.path.isfile(filepath): # was not downloaded
                        with open(filepath, 'wb') as file:
                            filebin = session.get(fileurl)
                            file.write(filebin.content)
                except Exception as exc:
                    print(exc, file=sys.stderr)
    session = requests.Session()
    #... whatever other requests config you need here
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    path, _ = os.path.splitext(pagepath)
    pagefolder = path+'_files' # page contents folder
    tags_inner = {'img': 'src', 'link': 'href', 'script': 'src'} # tag&inner tags to grab
    for tag, inner in tags_inner.items(): # saves resource files and rename refs
        savenRename(soup, pagefolder, session, url, tag, inner)
    with open(path+'.html', 'wb') as file: # saves modified html doc
        file.write(soup.prettify('utf-8'))


try:
    #----------------------АВТОРИЗАЦИЯ------------------------------------------------------------------------
    driver.get(url=main_url)
    login = driver.find_element(by=By.ID, value='login')
    login.clear()
    login.send_keys('popov123')
    time.sleep(1)
    button = driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/div/div[2]/form/div[2]/button').click()
    time.sleep(1)
    password_for_log = driver.find_element(by=By.ID, value='password')
    password_for_log.clear()
    password_for_log.send_keys('1234567')
    button = driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/div/div[2]/form/div[3]/button').click()
    time.sleep(1)

    '''
    #считываем из файла все курсы
    with open('cources.txt', 'r', encoding='utf-8') as f:
        res = f.readlines()
        for i in res:
            curse_urles.append(i)

    #перебираем все курсы
    for curse_url in curse_urles:
        try:
            #ОТКРЫВАЕМ СТРАНИЦУ КУРСА
            driver.get(curse_url)
            time.sleep(2)
            #Получаем название курса
            h3 = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div[3]/div/div/h3')
            
            curse_name = h3.text #название курса
            #если курс про питон
            if curse_name.lower().find('python') != -1:
                #Создаем папку с таким названием
                if not os.path.exists(curse_name):
                    os.mkdir(curse_name)
                else:
                    os.mkdir(curse_name + " copy")
                #мелкое описание курса
                curse_description = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div/div/div[3]/div/div/div[1]').text
                with open(curse_name + "/" + "description.txt", mode='a', encoding='utf-8') as file_handler:
                    file_handler.write(curse_description)
                
                #делаем 3 скриншота
                try:
                    for i in range(6):
                        driver.save_screenshot(curse_name + "/" + curse_name + f'{i+1}.png')
                        driver.execute_script("window.scrollBy(0,500)")
                        time.sleep(1)
                except:
                    pass

                ul = driver.find_elements(by=By.CLASS_NAME, value='list-group')
                lies = ul[0].find_elements(by=By.TAG_NAME, value='li')

                k = 0
                zapret = ["'", '"', ':', '?', '>', '<', '*', '|']
                for li in lies:
                    try:
                        k += 1
                        if k == 36:
                            pass
                        div1 = li.find_elements(by=By.TAG_NAME, value='div')
                        a = div1[0].find_element(by=By.TAG_NAME, value='a')
                        path = curse_name + '/' + a.text
                        for i in zapret:
                            if i in path:
                                path = path.replace(i,'')
                        os.mkdir(path)
                        with open(curse_name + '/' + 'links.txt', 'a', encoding='utf-8') as f:
                            f.write(a.get_attribute('href'))
                            f.write('\n')
                        time.sleep(1)
                    except Exception as e:
                        print(e)
                        continue
                    
                time.sleep(2)
            else:
                pass
        except:
            pass
    '''
    #получаем список папок текущей дериктории
    example_dir = os.getcwd()
    with os.scandir(example_dir) as files:
        subdirs = [file.name for file in files if file.is_dir()]
    subdirs.remove("__pycache__")

    tasks_links = [] #массив ссылок на задачи
    #перебираем список всех папок
    for subdir in subdirs:
        if os.path.exists(subdir + '/links.txt'):
            with open(subdir + '/links.txt', 'r', encoding='utf-8') as f:
                res = f.readlines()
                for i in res:
                    tasks_links.append(i)
            
            for a in tasks_links:
                driver.get(a)
                print(driver.current_url)
                time.sleep(1.5)

                 
                h3 = driver.find_element(by=By.XPATH, value='//*[@id="lesson-editor"]/div[1]/h3').text

                #делаем 3 скриншота
                try:
                    for i in range(6):
                        driver.save_screenshot(subdir + "/" + h3 + "/" + h3 + f'{i+1}.png')
                        driver.execute_script("window.scrollBy(0,500)")
                        time.sleep(0.2)
                except:
                    pass
            


                h3 = zapret_s(h3)

                div_topic = driver.find_element(by=By.CLASS_NAME, value='panel-body')
                list_a = div_topic.find_elements(by=By.TAG_NAME, value='a')


                for a in list_a:
                    if a.get_attribute('href').find('docs.google.com') != -1:
                        with open(subdir + '/' + h3 + '/topic.txt', 'a', encoding='utf-8') as f:
                            f.write(a.get_attribute('href'))
                            f.write('\n')

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                #ol1 = driver.find_element(by=By.CSS_SELECTOR, value='#lesson-tasks .task-items')
                ol = driver.find_element(by=By.XPATH, value='//*[@id="lesson-tasks"]/div[1]/ol')
                lies = driver.find_elements(by=By.CLASS_NAME, value='box-header')

                lies_headers = []
                for i in range(5):
                    try:
                        res =  driver.find_element(by=By.XPATH, value=f'//*[@id="lesson-tasks"]/div[1]/ol/li[{i+1}]/div/div[1]/a')
                        res = res.text
                        res = zapret_s(res)
                        os.mkdir(subdir + '/' + h3 + '/' + res)
                        try:
                            ol = driver.find_element(by=By.XPATH, value=f'//*[@id="lesson-tasks"]/div[1]/ol/li[{i+1}]/div/div[2]/div/div/div/div[2]/ol')
                            lies = ol.find_elements(by=By.TAG_NAME, value='li')
                            for j in lies:
                                a = j.find_element(by=By.TAG_NAME, value='a').get_attribute('href')
                                with open(subdir + '/' + h3 + '/' + res +'/tasks.txt', 'a', encoding='utf-8') as f:
                                    f.write(a)
                                    f.write('\n')
                        except Exception as ex:
                            print(ex)
                        lies_headers.append(res)
                    except:
                        pass

                #путь до заголовка - //*[@id="lesson-tasks"]/div[1]/ol/li[1]/div/div[1]/a
                #                    //*[@id="lesson-tasks"]/div[1]/ol/li[2]/div/div[1]/a
            

                #//*[@id="lesson-tasks"]/div[1]/ol/li[1]/div/div[2]/div/div/div/div[2]/ol
                #//*[@id="lesson-tasks"]/div[1]/ol/li[2]/div/div[2]/div/div/div/div[2]/ol
                #//*[@id="lesson-tasks"]/div[1]/ol/li[1]/div/div[2]/div/div/div/div[2]/ol

                #получаем ol каждого блока
            
                   

                '''
                elements = driver.find_elements(by=By.TAG_NAME, value='img')
                time.sleep(1)
                k = 0
                for elem in elements:
                    k += 1
                    с = elem.get_attribute('src')
                    p = requests.get(с)
                    with open(subdir + '/' + h3 + '/' + f"{k}.jpg", "wb") as f:
                        f.write(p.content)
                

                elements = driver.find_elements(by=By.TAG_NAME, value='bdi')
   
                for element in elements:
                    with open(subdir + '/' + h3 + "/infos.txt", mode='a', encoding='utf-8') as file_handler:
                        file_handler.write(element.text)
                        file_handler.write('\n')
                '''
    
except Exception as ex:
    print(ex)
finally:
    driver.close()
