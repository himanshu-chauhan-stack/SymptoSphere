(() => {
    const STORAGE_KEY = "symptosphere.language";
    const DEFAULT_LANGUAGE = "en";
    const SUPPORTED = new Set(["en", "hi"]);

    const cache = new Map();
    let currentLanguage = DEFAULT_LANGUAGE;
    let currentBundle = {};

    function interpolate(template, element) {
        if (typeof template !== "string") {
            return template;
        }

        const values = {
            count: element.getAttribute("data-count") || "",
            accuracy: element.getAttribute("data-accuracy") || "",
            value: element.getAttribute("data-value") || "",
            model: element.getAttribute("data-model") || "",
            years: element.getAttribute("data-years") || "",
            rating: element.getAttribute("data-rating") || "",
        };

        return template.replaceAll(/\{(count|accuracy|value|model|years|rating)\}/g, (_, key) => values[key] ?? "");
    }

    async function fetchBundle(language) {
        if (cache.has(language)) {
            return cache.get(language);
        }

        const response = await fetch(`/api/translations/${language}`);
        if (!response.ok) {
            throw new Error(`Failed translation fetch for ${language}`);
        }

        const data = await response.json();
        cache.set(language, data);
        return data;
    }

    function defaultSymptomLabel(raw) {
        return raw
            .replaceAll("_", " ")
            .replaceAll(".1", " duplicate")
            .replace(/\s+/g, " ")
            .trim()
            .replace(/\b\w/g, (match) => match.toUpperCase());
    }

    function applyText(bundle) {
        document.querySelectorAll("[data-i18n]").forEach((element) => {
            const key = element.getAttribute("data-i18n");
            if (!key) {
                return;
            }

            const value = bundle[key];
            if (typeof value === "string") {
                element.innerHTML = interpolate(value, element);
            }
        });

        document.querySelectorAll("[data-i18n-placeholder]").forEach((element) => {
            const key = element.getAttribute("data-i18n-placeholder");
            if (!key) {
                return;
            }

            const value = bundle[key];
            if (typeof value === "string") {
                element.setAttribute("placeholder", interpolate(value, element));
            }
        });

        document.querySelectorAll("[data-i18n-title]").forEach((element) => {
            const key = element.getAttribute("data-i18n-title");
            if (!key) {
                return;
            }

            const value = bundle[key];
            if (typeof value === "string") {
                element.setAttribute("title", interpolate(value, element));
            }
        });

        document.querySelectorAll("[data-i18n-aria-label]").forEach((element) => {
            const key = element.getAttribute("data-i18n-aria-label");
            if (!key) {
                return;
            }

            const value = bundle[key];
            if (typeof value === "string") {
                element.setAttribute("aria-label", interpolate(value, element));
            }
        });
    }

    function applySymptomMap(bundle) {
        const map = bundle.symptoms || {};

        document.querySelectorAll("[data-symptom-key]").forEach((element) => {
            const key = element.getAttribute("data-symptom-key");
            if (!key) {
                return;
            }

            if (!element.dataset.originalText) {
                element.dataset.originalText = element.textContent || "";
            }

            const translated = map[key];
            if (typeof translated === "string" && translated.trim()) {
                element.textContent = translated;
            } else if (currentLanguage === "en") {
                element.textContent = defaultSymptomLabel(key);
            } else {
                element.textContent = element.dataset.originalText || defaultSymptomLabel(key);
            }
        });
    }

    function applyDiseaseMap(bundle) {
        const map = bundle.diseases || {};

        document.querySelectorAll("[data-disease-key]").forEach((element) => {
            const key = element.getAttribute("data-disease-key");
            if (!key) {
                return;
            }

            if (!element.dataset.originalText) {
                element.dataset.originalText = element.textContent || "";
            }

            const translated = map[key];
            if (typeof translated === "string" && translated.trim()) {
                element.textContent = translated;
            } else {
                element.textContent = element.dataset.originalText || key;
            }
        });
    }

    function updateLanguageToggle() {
        const toggle = document.getElementById("languageToggle");
        if (!toggle) {
            return;
        }

        toggle.classList.toggle("is-hi", currentLanguage === "hi");
        toggle.setAttribute("data-language", currentLanguage);
    }

    function applyDocumentLanguage(language) {
        document.documentElement.lang = language;
        document.body.classList.toggle("is-hindi", language === "hi");
    }

    async function applyLanguage(language, persist = true) {
        const normalized = SUPPORTED.has(language) ? language : DEFAULT_LANGUAGE;

        try {
            const bundle = await fetchBundle(normalized);
            currentLanguage = normalized;
            currentBundle = bundle;

            applyDocumentLanguage(currentLanguage);
            applyText(bundle);
            applySymptomMap(bundle);
            applyDiseaseMap(bundle);
            updateLanguageToggle();

            if (persist) {
                localStorage.setItem(STORAGE_KEY, currentLanguage);
            }

            document.dispatchEvent(
                new CustomEvent("languageChanged", {
                    detail: {
                        language: currentLanguage,
                        bundle: currentBundle,
                    },
                }),
            );
        } catch (error) {
            if (normalized !== DEFAULT_LANGUAGE) {
                await applyLanguage(DEFAULT_LANGUAGE, persist);
            }
        }
    }

    function t(key, fallback = "") {
        const value = currentBundle[key];
        return typeof value === "string" ? value : fallback;
    }

    function refresh() {
        applyText(currentBundle);
        applySymptomMap(currentBundle);
        applyDiseaseMap(currentBundle);
        updateLanguageToggle();
    }

    function initLanguageToggle() {
        const toggle = document.getElementById("languageToggle");
        if (!toggle) {
            return;
        }

        toggle.addEventListener("click", async () => {
            const next = currentLanguage === "en" ? "hi" : "en";
            await applyLanguage(next, true);
        });
    }

    function bootstrap() {
        window.SymptoI18n = {
            get language() {
                return currentLanguage;
            },
            t,
            refresh,
            applyLanguage,
        };

        initLanguageToggle();

        const preferred = localStorage.getItem(STORAGE_KEY) || DEFAULT_LANGUAGE;
        void applyLanguage(preferred, false);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", bootstrap);
    } else {
        bootstrap();
    }
})();