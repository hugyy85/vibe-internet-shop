// ===== ОСНОВНОЙ JAVASCRIPT ДЛЯ JEWELRY STORE =====

document.addEventListener('DOMContentLoaded', function() {
    // Инициализация всех компонентов
    initializeNavigation();
    initializeProductCards();
    initializeShoppingCart();
    initializeFormValidation();
    initializeAnimations();
    initializeTooltips();
});

// ===== НАВИГАЦИЯ =====
function initializeNavigation() {
    // Активный пункт меню
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Плавная прокрутка
    const smoothScrollLinks = document.querySelectorAll('a[href^="#"]');
    smoothScrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Скрытие/показ навбара при прокрутке
    let lastScrollTop = 0;
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Скролл вниз
            navbar.style.transform = 'translateY(-100%)';
        } else {
            // Скролл вверх
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    });
}

// ===== КАРТОЧКИ ТОВАРОВ =====
function initializeProductCards() {
    const productCards = document.querySelectorAll('.product-card');
    
    productCards.forEach(card => {
        // Эффект наведения на изображение
        const imageWrapper = card.querySelector('.card-img-wrapper');
        if (imageWrapper) {
            imageWrapper.addEventListener('mouseenter', function() {
                const overlay = this.querySelector('.card-img-overlay');
                if (overlay) {
                    overlay.style.opacity = '1';
                }
            });
            
            imageWrapper.addEventListener('mouseleave', function() {
                const overlay = this.querySelector('.card-img-overlay');
                if (overlay) {
                    overlay.style.opacity = '0';
                }
            });
        }

        // Анимация появления карточек при прокрутке
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in-up');
                }
            });
        }, { threshold: 0.1 });

        observer.observe(card);
    });
}

// ===== КОРЗИНА =====
function initializeShoppingCart() {
    // Обновление счетчика корзины
    updateCartCounter();
    
    // Добавление в корзину с анимацией
    const addToCartButtons = document.querySelectorAll('a[href*="/add_to_cart/"]');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const href = this.getAttribute('href');
            
            // Анимация добавления
            this.classList.add('loading');
            this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Добавляем...';
            
            // Имитация добавления (в реальности здесь был бы AJAX)
            setTimeout(() => {
                window.location.href = href;
            }, 800);
        });
    });

    // Анимация удаления из корзины
    const removeButtons = document.querySelectorAll('a[href*="/remove_from_cart/"]');
    removeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            if (confirm('Удалить товар из корзины?')) {
                const cartItem = this.closest('.card');
                cartItem.style.transition = 'all 0.3s ease';
                cartItem.style.transform = 'translateX(100%)';
                cartItem.style.opacity = '0';
                
                setTimeout(() => {
                    window.location.href = this.getAttribute('href');
                }, 300);
            }
        });
    });
}

// Обновление счетчика корзины
function updateCartCounter() {
    // В реальном приложении здесь был бы AJAX запрос
    const cartBadge = document.querySelector('.navbar .badge');
    if (cartBadge) {
        cartBadge.style.animation = 'pulse 0.5s ease';
    }
}

// ===== ВАЛИДАЦИЯ ФОРМ =====
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!this.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
                
                // Показываем первое поле с ошибкой
                const firstInvalidField = this.querySelector(':invalid');
                if (firstInvalidField) {
                    firstInvalidField.focus();
                    firstInvalidField.scrollIntoView({
                        behavior: 'smooth',
                        block: 'center'
                    });
                }
            }
            
            this.classList.add('was-validated');
        });

        // Валидация в реальном времени
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                if (this.checkValidity()) {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                } else {
                    this.classList.remove('is-valid');
                    this.classList.add('is-invalid');
                }
            });
        });
    });

    // Форматирование телефона
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', formatPhoneNumber);
    });
}

function formatPhoneNumber(e) {
    let value = e.target.value.replace(/\D/g, '');
    
    if (value.startsWith('8')) {
        value = '7' + value.slice(1);
    }
    
    if (value.startsWith('7')) {
        value = value.slice(1);
    }
    
    let formattedValue = '+7';
    if (value.length >= 1) formattedValue += ' (' + value.slice(0, 3);
    if (value.length >= 4) formattedValue += ') ' + value.slice(3, 6);
    if (value.length >= 7) formattedValue += '-' + value.slice(6, 8);
    if (value.length >= 9) formattedValue += '-' + value.slice(8, 10);
    
    e.target.value = formattedValue;
}

// ===== АНИМАЦИИ =====
function initializeAnimations() {
    // Анимация появления элементов при прокрутке
    const animatedElements = document.querySelectorAll('.card, .feature-icon, .hero-section > *');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    animatedElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        element.style.transition = 'all 0.6s ease';
        observer.observe(element);
    });

    // Параллакс эффект для hero секции
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const heroSection = document.querySelector('.hero-section');
        
        if (heroSection) {
            const rate = scrolled * -0.5;
            heroSection.style.transform = `translateY(${rate}px)`;
        }
    });
}

// ===== ПОДСКАЗКИ =====
function initializeTooltips() {
    // Инициализация Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// ===== ПОИСК =====
function initializeSearch() {
    const searchInput = document.querySelector('#searchInput');
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length >= 2) {
                searchTimeout = setTimeout(() => {
                    performSearch(query);
                }, 500);
            }
        });
    }
}

function performSearch(query) {
    // В реальном приложении здесь был бы AJAX запрос
    console.log('Поиск:', query);
}

// ===== ФИЛЬТРЫ =====
function initializeFilters() {
    const filterButtons = document.querySelectorAll('.category-filter .btn');
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Убираем активный класс у всех кнопок
            filterButtons.forEach(btn => btn.classList.remove('active'));
            
            // Добавляем активный класс к текущей кнопке
            this.classList.add('active');
            
            // Переходим по ссылке
            setTimeout(() => {
                window.location.href = this.getAttribute('href');
            }, 150);
        });
    });
}

// ===== УТИЛИТЫ =====
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 100px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Автоматическое скрытие через 5 секунд
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

function formatPrice(price) {
    return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB',
        minimumFractionDigits: 0
    }).format(price);
}

// ===== ЗАГРУЗКА ИЗОБРАЖЕНИЙ =====
function initializeLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('shimmer');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => {
        img.classList.add('shimmer');
        imageObserver.observe(img);
    });
}

// ===== ОБРАБОТКА ОШИБОК =====
window.addEventListener('error', function(e) {
    console.error('JavaScript Error:', e.error);
    // В реальном приложении здесь была бы отправка ошибки на сервер
});

// ===== ЭКСПОРТ ФУНКЦИЙ ДЛЯ ИСПОЛЬЗОВАНИЯ В ДРУГИХ СКРИПТАХ =====
window.JewelryStore = {
    showNotification,
    formatPrice,
    updateCartCounter,
    performSearch
};