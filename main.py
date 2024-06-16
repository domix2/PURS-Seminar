from flask import Flask,render_template,request,redirect,url_for,session
import MySQLdb

app = Flask ("Seminar")

app.secret_key = '_5#y2L"F4Q8z-n-xec]/'

connection = MySQLdb.connect(host="localhost", user="domi", passwd ="1234", db="seminar")
cursor = connection.cursor()

@app.get('/')
def odabir():
    response = render_template('main.html', title = 'Seminar')
    return response

@app.get('/login')
def login():
    response = render_template('login.html', title = 'Prijava')
    return response

@app.get('/logout')
def odjava():
    session.pop('username', None)
    response = render_template('login.html', title = 'Prijava')
    return response

@app.post('/login')
def login_user():
    username = request.form['username']
    password = request.form['password']

    if username and password:
        session['username'] = username

        query = "SELECT * FROM korisnik WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            print('uspješna prijava')
            return render_template('pocetna.html', username=username)
        else:
            print('neuspješna prijava')
            return render_template('login.html', title='Prijava', error='Netočno upisani podaci')

    return render_template('login.html', title='Prijava', error='Invalid form data')

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
     success_message = "Registracija uspješna."
     response = render_template('login.html', title='Prijava', success_message=success_message)
     return response 

@app.get('/home')
def pocetna():
    if 'username' in session:
        return render_template('pocetna.html', title='Pocetna stranica', username=session['username'])
    else:
        return redirect(url_for('login'))

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

@app.post('/obrada')
def pregled_podataka():
    return




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)