# Guide pour envoyer le projet sur GitHub

## Prérequis
- Git installé (vous l'avez déjà installé)
- Compte GitHub : DizeAnalytics
- Email : dizeanalytics@gmail.com

## Étapes à suivre

### 1. Ouvrir Git Bash ou PowerShell en tant qu'administrateur

Si Git n'est pas reconnu dans PowerShell, utilisez **Git Bash** qui s'installe avec Git.

### 2. Configurer Git (une seule fois)

```bash
git config --global user.name "DizeAnalytics"
git config --global user.email "dizeanalytics@gmail.com"
```

### 3. Naviguer vers le dossier du projet

```bash
cd C:\Users\SURVEIL\Desktop\IBC_SARL
```

### 4. Initialiser le dépôt Git (si pas déjà fait)

```bash
git init
```

### 5. Vérifier le fichier .gitignore

Le fichier `.gitignore` existe déjà et exclut :
- `db.sqlite3` (base de données)
- `media/` (fichiers uploadés)
- `staticfiles/` (fichiers statiques collectés)
- `__pycache__/` (fichiers Python compilés)
- `.env` (variables d'environnement)

### 6. Ajouter tous les fichiers

```bash
git add .
```

### 7. Faire le premier commit

```bash
git commit -m "Initial commit - Projet IBC SARL BTP"
```

### 8. Créer le dépôt sur GitHub

1. Aller sur https://github.com/DizeAnalytics
2. Cliquer sur "New repository"
3. Nom du dépôt : `Ibcsarlbtp`
4. Description : "Site web IBC SARL BTP - Django"
5. Choisir **Public** ou **Private**
6. **NE PAS** cocher "Initialize with README" (le projet existe déjà)
7. Cliquer sur "Create repository"

### 9. Ajouter le remote GitHub

```bash
git remote add origin https://github.com/DizeAnalytics/Ibcsarlbtp.git
```

### 10. Pousser le code sur GitHub

```bash
git branch -M main
git push -u origin main
```

Si GitHub demande une authentification :
- Utilisez un **Personal Access Token** (PAT) au lieu du mot de passe
- Pour créer un PAT : GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token
- Donnez les permissions : `repo` (tous les droits sur les dépôts)

### 11. Vérifier sur GitHub

Allez sur https://github.com/DizeAnalytics/Ibcsarlbtp pour voir votre code.

## Commandes utiles pour la suite

### Voir l'état des fichiers
```bash
git status
```

### Ajouter des modifications
```bash
git add .
git commit -m "Description des modifications"
git push
```

### Voir l'historique
```bash
git log
```

## Notes importantes

⚠️ **Ne jamais commiter** :
- `db.sqlite3` (base de données)
- Fichiers dans `media/` (photos uploadées)
- Fichiers sensibles comme `.env` avec les clés secrètes

✅ **Fichiers à commiter** :
- Code source Python
- Templates HTML
- CSS et JavaScript
- `requirements.txt`
- `README.md`
- `.gitignore`

## En cas de problème

Si Git n'est pas reconnu :
1. Redémarrer le terminal/PowerShell
2. Vérifier que Git est dans le PATH : `where git` (dans PowerShell)
3. Utiliser Git Bash au lieu de PowerShell

Si erreur d'authentification :
- Utiliser un Personal Access Token au lieu du mot de passe
- Vérifier que le token a les bonnes permissions
