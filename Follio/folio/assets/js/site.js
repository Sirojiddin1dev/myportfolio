document.addEventListener('DOMContentLoaded', () => {
    const menuTrigger = document.querySelector('[data-menu-trigger]');
    const mobileMenu = document.querySelector('[data-menu]');

    if (menuTrigger && mobileMenu) {
        const closeMenu = () => {
            menuTrigger.classList.remove('dl-active');
            mobileMenu.classList.remove('dl-menuopen');
            menuTrigger.setAttribute('aria-expanded', 'false');
        };

        menuTrigger.addEventListener('click', (event) => {
            event.stopPropagation();
            const isExpanded = menuTrigger.getAttribute('aria-expanded') === 'true';
            menuTrigger.classList.toggle('dl-active', !isExpanded);
            mobileMenu.classList.toggle('dl-menuopen', !isExpanded);
            menuTrigger.setAttribute('aria-expanded', String(!isExpanded));
        });

        mobileMenu.querySelectorAll('a').forEach((link) => {
            link.addEventListener('click', closeMenu);
        });

        document.addEventListener('click', (event) => {
            if (!mobileMenu.contains(event.target) && !menuTrigger.contains(event.target)) {
                closeMenu();
            }
        });

        document.addEventListener('keydown', (event) => {
            if (event.key === 'Escape') {
                closeMenu();
            }
        });
    }

    document.querySelectorAll('[data-tabs]').forEach((tabsRoot) => {
        const triggers = Array.from(tabsRoot.querySelectorAll('[data-tab-trigger]'));
        const panels = Array.from(tabsRoot.querySelectorAll('[data-tab-panel]'));

        const activateTab = (targetId) => {
            triggers.forEach((trigger) => {
                const isActive = trigger.dataset.tabTrigger === targetId;
                trigger.classList.toggle('is-active', isActive);
                trigger.setAttribute('aria-selected', String(isActive));
                trigger.tabIndex = isActive ? 0 : -1;
            });

            panels.forEach((panel) => {
                panel.hidden = panel.dataset.tabPanel !== targetId;
            });
        };

        triggers.forEach((trigger) => {
            trigger.addEventListener('click', () => activateTab(trigger.dataset.tabTrigger));
        });

        const activeTrigger = triggers.find((trigger) => trigger.classList.contains('is-active')) || triggers[0];
        if (activeTrigger) {
            activateTab(activeTrigger.dataset.tabTrigger);
        }
    });

    document.querySelectorAll('[data-slider]').forEach((sliderRoot) => {
        const track = sliderRoot.querySelector('[data-slider-track]');
        const slides = Array.from(sliderRoot.querySelectorAll('[data-slider-slide]'));
        const previousButton = sliderRoot.querySelector('[data-slider-prev]');
        const nextButton = sliderRoot.querySelector('[data-slider-next]');
        const statusLabel = sliderRoot.querySelector('[data-slider-status]');

        if (!track || slides.length === 0) {
            return;
        }

        let activeIndex = 0;

        const syncSlider = () => {
            track.style.transform = `translateX(-${activeIndex * 100}%)`;

            if (previousButton) {
                previousButton.disabled = activeIndex === 0;
            }

            if (nextButton) {
                nextButton.disabled = activeIndex === slides.length - 1;
            }

            if (statusLabel) {
                statusLabel.textContent = `${activeIndex + 1} / ${slides.length}`;
            }
        };

        previousButton?.addEventListener('click', () => {
            activeIndex = Math.max(0, activeIndex - 1);
            syncSlider();
        });

        nextButton?.addEventListener('click', () => {
            activeIndex = Math.min(slides.length - 1, activeIndex + 1);
            syncSlider();
        });

        syncSlider();
    });

    const backToTopLink = document.querySelector('[data-back-to-top]');
    if (backToTopLink) {
        const toggleBackToTop = () => {
            backToTopLink.style.display = window.scrollY > 500 ? 'block' : 'none';
        };

        toggleBackToTop();
        window.addEventListener('scroll', toggleBackToTop, { passive: true });
    }
});
