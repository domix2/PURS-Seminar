from flask import Flask,render_template,request,redirect,url_for,session,jsonify
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
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM izmjereni_rezultati"
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            # Convert the results to a list of dictionaries for easy handling in the template
            result_list = []
            for row in results:
                result_list.append({
                    "id": row[0],
                    "temperatura": row[1],
                    "vlaga": row[2],
                    "vrijeme": row[3]
                })
            return render_template('rezultati.html', title='Očitani rezultati', results=result_list)
        except MySQLdb.Error as e:
            return render_template('rezultati.html', title='Očitani rezultati', error=f"Database error: {e}")
    else:
        return render_template('rezultati.html', title='Očitani rezultati', error="Failed to connect to the database")


@app.get('/obrada')
def pozivanje_podataka():
    response = render_template('obrada.html', title='Dohvat Podataka')
    return response

@app.post('/obrada')
def data_api():
    if request.is_json:
        data = request.get_json()
        temperatura = data.get('temperatura')
        vlaga = data.get('vlaga')

        if connection:
            try:
                cursor = connection.cursor()
                query = "INSERT INTO izmjereni_rezultati (temperatura, vlaga) VALUES (%s, %s)"
                cursor.execute(query, (temperatura, vlaga))
                connection.commit()
                cursor.close()
                # Don't close the connection here, as it should remain open for further requests
                return jsonify({"message": "Data inserted successfully"}), 201
            except MySQLdb.Error as e:
                return jsonify({"message": f"Database error: {e}"}), 500
        else:
            return jsonify({"message": "Failed to connect to the database"}), 500
    else:
        return jsonify({"message": "Request body must be JSON"}), 400



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)