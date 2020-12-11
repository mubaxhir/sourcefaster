from selenium import webdriver
from pyvirtualdisplay import Display
import time
from googletrans import Translator
from tox import INFO

def main(number):
    display = Display(visible=0, size=(1200, 800))
    display.start()
    #'91420984181166746P'
    translator = Translator()
    PATH = "/usr/bin/geckodriver"
    print(PATH)
    driver = webdriver.Firefox(executable_path=PATH)
    try:
        print('searching........')
        driver.get("https://aiqicha.baidu.com/s?q={}&t=0".format(number))

        next = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[1]/div[2]/div[2]/div/div/div[2]/div/h3/a').get_attribute('href')
        driver.get(next)
        # time.sleep(4)

        print('scraping....')
        Info =[]
        name = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[1]/div[1]/div[2]/div[1]/h2').text
        nam = translator.translate(name,src="zh-cn",dest="en")
        Info.append(nam.text)
        
        tags = driver.find_elements_by_xpath('/html/body/div[1]/div[1]/div/div[1]/div[1]/div[2]/div[2]/span')
        for tag in tags:
            tag = translator.translate(tag.text,src="zh-cn",dest="en")
            print(tag.text)
            Info.append(tag.text)
    except Exception as e:
        print(e)
        driver.quit()
        display.stop()  
        raise Exception

    phone  = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[1]/div[1]/div[2]/div[3]/div[1]/p[1]/span')
    Info.append(phone.text)

    email = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[1]/div[1]/div[2]/div[3]/div[1]/p[2]/span')
    Info.append(email.text)

    website = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[1]/div[1]/div[2]/div[3]/div[2]/p[1]/a')
    Info.append(website.text)


    address = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[1]/div[1]/div[2]/div[3]/div[2]/p[2]/span').text
    address = translator.translate(address,src="zh-cn",dest="en")
    Info.append(address.text)

    des = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[1]/div[1]/div[2]/div[3]/div[3]/div').text
    des = translator.translate(des,src="zh-cn",dest="en")
    t= des.text
    t = t.replace('... expand', ' ')
    Info.append(t)

    table = driver.find_elements_by_xpath('/html/body/div[1]/div[1]/div/div[6]/div[1]/div[3]/table/tbody/tr')
    Table =[]

    for tr in table:
        TD =[]
        tds = tr.find_elements_by_tag_name('td')
        for td in tds:
            text = translator.translate(td.text,src="zh-cn",dest="en")
            t =text.text
            t = t.replace('... expand' ,' ')
            TD.append(t)
            
        Table.append(TD)

    driver.quit()
    display.stop()  

    return Info,Table
