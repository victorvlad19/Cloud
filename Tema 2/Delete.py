import sqlite3

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
    count = 0
    # Verifica datele
    for row in rows:
        for d in data:
            if str(row[3]) == str(d):
                count+=1
    if count != len(data):
        return "404"
    else:
        pass

def delete_collection_music(data):
    # Conexiune cu baza de date
    try:
        conn = sqlite3.connect("music")
    except sqlite3.Error as e:
        print(e)
    # Preia datele
    cursor = conn.cursor()
    try:
        for d in data:
            cursor.execute("DELETE FROM music WHERE id=?",(d,))
            conn.commit()
    except:
        return "FAIL"
    return "OK"

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
    if ok != True:
        return "404"
    else:
        pass

def delete_specific_music(id):
    # Conexiune cu baza de date
    try:
        conn = sqlite3.connect("music")
    except sqlite3.Error as e:
        print(e)
    # Preia datele
    cursor = conn.cursor()
    print(id)
    try:
        cursor.execute("DELETE FROM music WHERE id=?", ((id),))
        conn.commit()
    except:
        return "FAIL"
    return "OK"