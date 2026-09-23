import sqlite3
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "inscriptions.db")

# ---- Configuration : modifie ces valeurs si besoin ----
FORMATION_NOM = "Atelier Visuel"
FORMATION_SOUS_TITRE = "Photoshop & Illustrator — une seule inscription"
PRIX_FCFA = 5000
NUMERO_WAVE = "78 446 21 39"
NUMERO_OM = "78 446 21 39"
NUMERO_2 = "78 650 85 10"
LIEN_WHATSAPP = "https://chat.whatsapp.com/JE9gBdTqzKI0SB3nXgcqtO?s=cl&p=i&mlu=4&ilr=4"
# Change ce mot de passe avant de partager le lien admin à qui que ce soit
ADMIN_CLE = os.environ.get("ADMIN_CLE")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS inscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            telephone TEXT NOT NULL,
            email TEXT NOT NULL DEFAULT '',
            niveau TEXT NOT NULL,
            moyen_paiement TEXT NOT NULL,
            date_inscription TEXT NOT NULL,
            paiement_confirme INTEGER DEFAULT 0
        )
        """
    )

    colonnes = [row["name"] for row in conn.execute("PRAGMA table_info(inscriptions)")]
    if "email" not in colonnes:
        conn.execute("ALTER TABLE inscriptions ADD COLUMN email TEXT NOT NULL '' ")
    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def inscription():
    erreurs = {}
    valeurs = {"nom": "", "telephone": "", "email": "", "niveau": "debutant", "moyen_paiement": "wave"}

    if request.method == "POST":
        valeurs["nom"] = request.form.get("nom", "").strip()
        valeurs["telephone"] = request.form.get("telephone", "").strip()
        valeurs["email"] = request.form.get("email", "").strip()
        valeurs["niveau"] = request.form.get("niveau", "debutant")
        valeurs["moyen_paiement"] = request.form.get("moyen_paiement", "wave")

        if len(valeurs["nom"]) < 2:
            erreurs["nom"] = "Indique ton nom complet."
        if len(valeurs["telephone"]) < 8:
            erreurs["telephone"] = "Indique un numéro de téléphone valide."
        if "@" not in valeurs["email"] or "." not in valeurs["email"]:
            erreurs["email"] = "Indique une adresse email valide."

        if not erreurs:
            conn = get_db()
            cur = conn.execute(
                """INSERT INTO inscriptions
                   (nom, telephone, email, niveau, moyen_paiement, date_inscription)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    valeurs["nom"],
                    valeurs["telephone"],
                    valeurs["email"],
                    valeurs["niveau"],
                    valeurs["moyen_paiement"],
                    datetime.now().strftime("%Y-%m-%d %H:%M"),
                ),
            )
            conn.commit()
            inscription_id = cur.lastrowid
            conn.close()
            return redirect(url_for("paiement", inscription_id=inscription_id))

    return render_template(
        "inscription.html",
        formation_nom=FORMATION_NOM,
        formation_sous_titre=FORMATION_SOUS_TITRE,
        prix=PRIX_FCFA,
        erreurs=erreurs,
        valeurs=valeurs,
    )


@app.route("/paiement/<int:inscription_id>")
def paiement(inscription_id):
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM inscriptions WHERE id = ?", (inscription_id,)
    ).fetchone()
    conn.close()
    if row is None:
        abort(404)

    return render_template(
        "paiement.html",
        formation_nom=FORMATION_NOM,
        prix=PRIX_FCFA,
        numero_wave=NUMERO_WAVE,
        numero_om=NUMERO_OM,
        numero2=NUMERO_2,
        inscrit=row,
        lien_whatsapp=LIEN_WHATSAPP,
    )


@app.route("/paiement/<int:inscription_id>/confirmer", methods=["POST"])
def confirmer_paiement(inscription_id):
    conn = get_db()
    conn.execute(
        "UPDATE inscriptions SET paiement_confirme = 1 WHERE id = ?",
        (inscription_id,),
    )
    conn.commit()
    conn.close()
    return redirect(lien_whatsapp_redirect())


def lien_whatsapp_redirect():
    return LIEN_WHATSAPP


@app.route("/admin")
def admin():
    cle = request.args.get("cle", "")
    if cle != ADMIN_CLE:
        abort(403)
    conn = get_db()
    inscrits = conn.execute(
        "SELECT * FROM inscriptions ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return render_template("admin.html", inscrits=inscrits, formation_nom=FORMATION_NOM)


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
