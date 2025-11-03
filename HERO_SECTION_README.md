# Gestion de la Section Hero - Page d'Accueil

## 📋 Vue d'ensemble

La section hero de la page d'accueil est maintenant entièrement programmable via la base de données. Vous pouvez modifier le titre, le sous-titre, l'image de fond et l'opacité de l'overlay directement depuis l'interface d'administration Django ou via les scripts de gestion.

## 🎯 Fonctionnalités

### ✅ Modèle HomePageHero
- **Titre principal** : Texte affiché en grand sur l'image
- **Sous-titre** : Description sous le titre principal
- **Image de fond** : Image qui apparaît en arrière-plan
- **Opacité overlay** : Contrôle la transparence du texte sur l'image (0-1)
- **Statut actif** : Une seule section hero peut être active à la fois

### ✅ Interface d'Administration
- Gestion complète via l'admin Django
- Prévisualisation des modifications
- Validation automatique (une seule section active)
- Upload d'images facilité

### ✅ Scripts de Gestion
- Script de création automatique avec l'image existante
- Script de gestion en ligne de commande
- Mise à jour rapide des contenus

## 🚀 Utilisation

### Via l'Interface d'Administration

1. Connectez-vous à l'admin Django : `http://localhost:8000/admin/`
2. Allez dans **Website** → **Sections Hero de la page d'accueil**
3. Modifiez les champs souhaités :
   - **Titre principal** : Le texte principal affiché
   - **Sous-titre** : La description sous le titre
   - **Image de fond** : Upload d'une nouvelle image
   - **Opacité de l'overlay** : Valeur entre 0 (transparent) et 1 (opaque)
4. Sauvegardez les modifications

### Via les Scripts de Gestion

#### Lister les sections hero
```bash
python manage_hero.py list
```

#### Modifier le titre
```bash
python manage_hero.py title 1 "NOUVEAU TITRE"
```

#### Modifier le sous-titre
```bash
python manage_hero.py subtitle 1 "Nouveau sous-titre personnalisé"
```

#### Modifier l'opacité
```bash
python manage_hero.py opacity 1 0.7
```

#### Activer une section hero
```bash
python manage_hero.py activate 1
```

## 📁 Fichiers Modifiés

### Modèles (`website/models.py`)
- Ajout du modèle `HomePageHero`
- Méthodes de gestion automatique des sections actives
- Validation des données

### Vues (`website/views.py`)
- Import du nouveau modèle
- Ajout de `hero_section` au contexte de la page d'accueil

### Templates (`templates/website/index.html`)
- Section hero dynamique basée sur les données de la base
- Fallback vers l'image statique si aucune section n'est configurée
- Support de l'opacité personnalisée

### Administration (`website/admin.py`)
- Interface d'administration complète pour `HomePageHero`
- Validation et contraintes d'unicité
- Interface utilisateur optimisée

## 🔧 Scripts Utilitaires

### `create_default_hero.py`
Crée une section hero par défaut avec l'image existante `AZI GROUP.PNG`.

### `manage_hero.py`
Script de gestion en ligne de commande pour modifier rapidement les sections hero.

## 🎨 Personnalisation CSS

L'opacité de l'overlay est appliquée via le style inline :
```html
<div class="hero-overlay" style="opacity: {{ hero_section.overlay_opacity }};">
```

Vous pouvez également personnaliser les styles CSS dans `static/css/style.css` pour la classe `.hero-overlay`.

## 📝 Notes Techniques

- **Une seule section active** : Le système garantit qu'une seule section hero est active à la fois
- **Fallback automatique** : Si aucune section hero n'est configurée, le système utilise l'image statique par défaut
- **Upload d'images** : Les images sont stockées dans `media/homepage/`
- **Migrations** : Les migrations ont été créées et appliquées automatiquement

## 🚀 Prochaines Améliorations Possibles

- Support des images multiples avec rotation automatique
- Animations CSS personnalisables
- Support des vidéos de fond
- A/B testing des sections hero
- Intégration avec un CDN pour les images
