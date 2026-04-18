(() => {
    const DEFAULT_LANGUAGE = "en";
    const SUPPORTED_LANGUAGES = ["en", "hi"];

    let currentLanguage = DEFAULT_LANGUAGE;
    let currentTranslations = {};
    const cache = {};

    async function fetchTranslations(language) {
        if (cache[language]) {
            return cache[language];
        }

        const response = await fetch(`/api/translations/${language}`);
        if (!response.ok) {
            throw new Error(`Translation fetch failed: ${language}`);
        }

        const payload = await response.json();
        cache[language] = payload;
        return payload;
    }

    function fillTemplate(value, element) {
        if (typeof value !== "string") {
            return value;
        }

        let output = value;
        const count = element.dataset.count;
        const accuracy = element.dataset.accuracy;

        if (count) {
            output = output.replaceAll("{count}", count);
        }
        if (accuracy) {
            output = output.replaceAll("{accuracy}", accuracy);
        }
        return output;
    }

    function applyTextTranslations(translations) {
        document.querySelectorAll("[data-i18n-key]").forEach((element) => {
            const key = element.dataset.i18nKey;
            if (!key) {
                return;
            }
            const value = translations[key];
            if (typeof value === "string") {
                element.textContent = fillTemplate(value, element);
            }
        });

        document.querySelectorAll("[data-i18n-placeholder]").forEach((element) => {
            const key = element.dataset.i18nPlaceholder;
            if (!key) {
                return;
            }
            const value = translations[key];
            if (typeof value === "string") {
                element.setAttribute("placeholder", value);
            }
        });
    }

    function applySymptomTranslations(translations) {
        const symptomMap = translations.symptoms || {};
        document.querySelectorAll("[data-symptom-key]").forEach((element) => {
            const key = element.dataset.symptomKey;
            if (!key) {
                return;
            }

            const value = symptomMap[key];
            if (typeof value === "string" && value.trim()) {
                element.textContent = value;
            }
        });
    }

    function applyDiseaseTranslations(translations) {
        const diseaseMap = translations.diseases || {};
        document.querySelectorAll("[data-disease-key]").forEach((element) => {
            const key = element.dataset.diseaseKey;
            if (!key) {
                return;
            }

            const value = diseaseMap[key];
            if (typeof value === "string" && value.trim()) {
                element.textContent = value;
            }
        });
    }

    function updateLanguageToggleLabel() {
        const button = document.getElementById("languageToggle");
        if (!button) {
            return;
        }

        const nextLanguage = currentLanguage === "en" ? "हिंदी" : "English";
        const prefix = currentLanguage === "en" ? "EN" : "HI";
        button.textContent = `${prefix} | ${nextLanguage}`;
    }

    async function applyLanguage(language, persist = true) {
        const selected = SUPPORTED_LANGUAGES.includes(language) ? language : DEFAULT_LANGUAGE;

        try {
            const translations = await fetchTranslations(selected);
            currentLanguage = selected;
            currentTranslations = translations;

            document.documentElement.lang = selected;
            applyTextTranslations(translations);
            applySymptomTranslations(translations);
            applyDiseaseTranslations(translations);
            updateLanguageToggleLabel();

            if (persist) {
                localStorage.setItem("symptosphere.language", selected);
            }

            document.dispatchEvent(
                new CustomEvent("languageChanged", {
                    detail: {
                        language: selected,
                        translations,
                    },
                }),
            );
        } catch (error) {
            if (selected !== DEFAULT_LANGUAGE) {
                await applyLanguage(DEFAULT_LANGUAGE, persist);
            }
        }
    }

    function translate(key, fallback = "") {
        const value = currentTranslations[key];
        if (typeof value === "string") {
            return value;
        }
        return fallback;
    }

    function bootstrap() {
        window.SymptoI18n = {
            get language() {
                return currentLanguage;
            },
            translate,
        };

        const toggle = document.getElementById("languageToggle");
        if (toggle) {
            toggle.addEventListener("click", async () => {
                const next = currentLanguage === "en" ? "hi" : "en";
                await applyLanguage(next);
            });
        }

        const stored = localStorage.getItem("symptosphere.language") || DEFAULT_LANGUAGE;
        void applyLanguage(stored, false);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", bootstrap);
    } else {
        bootstrap();
    }
})();
