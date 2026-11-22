/* ═══════════════════════════════════════════════════════════════════════════
   Ingeniería & Automatización by Ingversia — main.js
   JS Vanilla · Drawer Accesible · Scroll Reveal · Spotlight · Constructor Técnico
   ═══════════════════════════════════════════════════════════════════════════ */

(function () {
  'use strict';

  const WHATSAPP_NUMBER = '573229637406';
  const CONTACT_EMAIL = 'contacto@ingversia.com';
  const prefersReducedMotion = Boolean(
    window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches
  );

  /* ── 1. DRAWER MÓVIL ACCESIBLE CON FOCUS TRAP ── */
  function initMobileDrawer() {
    const toggleBtn = document.getElementById('navMobileToggle');
    const overlay = document.getElementById('mobileDrawerOverlay');
    const drawer = document.getElementById('mobileDrawer');
    const closeBtn = document.getElementById('mobileDrawerClose');

    if (!toggleBtn || !overlay || !drawer) return;

    const getFocusable = () =>
      Array.from(
        drawer.querySelectorAll('a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])')
      );

    function openDrawer() {
      overlay.removeAttribute('inert');
      overlay.setAttribute('aria-hidden', 'false');
      overlay.classList.add('active');
      toggleBtn.setAttribute('aria-expanded', 'true');
      document.body.style.overflow = 'hidden';

      void drawer.offsetWidth;
      if (closeBtn) {
        closeBtn.focus({ preventScroll: true });
      } else {
        const focusable = getFocusable();
        if (focusable[0]) focusable[0].focus({ preventScroll: true });
      }
    }

    function closeDrawer(restoreFocus = true) {
      if (!overlay.classList.contains('active')) return;
      overlay.classList.remove('active');
      overlay.setAttribute('aria-hidden', 'true');
      overlay.setAttribute('inert', '');
      toggleBtn.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';

      if (restoreFocus) {
        toggleBtn.focus();
      }
    }

    toggleBtn.addEventListener('click', openDrawer);
    closeBtn?.addEventListener('click', () => closeDrawer(true));

    overlay.addEventListener('click', (event) => {
      if (event.target === overlay) {
        closeDrawer(true);
      }
    });

    drawer.querySelectorAll('a[href]').forEach((link) => {
      link.addEventListener('click', () => closeDrawer(false));
    });

    document.addEventListener('keydown', (event) => {
      if (!overlay.classList.contains('active')) return;

      if (event.key === 'Escape') {
        event.preventDefault();
        closeDrawer(true);
        return;
      }

      if (event.key === 'Tab') {
        const focusable = getFocusable();
        if (!focusable.length) return;
        const first = focusable[0];
        const last = focusable[focusable.length - 1];

        if (event.shiftKey && document.activeElement === first) {
          event.preventDefault();
          last.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
          event.preventDefault();
          first.focus();
        }
      }
    });
  }

  /* ── 2. SCROLL REVEAL PROGRESIVO ── */
  function initScrollReveal() {
    const elements = document.querySelectorAll('.reveal-on-scroll');
    if (!elements.length || prefersReducedMotion) {
      elements.forEach((el) => el.classList.add('is-revealed'));
      return;
    }

    document.documentElement.classList.add('has-scroll-reveal');

    const revealVisibleNow = () => {
      const vh = window.innerHeight || 800;
      elements.forEach((el) => {
        const rect = el.getBoundingClientRect();
        if (rect.top <= vh + 80) {
          el.classList.add('is-revealed');
        }
      });
    };

    revealVisibleNow();

    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add('is-revealed');
              observer.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.04, rootMargin: '0px 0px 80px 0px' }
      );

      elements.forEach((el) => {
        if (!el.classList.contains('is-revealed')) {
          observer.observe(el);
        }
      });
    } else {
      elements.forEach((el) => el.classList.add('is-revealed'));
    }

    setTimeout(() => {
      elements.forEach((el) => el.classList.add('is-revealed'));
    }, 1200);
  }

  /* ── 3. EFECTO SPOTLIGHT EN TARJETAS ── */
  function initSpotlightCards() {
    if (prefersReducedMotion) return;
    const cards = document.querySelectorAll('.spotlight-card');
    if (!cards.length) return;

    cards.forEach((card) => {
      const setMouse = (x, y) => {
        const rect = card.getBoundingClientRect();
        card.style.setProperty('--mouse-x', `${x - rect.left}px`);
        card.style.setProperty('--mouse-y', `${y - rect.top}px`);
      };

      card.addEventListener('mousemove', (e) => setMouse(e.clientX, e.clientY));
      card.addEventListener('mouseleave', () => {
        card.style.setProperty('--mouse-x', '-999px');
        card.style.setProperty('--mouse-y', '-999px');
      });
      card.addEventListener(
        'touchmove',
        (e) => {
          if (e.touches?.[0]) setMouse(e.touches[0].clientX, e.touches[0].clientY);
        },
        { passive: true }
      );
      card.addEventListener(
        'touchend',
        () => {
          setTimeout(() => {
            card.style.setProperty('--mouse-x', '-999px');
            card.style.setProperty('--mouse-y', '-999px');
          }, 450);
        },
        { passive: true }
      );
    });
  }

  /* ── 4. CONSTRUCTOR INTERACTIVO DE DIAGNÓSTICO TÉCNICO ── */
  const SERVICES_CONFIG = {
    mikrotik: {
      label: 'Redes & MikroTik',
      subject: 'Diagnóstico Técnico Redes MikroTik — Ingeniería by Ingversia',
      placeholder: 'Ej: Tenemos 2 ISP (fibra + respaldo), router RB4011, 25 usuarios y POS/VPN que se cae al conmutar...',
      symptoms: [
        'Failover Dual-WAN no conmuta en producción',
        'Balanceo PCC / separación tráfico POS-VoIP-cámaras',
        'VPN entre sedes o teletrabajo (WireGuard / IPsec)',
        'Segmentación VLANs, QoS y hardening RouterOS',
        'Auditoría / rescate de red hecha por terceros',
        'Servidor local seguro, acceso Zero Trust y backups 3-2-1'
      ]
    },
    pcb: {
      label: 'Electrónica, PCB & RF',
      subject: 'Cotización Electrónica / PCB / Firmware — Ingeniería by Ingversia',
      placeholder: 'Ej: Necesitamos diseñar tarjeta 2 o 4 capas con ESP32/STM32, etapa RS-485 y carcasa 3D...',
      symptoms: [
        'Diseño de esquemático y layout PCB (Gerbers + BOM)',
        'Etapa de Radiofrecuencia (RF) / enlace inalámbrico',
        'Firmware embebido y adquisición de sensores',
        'Armado, pruebas de banco y soldadura SMD/THT',
        'Hardware + carcasa a medida con BerdeX 3D'
      ]
    },
    plc: {
      label: 'Automatización, PLC & Telemetría',
      subject: 'Proyecto Automatización PLC / Telemetría — Ingeniería by Ingversia',
      placeholder: 'Ej: Tablero con PLC, señales 4-20 mA / Modbus RTU, necesitamos registro histórico y alertas...',
      symptoms: [
        'Programación e integración de PLC / tablero de control',
        'Instrumentación Modbus RTU/TCP, RS-485 o 4-20 mA',
        'Tablero HMI/web local, adquisición de datos y alertas',
        'Solución inspirada en arquitectura NEXUS (Edge + reportes)'
      ]
    },
    manuales: {
      label: 'Manuales & Levantamiento Técnico',
      subject: 'Solicitud Levantamiento y Manual Técnico — Ingeniería by Ingversia',
      placeholder: 'Ej: Tablero eléctrico y red sin planos; necesitamos diagrama unifilar, borneras y manual de fallas...',
      symptoms: [
        'Levantamiento de tablero o circuito sin documentación',
        'Manual de operación, mantenimiento y troubleshooting',
        'Diagramas eléctricos, electrónicos o topología de red',
        'Estandarización técnica para auditoría o capacitación'
      ]
    }
  };

  function initDiagnosticBuilder() {
    const builder = document.getElementById('diagnosticBuilder');
    if (!builder) return;

    const serviceTabs = Array.from(builder.querySelectorAll('.diag-tab[data-service]'));
    const symptomsContainer = document.getElementById('diagSymptomChips');
    const modeChips = Array.from(builder.querySelectorAll('.diag-chip[data-mode]'));
    const companyInput = document.getElementById('diagCompany');
    const cityInput = document.getElementById('diagCity');
    const notesInput = document.getElementById('diagNotes');
    const previewEl = document.getElementById('diagPreviewText');
    const waBtn = document.getElementById('diagWhatsappBtn');
    const emailBtn = document.getElementById('diagEmailBtn');
    const copyBtn = document.getElementById('diagCopyBtn');
    const copyStatus = document.getElementById('diagCopyStatus');

    const defaultService = builder.dataset.defaultService;
    const state = {
      service: SERVICES_CONFIG[defaultService] ? defaultService : 'mikrotik',
      symptom: '',
      mode: 'Diagnóstico técnico inicial'
    };

    function renderSymptoms() {
      if (!symptomsContainer) return;
      const config = SERVICES_CONFIG[state.service];
      const list = config.symptoms;
      state.symptom = list[0];
      symptomsContainer.innerHTML = '';

      list.forEach((item, index) => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = `diag-chip${index === 0 ? ' is-active' : ''}`;
        btn.dataset.symptom = item;
        btn.setAttribute('aria-pressed', index === 0 ? 'true' : 'false');
        btn.textContent = item;
        btn.addEventListener('click', () => {
          state.symptom = item;
          symptomsContainer.querySelectorAll('.diag-chip').forEach((chip) => {
            const active = chip === btn;
            chip.classList.toggle('is-active', active);
            chip.setAttribute('aria-pressed', active ? 'true' : 'false');
          });
          updateOutput();
        });
        symptomsContainer.appendChild(btn);
      });

      if (notesInput) {
        notesInput.placeholder = config.placeholder;
      }
    }

    function buildMessage() {
      const config = SERVICES_CONFIG[state.service];
      const company = companyInput?.value.trim();
      const city = cityInput?.value.trim();
      const notes = notesInput?.value.trim();

      const lines = [
        'Hola equipo de Ingeniería & Automatización (Ingversia), solicito revisión técnica:',
        '',
        `• Frente: ${config.label}`,
        `• Necesidad principal: ${state.symptom}`,
        `• Modalidad: ${state.mode}`
      ];

      if (company) lines.push(`• Empresa / Contacto: ${company}`);
      if (city) lines.push(`• Ciudad / Atención: ${city}`);
      if (notes) lines.push(`• Detalle técnico: ${notes}`);

      lines.push('', 'Quedo atento para coordinar el diagnóstico y alcance.');
      return lines.join('\n');
    }

    function updateOutput() {
      const config = SERVICES_CONFIG[state.service];
      const message = buildMessage();

      if (previewEl) previewEl.textContent = message;
      if (waBtn) {
        waBtn.href = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`;
      }
      if (emailBtn) {
        emailBtn.href = `mailto:${CONTACT_EMAIL}?subject=${encodeURIComponent(config.subject)}&body=${encodeURIComponent(message)}`;
      }
    }

    function selectService(key) {
      if (!SERVICES_CONFIG[key]) return;
      state.service = key;
      serviceTabs.forEach((tab) => {
        const active = tab.dataset.service === key;
        tab.classList.toggle('is-active', active);
        tab.setAttribute('aria-selected', active ? 'true' : 'false');
      });
      renderSymptoms();
      updateOutput();
    }

    function selectMode(modeName) {
      if (!modeName) return;
      state.mode = modeName;
      modeChips.forEach((chip) => {
        const active = chip.dataset.mode === modeName;
        chip.classList.toggle('is-active', active);
        chip.setAttribute('aria-pressed', active ? 'true' : 'false');
      });
      updateOutput();
    }

    serviceTabs.forEach((tab) => {
      tab.addEventListener('click', () => selectService(tab.dataset.service));
    });

    modeChips.forEach((chip) => {
      chip.addEventListener('click', () => selectMode(chip.dataset.mode));
    });

    [companyInput, cityInput, notesInput].forEach((input) => {
      input?.addEventListener('input', updateOutput);
    });

    copyBtn?.addEventListener('click', async () => {
      const text = buildMessage();
      let copied = false;

      if (navigator.clipboard?.writeText) {
        try {
          await navigator.clipboard.writeText(text);
          copied = true;
        } catch {
          copied = false;
        }
      }

      if (!copied) {
        const temp = document.createElement('textarea');
        temp.value = text;
        temp.setAttribute('readonly', '');
        temp.style.position = 'fixed';
        temp.style.left = '-9999px';
        document.body.appendChild(temp);
        temp.select();
        try {
          copied = document.execCommand('copy');
        } catch {
          copied = false;
        }
        document.body.removeChild(temp);
      }

      if (copyStatus) {
        copyStatus.textContent = copied
          ? 'Resumen copiado al portapapeles. Puedes pegarlo en WhatsApp o correo.'
          : 'No fue posible copiar automáticamente; usa el botón de WhatsApp o correo.';
        setTimeout(() => {
          copyStatus.textContent = '';
        }, 4000);
      }
    });

    // Permitir que tarjetas de modalidades o botones internos preseleccionen el constructor
    document.querySelectorAll('[data-select-mode], [data-select-service]').forEach((trigger) => {
      trigger.addEventListener('click', () => {
        const svc = trigger.dataset.selectService;
        const mode = trigger.dataset.selectMode;
        if (svc) selectService(svc);
        if (mode) selectMode(mode);
      });
    });

    selectService(state.service);
    selectMode(state.mode);
  }

  /* ── 5. NAVBAR FLOTANTE (SCROLL STATE) & DROPDOWN ACCESIBLE ── */
  function initFloatingNavbar() {
    const navbar = document.getElementById('mainNavbar');
    if (!navbar) return;

    const onScroll = () => {
      navbar.classList.toggle('scrolled', window.scrollY > 24);
    };

    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  function initNavDropdown() {
    const dropdown = document.querySelector('.nav-has-dropdown');
    const trigger = dropdown?.querySelector('.nav-dropdown-trigger');
    if (!dropdown || !trigger) return;

    function setOpen(open) {
      dropdown.classList.toggle('is-open', open);
      trigger.setAttribute('aria-expanded', open ? 'true' : 'false');
    }

    trigger.addEventListener('click', (event) => {
      event.preventDefault();
      event.stopPropagation();
      setOpen(!dropdown.classList.contains('is-open'));
    });

    dropdown.querySelectorAll('.dropdown-link').forEach((link) => {
      link.addEventListener('click', () => setOpen(false));
    });

    document.addEventListener('click', (event) => {
      if (!dropdown.contains(event.target)) {
        setOpen(false);
      }
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && dropdown.classList.contains('is-open')) {
        setOpen(false);
        trigger.focus();
      }
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    initFloatingNavbar();
    initNavDropdown();
    initMobileDrawer();
    initScrollReveal();
    initSpotlightCards();
    initDiagnosticBuilder();
  });
})();
