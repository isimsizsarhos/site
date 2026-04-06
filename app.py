from flask import Flask, request, redirect
import os
import sqlite3

app = Flask(__name__)

def veritabani_olustur():
    conn = sqlite3.connect("mesajlar.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mesajlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT NOT NULL,
            mesaj TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

veritabani_olustur()

@app.route("/")
def anasayfa():
    return open("index.html", encoding="utf-8").read()

@app.route("/mesaj-gonder", methods=["POST"])
def mesaj_gonder():
    isim = request.form.get("isim")
    mesaj = request.form.get("mesaj")
    conn = sqlite3.connect("mesajlar.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO mesajlar (isim, mesaj) VALUES (?, ?)", (isim, mesaj))
    conn.commit()
    conn.close()
    return redirect("/mesajlar")

@app.route("/mesajlar")
def mesajlar():
    conn = sqlite3.connect("mesajlar.db")
    cursor = conn.cursor()
    cursor.execute("SELECT isim, mesaj FROM mesajlar ORDER BY id DESC")
    sonuclar = cursor.fetchall()
    conn.close()

    html = "<h1>Gelen Mesajlar</h1>"
    if sonuclar:
        for isim, mesaj in sonuclar:
            html += f"<div><b>{isim}:</b> {mesaj}</div><hr>"
    else:
        html += "<p>Henüz mesaj yok.</p>"

    html += '<br><a href="/">Ana sayfaya dön</a>'
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
