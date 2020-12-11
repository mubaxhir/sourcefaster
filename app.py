from flask import render_template, Flask, session, redirect, url_for, jsonify, request
from selenium import webdriver
import Alibaba2_corrected as Alibaba
import check as ch
import models as dbHandler
import os
import shutil

Main_driver = ''
Message_driver = ''

username =''
password =''
url=''
temp1=''
temp2=''
temp3=''
Ask = ''

backup_verifications = []

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

def get_user():
    return session.get('user')

def get_status():
    return session.get('logged_in')


def AllowAccess(username):
    dir = "/usr/bin/"+username
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
    except:
        return False

    shutil.copyfile('geckodriver.exe', dir+'/'+'geckodriver.exe')
    return True


@app.route('/run', methods=['POST', 'GET'])
def run():
    if not get_status():
        return render_template('main_page/index.html')

    global username , password , url , temp1, temp2, temp3 , Message_driver ,Ask
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        url = request.form['url']
        temp1 = request.form['temp1']
        temp2 = request.form['temp2']
        temp3= request.form['temp3']
        Ask = request.form['Ask']


    if (Ask == 0 or Ask == '0'):
        file = open(username+'.txt', 'w')
        file.write( url+ '\n')
        file.write(str(0) + '\n')
        file.write(str(0) + '\n')
        file.write(str(0) + '\n')
        file.write(str(' ') + '\n')
        file.close()

    PATH = '/usr/bin/'+ username + "/geckodriver"
    Message_driver = webdriver.Firefox(executable_path=PATH)
    Message_driver = Alibaba.login(Message_driver , username , password)

    return render_template('output.html', message = "Output:" , show=False )


@app.route('/output', methods=['POST', 'GET'])
def output():
    if not get_status():
        return render_template('main_page/index.html')

    global username, password, url, temp1, temp2, temp3, Message_driver , Main_driver

    Temp = [temp1 , temp2 , temp3]
    PATH ="/usr/bin/"+ username + "/geckodriver"
    Main_driver = webdriver.Firefox(executable_path=PATH)
    Main_driver = Alibaba.login(Main_driver, username, password)

    Main_driver, Message_driver, output, check = Alibaba.main(Main_driver, Message_driver, url, Temp, username)

    if check:
        return render_template('Captach.html', show=True, output=output)

    return render_template('output.html', message="Output:", show=True , output = output ,  timer=1)


@app.route('/register', methods=['POST'])
def register():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        dbHandler.insertUser(username, password)
        #users = dbHandler.retrieveUsers()
        AllowAccess(username)
        session['logged_in'] = True
        session['user'] = username
        return redirect(url_for('check'))


@app.route('/verify', methods=['POST'])
def verify():
    number = request.form['lnumber']
    print(number)
    try:                
        Info ,Table= ch.main(number)
    except Exception:
        print('failiure')
        return jsonify(messege="not found")
    else:
        backup_verifications.append({'name': Info[1] , 'Info':Info[2:], 'Table':Table})
        print('success')
        return jsonify(messege="success")


@app.route('/check', methods=['POST','GET'])
def check():
    if not get_status():
        return render_template('main_page/index.html')

    if (get_status()) and (request.method == 'GET'):
        try:
            data = backup_verifications.pop(-1)
            return render_template('dashboard/check_dashboard.html', name=data['name'] , Info=data['Info'] ,Table=data['Table'])
        except:
            return render_template('dashboard/licence_dashboard.html')

    number = request.form['lnumber']
    try: 
        Info ,Table= ch.main(number)
        return render_template('dashboard/check_dashboard.html', name=Info[1] , Info=Info[2:] ,Table=Table)
    except Exception as e:
        print(e)
        messege="unable to load page"
        return render_template('dashboard/licence_dashboard.html', messege=messege)


@app.route('/alibaba/script', methods=['POST', 'GET'])
def alibaba_script():
    if not get_status():
        return render_template('main_page/index.html')
    return render_template('dashboard/script_dashboard.html', user=username)


@app.route('/', methods=['POST', 'GET'])
def home():
    # if requst is get then user needs a non logged in home page

    if (not get_status()) and (request.method == 'GET'):
        return render_template('main_page/index.html')

    if (get_status()) and (request.method == 'GET'):
        return render_template('dashboard/licence_dashboard.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #dbHandler.insertUser(username, password)
        users = dbHandler.retrieveUsers()

        Us = (username ,password)
        print(Us in users,Us)

        if (Us in users):
            session['logged_in'] = True
            session['user'] = username
            return redirect(url_for('home'))
        else:
            message = "User Name Or password is incorrect TRY AGAIN"
            return render_template('main_page/index.html', message=message)
    else:
        message =''
        session['logged_in'] = False
        return render_template('main_page/index.html', message = message)


@app.route("/logout")
def logout():
    session['logged_in'] = False
    session['user'] = None
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
