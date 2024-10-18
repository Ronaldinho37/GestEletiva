document.addEventListener('DOMContentLoaded', function() {
    const menuBtn = document.getElementById('menu-btn');
    const closeBtn = document.getElementById('close-btn');
    const sideNav = document.getElementById('side-nav');
    const effect = document.getElementById('effect');
    const themeSwitcher = document.getElementById('theme-switcher');
    const dropdownButtons = document.querySelectorAll('.dropdown-btn');

    menuBtn.addEventListener('click', function() {
        sideNav.style.right = '0'; /* Abrir o menu pela direita */
        effect.classList.remove('visible');
    });

    closeBtn.addEventListener('click', function() {
        sideNav.style.right = '-300px'; /* Alterado para fechar completamente o menu */
        effect.classList.remove('visible');
    });

    const sobreLink = document.getElementById('sobre');
    if (sobreLink) {
        sobreLink.addEventListener('click', function(event) {
            event.preventDefault();
            sideNav.style.right = '-400px'; /* Alterado para fechar completamente o menu */
            effect.classList.add('visible');
            setTimeout(function() {
                window.location.href = sobreLink.href;
            }, 3000);
        });
    }

    const logoLink = document.getElementById('logoLink');
    if (logoLink) {
        logoLink.addEventListener('click', function(event) {
            event.preventDefault();
            sideNav.style.right = '-400px'; /* Alterado para fechar completamente o menu */
            effect.classList.add('visible');
            setTimeout(function() {
                window.location.href = logoLink.href;
            }, 3000);
        });
    }

    const eletivasLink = document.getElementById('eletivaLink');
    if (eletivasLink) {
        eletivasLink.addEventListener('click', function(event) {
            event.preventDefault();
            sideNav.style.right = '-400px'; /* Alterado para fechar completamente o menu */
            effect.classList.add('visible');
            setTimeout(function() {
                window.location.href = eletivasLink.href;
            }, 3000);
        });
    }

    

    const tutorLink = document.getElementById('tutorLink');
    if (tutorLink) {
        tutorLink.addEventListener('click', function(event) {
            event.preventDefault();
            sideNav.style.right = '-400px'; /* Alterado para fechar completamente o menu */
            effect.classList.add('visible');
            setTimeout(function() {
                window.location.href = tutorLink.href;
            }, 3000);
        });
    }

    const overlay = document.getElementById('overlay');
    menuBtn.addEventListener('click', function() {
        sideNav.style.right = '0'; /* Abrir o menu pela direita */
        overlay.classList.add('show');
    });

    closeBtn.addEventListener('click', function() {
        sideNav.style.right = '-400px'; /* Alterado para fechar completamente o menu */
        overlay.classList.remove('show');
    });

    overlay.addEventListener('click', function() {
        sideNav.style.right = '-400px'; /* Alterado para fechar completamente o menu */
        overlay.classList.remove('show');
    });

    themeSwitcher.addEventListener('click', function() {
        document.body.classList.toggle('dark-theme');
        themeSwitcher.textContent = document.body.classList.contains('dark-theme') ? '🌙' : '🔆';
    });

    dropdownButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const targetId = button.getAttribute('data-target');
            const dropdown = document.getElementById(targetId);
            const isActive = dropdown.parentElement.classList.toggle('active');
            document.querySelectorAll('.dropdown-content').forEach(d => {
                if (d !== dropdown) {
                    d.parentElement.classList.remove('active');
                }
            });
            dropdown.style.display = isActive ? 'block' : 'none';
        });
    });

    document.addEventListener('click', function(event) {
        if (!event.target.closest('.menu-item') && !event.target.closest('.dropdown-content')) {
            document.querySelectorAll('.dropdown-content').forEach(dropdown => {
                dropdown.parentElement.classList.remove('active');
                dropdown.style.display = 'none';
            });
        }
    });
});
