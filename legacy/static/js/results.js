(() => {
    function initConfidenceBars() {
        const bars = document.querySelectorAll(".confidence-fill[data-confidence]");
        if (!bars.length) {
            return;
        }

        const animateBar = (bar) => {
            const confidence = Number(bar.getAttribute("data-confidence") || "0");
            const delay = Number(bar.getAttribute("data-delay") || "0");
            const bounded = Math.min(Math.max(confidence, 0), 100);

            window.setTimeout(() => {
                bar.style.width = `${bounded}%`;
                window.setTimeout(() => {
                    bar.classList.add("shine");
                }, 700);
            }, delay);
        };

        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        animateBar(entry.target);
                        observer.unobserve(entry.target);
                    }
                });
            },
            {
                threshold: 0.4,
            },
        );

        bars.forEach((bar) => observer.observe(bar));
    }

    function initModelComparisonToggle() {
        const button = document.getElementById("modelToggle");
        const panel = document.getElementById("modelPanel");
        if (!button || !panel) {
            return;
        }

        button.addEventListener("click", () => {
            const expanded = button.getAttribute("aria-expanded") === "true";
            button.setAttribute("aria-expanded", expanded ? "false" : "true");
            panel.classList.toggle("is-open", !expanded);
        });
    }

    function initTreatmentTabs() {
        const tabs = Array.from(document.querySelectorAll(".treatment-tab"));
        const panes = Array.from(document.querySelectorAll(".treatment-pane"));
        const indicator = document.getElementById("tabIndicator");
        if (!tabs.length || !panes.length) {
            return;
        }

        const activate = (targetTab) => {
            tabs.forEach((tab, index) => {
                const active = tab === targetTab;
                tab.classList.toggle("is-active", active);

                if (active && indicator) {
                    indicator.style.transform = `translateX(${index * 100}%)`;
                }
            });

            const target = targetTab.getAttribute("data-tab-target");
            panes.forEach((pane) => {
                pane.classList.toggle("is-active", pane.getAttribute("data-tab-content") === target);
            });
        };

        tabs.forEach((tab) => {
            tab.addEventListener("click", () => activate(tab));
        });

        activate(tabs[0]);
    }

    function initTypewriterMessages() {
        const elements = document.querySelectorAll("[data-typewriter][data-message]");
        if (!elements.length) {
            return;
        }

        const runTypewriter = (element) => {
            if (element.dataset.typed === "true") {
                return;
            }

            const message = element.getAttribute("data-message") || "";
            let index = 0;
            element.textContent = "";

            const timer = window.setInterval(() => {
                element.textContent += message.charAt(index);
                index += 1;

                if (index >= message.length) {
                    window.clearInterval(timer);
                    element.dataset.typed = "true";
                }
            }, 16);
        };

        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        runTypewriter(entry.target);
                        observer.unobserve(entry.target);
                    }
                });
            },
            {
                threshold: 0.45,
            },
        );

        elements.forEach((element) => observer.observe(element));
    }

    function bootstrap() {
        initConfidenceBars();
        initModelComparisonToggle();
        initTreatmentTabs();
        initTypewriterMessages();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", bootstrap);
    } else {
        bootstrap();
    }
})();
