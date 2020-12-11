from selenium import webdriver
import time
import random
global username
def Pause(driver,page_no ,Total_send ,Suppliers_Name ,index,username):
    print('Saving To file')
    URL=driver.current_url

    file = open(username+'.txt' , 'w')

    file.write(URL+'\n')
    file.write(str(page_no)+'\n')
    file.write(str(Total_send)+'\n')
    file.write(str(index)+'\n')
    for name in Suppliers_Name:
        file.write(str(name)+'\n')

    file.close()


def Resume(username):
    print(username)
    file = open(username+'.txt', 'r')
    lines=[]
    for line in file:
        line =line.replace('\n','')
        lines.append(line)
    link =lines[0]
    #print(link)
    page_no = lines[1]
    #print(page_no)
    Total_send = lines[2]
    #print(Total_send)
    Index1 = lines[3]
    #print(Index1)
    Suppliers  = lines[4:]
    #print(Suppliers,type(Suppliers))
    return link,int(page_no),int(Total_send),int (Index1), Suppliers

def login(driver , username ,password):
    driver.get('https://passport.alibaba.com/icbu_login.htm?tracelog=hd_signin')
    time.sleep(5)
    print('login ....')
    driver.find_element_by_xpath('//*[@id="fm-login-id"]').send_keys(username)
    driver.find_element_by_xpath('//*[@id="fm-login-password"]').send_keys(password)

    driver.find_element_by_xpath('//*[@id="fm-login-submit"]').click()
    time.sleep(10)

    return driver


def Wait(Total_send):
    if (Total_send % 20 == 0):
        wait = random.uniform(0.5, 1)
        print(wait, 'hour ')
        time.sleep(wait * 3)
    else:
        wait = random.randint(5, 12)
        print('waiting.............', wait)
        time.sleep(wait)


def PressSend(driver1, send_button):
    # send message button
    try:
        driver1.find_element_by_xpath('/html/body/div[3]/div/form/div[1]/div[5]/div[3]/div[2]/input').click()
        send_button = True
    except:
        try:
            driver1.find_element_by_xpath('/html/body/div[2]/div/form/div[1]/div[5]/div[3]/div[2]/input').click()
            send_button = True
        except:
            try:
                driver1.find_element_by_xpath('/html/body/div[4]/div/form/div[1]/div[5]/div[3]/div/input').click()
                send_button = True
            except:
                try:
                    driver1.find_element_by_xpath('/html/body/div[3]/div/form/div[1]/div[5]/div[3]/div/input').click()
                    send_button = True
                except:
                    send_button = False
    return send_button


def main(driver , driver1 , url ,templets,username  ):
    outputs = []

    #PATH = "geckodriver"
    #driver = webdriver.Firefox(executable_path=PATH)
    #driver1 = webdriver.Firefox(executable_path=PATH)
    print('Start Main')
    #driver = login(driver , username , password)
    # enter Templates name inthe files_name below
    #Files_Name = ['Template 1.txt', 'Template 2.txt', 'Template 3.txt']

    # 'https://offer.alibaba.com/catalogs/products/cid100002954?spm=a2700.7746188.1997230041.2.7af2ESxZESxZZo'
    #print()
    #Ask = input('Press 1. to resume pervoius script \nPress 2. To start new Script \n')


    print('Starting New...')
    print(username)
    link, page_no, Total_send, indexI, Suppliers_Name = Resume(username)
    print('staring From Page N0 ', page_no + 1)
    driver.get(link)
    time.sleep(10)



    #driver1 = login(driver1)
    while (True):
        i = indexI
        # Xpath For total Iteams on page
        try:
            #xpath = '//*[@id="root"]/div/div[3]/div[2]/div/div/div/div'
            xpath =         '/html/body/div[1]/div[3]/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[4]/div[1]/div'
            Next_path =   '/html/body/div[1]/div[3]/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[4]/div[2]'
            Divs = driver.find_elements_by_xpath(xpath)
        except:
            xpath = '//*[@id="root"]/div/div[4]/div[2]/div/div/div/div'

            Divs = driver.find_elements_by_xpath(xpath)

        #//*[@id="root"]/div/div[3]/div[2]/div/div/div/div[1]

        print('Total Items on this  page', len(Divs))
        outputs.append('Total Items on this  page '+str(len(Divs)))

        for div in Divs:
            print(i , Total_send)

            M = div.find_element_by_class_name('item-main')
            N= M.find_element_by_class_name('item-info')
            O = N.find_element_by_class_name('stitle')
            name = O.find_element_by_tag_name('a').text
            print(name)

            '''
            try:
                name = driver.find_element_by_xpath(xpath + '[' + str(i) + ']/div/div[3]/a').text
            except:
                try:
                    name = driver.find_element_by_xpath(xpath + '[' + str(i) + ']/div/div[3]/div[1]/a').text
                except:
                    try:
                        name = driver.find_element_by_xpath(xpath + '[' + str(i) + ']/div/div[2]/div[2]/a').text
                    except:
                        name = ''
                        if 'Name Xpath not finded... Check or contact to Admin' not in outputs:
                            print('Name Xpath not finded... Check or contact to Admin')
                            outputs.append('Name Xpath not finded... Check or contact to Admin')
                        continue
            '''

            if (name in Suppliers_Name):
                print(i, 'Already Sent Message to', name)
                outputs.append(str(i)+'Already Sent Message to'+str(name))
                i += 1
                continue
            else:
                Suppliers_Name.append(name)
                print(i, 'Sending Message to ', name)
                outputs.append(str(i)+' Sending Message to '+ str(name))

            M = div.find_element_by_class_name('item-main')
            N = M.find_element_by_class_name('item-info')
            O = N.find_element_by_class_name('contact')
            contact = O.find_element_by_tag_name('a')
            print(name)

            '''
            try:
                contact = driver.find_element_by_xpath(xpath + '[' + str(i) + ']/div/div[4]/a[1]')
            except:
                try:
                    contact = driver.find_element_by_xpath(xpath + '[' + str(i) + ']/div/div[3]/a')
                except:
                    contact = driver.find_element_by_xpath(xpath + '[' + str(i) + ']/div/div[2]/div[5]/a[1]')
            '''
            i += 1
            contact = contact.get_attribute('href')

            driver1.get(contact)

            index = random.randint(0, 2)
            print('templete............', index)
            outputs.append('templete............'+ str(index))

            data = templets[index]
            print(data)
            time.sleep(15)
            driver1.find_element_by_xpath('//*[@id="inquiry-content"]').send_keys(data)
            send_button = False

            send_button = PressSend(driver1, send_button)

            if (send_button == False):
                Pause(driver, page_no, Total_send, Suppliers_Name, indexI ,username)
                driver.close()
                return driver, driver1, 'Plesae Solve the capthca and start or check xpath of Send Button for more Details Contact admin \nThanks' ,True

            #send_button = PressSend(driver1, send_button)

            Total_send += 1

            print ('Total successfull send inquiry  to', Total_send, 'Suppliers :)')
            outputs.append('Total successfull send inquiry  to '+str(Total_send)+ ' Suppliers :)')
            # random wait
            Wait(Total_send)


            if Total_send % 3 == 0:
                Pause(driver,page_no, Total_send, Suppliers_Name, indexI, username)
                driver.close()
                return driver, driver1, outputs , False

        #driver.execute_script("window.scrollTo(0,1500)")

        driver.execute_script("window.scrollTo(0 , document.body.scrollHeight)")
        print('Getting the next page')
        outputs.append('Getting the next page')
        '''
        N = driver.find_element_by_xpath(Next_path)
        M = N.find_element_by_class_name('m-pagination util-clearfix')
        N = M.find_element_by_class_name('util-right util-clearfix')
        O = N.find_element_by_class_name('ui2-pagination')
        P = O.find_element_by_class_name('ui2-pagination-pages')
        next = P.find_element_by_class_name('next')
        driver.execute_script("arguments[0].click();", next)
        print('Getting the next page')
        outputs.append('Getting the next page')
        
        page_no += 1
            # this time wait is may depend on your internet speed or many other factors
        wait = 25
        time.sleep(wait)
        #except:
        #    print('no more pages')
        #    outputs.append('no more pages')
        #    
        
        
        '''

        try:
            next = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[4]/div/div[1]/a[last()]')


            driver.execute_script("arguments[0].click();", next)

            print('next page')
            page_no += 1
            outputs.append('Next Page' + str(page_no))

            # this time wait is may depend on your internet speed or many other factors
            wait = 25
            time.sleep(wait)
            indexI = 0
        except:
            try:

                next = driver.find_element_by_xpath('/html/body/div[5]/div[1]/div/div[4]/div/div[1]/a[last()]')

                driver.execute_script("arguments[0].click();", next)

                print('next page')
                page_no += 1
                outputs.append('Next Page' + str(page_no))
                # this time wait is may depend on your internet speed or many other factors
                wait = 25
                time.sleep(wait)
                indexI = 0
            except:
                try:
                    next = driver.find_element_by_xpath('/html/body/div[5]/div[1]/div/div[4]/div/div[1]/a[last()]')

                    # /html/body/div[5]/div[1]/div/div[4]/div/div[1]/a[6]
                    driver.execute_script("arguments[0].click();", next)
                    print('next page')

                    page_no += 1
                    outputs.append('Next Page' + str(page_no))

                    # this time wait is may depend on your internet speed or many other factors
                    wait = 25
                    time.sleep(wait)
                    indexI = 0
                except:
                    try:

                        next = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div[2]/div[1]/div[2]/div[1]/div/div[4]/div[2]/div/div/div/div[2]/a[last()]')
                        # /html/body/div[5]/div[1]/div/div[4]/div/div[1]/a[6]
                        driver.execute_script("arguments[0].click();", next)
                        print('next page')

                        page_no += 1
                        outputs.append('Next Page' + str(page_no))
                        # this time wait is may depend on your internet speed or many other factors
                        wait = 25
                        time.sleep(wait)
                        indexI = 0
                    except:
                        print('no more pages')
                        outputs.append('no more pages')
                        break

        #if ((page_no % 2) == 0 or Total_send % 20 == 0):
            #input('Pause Y/N \n')
            #Ask_Again = ''
            #if (Ask_Again.lower() == 'y'):
            #Pause(driver, driver1, page_no, Total_send, Suppliers_Name , indexI)
            #return driver, driver1, outputs
    print('Allllllllllllll DOneeeeeeeeeeeeeeeeeeeeeeeeeeeeee', Total_send)

    outputs.append('All Done '+str(Total_send))

    Pause(driver, driver1, page_no, Total_send, Suppliers_Name, indexI ,username)
    driver.close()
    return driver , driver1 , outputs , False




