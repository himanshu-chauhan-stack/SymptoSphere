(() => {
    function updateSelectedCountText(count) {
        const counter = document.getElementById("selectedCount");
        if (!counter) {
            return;
        }

        const i18n = window.SymptoI18n;
        if (i18n && typeof i18n.translate === "function") {
            const template = i18n.translate("selected_count", "{count} selected");
            counter.textContent = template.replace("{count}", String(count));
        } else {
            counter.textContent = `${count} selected`;
        }
        counter.dataset.count = String(count);
    }

    function initSearch() {
        const searchInput = document.getElementById("symptomSearch");
        const grid = document.getElementById("symptomGrid");
        if (!searchInput || !grid) {
            return;
        }

        const items = Array.from(grid.querySelectorAll("[data-symptom-item]"));

        const filter = () => {
            const query = searchInput.value.trim().toLowerCase();
            items.forEach((item) => {
                const raw = (item.getAttribute("data-search") || "").toLowerCase();
                const liveText = (item.querySelector(".symptom-text")?.textContent || "").toLowerCase();
                const matched = !query || raw.includes(query) || liveText.includes(query);
                item.style.display = matched ? "flex" : "none";
            });
        };

        searchInput.addEventListener("input", filter);
        document.addEventListener("languageChanged", filter);
    }

    function initSelectionCount() {
        const form = document.getElementById("predictionForm");
        if (!form) {
            return;
        }

        const checkboxes = Array.from(form.querySelectorAll("input.symptom-input"));

        const refresh = () => {
            const checked = checkboxes.filter((input) => input.checked).length;
            updateSelectedCountText(checked);
        };

        checkboxes.forEach((checkbox) => checkbox.addEventListener("change", refresh));
        document.addEventListener("languageChanged", refresh);
        refresh();
    }

    function initLoadingOverlay() {
        const form = document.getElementById("predictionForm");
        const overlay = document.getElementById("loadingOverlay");
        if (!form || !overlay) {
            return;
        }

        form.addEventListener("submit", (event) => {
            const selected = form.querySelectorAll("input.symptom-input:checked").length;
            if (!selected) {
                event.preventDefault();
                return;
            }

            overlay.classList.add("is-visible");
            overlay.setAttribute("aria-hidden", "false");
        });
    }

    function bootstrap() {
        initSearch();
        initSelectionCount();
        initLoadingOverlay();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", bootstrap);
    } else {
        bootstrap();
    }
})();
