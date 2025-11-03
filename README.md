# AZI GROUP - Site Web (Django)

Site web moderne et dynamique pour AZI GROUP, développé avec Django.

## 🚀 Fonctionnalités

- **Site responsive** avec design moderne
- **Gestion de contenu** via l’interface d’administration Django
- **Formulaire de contact** avec stockage en base
- **Actualités / blog**
- **Gestion des entreprises** du groupement

## 📋 Prérequis

- Python 3.10+ (recommandé)
- pip
- virtualenv (recommandé)

## 🛠️ Installation (développement)

```bash
cd AZI_GROUP
python -m venv .venv
.venv\Scripts\activate        # Windows PowerShell
pip install -r requirements.txt

# Créer le fichier .env (facultatif mais recommandé)
# Voir l’exemple plus bas

# Appliquer les migrations
python manage.py migrate

# (Optionnel) Créer un superuser pour /admin
python manage.py createsuperuser

# Lancer le serveur de dev
python manage.py runserver
```

- Site: `http://localhost:8000`
- Admin: `http://localhost:8000/admin`

## ⚙️ Configuration

Créer un fichier `.env` à la racine (même dossier que `manage.py`) avec par exemple:

```
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
# DATABASE_URL=postgres://user:pass@host:5432/dbname  # si vous utilisez Postgres
```

Assurez-vous que ces variables sont lues dans `settings.py` (le projet peut déjà gérer cela, sinon utilisez `python-dotenv` ou `dj-database-url`).

## 📁 Structure (extrait)

```
AZI_GROUP/
├── azigroup_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── website/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/website/
├── templates/
├── static/                      # sources statiques (dev)
├── staticfiles/                 # collectstatic (prod) – ignoré par Git
├── media/                       # uploads – ignoré par Git
├── manage.py
└── requirements.txt
```

## 🗄️ Base de données

- Dev par défaut: SQLite (fichier `db.sqlite3`, ignoré par Git)
- Prod: utilisez Postgres/MySQL, configurez `DATABASE_URL` et les cred.

Appliquer les migrations:

```bash
python manage.py migrate
```

## 🎨 Fichiers statiques et médias

- En dev, servez via `runserver`.
- En prod, exécutez:

```bash
python manage.py collectstatic --noinput
```

Puis servez `staticfiles/` via votre serveur (Nginx, CDN, etc.). Les uploads utilisateurs vont dans `media/`.

> Remarque: `.gitignore` exclut `db.sqlite3`, `media/` et `staticfiles/` pour garder le dépôt léger.

## 🚀 Déploiement (aperçu)

- Définir `DJANGO_DEBUG=False` et `DJANGO_ALLOWED_HOSTS`
- Configurer une base managée (ex: Postgres) et les variables d’env
- Lancer les migrations et `collectstatic`
- Servir via WSGI/ASGI (ex: Gunicorn + Nginx)

## 📞 Support

Pour toute question ou problème :
- Email : contact@azigroup.com
- Téléphone : +223 XX XX XX XX

## 📄 Licence

© 2025 AZI GROUP. Tous droits réservés.

---

**AZI GROUP** - Excellence Opérationnelle au Service de l'Impact en Afrique de l'Ouest
