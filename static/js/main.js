// JavaScript principal pour le site IBC Sarl BTP

// Toggle mobile menu professionnel
function toggleMenu() {
    const navLinks = document.querySelector('.nav-links');
    const hamburger = document.querySelector('.hamburger');
    const overlay = document.querySelector('.nav-overlay');
    const willOpen = !navLinks.classList.contains('active');

    navLinks.classList.toggle('active');
    hamburger.classList.toggle('active');

    if (hamburger) hamburger.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
    if (overlay) overlay.classList.toggle('active');

    // Empêcher le scroll du body quand le menu est ouvert
    document.body.style.overflow = willOpen ? 'hidden' : '';
}

function closeMenu() {
    const navLinks = document.querySelector('.nav-links');
    const hamburger = document.querySelector('.hamburger');
    const overlay = document.querySelector('.nav-overlay');
    navLinks.classList.remove('active');
    hamburger.classList.remove('active');
    if (hamburger) {
        hamburger.setAttribute('aria-expanded', 'false');
    }
    if (overlay) {
        overlay.classList.remove('active');
    }
    document.body.style.overflow = '';
}

// Smooth scrolling pour les liens d'ancrage
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Animation d'apparition au scroll
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeInUp 1s ease forwards';
        }
    });
}, { threshold: 0.1 });

// Observer les éléments à animer
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.company-card, .service-card, .news-card, .value-card').forEach(card => {
        observer.observe(card);
    });
});

// Gestion du formulaire de contact avec AJAX
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            
            // Log pour débogage
            console.log('Données du formulaire:', data);
            
            // Validation côté client
            if (!data.name || !data.email || !data.message) {
                showFlashMessage('Veuillez remplir tous les champs obligatoires.', 'error');
                return;
            }
            
            // Nettoyer les données vides (les convertir en null pour les champs optionnels)
            if (!data.phone || data.phone.trim() === '') {
                delete data.phone;
            }
            if (!data.company || data.company.trim() === '') {
                delete data.company;
            }
            if (!data.service || data.service.trim() === '') {
                delete data.service;
            }
            
            // Récupérer le token CSRF
            const csrftoken = getCookie('csrftoken') || document.querySelector('[name=csrfmiddlewaretoken]')?.value;
            
            console.log('Données envoyées:', JSON.stringify(data));
            
            // Envoi AJAX
            fetch('/api/contact/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken || ''
                },
                body: JSON.stringify(data)
            })
            .then(response => {
                // Vérifier si la réponse est OK
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.message || 'Erreur serveur');
                    });
                }
                return response.json();
            })
            .then(result => {
                if (result.success) {
                    showFlashMessage(result.message, 'success');
                    contactForm.reset();
                } else {
                    // Afficher les erreurs détaillées si disponibles
                    let errorMessage = result.message || 'Une erreur est survenue';
                    if (result.errors) {
                        const errorList = Object.values(result.errors).flat().join(', ');
                        if (errorList) {
                            errorMessage += ': ' + errorList;
                        }
                    }
                    showFlashMessage(errorMessage, 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showFlashMessage(error.message || 'Une erreur est survenue lors de l\'envoi du message.', 'error');
            });
        });
    }
});

// Fonction pour afficher les messages flash
function showFlashMessage(message, type) {
    const flashContainer = document.querySelector('.flash-messages') || createFlashContainer();
    
    const flashMessage = document.createElement('div');
    flashMessage.className = `flash-message flash-${type}`;
    flashMessage.innerHTML = `
        ${message}
        <button onclick="this.parentElement.remove()">&times;</button>
    `;
    
    flashContainer.appendChild(flashMessage);
    
    // Supprimer automatiquement après 5 secondes
    setTimeout(() => {
        if (flashMessage.parentElement) {
            flashMessage.remove();
        }
    }, 5000);
}

// Créer le conteneur de messages flash s'il n'existe pas
function createFlashContainer() {
    const container = document.createElement('div');
    container.className = 'flash-messages';
    document.body.appendChild(container);
    return container;
}

// Animation de compteur pour les statistiques
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    
    function updateCounter() {
        start += increment;
        element.textContent = Math.floor(start);
        
        if (start < target) {
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target;
        }
    }
    
    updateCounter();
}

// Lazy loading pour les images
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
});

// Gestion des formulaires avec validation en temps réel
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                if (this.classList.contains('error')) {
                    validateField(this);
                }
            });
        });
    });
});

// Validation d'un champ
function validateField(field) {
    const value = field.value.trim();
    const type = field.type;
    const required = field.hasAttribute('required');
    
    // Supprimer les classes d'erreur précédentes
    field.classList.remove('error');
    
    // Validation basique
    if (required && !value) {
        showFieldError(field, 'Ce champ est obligatoire');
        return false;
    }
    
    if (type === 'email' && value && !isValidEmail(value)) {
        showFieldError(field, 'Veuillez entrer une adresse email valide');
        return false;
    }
    
    if (type === 'tel' && value && !isValidPhone(value)) {
        showFieldError(field, 'Veuillez entrer un numéro de téléphone valide');
        return false;
    }
    
    return true;
}

// Afficher une erreur sur un champ
function showFieldError(field, message) {
    field.classList.add('error');
    
    // Supprimer l'ancien message d'erreur
    const existingError = field.parentElement.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
    
    // Ajouter le nouveau message d'erreur
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.textContent = message;
    field.parentElement.appendChild(errorDiv);
}

// Validation email
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Validation téléphone
function isValidPhone(phone) {
    const phoneRegex = /^[\+]?[0-9\s\-\(\)]{10,}$/;
    return phoneRegex.test(phone);
}

// Effet de parallaxe pour le hero
window.addEventListener('scroll', function() {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('.hero');
    
    if (hero) {
        const rate = scrolled * -0.5;
        hero.style.transform = `translateY(${rate}px)`;
    }
});

// Gestion du mode sombre (optionnel)
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

// Charger le mode sombre depuis le localStorage
document.addEventListener('DOMContentLoaded', function() {
    if (localStorage.getItem('darkMode') === 'true') {
        document.body.classList.add('dark-mode');
    }
});

// Fonction utilitaire pour formater les dates
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Fonction pour récupérer un cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Fonction pour copier du texte dans le presse-papiers
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showFlashMessage('Texte copié dans le presse-papiers !', 'success');
    }, function(err) {
        console.error('Erreur lors de la copie: ', err);
        showFlashMessage('Erreur lors de la copie', 'error');
    });
}

// Gestion des modales
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// Fermer les modales en cliquant à l'extérieur
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal')) {
        e.target.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
});

// Gestion du scroll vers le haut
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Afficher/masquer le bouton "scroll to top"
window.addEventListener('scroll', function() {
    const scrollButton = document.querySelector('.scroll-to-top');
    if (scrollButton) {
        if (window.pageYOffset > 300) {
            scrollButton.style.display = 'block';
        } else {
            scrollButton.style.display = 'none';
        }
    }
});
