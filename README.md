# Atelier Visuel — Site d'inscription

Site Flask pour l'inscription à la formation Photoshop & Illustrator, avec
instructions de paiement (Wave / Orange Money) puis redirection vers le
groupe WhatsApp.

## Lancer le site sur ton ordinateur

1. Installe Python 3 si ce n'est pas déjà fait.
2. Dans un terminal, place-toi dans ce dossier :
   ```
   cd atelier_visuel
   ```
python3 -m venv my_env
source venv/bin/activate      # (Windows: venv\Scripts\activate)
pour le cas de bash dans windows: 
# Pour activer l'environnement "venv"
source venv/Scripts/activate

# Ou pour activer l'environnement "my_env"
source my_env/Scripts/activate

pip install -r requirements.txt
python3 app.py

3. Installe les dépendances :
   ```
   pip install -r requirements.txt
   ```
4. Lance le site :
   ```
   python3 app.py
   ```
5. Ouvre ton navigateur à l'adresse : `http://localhost:5000`

6. Page admin (/admin?cle=atelier2026) pour voir 
   la liste des inscrits et leur statut de paiement

Les inscriptions sont automatiquement enregistrées dans un fichier
`inscriptions.db` (créé au premier lancement) dans ce même dossier.

## Voir la liste des inscrits

Va à l'adresse :
```
http://localhost:5000/admin?cle=atelier2026
```

**Important : change ce mot de passe** avant de mettre le site en ligne.
Il se trouve dans `app.py`, ligne `ADMIN_CLE = "atelier2026"`.

## Modifier les informations (prix, numéros, lien WhatsApp)

Tout est regroupé en haut du fichier `app.py`, dans la section
"Configuration" :
- `FORMATION_NOM`
- `PRIX_FCFA`
- `NUMERO_WAVE` / `NUMERO_OM`
- `LIEN_WHATSAPP`
- `ADMIN_CLE`

## Mettre le site en ligne (pour que d'autres y accèdent)

Ce site tourne en local pour l'instant. Pour le rendre accessible sur
internet, il faut l'héberger. Options simples et gratuites/peu chères :

- **PythonAnywhere** (gratuit pour démarrer, simple pour Flask)
- **Render.com** (gratuit avec quelques limites)
- **Railway.app**

Dans tous les cas : dépose ces fichiers, indique `app.py` comme point
d'entrée, et assure-toi que `requirements.txt` est bien détecté pour
installer Flask automatiquement.

## Important à savoir

- Le site ne se connecte à **aucune vraie API de paiement**. Il affiche
  simplement tes numéros Wave / Orange Money et attend une confirmation
  manuelle de l'utilisateur. Vérifie donc toi-même les paiements reçus
  avant de considérer une inscription comme réellement payée — la page
  admin te sert d'aide-mémoire, pas de preuve de paiement.
- Pense à changer `ADMIN_CLE` avant de partager le site publiquement.
