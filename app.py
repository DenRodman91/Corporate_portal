from flask import Flask, render_template,  request, jsonify, make_response, send_file, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
import base64
import pandas as pd
import sqlite3
from io import BytesIO
from datetime import timedelta
from flask import session
import datetime
from datetime import datetime
from werkzeug.utils import secure_filename
import logging
import telebot
import subprocess





current_date = datetime.now()
formatted_date = current_date.strftime("%d.%m")

application = Flask(__name__)
application.config['SECRET_KEY'] = '121212'
login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = "login"
class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username

application.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=72)
users = {
    'admin': User("admin0206199341", "Главный Администратор")
}
dostup = {
    'Главный Администратор':[1000]
}
@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@application.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_key = request.form['user_key']

        user = users.get(user_key)
        if user:
            login_user(user)
            session.permanent = True
            return redirect(url_for('index'))

    return '''<form method="post">
               Enter your key: <input type="text" name="user_key"><br>
               <input type="submit" value="Login">
             </form>'''

logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
@application.route("/", methods=['GET', 'POST'])
@login_required
def index():
    current_date = datetime.now()
    formatted_date = current_date.strftime("2000-%m-%d")
    username = current_user.username
    dost = dostup[username]
    conn = sqlite3.connect('db/news_c.db')
    df = pd.read_sql_query("SELECT * FROM news", conn)
    df['text'] = df['text'].str.replace("\n", "<br>")
    df  = df.iloc[::-1] 
    conn2 = sqlite3.connect('db/team.db')
    df_dr = pd.read_sql_query("SELECT * FROM team", conn2)
    df_dr = df_dr.dropna(subset=['ДатаРождения'])
    df_dr = df_dr.sort_values(by='ДатаРождения') 
    return render_template('index.html', df_news = df, 
                                        df_dr = df_dr,
                                        dost = dost,
                                        today = str(formatted_date))



@application.route("/about", methods=['GET', 'POST'])
@login_required
def about():
    username = current_user.username
    dost = dostup[username]
    return render_template('about.html', dost = dost)




@application.route("/employee/<int:id>", methods=['GET', 'POST'])
@application.route("/employee", methods=['GET', 'POST'])
@login_required
def employee(id = 0):
    username = current_user.username
    dost = dostup[username]
    if id == 0:
        conn = sqlite3.connect('db/team.db')
        df = pd.read_sql_query("SELECT * FROM team WHERE Статус = 'Активно работаю'", conn)
        return render_template('employee.html', df_all = df, dost = dost)
    else:
        conn = sqlite3.connect('db/team.db')
        df = pd.read_sql_query("SELECT * FROM team", conn)
        df = df[df['ID'] == id]
        return render_template('employee_body.html', df_all = df, dost = dost)



@application.route('/upload', methods=['POST'])
@login_required
def upload_files():
    import processing
    text_valueYM = request.form.get('dataYM', '0')
    text_valueOZ = request.form.get('dataOZ', '0')
    hraneniePI = request.form.get('hraneniePI', '')
    reklamaPI = request.form.get('reklamaPI', '0')
    priemkaPI = request.form.get('priemkaPI', '0')
    otherPI = request.form.get('otherPI', '0')
    otherotherPI = request.form.get('otherotherPI', '0')
    hranenieKOL = request.form.get('hranenieKOL', '0')
    reklamaKOL = request.form.get('reklamaKOL', '0')
    priemkaKOL = request.form.get('priemkaKOL', '0')
    otherKOL = request.form.get('otherKOL', '0')
    otherotherKOL = request.form.get('otherotherKOL', '0')
    hranenieGIZ = request.form.get('hranenieGIZ', '')
    reklamaGIZ = request.form.get('reklamaGIZ', '0')
    priemkaGIZ = request.form.get('priemkaGIZ', '0')
    otherGIZ = request.form.get('otherGIZ', '0')
    otherotherGIZ = request.form.get('otherotherGIZ', '0')
    hranenieUL = request.form.get('hranenieUL', '')
    reklamaUL = request.form.get('reklamaUL', '0')
    priemkaUL = request.form.get('priemkaUL', '0')
    otherUL = request.form.get('otherUL', '0')
    otherotherUL = request.form.get('otherotherUL', '0')
    hraneniePER = request.form.get('hraneniePER', '0')
    reklamaPER = request.form.get('reklamaPER', '0')
    priemkaPER = request.form.get('priemkaPER', '0')
    otherPER = request.form.get('otherPER', '0')
    otherotherPER = request.form.get('otherotherPER', '0')
    dfs = []
    upload_folder = 'downloads'
    # Убедитесь, что директория существует, иначе создайте её
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    uploaded_files = request.files
    
    for input_name, file in uploaded_files.items():
        if file and file.filename:
            cab = input_name
            filename = secure_filename(input_name + os.path.splitext(file.filename)[1])
            print(input_name)
            save_path = os.path.join(upload_folder, filename)
            file.save(save_path)
            # Теперь, когда файл сохранен, мы можем его прочитать
            df = pd.read_excel(save_path, header=0, engine='openpyxl')
            if input_name == 'WBPIAT':
                ch = processing.reestrMP(df, cab, [hraneniePI, reklamaPI, priemkaPI, otherPI, otherotherPI])
            elif input_name =='WBKOL':
                ch = processing.reestrMP(df, cab, [hranenieKOL, reklamaKOL, priemkaKOL, otherKOL, otherotherKOL])
            elif input_name =='WBGIZ':
                ch = processing.reestrMP(df, cab, [hranenieGIZ, reklamaGIZ, priemkaGIZ, otherGIZ, otherotherGIZ])
            elif input_name =='WBUL':
                ch = processing.reestrMP(df, cab, [hranenieUL, reklamaUL, priemkaUL, otherUL, otherotherUL])
            elif input_name =='WBPER':
                ch = processing.reestrMP(df, cab, [hraneniePER, reklamaPER, priemkaPER, otherPER, otherotherPER])    
            elif input_name =='OZPIAT':
                ch = processing.reestrMP(df, cab, [0, 0, 0, 0, 0]) 
            dfs.append(ch)
    try:    
        df_combined = pd.concat(dfs, ignore_index=True)
        return df_combined.to_html(border = 0, classes='myTable')
    except:
        return ch.to_html(border = 0, classes='myTable')  
   


import dash
import dash_bootstrap_components as dbc
import daahboard_app
app = dash.Dash(__name__, server=application, url_base_pathname='/dashboard/', external_stylesheets=[dbc.themes.BOOTSTRAP])
daahboard_app.dash(app)


@application.route('/y')
@login_required
def y():
    username = current_user.username
    dost = dostup[username]
    return render_template('y.html', dost = dost)


@application.route('/DownloadReports')
@login_required
def DownloadReports():
#BLOCK for Reports MP ___________________
    conn = sqlite3.connect('db/reports.db')
    # Запрос на выборку данных из определенной таблицы
    query = "SELECT * FROM 'reportsMP'"
    query2 = "SELECT * FROM 'reportsOZ'"
# Загрузка данных в DataFrame
    df = pd.read_sql_query(query, conn)
    df2 = pd.read_sql_query(query2, conn)

#BLOCK for Realizations MP ___________________
    # Сохранение DataFrame в Excel в памяти
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='WB reports')
        df2.to_excel(writer, sheet_name='OZON reports')

    # Перемещение указателя в начало потока
    output.seek(0)

    # Создание ответа
    response = make_response(send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
    
    # Установка заголовка Content-Disposition для определения имени файла
    response.headers['Content-Disposition'] = 'attachment; filename=report.xlsx'

    return response


@application.route('/createnews', methods=['GET','POST'])
@login_required
def createnews():
    if request.method == 'POST':
        conn = sqlite3.connect('db/news_c.db')
        cur = conn.cursor()
        
        # Получение данных из формы
        category = request.form['cat']
        text = request.form['text']
        # Для файла используйте request.files
        photo = request.files.get('fotonews')
        filename = photo.filename
        current_date = datetime.now()
        formatted_date = current_date.strftime("%d.%m.%Y")
        cur.execute(""" INSERT INTO news(category, text, foto, data) VALUES (?,?,?,?)""", (category, text, filename, formatted_date))
        conn.commit()
        conn.close()
        save_path = os.path.join(f'static/img' , filename)

        # Сохранение файла
        TOKEN = 'YOUR_TOKEN'
        bot = telebot.TeleBot(TOKEN, parse_mode='html')
        with open(save_path, 'wb') as file:
            file.write(photo.read())
        with open(f'static/img/{filename}', 'rb') as document:
            bot.send_photo(chat_id='chat_id', photo=document, caption=text)
        
    return render_template('createnews.html')

@application.route('/newEmpl', methods=['GET','POST'])
@login_required
def newEmpl():
    if request.method == 'POST':
        fio = request.form.get('ФИО')
        birthdate = request.form.get('ДатаРождения')
        telegram = request.form.get('Телеграм')
        email = request.form.get('Почта')
        position = request.form.get('Должность')
        department = request.form.get('Отдел')
        phone = request.form.get('Телефон')
        photo = request.form.get('Фото')
        facts = request.form.get('Факты')
        hired_date = request.form.get('ПринятДата')
        category = request.form.get('Категория')
        work = request.form.get('Работа')

        conn = sqlite3.connect('db/team.py')
        cur = conn.cursor()    
        cur.execute(""" INSERT INTO team(ФИО, ДатаРождения, Телеграм, Почта, Должность, Отдел, Телефон, Фото, Факты, ПринятДата, Категория) VALUES (?,?,?,?,?,?,?,?,?,?,?)""", (fio, birthdate, telegram, email, position, department, phone, photo, facts, hired_date, category, work))





@application.route('/robot4', methods=['POST', 'GET'])
def robot5():
    
    subprocess.run(['/usr/bin/python3', '/home/devel/RZV_get_only.py'], check=True)
    return 'Готово, проверяйте!'
    
@application.route('/otzivi', methods=['POST', 'GET'])
def robot4():
    import all_otzivi
    all_otzivi.collect()
    return 'Done'

@application.route('/robot2', methods=['POST', 'GET'])
def robot2():
    subprocess.run(['/usr/bin/python3', '/home/devel/COPY_Svods.py'], check=True)
    return 'Готово, проверяйте!'

@application.route('/sborka', methods=['POST', 'GET'])
def robot6():
    subprocess.run(['/usr/local/bin/python3.10', '/home/devel/SQL/general.py'], check=True)
    return 'Готово, проверяйте!'


@application.route('/updatesqlgoogle', methods=['POST', 'GET'])
def robot7():
    subprocess.run(['/usr/local/bin/python3.10', 'from_SQL_to_Google/updateeveryone.py'], check=True)
    return 'Готово, проверяйте!'


#_____API__________API__________API__________API__________API____________________API____________________API____________________API____________________API__________
import gspread
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
import time
def to_google(id, shname, df, xy):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = None
    if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    try:
        # Загрузите учетные данные для доступа к Google Sheets API
        gc = gspread.authorize(creds)

        spreadsheet = gc.open_by_key(id)
        worksheet = spreadsheet.worksheet(shname)
        # # Преобразовать DataFrame в двумерный массив строк
        data_to_append = df.astype(str).values.tolist()
        worksheet.update(xy, data_to_append, value_input_option='USER_ENTERED')
        
    except HttpError as err:
        print(err)

from sqlalchemy import create_engine, text
@application.route('/apigoogle', methods=['GET'])
def query_data2():
        # Получаем параметры из строки запроса
    param1 = request.args.get('datestart', default=None, type=str)
    param2 = request.args.get('dateend', default=None, type=str)
    param3 = request.args.get('id', default=None, type=str) #id google tabl
    param4 = request.args.get('shname', default=None, type=str)#sheet name
    param5 = request.args.get('view', default=None, type=str)#name view
    # connection_string = f"mysql+pymysql://root:@7ehaTCvJr44rvikB localhost:33066"
    engine = create_engine('mysql+pymysql://root:passwordB@localhost:PORT/NAME')
    sql_query = text(f"""
    SELECT * FROM {param5} 
    WHERE `ДатаЗаказа` COLLATE utf8mb4_unicode_ci >= :param1 
    AND `ДатаЗаказа` COLLATE utf8mb4_unicode_ci <= :param2
    """)

    # Выполнение запроса с безопасной передачей параметров
    df = pd.read_sql_query(sql_query, engine, params={'param1': param1, 'param2': param2, 'param5': param5 })
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            df[column] = df[column].apply(lambda x: f'{x}'.replace('.', ',') if not pd.isnull(x) else x)
    to_google(id=param3, shname=param4, df=df, xy='A2')

    return 'ready'


@application.route('/apiposition', methods=['GET'])
def query_data3():
        # Получаем параметры из строки запроса
    param1 = request.args.get('datestart', default=None, type=str)
    param2 = request.args.get('dateend', default=None, type=str)
    param3 = request.args.get('id', default=None, type=str) #id google tabl
    param4 = request.args.get('shname', default=None, type=str)#sheet name
    param5 = request.args.get('view', default=None, type=str)#name view
    engine = create_engine('mysql+pymysql://root:passwordB@localhost:PORT/NAME')
    sql_query = text(f"""
    SELECT * FROM {param5} 
    WHERE `Дата` COLLATE utf8mb4_unicode_ci >= :param1 
    AND `Дата` COLLATE utf8mb4_unicode_ci <= :param2
    """)

    # Выполнение запроса с безопасной передачей параметров
    df = pd.read_sql_query(sql_query, engine, params={'param1': param1, 'param2': param2, 'param5': param5 })
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            df[column] = df[column].apply(lambda x: f'{x}'.replace('.', ',') if not pd.isnull(x) else x)
    to_google(id=param3, shname=param4, df=df, xy='B2')

    return 'ready'



@application.route('/apisklad', methods=['GET'])
def query_data4():
        # Получаем параметры из строки запроса
    param3 = request.args.get('id', default=None, type=str) #id google tabl
    param4 = request.args.get('shname', default=None, type=str)#sheet name
    param5 = request.args.get('view', default=None, type=str)#name view
    engine = create_engine('mysql+pymysql://root:passwordB@localhost:PORT/NAME')
    sql_query = text(f"""
    SELECT * FROM {param5} 
    """)
    # Выполнение запроса с безопасной передачей параметров
    df = pd.read_sql_query(sql_query, engine, params={'param5': param5 })
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            df[column] = df[column].apply(lambda x: f'{x}'.replace('.', ',') if not pd.isnull(x) else x)
    to_google(id=param3, shname=param4, df=df, xy='A3')

    return 'ready'

@application.route('/apitridney', methods=['GET'])
def query_data7():
        # Получаем параметры из строки запроса
    param3 = request.args.get('id', default=None, type=str) #id google tabl
    param4 = request.args.get('shname', default=None, type=str)#sheet name
    engine = create_engine('mysql+pymysql://root:passwordB@localhost:PORT/NAME')
    sql_query = text(f"""
    SELECT * FROM 30днейсуммы
    """)
    # Выполнение запроса с безопасной передачей параметров
    df = pd.read_sql_query(sql_query, engine)
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            df[column] = df[column].apply(lambda x: f'{x}'.replace('.', ',') if not pd.isnull(x) else x)
    to_google(id=param3, shname=param4, df=df, xy='A3')

    return 'ready'



@application.route('/apidevdney', methods=['GET'])
def query_data8():
        # Получаем параметры из строки запроса
    param3 = request.args.get('id', default=None, type=str) #id google tabl
    param4 = request.args.get('shname', default=None, type=str)#sheet name
    param5 = request.args.get('view', default=None, type=str)#name view
    engine = create_engine('mysql+pymysql://root:passwordB@localhost:PORT/NAME')
    sql_query = text(f"""
    SELECT * FROM 90днейсуммы
    """)
    # Выполнение запроса с безопасной передачей параметров
    df = pd.read_sql_query(sql_query, engine)
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            df[column] = df[column].apply(lambda x: f'{x}'.replace('.', ',') if not pd.isnull(x) else x)
    to_google(id=param3, shname=param4, df=df, xy='A3')

    return 'ready'



@application.route('/apidolya', methods=['GET'])
def query_data5():
        # Получаем параметры из строки запроса
    param3 = request.args.get('id', default=None, type=str) #id google tabl
    param4 = request.args.get('shname', default=None, type=str)#sheet name
    param5 = request.args.get('view', default=None, type=str)#name view
    engine = create_engine('mysql+pymysql://root:passwordB@localhost:PORT/NAME')
    sql_query = text(f"""
    SELECT * FROM {param5} 
    """)
    # Выполнение запроса с безопасной передачей параметров
    df = pd.read_sql_query(sql_query, engine, params={'param5': param5 })
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            df[column] = df[column].apply(lambda x: f'{x}'.replace('.', ',') if not pd.isnull(x) else x)
    to_google(id=param3, shname=param4, df=df, xy='A1')

    return 'ready'




@application.route('/apividacha', methods=['GET'])
def query_data6():
        # Получаем параметры из строки запроса
    param3 = request.args.get('id', default=None, type=str) #id google tabl
    param4 = request.args.get('shname', default=None, type=str)#sheet name
    param5 = request.args.get('view', default=None, type=str)#name view
    engine = create_engine('mysql+pymysql://root:passwordB@localhost:PORT/NAME')
    sql_query = text(f"""
    SELECT * FROM {param5} 
    """)
    # Выполнение запроса с безопасной передачей параметров
    df = pd.read_sql_query(sql_query, engine, params={'param5': param5 })
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            df[column] = df[column].apply(lambda x: f'{x}'.replace('.', ',') if not pd.isnull(x) else x)
    to_google(id=param3, shname=param4, df=df, xy='B3')

    return 'ready'




@application.route('/addart', methods=['POST'])
def addart():
    if request.is_json:
        # Получаем JSON-данные
        data = request.get_json()
        # Допустим, вы хотите получить имя листа и список данных
        sheet_name = data.get('sheetname', 'Не указано')
        sheet_data = data.get('data', [])
        engine = create_engine('mysql+pymysql://root:passwordB@localhost:PORT/NAME')
        df = pd.DataFrame(sheet_data)
        df['ДатаДобавленияМатрицу'] = pd.to_datetime(df['ДатаДобавленияМатрицу'], dayfirst=True).dt.strftime('%Y-%m-%d')
        # df['ДатаОкончанияДоговораАП	'] = pd.to_datetime(df['ДатаОкончанияДоговораАП	'], dayfirst=True).dt.strftime('%Y-%m-%d')

        try:
            df.to_sql(name=sheet_name, con=engine, if_exists='append', index=False)
        except Exception as e:
            return jsonify({"success": False, "message": e}), 400
        # Отправляем ответ клиенту
        return jsonify({"success": True, "message": "Данные успешно получены"}), 200
    else:
        return jsonify({"success": False, "message": "Неверный формат данных"}), 400


    



import xml.etree.ElementTree as ET
import requests
@application.route('/apicb', methods=['GET'])
def valuta():
    param3 = request.args.get('id', default=None, type=str) #id google tabl
    param4 = request.args.get('shname', default=None, type=str)#sheet name
    date = datetime.now().strftime("%d.%m.%Y")
    url_doll = f"http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=01.02.2023&date_req2={date}&VAL_NM_RQ=R01235"

    url_uan = f"http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=01.02.2023&date_req2={date}&VAL_NM_RQ=R01375"

    url_eu = f"http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=01.02.2023&date_req2={date}&VAL_NM_RQ=R01239"

    url_dir = f"http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=01.02.2023&date_req2={date}&VAL_NM_RQ=R01230"

    url_gdol = f"http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=01.02.2023&date_req2={date}&VAL_NM_RQ=R01200"

    response1 = requests.get(url_doll)
    response2 = requests.get(url_uan)
    response3 = requests.get(url_eu)
    response4 = requests.get(url_dir)
    response5 = requests.get(url_gdol)
    # Разбор XML
    root1 = ET.fromstring(response1.content)
    root2 = ET.fromstring(response2.content)
    root3 = ET.fromstring(response3.content)
    root4 = ET.fromstring(response4.content)
    root5 = ET.fromstring(response5.content)

    # Собираем данные для DataFrame
    data = []
    uan = []
    dol = []
    eu = []
    dir = []
    gondol = []

    for record in root1.findall('.//Record'):
        date = record.get('Date')
        data.append(date)

    for record in root2.findall('.//Record'):
        value = float(record.find('Value').text.replace(',','.'))/float(record.find('Nominal').text.replace(',','.'))
        
        uan.append(str(value).replace('.',','))

    for record in root1.findall('.//Record'):
        value = float(record.find('Value').text.replace(',','.'))/float(record.find('Nominal').text.replace(',','.'))
        dol.append(str(value).replace('.',','))

    for record in root3.findall('.//Record'):
        value = float(record.find('Value').text.replace(',','.'))/float(record.find('Nominal').text.replace(',','.'))
        eu.append(str(value).replace('.',','))

    for record in root4.findall('.//Record'):
        value = float(record.find('Value').text.replace(',','.'))/float(record.find('Nominal').text.replace(',','.'))
        dir.append(str(value).replace('.',','))

    for record in root5.findall('.//Record'):
        value = float(record.find('Value').text.replace(',','.'))/float(record.find('Nominal').text.replace(',','.'))
        gondol.append(str(value).replace('.',','))
    df = pd.DataFrame({
        'Дата': data,
        'Доллар': dol,
        'Евро': eu,
        'Юань': uan,
        'ГонконгскийДоллар': gondol,
        'Дирхам': dir
    })

    # Преобразование типов данных, если необходимо
    df['Дата'] = pd.to_datetime(df['Дата'], format='%d.%m.%Y')
    to_google(id = param3, shname = param4, df = df, xy='L2')
    return 'ready'


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5010, debug=True)


