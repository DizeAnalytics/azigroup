/**
 * Lightbox Moderne pour IBC SARL
 * Gestion des galeries d'images avec navigation
 */

class Lightbox {
    constructor(selector = '.gallery-item') {
        this.selector = selector;
        this.images = [];
        this.currentIndex = 0;
        this.overlay = null;
        this.imgElement = null;
        this.init();
    }

    init() {
        // Créer la structure HTML de la lightbox
        this.createLightboxHTML();
        
        // Récupérer tous les éléments de la galerie
        this.collectImages();
        
        // Attacher les événements
        this.attachEvents();
    }

    createLightboxHTML() {
        // Vérifier si la lightbox existe déjà
        if (document.getElementById('lightboxOverlay')) {
            this.overlay = document.getElementById('lightboxOverlay');
            this.imgElement = document.getElementById('lightboxImg');
            return;
        }

        // Créer la structure de la lightbox
        const lightboxHTML = `
            <div class="lightbox-overlay" id="lightboxOverlay" role="dialog" aria-modal="true" aria-label="Visionneuse d'images">
                <div class="lightbox-content">
                    <button class="lightbox-close" id="lightboxClose" aria-label="Fermer" title="Fermer (Esc)">×</button>
                    <button class="lightbox-nav lightbox-prev" id="lightboxPrev" aria-label="Image précédente" title="Précédent (←)">‹</button>
                    <button class="lightbox-nav lightbox-next" id="lightboxNext" aria-label="Image suivante" title="Suivant (→)">›</button>
                    <div class="lightbox-loader" id="lightboxLoader"></div>
                    <img id="lightboxImg" class="lightbox-img" src="" alt="Image agrandie">
                    <div class="lightbox-counter" id="lightboxCounter"></div>
                    <div class="lightbox-caption" id="lightboxCaption" style="display: none;"></div>
                </div>
            </div>
        `;

        // Ajouter au DOM
        document.body.insertAdjacentHTML('beforeend', lightboxHTML);

        // Récupérer les références
        this.overlay = document.getElementById('lightboxOverlay');
        this.imgElement = document.getElementById('lightboxImg');
        this.loader = document.getElementById('lightboxLoader');
        this.counter = document.getElementById('lightboxCounter');
        this.caption = document.getElementById('lightboxCaption');
        this.prevBtn = document.getElementById('lightboxPrev');
        this.nextBtn = document.getElementById('lightboxNext');
        this.closeBtn = document.getElementById('lightboxClose');
    }

    collectImages() {
        // Récupérer toutes les images de la galerie
        const items = document.querySelectorAll(this.selector);
        this.images = Array.from(items).map(item => {
            const img = item.querySelector('img');
            const link = item.querySelector('a') || item;
            return {
                src: link.href || link.dataset.src || (img ? img.src : ''),
                alt: img ? (img.alt || '') : '',
                caption: link.dataset.caption || item.dataset.caption || ''
            };
        });
    }

    attachEvents() {
        // Événements de clic sur les éléments de la galerie
        document.querySelectorAll(this.selector).forEach((item, index) => {
            const clickTarget = item.querySelector('a') || item.querySelector('img') || item;
            clickTarget.addEventListener('click', (e) => {
                e.preventDefault();
                this.open(index);
            });
            
            // Rendre cliquable
            clickTarget.style.cursor = 'pointer';
        });

        // Bouton fermer
        if (this.closeBtn) {
            this.closeBtn.addEventListener('click', () => this.close());
        }

        // Boutons navigation
        if (this.prevBtn) {
            this.prevBtn.addEventListener('click', () => this.prev());
        }
        if (this.nextBtn) {
            this.nextBtn.addEventListener('click', () => this.next());
        }

        // Clic sur l'overlay pour fermer
        this.overlay.addEventListener('click', (e) => {
            if (e.target === this.overlay) {
                this.close();
            }
        });

        // Navigation au clavier
        document.addEventListener('keydown', (e) => {
            if (!this.overlay.classList.contains('active')) return;

            switch(e.key) {
                case 'Escape':
                    this.close();
                    break;
                case 'ArrowLeft':
                    this.prev();
                    break;
                case 'ArrowRight':
                    this.next();
                    break;
            }
        });

        // Empêcher le défilement quand la lightbox est ouverte
        this.overlay.addEventListener('transitionend', () => {
            if (this.overlay.classList.contains('active')) {
                document.body.style.overflow = 'hidden';
            } else {
                document.body.style.overflow = '';
            }
        });
    }

    open(index) {
        this.currentIndex = index;
        this.updateImage();
        this.overlay.classList.add('active');
        this.updateNavButtons();
    }

    close() {
        this.overlay.classList.remove('active');
        setTimeout(() => {
            this.imgElement.src = '';
        }, 300);
    }

    prev() {
        if (this.currentIndex > 0) {
            this.currentIndex--;
            this.updateImage();
            this.updateNavButtons();
        }
    }

    next() {
        if (this.currentIndex < this.images.length - 1) {
            this.currentIndex++;
            this.updateImage();
            this.updateNavButtons();
        }
    }

    updateImage() {
        const image = this.images[this.currentIndex];
        
        // Afficher le loader
        this.loader.style.display = 'block';
        this.imgElement.style.opacity = '0';

        // Charger l'image
        const img = new Image();
        img.onload = () => {
            this.imgElement.src = image.src;
            this.imgElement.alt = image.alt;
            this.imgElement.classList.add('sliding');
            
            // Masquer le loader et afficher l'image
            setTimeout(() => {
                this.loader.style.display = 'none';
                this.imgElement.style.opacity = '1';
            }, 100);

            // Retirer l'animation après
            setTimeout(() => {
                this.imgElement.classList.remove('sliding');
            }, 300);
        };
        img.src = image.src;

        // Mettre à jour le compteur
        this.counter.textContent = `${this.currentIndex + 1} / ${this.images.length}`;

        // Mettre à jour la légende
        if (image.caption) {
            this.caption.textContent = image.caption;
            this.caption.style.display = 'block';
        } else {
            this.caption.style.display = 'none';
        }
    }

    updateNavButtons() {
        // Désactiver le bouton précédent si on est au début
        if (this.prevBtn) {
            this.prevBtn.disabled = this.currentIndex === 0;
        }

        // Désactiver le bouton suivant si on est à la fin
        if (this.nextBtn) {
            this.nextBtn.disabled = this.currentIndex === this.images.length - 1;
        }
    }
}

// Auto-initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    // Initialiser pour les galeries de news
    if (document.querySelector('.news-gallery-item')) {
        new Lightbox('.news-gallery-item');
    }

    // Initialiser pour les galeries de projets
    if (document.querySelector('.pd-gallery-grid > div')) {
        new Lightbox('.pd-gallery-grid > div');
    }
});
