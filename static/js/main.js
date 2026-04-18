(() => {
    const PARTICLE_COUNT = 68;

    function setActiveNav() {
        const path = window.location.pathname;
        document.querySelectorAll(".navbar a").forEach((link) => {
            const href = link.getAttribute("href");
            if (!href) {
                return;
            }
            const isRoot = href === "/";
            const active = isRoot ? path === "/" : path.startsWith(href);
            link.classList.toggle("is-active", active);
        });
    }

    function initRevealAnimations() {
        const targets = document.querySelectorAll(".reveal-up, .reveal-up-delay");
        if (!targets.length) {
            return;
        }

        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("is-visible");
                        observer.unobserve(entry.target);
                    }
                });
            },
            {
                threshold: 0.12,
                rootMargin: "0px 0px -40px 0px",
            },
        );

        targets.forEach((target) => observer.observe(target));
    }

    function initCounters() {
        const counters = document.querySelectorAll(".counter[data-counter-target]");
        if (!counters.length) {
            return;
        }

        counters.forEach((counter) => {
            const target = Number(counter.dataset.counterTarget || "0");
            let start = 0;
            const duration = 1200;
            const frameRate = 1000 / 60;
            const step = Math.max(1, Math.ceil(target / (duration / frameRate)));

            const update = () => {
                start += step;
                if (start >= target) {
                    counter.textContent = `${target}${target >= 90 ? "+" : ""}`;
                    return;
                }
                counter.textContent = String(start);
                window.requestAnimationFrame(update);
            };

            window.requestAnimationFrame(update);
        });
    }

    function initConfidenceBars() {
        const bars = document.querySelectorAll(".confidence-fill");
        if (!bars.length) {
            return;
        }

        window.setTimeout(() => {
            bars.forEach((bar) => {
                const target = bar.style.getPropertyValue("--target-width") || "0%";
                bar.style.width = target;
            });
        }, 260);
    }

    function initAppointmentModal() {
        const modal = document.getElementById("appointmentModal");
        const closeButton = document.getElementById("closeModalButton");
        const triggerButtons = document.querySelectorAll(".book-appointment-btn");

        if (!modal || !closeButton || !triggerButtons.length) {
            return;
        }

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

        triggerButtons.forEach((button) => {
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

    function initParticles() {
        const host = document.getElementById("particle-layer");
        if (!host) {
            return;
        }

        const canvas = document.createElement("canvas");
        const context = canvas.getContext("2d");
        if (!context) {
            return;
        }

        host.appendChild(canvas);

        const particles = [];

        function resize() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }

        function randomParticle() {
            return {
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                size: Math.random() * 2.5 + 0.4,
                speedX: (Math.random() - 0.5) * 0.28,
                speedY: (Math.random() - 0.5) * 0.28,
                hue: Math.random() > 0.5 ? "0, 212, 255" : "0, 255, 136",
            };
        }

        resize();

        for (let i = 0; i < PARTICLE_COUNT; i += 1) {
            particles.push(randomParticle());
        }

        function animate() {
            context.clearRect(0, 0, canvas.width, canvas.height);

            particles.forEach((particle) => {
                particle.x += particle.speedX;
                particle.y += particle.speedY;

                if (particle.x < -8 || particle.x > canvas.width + 8) {
                    particle.speedX *= -1;
                }
                if (particle.y < -8 || particle.y > canvas.height + 8) {
                    particle.speedY *= -1;
                }

                context.beginPath();
                context.fillStyle = `rgba(${particle.hue}, 0.45)`;
                context.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
                context.fill();
            });

            for (let i = 0; i < particles.length; i += 1) {
                for (let j = i + 1; j < particles.length; j += 1) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const distance = Math.sqrt(dx * dx + dy * dy);

                    if (distance < 120) {
                        const alpha = (1 - distance / 120) * 0.15;
                        context.strokeStyle = `rgba(0, 212, 255, ${alpha})`;
                        context.lineWidth = 1;
                        context.beginPath();
                        context.moveTo(particles[i].x, particles[i].y);
                        context.lineTo(particles[j].x, particles[j].y);
                        context.stroke();
                    }
                }
            }

            window.requestAnimationFrame(animate);
        }

        window.addEventListener("resize", resize);
        window.requestAnimationFrame(animate);
    }

    function bootstrap() {
        setActiveNav();
        initRevealAnimations();
        initCounters();
        initConfidenceBars();
        initAppointmentModal();
        initParticles();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", bootstrap);
    } else {
        bootstrap();
    }
})();
