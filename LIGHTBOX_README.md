# 📸 Lightbox Moderne - Documentation

## 🎯 Fonctionnalités

La lightbox moderne a été ajoutée aux pages suivantes :
- ✅ Page de détail des actualités (`/news/<slug>/`)
- ✅ Page de détail des projets (`/projects/<slug>/`)

## ✨ Caractéristiques

### 🖼️ Affichage des images
- **Clic sur une image** → Ouverture en plein écran
- **Navigation** entre les images avec les flèches ← →
- **Compteur** d'images (ex: 3/5)
- **Légendes** affichées automatiquement
- **Effet de zoom** élégant au survol

### ⌨️ Contrôles clavier
- `ESC` → Fermer la lightbox
- `←` → Image précédente
- `→` → Image suivante

### 🖱️ Contrôles souris
- **Clic sur X** → Fermer
- **Clic sur fond noir** → Fermer
- **Flèches de navigation** → Parcourir les images

### 📱 Responsive
- Adapté automatiquement pour mobile, tablette et desktop
- Boutons tactiles optimisés
- Gestes de swipe (à venir)

## 🎨 Design

### Effets visuels
- **Glassmorphism** sur les boutons
- **Animations fluides** (zoom in, fade, slide)
- **Overlay avec blur** pour mettre en valeur l'image
- **Icône de zoom 🔍** au survol des miniatures
- **Loader** pendant le chargement des images

### Couleurs
- Fond overlay : Noir semi-transparent (95%)
- Boutons : Blanc translucide avec effet blur
- Accent : Violet (#667eea → #764ba2)
- Hover : Animation avec changement de couleur

## 📂 Fichiers créés

### CSS
- `static/css/lightbox.css` - Styles de la lightbox

### JavaScript
- `static/js/lightbox.js` - Logique de la lightbox (classe réutilisable)

### Templates modifiés
- `templates/website/news_detail.html` - Ajout lightbox + styles
- `templates/website/project_detail.html` - Migration vers nouvelle lightbox

## 🚀 Utilisation

### Pour ajouter une galerie dans une nouvelle page

1. **Inclure les fichiers CSS et JS** :
```django
{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/lightbox.css' %}">
{% endblock %}

{% block extra_js %}
<script src="{% static 'js/lightbox.js' %}"></script>
{% endblock %}
```

2. **Structure HTML** :
```html
<div class="gallery-container">
    <div class="gallery-item" data-caption="Légende optionnelle">
        <a href="chemin/vers/image-grande.jpg" data-caption="Légende">
            <img src="chemin/vers/miniature.jpg" alt="Description">
        </a>
    </div>
    <!-- Répéter pour chaque image -->
</div>
```

3. **Initialiser la lightbox** :
```javascript
new Lightbox('.gallery-item');
```

## 🔧 Personnalisation

### Modifier le sélecteur
```javascript
// Par défaut : '.gallery-item'
new Lightbox('.ma-classe-personnalisee');
```

### Modifier les styles
Éditer `static/css/lightbox.css` pour personnaliser :
- Couleurs des boutons
- Tailles et positions
- Animations
- Effets visuels

## 📊 Performances

- **Lazy loading** : Images chargées uniquement quand nécessaire
- **Pré-chargement** : Image suivante pré-chargée pour navigation fluide
- **Optimisations** : Transitions CSS plutôt que JavaScript
- **Légèreté** : ~200 lignes de JS, ~300 lignes de CSS

## 🐛 Dépannage

### Les images ne s'ouvrent pas
1. Vérifier que `lightbox.css` et `lightbox.js` sont bien inclus
2. Vérifier la structure HTML (balise `<a>` avec `href`)
3. Ouvrir la console du navigateur pour voir les erreurs

### Pas de navigation entre images
1. Vérifier que plusieurs images existent dans la galerie
2. Vérifier que le sélecteur CSS correspond aux éléments

### Styles cassés
1. Vider le cache du navigateur (Ctrl + F5)
2. Vérifier que le CSS est bien chargé (onglet Network)

## 💡 Améliorations futures

- [ ] Gestes de swipe pour mobile
- [ ] Diaporama automatique
- [ ] Zoom/Pan sur les images
- [ ] Partage sur réseaux sociaux
- [ ] Téléchargement d'image
- [ ] Plein écran (Fullscreen API)

## 📞 Support

Pour toute question ou problème, contacter l'équipe de développement.

---

**Version** : 1.0  
**Date** : Janvier 2026  
**Auteur** : IBC SARL Development Team
