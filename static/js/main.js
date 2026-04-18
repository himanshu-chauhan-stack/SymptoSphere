(() => {
    const IS_MOBILE_VIEW = window.matchMedia("(max-width: 900px)").matches;
    const PREFERS_REDUCED_MOTION = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    function setActiveNav() {
        const path = window.location.pathname;
        const links = document.querySelectorAll(".site-nav-link");

        links.forEach((link) => {
            const nav = link.getAttribute("data-nav");
            if (!nav) {
                return;
            }

            const isHome = nav === "home" && path === "/";
            const isPredict = nav === "predict" && path.startsWith("/predict");
            const isAbout = nav === "about" && path.startsWith("/about");
            const isResults = nav === "predict" && path.startsWith("/results");

            link.classList.toggle("is-active", isHome || isPredict || isAbout || isResults);
        });
    }

    function initHeaderScrollEffect() {
        const header = document.getElementById("siteHeader");
        if (!header) {
            return;
        }

        const update = () => {
            header.classList.toggle("is-scrolled", window.scrollY > 100);
        };

        update();
        window.addEventListener("scroll", update, { passive: true });
    }

    function initScrollReveal() {
        const targets = document.querySelectorAll("[data-reveal]");
        if (!targets.length) {
            return;
        }

        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("revealed");
                        observer.unobserve(entry.target);
                    }
                });
            },
            {
                threshold: 0.12,
                rootMargin: "0px 0px -8% 0px",
            },
        );

        targets.forEach((target) => observer.observe(target));
    }

    function initWordReveal() {
        const splitTargets = document.querySelectorAll("[data-word-reveal]");

        splitTargets.forEach((element) => {
            if (element.dataset.wordWrapped === "true") {
                return;
            }

            const text = (element.textContent || "").trim();
            if (!text) {
                return;
            }

            const words = text.split(/\s+/);
            element.textContent = "";

            words.forEach((word, index) => {
                const span = document.createElement("span");
                span.className = "word-fragment";
                span.style.setProperty("--word-index", String(index));
                span.textContent = word;
                element.appendChild(span);

                if (index < words.length - 1) {
                    element.appendChild(document.createTextNode(" "));
                }
            });

            element.dataset.wordWrapped = "true";
        });
    }

    function initAnimatedCounters() {
        const counters = document.querySelectorAll("[data-counter-target]");
        if (!counters.length) {
            return;
        }

        const animateCounter = (counter) => {
            if (counter.dataset.counterAnimated === "true") {
                return;
            }

            const targetRaw = counter.getAttribute("data-counter-target") || "0";
            const target = Number(targetRaw);
            const suffix = counter.getAttribute("data-counter-suffix") || "";
            const duration = 1450;
            const start = performance.now();

            const hasDecimals = String(targetRaw).includes(".");
            const decimals = hasDecimals ? 1 : 0;

            const tick = (now) => {
                const elapsed = now - start;
                const progress = Math.min(elapsed / duration, 1);
                const eased = 1 - Math.pow(1 - progress, 3);
                const value = target * eased;

                if (hasDecimals) {
                    counter.textContent = `${value.toFixed(decimals)}${suffix}`;
                } else {
                    counter.textContent = `${Math.round(value)}${suffix}`;
                }

                if (progress < 1) {
                    window.requestAnimationFrame(tick);
                } else {
                    counter.textContent = `${targetRaw}${suffix}`;
                    counter.dataset.counterAnimated = "true";
                }
            };

            window.requestAnimationFrame(tick);
        };

        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        animateCounter(entry.target);
                        observer.unobserve(entry.target);
                    }
                });
            },
            {
                threshold: 0.5,
            },
        );

        counters.forEach((counter) => observer.observe(counter));
    }

    function initFeatureTilt() {
        const cards = document.querySelectorAll(".tilt-card");
        if (!cards.length) {
            return;
        }

        cards.forEach((card) => {
            card.addEventListener("mousemove", (event) => {
                const rect = card.getBoundingClientRect();
                const px = (event.clientX - rect.left) / rect.width;
                const py = (event.clientY - rect.top) / rect.height;
                const rotateY = (px - 0.5) * 10;
                const rotateX = (0.5 - py) * 10;
                card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
            });

            card.addEventListener("mouseleave", () => {
                card.style.transform = "perspective(1000px) rotateX(0deg) rotateY(0deg)";
            });
        });
    }

    function createBurst(button, originX, originY) {
        const amount = 11;

        for (let i = 0; i < amount; i += 1) {
            const particle = document.createElement("span");
            particle.className = "burst-particle";
            particle.style.left = `${originX}px`;
            particle.style.top = `${originY}px`;
            particle.style.setProperty("--x", `${(Math.random() - 0.5) * 80}px`);
            particle.style.setProperty("--y", `${(Math.random() - 0.5) * 80}px`);

            button.appendChild(particle);
            window.setTimeout(() => particle.remove(), 700);
        }
    }

    function initBurstButtons() {
        const buttons = document.querySelectorAll(".burst-button");
        if (!buttons.length) {
            return;
        }

        buttons.forEach((button) => {
            button.addEventListener("mouseenter", (event) => {
                const rect = button.getBoundingClientRect();
                const x = event.clientX - rect.left;
                const y = event.clientY - rect.top;
                createBurst(button, x, y);
            });
        });
    }

    function initModal() {
        const modal = document.getElementById("appointmentModal");
        const closeButton = document.getElementById("appointmentCloseButton");
        if (!modal || !closeButton) {
            return;
        }

        const openButtons = document.querySelectorAll(".open-appointment-modal, .book-appointment-btn");

        const openModal = () => {
            modal.classList.add("is-open");
            modal.setAttribute("aria-hidden", "false");
            document.body.style.overflow = "hidden";
        };

        const closeModal = () => {
            modal.classList.remove("is-open");
            modal.setAttribute("aria-hidden", "true");
            document.body.style.overflow = "";
        };

        openButtons.forEach((button) => {
            button.addEventListener("click", openModal);
        });

        closeButton.addEventListener("click", closeModal);

        modal.addEventListener("click", (event) => {
            if (event.target === modal) {
                closeModal();
            }
        });

        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape" && modal.classList.contains("is-open")) {
                closeModal();
            }
        });
    }

    function initPageTransitions() {
        const links = document.querySelectorAll("a[data-page-link]");

        links.forEach((link) => {
            link.addEventListener("click", (event) => {
                const href = link.getAttribute("href");
                if (!href || href.startsWith("#")) {
                    return;
                }

                if (link.getAttribute("target") === "_blank") {
                    return;
                }

                const target = new URL(href, window.location.origin);
                if (target.origin !== window.location.origin) {
                    return;
                }

                event.preventDefault();
                document.body.classList.add("is-page-leaving");

                window.setTimeout(() => {
                    window.location.href = target.href;
                }, 220);
            });
        });
    }

    function initCanvasNetwork() {
        if (IS_MOBILE_VIEW || PREFERS_REDUCED_MOTION) {
            return;
        }

        const canvas = document.getElementById("bioluminescent-canvas");
        if (!(canvas instanceof HTMLCanvasElement)) {
            return;
        }

        const context = canvas.getContext("2d");
        if (!context) {
            return;
        }

        const mouse = {
            x: -9999,
            y: -9999,
            active: false,
        };

        const particles = [];
        const particleCount = 220;

        const createParticle = () => {
            const isNode = Math.random() < 0.14;
            return {
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * (isNode ? 0.22 : 0.32),
                vy: (Math.random() - 0.5) * (isNode ? 0.22 : 0.32),
                size: isNode ? Math.random() * 2.2 + 1.8 : Math.random() * 1.8 + 0.5,
                type: isNode ? "hex" : "dot",
                hue: Math.random() > 0.3 ? "0,212,255" : "0,255,136",
            };
        };

        const resize = () => {
            const dpr = window.devicePixelRatio || 1;
            canvas.width = Math.floor(window.innerWidth * dpr);
            canvas.height = Math.floor(window.innerHeight * dpr);
            canvas.style.width = `${window.innerWidth}px`;
            canvas.style.height = `${window.innerHeight}px`;
            context.setTransform(dpr, 0, 0, dpr, 0, 0);

            if (!particles.length) {
                for (let i = 0; i < particleCount; i += 1) {
                    particles.push(createParticle());
                }
            }
        };

        const drawHex = (x, y, radius, color) => {
            context.beginPath();
            for (let i = 0; i < 6; i += 1) {
                const angle = (Math.PI / 3) * i;
                const px = x + radius * Math.cos(angle);
                const py = y + radius * Math.sin(angle);
                if (i === 0) {
                    context.moveTo(px, py);
                } else {
                    context.lineTo(px, py);
                }
            }
            context.closePath();
            context.strokeStyle = color;
            context.lineWidth = 1;
            context.stroke();
        };

        const updateParticle = (particle) => {
            particle.x += particle.vx;
            particle.y += particle.vy;

            if (particle.x < 0 || particle.x > window.innerWidth) {
                particle.vx *= -1;
            }

            if (particle.y < 0 || particle.y > window.innerHeight) {
                particle.vy *= -1;
            }

            if (mouse.active) {
                const dx = mouse.x - particle.x;
                const dy = mouse.y - particle.y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < 140) {
                    const pull = (140 - distance) / 1400;
                    particle.x += dx * pull;
                    particle.y += dy * pull;
                }
            }
        };

        const drawParticle = (particle) => {
            const alpha = particle.type === "hex" ? 0.8 : 0.45;
            const color = `rgba(${particle.hue},${alpha})`;

            if (particle.type === "hex") {
                drawHex(particle.x, particle.y, particle.size + 1.3, color);
            } else {
                context.beginPath();
                context.fillStyle = color;
                context.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
                context.fill();
            }
        };

        const drawConnections = () => {
            for (let i = 0; i < particles.length; i += 1) {
                const a = particles[i];
                for (let j = i + 1; j < particles.length; j += 1) {
                    const b = particles[j];
                    const dx = a.x - b.x;
                    const dy = a.y - b.y;
                    const distance = Math.sqrt(dx * dx + dy * dy);

                    if (distance < 110) {
                        const alpha = (1 - distance / 110) * 0.18;
                        context.beginPath();
                        context.strokeStyle = `rgba(0,212,255,${alpha})`;
                        context.lineWidth = 0.8;
                        context.moveTo(a.x, a.y);
                        context.lineTo(b.x, b.y);
                        context.stroke();
                    }
                }
            }
        };

        const loop = () => {
            context.clearRect(0, 0, window.innerWidth, window.innerHeight);

            particles.forEach((particle) => {
                updateParticle(particle);
                drawParticle(particle);
            });

            drawConnections();
            window.requestAnimationFrame(loop);
        };

        window.addEventListener("resize", resize);

        document.addEventListener("mousemove", (event) => {
            mouse.x = event.clientX;
            mouse.y = event.clientY;
            mouse.active = true;
        });

        document.addEventListener("mouseleave", () => {
            mouse.active = false;
        });

        resize();
        window.requestAnimationFrame(loop);
    }

    function bootstrap() {
        setActiveNav();
        initHeaderScrollEffect();
        initWordReveal();
        initScrollReveal();
        initAnimatedCounters();
        initFeatureTilt();
        initBurstButtons();
        initPageTransitions();
        initModal();
        initCanvasNetwork();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", bootstrap);
    } else {
        bootstrap();
    }
})();