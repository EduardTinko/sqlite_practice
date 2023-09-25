import sqlite3

from flask import Flask, render_template
from faker import Faker


app = Flask(__name__)
fake = Faker()


@app.route('/')
def start():
    return f'Hello user'


def create_tables():
    with sqlite3.connect('tutorial.db') as con:
        cur = con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS customers (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, '
                    'firstname varchar, lastname varchar, email varchar, birthday int)')
        cur.execute('CREATE TABLE IF NOT EXISTS tracks (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, '
                    'title varchar, artist_name varchar, duration int, release_year int)')
        count_customers = list(cur.execute("SELECT * FROM customers"))
        count_track = list(cur.execute("SELECT * FROM tracks"))
        if not count_customers:
            filling_customers(100)
        if not count_track:
            filling_tracks(100)
        con.commit()


def filling_customers(count):
    date_customers = []
    for item in range(count):
        firstname = fake.first_name()
        lastname = fake.last_name()
        email = fake.email()
        birthday = fake.date()
        date_customers.append([firstname, lastname, email, birthday])
    with sqlite3.connect('tutorial.db') as con:
        cur = con.cursor()
        for item in date_customers:
            cur.execute('INSERT INTO customers(firstname, lastname, email, birthday) VALUES(?, ?, ?, ?)', item)


def filling_tracks(count):
    date_tracks = []
    for item in range(count):
        title = fake.catch_phrase()
        artist_name = fake.name()
        duration = fake.random_int(min=30, max=450)
        release_year = fake.year()
        date_tracks.append([title, artist_name, duration, release_year])
    with sqlite3.connect('tutorial.db') as con:
        cur = con.cursor()
        for item in date_tracks:
            cur.execute('INSERT INTO tracks(title, artist_name, duration, release_year) VALUES(?, ?, ?, ?)', item)


@app.route('/names')
def get_number_names():
    with sqlite3.connect('tutorial.db') as con:
        cur = con.cursor()
        names = cur.execute("SELECT firstname FROM customers")
        number_name = len(set(names))
        return f'<h2>Кількість унікальних імен: {number_name}<h2/>'


@app.route('/tracks/')
def get_number_tracks():
    with sqlite3.connect('tutorial.db') as con:
        cur = con.cursor()
        res = cur.execute("SELECT ID FROM tracks")
        number_tracks = len(res.fetchall())
        return f'<h2>Кількість треків: {number_tracks}<h2/>'


@app.route('/tracks-sec/')
def get_tracks():
    with sqlite3.connect('tutorial.db') as con:
        cur = con.cursor()
        res = cur.execute("SELECT * FROM tracks")
        tracks = res.fetchall()
        return render_template('tracks.html', tracks=tracks)


if __name__ == '__main__':
    create_tables()
    app.run()

