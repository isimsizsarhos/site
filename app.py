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

    mesaj_html = ""
    if sonuclar:
        for isim, mesaj in sonuclar:
            mesaj_html += f"""
            <div style="padding:12px 0; border-bottom:1px solid #e0e0e0;">
                <div style="font-size:13px; font-weight:500; color:#1e40af; margin-bottom:4px;">{isim}</div>
                <div style="font-size:15px; color:#333;">{mesaj}</div>
            </div>
            """
    else:
        mesaj_html = "<p style='color:#999; font-size:15px;'>Henüz mesaj yok.</p>"

    return f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
      <meta charset="UTF-8"/>
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <title>Mesajlar</title>
      <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
          font-family: Arial, sans-serif;
          background: #f5f5f5;
          min-height: 100vh;
          display: flex;
          justify-content: center;
          padding: 2rem 1rem;
        }}
        .kart {{
          background: white;
          border-radius: 12px;
          border: 1px solid #e0e0e0;
          max-width: 520px;
          width: 100%;
          overflow: hidden;
        }}
        .hero {{
          padding: 2rem 1.25rem;
          border-bottom: 1px solid #e0e0e0;
        }}
        .hero h1 {{ font-size: 20px; font-weight: 500; }}
        .hero p {{ font-size: 13px; color: #999; margin-top: 4px; }}
        .icerik {{ padding: 1.25rem; }}
        .footer {{
          text-align: center;
          padding: 1.25rem;
          font-size: 13px;
          color: #aaa;
          border-top: 1px solid #e0e0e0;
        }}
      </style>
    </head>
    <body>
      <div class="kart">
        <div class="hero">
          <h1>Gelen Mesajlar</h1>
          <p>{len(sonuclar)} mesaj</p>
        </div>
        <div class="icerik">
          {mesaj_html}
        </div>
        <div class="footer">
          <a href="/" style="color:#1e40af; text-decoration:none;">← Ana sayfaya dön</a>
        </div>
      </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))