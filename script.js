const body = document.body;
const header = document.querySelector("[data-header]");
const menuToggle = document.querySelector("[data-menu-toggle]");
const navLinks = document.querySelectorAll(".nav a");
const year = document.querySelector("[data-year]");
const form = document.querySelector("[data-contact-form]");
const cookieStorageKey = "orquiviaCookieConsent";

if (year) {
  year.textContent = new Date().getFullYear();
}

const syncHeader = () => {
  header?.classList.toggle("is-scrolled", window.scrollY > 12);
};

syncHeader();
window.addEventListener("scroll", syncHeader, { passive: true });

menuToggle?.addEventListener("click", () => {
  const isOpen = body.classList.toggle("menu-open");
  menuToggle.setAttribute("aria-expanded", String(isOpen));
  menuToggle.setAttribute("aria-label", isOpen ? "Cerrar menú" : "Abrir menú");
});

navLinks.forEach((link) => {
  link.addEventListener("click", () => {
    body.classList.remove("menu-open");
    menuToggle?.setAttribute("aria-expanded", "false");
    menuToggle?.setAttribute("aria-label", "Abrir menú");
  });
});

const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.16 }
);

document.querySelectorAll(".reveal").forEach((element) => revealObserver.observe(element));

const counterObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;

      const element = entry.target;
      const target = Number(element.dataset.counter);
      const duration = 1200;
      const start = performance.now();

      const tick = (now) => {
        const progress = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        element.textContent = Math.round(target * eased).toLocaleString("es-ES");

        if (progress < 1) {
          requestAnimationFrame(tick);
        }
      };

      requestAnimationFrame(tick);
      counterObserver.unobserve(element);
    });
  },
  { threshold: 0.6 }
);

document.querySelectorAll("[data-counter]").forEach((element) => counterObserver.observe(element));

form?.addEventListener("submit", (event) => {
  event.preventDefault();

  const data = new FormData(form);
  const nombre = data.get("nombre") || "";
  const email = data.get("email") || "";
  const mensaje = data.get("mensaje") || "";
  const subject = encodeURIComponent(`Consulta web Orquivia - ${nombre}`);
  const bodyText = encodeURIComponent(`Nombre: ${nombre}\nEmail: ${email}\n\nMensaje:\n${mensaje}`);

  window.location.href = `mailto:contacto@orquivia.com?subject=${subject}&body=${bodyText}`;
});

const showCookieBanner = () => {
  if (localStorage.getItem(cookieStorageKey)) return;

  const banner = document.createElement("section");
  banner.className = "cookie-banner";
  banner.setAttribute("aria-label", "Aviso de cookies");
  banner.innerHTML = `
    <div>
      <strong>Cookies</strong>
      <p>
        Usamos cookies técnicas y una preferencia local para recordar tu elección. Si en el futuro añadimos analítica,
        solo se activará si aceptas.
      </p>
      <a href="politica-cookies.html">Política de cookies</a>
    </div>
    <div class="cookie-actions">
      <button class="button secondary" type="button" data-cookie-choice="rejected">Rechazar</button>
      <button class="button primary" type="button" data-cookie-choice="accepted">Aceptar</button>
    </div>
  `;

  document.body.appendChild(banner);

  banner.querySelectorAll("[data-cookie-choice]").forEach((button) => {
    button.addEventListener("click", () => {
      localStorage.setItem(cookieStorageKey, button.dataset.cookieChoice);
      banner.classList.add("is-hidden");
      window.setTimeout(() => banner.remove(), 220);
    });
  });
};

document.querySelectorAll("[data-cookie-reset]").forEach((button) => {
  button.addEventListener("click", () => {
    localStorage.removeItem(cookieStorageKey);
    showCookieBanner();
  });
});

showCookieBanner();
