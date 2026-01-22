# Script PowerShell pour configurer Git et envoyer sur GitHub
# Exécuter dans PowerShell : .\setup_git.ps1

Write-Host "=== Configuration Git pour IBC SARL BTP ===" -ForegroundColor Cyan

# Vérifier si Git est installé
try {
    $gitVersion = git --version
    Write-Host "Git trouvé : $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "ERREUR : Git n'est pas installé ou pas dans le PATH" -ForegroundColor Red
    Write-Host "Veuillez installer Git depuis https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# Configuration Git
Write-Host "`nConfiguration de Git..." -ForegroundColor Cyan
git config --global user.name "DizeAnalytics"
git config --global user.email "dizeanalytics@gmail.com"

Write-Host "✓ Git configuré avec :" -ForegroundColor Green
Write-Host "  Nom : DizeAnalytics" -ForegroundColor White
Write-Host "  Email : dizeanalytics@gmail.com" -ForegroundColor White

# Vérifier si déjà un dépôt Git
if (Test-Path .git) {
    Write-Host "`n✓ Dépôt Git déjà initialisé" -ForegroundColor Green
} else {
    Write-Host "`nInitialisation du dépôt Git..." -ForegroundColor Cyan
    git init
    Write-Host "✓ Dépôt Git initialisé" -ForegroundColor Green
}

# Ajouter tous les fichiers
Write-Host "`nAjout des fichiers..." -ForegroundColor Cyan
git add .

# Vérifier les fichiers à commiter
Write-Host "`nFichiers à commiter :" -ForegroundColor Cyan
git status --short

# Faire le commit
Write-Host "`nCréation du commit..." -ForegroundColor Cyan
$commitMessage = "Initial commit - Projet IBC SARL BTP"
git commit -m $commitMessage

Write-Host "`n✓ Commit créé avec succès" -ForegroundColor Green

# Vérifier si le remote existe
$remoteExists = git remote | Select-String -Pattern "origin"
if ($remoteExists) {
    Write-Host "`nRemote 'origin' existe déjà" -ForegroundColor Yellow
    Write-Host "URL actuelle :" -ForegroundColor Cyan
    git remote get-url origin
} else {
    Write-Host "`nAjout du remote GitHub..." -ForegroundColor Cyan
    git remote add origin https://github.com/DizeAnalytics/Ibcsarlbtp.git
    Write-Host "✓ Remote ajouté" -ForegroundColor Green
}

# Renommer la branche en main
Write-Host "`nConfiguration de la branche..." -ForegroundColor Cyan
git branch -M main

Write-Host "`n=== Configuration terminée ===" -ForegroundColor Green
Write-Host "`nProchaines étapes :" -ForegroundColor Cyan
Write-Host "1. Créer le dépôt sur GitHub : https://github.com/new" -ForegroundColor White
Write-Host "   - Nom : Ibcsarlbtp" -ForegroundColor White
Write-Host "   - Propriétaire : DizeAnalytics" -ForegroundColor White
Write-Host "   - NE PAS initialiser avec README" -ForegroundColor Yellow
Write-Host "`n2. Pousser le code :" -ForegroundColor White
Write-Host "   git push -u origin main" -ForegroundColor Yellow
Write-Host "`n3. Si demande d'authentification, utiliser un Personal Access Token" -ForegroundColor Yellow
Write-Host "   (GitHub → Settings → Developer settings → Personal access tokens)" -ForegroundColor White
