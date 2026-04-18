(() => {
    const IS_MOBILE_VIEW = window.matchMedia("(max-width: 900px)").matches;

    const CATEGORY_CONFIG = [
        {
            id: "fever",
            icon: "+",
            key: "category_fever",
            keywords: ["fever", "chills", "shivering", "sweating", "dehydration", "malaise"],
        },
        {
            id: "respiratory",
            icon: "~",
            key: "category_respiratory",
            keywords: ["cough", "breath", "phlegm", "sputum", "throat", "sinus", "nose", "congestion", "chest"],
        },
        {
            id: "digestive",
            icon: "*",
            key: "category_digestive",
            keywords: ["stomach", "abdominal", "vomit", "nausea", "appetite", "diarrhoea", "constipation", "liver", "urine", "bowel"],
        },
        {
            id: "neurological",
            icon: "@",
            key: "category_neuro",
            keywords: ["head", "dizz", "vision", "slurred", "balance", "smell", "sensorium", "coma", "weakness", "brain"],
        },
        {
            id: "pain",
            icon: "!",
            key: "category_pain",
            keywords: ["pain", "cramps", "stiff", "swelling", "joint", "muscle", "neck", "back", "knee", "hip", "walking"],
        },
        {
            id: "skin",
            icon: "#",
            key: "category_skin",
            keywords: ["skin", "itch", "rash", "blister", "nails", "patches", "red", "pimples", "blackheads", "ooze"],
        },
        {
            id: "metabolic",
            icon: "$",
            key: "category_metabolic",
            keywords: ["weight", "thyroid", "hunger", "sugar", "obesity", "fatigue", "lethargy", "polyuria"],
        },
        {
            id: "mental",
            icon: "^",
            key: "category_mental",
            keywords: ["anxiety", "depression", "irritability", "mood", "restless", "concentration"],
        },
        {
            id: "general",
            icon: "=",
            key: "category_general",
            keywords: [],
        },
    ];

    const escapeRegex = (value) => value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

    const normalizeSearchText = (value) => value.toLowerCase().replace(/_/g, " ");

    function classifySymptom(value) {
        const normalized = normalizeSearchText(value);

        for (const category of CATEGORY_CONFIG) {
            if (category.id === "general") {
                continue;
            }

            if (category.keywords.some((keyword) => normalized.includes(keyword))) {
                return category.id;
            }
        }

        return "general";
    }

    function createSection(category) {
        const section = document.createElement("section");
        section.className = "symptom-category";
        section.dataset.category = category.id;

        const header = document.createElement("div");
        header.className = "symptom-category-header";

        const title = document.createElement("h3");
        title.className = "symptom-category-title";

        const icon = document.createElement("span");
        icon.textContent = category.icon;
        icon.setAttribute("aria-hidden", "true");

        const text = document.createElement("span");
        text.setAttribute("data-i18n", category.key);
        text.textContent = category.id;

        title.appendChild(icon);
        title.appendChild(text);

        const count = document.createElement("span");
        count.className = "symptom-category-count";
        count.textContent = "0";

        const grid = document.createElement("div");
        grid.className = "symptom-category-grid";

        header.appendChild(title);
        header.appendChild(count);

        section.appendChild(header);
        section.appendChild(grid);

        return {
            section,
            grid,
            count,
        };
    }

    function updateCounterText(count, selectedText, stickyText) {
        const t = window.SymptoI18n?.t || ((_, fallback) => fallback);
        const template = t("predict_selected_counter", "{count} symptoms selected");
        const output = template.replace("{count}", `<strong>${count}</strong>`);

        selectedText.innerHTML = output;
        stickyText.innerHTML = output;

        selectedText.dataset.count = String(count);
        stickyText.dataset.count = String(count);

        selectedText.classList.toggle("is-ready", count > 3);
    }

    function updateCategoryVisibility(sections) {
        sections.forEach((entry) => {
            const cards = entry.grid.querySelectorAll(".symptom-card");
            const visible = Array.from(cards).filter((card) => !card.classList.contains("is-filtered-out"));
            entry.count.textContent = String(visible.length);
            entry.section.classList.toggle("is-hidden", visible.length === 0);
        });
    }

    function injectRipple(card, event) {
        const rect = card.getBoundingClientRect();
        const ripple = document.createElement("span");
        ripple.className = "symptom-ripple";
        ripple.style.left = `${event.clientX - rect.left}px`;
        ripple.style.top = `${event.clientY - rect.top}px`;
        card.appendChild(ripple);
        window.setTimeout(() => ripple.remove(), 520);
    }

    function initializePredictPage() {
        const form = document.getElementById("predictionForm");
        const catalog = document.getElementById("symptomCatalog");
        const groups = document.getElementById("symptomGroups");
        const search = document.getElementById("symptomSearch");
        const submitButton = document.getElementById("predictSubmitButton");
        const clearButton = document.getElementById("clearSymptomsButton");
        const selectedText = document.getElementById("selectedCountText");
        const stickyText = document.getElementById("stickySelectedText");
        const loadingOverlay = document.getElementById("predictLoadingOverlay");

        if (!form || !catalog || !groups || !search || !submitButton || !clearButton || !selectedText || !stickyText || !loadingOverlay) {
            return;
        }

        // Ensure restored browser state never starts with an old filter.
        search.value = "";

        const cards = Array.from(catalog.querySelectorAll(".symptom-card"));
        if (!cards.length) {
            return;
        }

        const sectionMap = new Map();

        cards
            .sort((a, b) => {
                const aText = (a.querySelector(".symptom-label")?.textContent || "").toLowerCase();
                const bText = (b.querySelector(".symptom-label")?.textContent || "").toLowerCase();
                return aText.localeCompare(bText);
            })
            .forEach((card) => {
                const input = card.querySelector(".symptom-input");
                if (!(input instanceof HTMLInputElement)) {
                    return;
                }

                card.dataset.search = normalizeSearchText(input.value);

                card.addEventListener("pointerdown", (event) => {
                    injectRipple(card, event);
                });
            });

        if (IS_MOBILE_VIEW) {
            const mobileHeading = groups.querySelector("[data-i18n='predict_loading_categories']");
            if (mobileHeading) {
                mobileHeading.setAttribute("data-i18n", "category_general");
                mobileHeading.textContent = "General Indicators";
            }

            cards.forEach((card) => {
                card.dataset.category = "general";
                catalog.appendChild(card);
            });
        } else {
            CATEGORY_CONFIG.forEach((category) => {
                const entry = createSection(category);
                sectionMap.set(category.id, entry);
                groups.appendChild(entry.section);
            });

            cards.forEach((card) => {
                const input = card.querySelector(".symptom-input");
                if (!(input instanceof HTMLInputElement)) {
                    return;
                }

                const category = classifySymptom(input.value);
                const section = sectionMap.get(category) || sectionMap.get("general");
                section?.grid.appendChild(card);
                card.dataset.category = category;
            });

            catalog.remove();
        }

        if (typeof window.SymptoI18n?.refresh === "function") {
            window.SymptoI18n.refresh();
        }

        const allCards = Array.from(groups.querySelectorAll(".symptom-card"));
        const allInputs = Array.from(groups.querySelectorAll(".symptom-input"));
        let isSubmitting = false;

        const syncState = () => {
            const checked = allInputs.filter((input) => input.checked).length;

            allCards.forEach((card) => {
                const input = card.querySelector(".symptom-input");
                if (input instanceof HTMLInputElement) {
                    card.classList.toggle("is-selected", input.checked);
                }
            });

            updateCounterText(checked, selectedText, stickyText);

            submitButton.disabled = checked === 0;
            submitButton.classList.toggle("is-pulsing", checked > 0);
        };

        const runFilter = () => {
            const query = search.value.trim().toLowerCase();
            const regex = query ? new RegExp(escapeRegex(query), "i") : null;

            allCards.forEach((card) => {
                const label = card.querySelector(".symptom-label")?.textContent || "";
                const raw = card.dataset.search || "";
                const match = !regex || regex.test(label) || regex.test(raw);
                card.classList.toggle("is-filtered-out", !match);
            });

            if (sectionMap.size) {
                updateCategoryVisibility(Array.from(sectionMap.values()));
            }
        };

        allInputs.forEach((input) => {
            input.addEventListener("change", syncState);
        });

        clearButton.addEventListener("click", () => {
            allInputs.forEach((input) => {
                input.checked = false;
            });
            syncState();
        });

        search.addEventListener("input", runFilter);

        form.addEventListener("submit", (event) => {
            if (isSubmitting) {
                return;
            }

            const selectedCount = allInputs.filter((input) => input.checked).length;
            if (!selectedCount) {
                event.preventDefault();
                return;
            }

            event.preventDefault();
            isSubmitting = true;
            loadingOverlay.classList.add("is-active");
            loadingOverlay.setAttribute("aria-hidden", "false");

            window.setTimeout(() => {
                form.submit();
            }, 1300);
        });

        document.addEventListener("languageChanged", () => {
            syncState();
            runFilter();
        });

        syncState();
        runFilter();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initializePredictPage);
    } else {
        initializePredictPage();
    }
})();