# AZI GROUP - Site Web Dynamique

Site web moderne et dynamique pour AZI GROUP, développé avec Flask (Python).

## 🚀 Fonctionnalités

- **Site responsive** avec design moderne
- **Gestion dynamique du contenu** via interface d'administration
- **Système de contact** avec base de données
- **Actualités et blog** intégrés
- **Gestion des entreprises** du groupement
- **Interface d'administration** complète

## 📋 Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

## 🛠️ Installation

1. **Cloner ou télécharger le projet**
   ```bash
   cd AZI_GROUP
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancer l'application**
   ```bash
   python app.py
   ```

4. **Accéder au site**
   - Site principal : http://localhost:5000
   - Interface d'administration : http://localhost:5000/admin

## 📁 Structure du Projet

```
AZI_GROUP/
├── app.py                 # Application Flask principale
├── requirements.txt       # Dépendances Python
├── azigroup.db           # Base de données SQLite (créée automatiquement)
├── templates/            # Templates Jinja2
│   ├── base.html         # Template de base
│   ├── index.html        # Page d'accueil
│   ├── about.html        # Page À propos
│   ├── companies.html    # Page des entreprises
│   ├── contact.html      # Page de contact
│   ├── news.html         # Page des actualités
│   ├── news_detail.html  # Détail d'un article
│   └── admin/            # Templates d'administration
│       ├── dashboard.html
│       ├── contacts.html
│       ├── companies.html
│       └── news.html
├── static/               # Fichiers statiques
│   ├── css/
│   │   └── style.css     # Styles CSS
│   ├── js/
│   │   └── main.js       # JavaScript principal
│   └── images/           # Images du site
└── index.html            # Ancien fichier statique (référence)
```

## 🎯 Fonctionnalités Principales

### Site Public
- **Page d'accueil** : Présentation d'AZI GROUP avec actualités récentes
- **À propos** : Mission, valeurs et vision de l'entreprise
- **Nos Groupements** : Présentation des 4 entreprises du groupe
- **Actualités** : Blog et nouvelles du groupe
- **Contact** : Formulaire de contact fonctionnel

### Interface d'Administration
- **Tableau de bord** : Vue d'ensemble des statistiques
- **Gestion des contacts** : Consultation des messages reçus
- **Gestion des entreprises** : Modification des informations des groupements
- **Gestion des actualités** : Création et modification des articles

## 🗄️ Base de Données

Le site utilise SQLite avec les modèles suivants :

- **Contact** : Messages du formulaire de contact
- **Company** : Informations des entreprises du groupe
- **News** : Articles d'actualité

## 🎨 Personnalisation

### Modifier le Design
- Éditez `static/css/style.css` pour personnaliser l'apparence
- Les couleurs principales sont définies dans les variables CSS

### Ajouter du Contenu
- Utilisez l'interface d'administration pour gérer le contenu
- Ou modifiez directement les templates dans `templates/`

### Ajouter des Fonctionnalités
- Étendez `app.py` avec de nouvelles routes
- Créez de nouveaux modèles de données si nécessaire

## 🔧 Configuration

### Variables d'Environnement
Vous pouvez personnaliser l'application en modifiant les variables dans `app.py` :

```python
app.config['SECRET_KEY'] = 'votre-cle-secrete-ici'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///azigroup.db'
```

### Base de Données
La base de données SQLite est créée automatiquement au premier lancement avec des données d'exemple.

## 🚀 Déploiement

### Déploiement Local
```bash
python app.py
```

### Déploiement en Production
Pour un déploiement en production, considérez :
- Utiliser un serveur WSGI comme Gunicorn
- Configurer un serveur web comme Nginx
- Utiliser une base de données PostgreSQL ou MySQL
- Configurer HTTPS et la sécurité

## 📞 Support

Pour toute question ou problème :
- Email : contact@azigroup.com
- Téléphone : +223 XX XX XX XX

## 📄 Licence

© 2025 AZI GROUP. Tous droits réservés.

---

**AZI GROUP** - Excellence Opérationnelle au Service de l'Impact en Afrique de l'Ouest
