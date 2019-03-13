import json
import sqlite3

def check_specific_music(id):
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
    ok = False
    # Verifica datele
    for row in rows:
        if str(row[3]) == str(id):
            ok = True
    if ok == True:
        return "409"
    else:
        pass

def check_colection_music(data):
    # Conexiune cu baza de date
    try:
        conn = sqlite3.connect("music")
    except sqlite3.Error as e:
        print(e)
    # Preia datele
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM music")
    rows = cursor.fetchall()
    ok = False
    # Verifica datele
    for row in rows:
        for d in data:
            if str(row[3]) == str(d[3]):
                ok = True
    if ok == True:
        return "409"
    else:
        pass

def post_specific_music(id,data):
    # Conexiune cu baza de date
    try:
        conn = sqlite3.connect("music")
    except sqlite3.Error as e:
        print(e)
    # Preia datele
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO music (title, artist, year, id) VALUES (?,?,?,?)",(data[0],data[1],data[2],id))
        conn.commit()
    except:
        return "FAIL"
    return "OK"

def post_collection_music(data):
    # Conexiune cu baza de date
    try:
        conn = sqlite3.connect("music")
    except sqlite3.Error as e:
        print(e)
    # Preia datele
    cursor = conn.cursor()
    try:
        for d in data:
            cursor.execute("INSERT INTO music (title, artist, year, id) VALUES (?,?,?,?)",(d[0],d[1],d[2],d[3]))
            conn.commit()
    except:
        return "FAIL"
    return "OK"