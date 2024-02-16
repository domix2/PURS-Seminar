from flask import Flask,render_template,request,redirect,url_for,session
import MySQLdb

app = Flask ("Seminar")

app.secret_key = '_5#y2L"F4Q8z-n-xec]/'

connection = MySQLdb.connect(host="localhost", user="domi", passwd ="1234", db="seminar")
cursor = connection.cursor()

@app.get('/')
def odabir():
    username = request.args.get('user', 'Guest')
    response = render_template('main.html', title = 'Seminar', username = username)
    return response

@app.get('/login')
def login():
    response = render_template('login.html', title = 'Prijava')
    return response

@app.post('/login')
def login_user():
    username = request.form.get('newUsername')
    password = request.form.get('newPassword')
    query = "SELECT * FROM korisnik WHERE username = %s AND password = %s"
    cursor.execute(query,(username, password))
    connection.commit()
    response = render_template('pocetna.html', username=username)
    return response

@app.get('/register')
def register():
    response = render_template('register.html', title = 'Registracija')
    return response

@app.post('/register')
def register_user():
     ime = request.form.get('newName')
     prezime = request.form.get('newPrezime')
     username = request.form.get('newUsername')
     password = request.form.get('newPassword')
     # korisnik je definiran i ima sve ovlasti #
     query = "INSERT INTO korisnik (ime, prezime, username, password) VALUES (%s,%s,%s,%s)"
     cursor.execute(query, (ime, prezime, username, password))
     connection.commit()
     connection.close()
     response = render_template('login.html', title = 'Pocetna stranica')
     return response 

@app.get('/home')
def pocetna():
    response = render_template('pocetna.html', title = 'Pocetna stranica')
    return response

@app.get('/izmjerena_temperatura')
def temperatura():
    response = render_template('temperatura.html', title = 'izmjerena_temperatura')
    return response

@app.get('/izmjerena_vlaga')
def vlaga():
    response = render_template('vlaga.html', title = 'izmjerena_vlaga')
    return response

@app.get('/rezultati')
def rezultati():
    response = render_template('rezultati.html', title='Očitani rezultati')
    return response

@app.get('/obrada')
def pozivanje_podataka():
    response = render_template('obrada.html', title='Dohvat Podataka')
    return response


#@app.post('/login') #za testiranje prijave i preusmjeravanje na početnu stranicu 
#def logintest1():
    #username = request.form.get('username')
    #password = request.form.get('password')

    #if username == 'PURS' and password == '1234':
        #session['username'] = username
        #return redirect(url_for('pocetna'))
    #else:
        #return redirect(url_for('odabir'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)