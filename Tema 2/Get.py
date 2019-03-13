import json

# Conexiune cu baza de date
import sqlite3

def get_all_music():
    # Conexiune cu baza de date
    try:
        conn = sqlite3.connect("music")
    except sqlite3.Error as e:
        print(e)
    # Preia datele
    all_data = []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM music")
    rows = cursor.fetchall()
    # Formateaza datele
    for row in rows:
        all_data.append(row)
    return json.dumps(all_data)

def get_specific_music(id):
    # Conexiune cu baza de date
    try:
        conn = sqlite3.connect("music")
    except sqlite3.Error as e:
        print(e)
    # Preia datele
    id_data = []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM music")
    rows = cursor.fetchall()
    # Formateaza datele
    for row in rows:
        if str(row[3]) == str(id):
            id_data.append(row)
    if not id_data:
        return "Nil"
    else:
        return json.dumps(id_data[0])

def get_title_music():
    # Conexiune cu baza de date
    try:
        conn = sqlite3.connect("music")
    except sqlite3.Error as e:
        print(e)
    # Preia datele
    all_data = []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM music")
    rows = cursor.fetchall()
    # Formateaza datele
    for row in rows:
        all_data.append(row[0])
    return json.dumps(all_data)

def get_artist_music():
    # Conexiune cu baza de date
    try:
        conn = sqlite3.connect("music")
    except sqlite3.Error as e:
        print(e)
    # Preia datele
    all_data = []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM music")
    rows = cursor.fetchall()
    # Formateaza datele
    for row in rows:
        all_data.append(row[1])
    return json.dumps(all_data)

def get_year_music():
    # Conexiune cu baza de date
    try:
        conn = sqlite3.connect("music")
    except sqlite3.Error as e:
        print(e)
    # Preia datele
    all_data = []
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM music")
    rows = cursor.fetchall()
    # Formateaza datele
    for row in rows:
        all_data.append(row[2])
    return json.dumps(all_data)