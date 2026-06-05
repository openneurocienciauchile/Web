---
title: ''
summary: ''
date: 2022-10-24
type: landing

design:
  spacing: '0rem'

sections:

  # ─────────────────────────────────────────────────────────────
  # 1. HERO — Frontis + nodos animados (rediseño v2, CSS en head-end)
  # ─────────────────────────────────────────────────────────────
  - block: markdown
    id: hero-neuro
    content:
      title: ''
      text: |
        <div class="neuro-hero">
          <img class="neuro-hero-seal" src="/Web/uploads/escudo-blanco.png" alt="" aria-hidden="true">
          <canvas id="neuro-net" class="neuro-hero-canvas"></canvas>
          <div class="neuro-hero-inner">
            <p class="neuro-eyebrow neuro-rv">Facultad de Medicina · Universidad de Chile</p>
            <h1 class="neuro-h1 neuro-rv">Investigamos el <span class="neuro-glow">cerebro</span>, desde la célula hasta la conducta.</h1>
            <p class="neuro-lead neuro-rv">Una unidad académica que reúne a investigadores e investigadoras de la Universidad de Chile en torno a la docencia, la formación científica y la investigación en neurociencia con aplicación en salud.</p>
            <div class="neuro-cta neuro-rv">
              <a class="neuro-btn neuro-btn-primary" href="/Web/academicos/">Conoce nuestro equipo
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
              </a>
              <a class="neuro-btn neuro-btn-ghost" href="/Web/temas/">Áreas de investigación</a>
            </div>
          </div>
        </div>
    design:
      spacing:
        padding: ['0', '0', '0', '0']

  # ─────────────────────────────────────────────────────────────
  # 2. ÁREAS DE INVESTIGACIÓN — grilla de temas
  # ─────────────────────────────────────────────────────────────
  - block: markdown
    id: temas-home
    content:
      title: ''
      text: |
        <div class="neuro-temas">
          <div class="neuro-temas-inner">
            <div class="neuro-shead neuro-rv">
              <div>
                <p class="neuro-eyebrow neuro-eyebrow-blue">Líneas de trabajo</p>
                <h2 class="neuro-h2">Nueve áreas que articulan nuestra ciencia</h2>
                <p class="neuro-shead-sub">Desde la neurobiología molecular hasta la neurociencia cognitiva y clínica, organizadas en áreas temáticas que conectan laboratorios, académicos y formación.</p>
              </div>
              <a class="neuro-link-more" href="/Web/temas/">Ver todas las áreas
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
              </a>
            </div>
            <div class="neuro-grid">
              <a class="neuro-card neuro-rv" href="/Web/temas/neurobiologia-molecular-celular/"><span class="neuro-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><circle cx="12" cy="12" r="2"/><ellipse cx="12" cy="12" rx="10" ry="4.2"/><ellipse cx="12" cy="12" rx="10" ry="4.2" transform="rotate(60 12 12)"/><ellipse cx="12" cy="12" rx="10" ry="4.2" transform="rotate(120 12 12)"/></svg></span><span class="neuro-card-title">Neurobiología molecular y celular</span><span class="neuro-card-desc">Mecanismos moleculares y celulares de la función neuronal.</span></a>
              <a class="neuro-card neuro-rv" href="/Web/temas/neurociencia-cognitiva/"><span class="neuro-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12h4l3 8 4-16 3 8h4"/></svg></span><span class="neuro-card-title">Neurociencia cognitiva</span><span class="neuro-card-desc">Bases neurales de la percepción, memoria y atención.</span></a>
              <a class="neuro-card neuro-rv" href="/Web/temas/neurociencia-computacional-ia/"><span class="neuro-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="6" width="12" height="12" rx="1.5"/><rect x="9.5" y="9.5" width="5" height="5"/><path d="M9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/></svg></span><span class="neuro-card-title">Neurociencia computacional e IA</span><span class="neuro-card-desc">Modelos, análisis de datos y aprendizaje automático.</span></a>
              <a class="neuro-card neuro-rv" href="/Web/temas/neurociencia-desarrollo/"><span class="neuro-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22V11"/><path d="M12 11C12 7.5 9.3 5.5 5.5 5.5c-.2 3.6 2.4 5.7 6.5 5.5Z"/><path d="M12 13.2c0-3 2.4-4.8 5.8-4.8.2 3.1-2.3 5-5.8 4.8Z"/></svg></span><span class="neuro-card-title">Neurociencia del desarrollo</span><span class="neuro-card-desc">Maduración del sistema nervioso a lo largo de la vida.</span></a>
              <a class="neuro-card neuro-rv" href="/Web/temas/neurologia-clinica-traslacional/"><span class="neuro-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4h6v3H9z"/><path d="M8 14h2l1.2 3 2-6 1 3H17"/></svg></span><span class="neuro-card-title">Neurología clínica y traslacional</span><span class="neuro-card-desc">Del laboratorio a la práctica clínica y la salud.</span></a>
              <a class="neuro-card neuro-rv" href="/Web/temas/neuromodulacion-control-motor/"><span class="neuro-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 4 14h7l-1 8 9-12h-7l1-8z"/></svg></span><span class="neuro-card-title">Neuromodulación y control motor</span><span class="neuro-card-desc">Circuitos del movimiento y técnicas de modulación.</span></a>
              <a class="neuro-card neuro-rv" href="/Web/temas/neuropsicologia-cognicion/"><span class="neuro-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="9" r="4.5"/><path d="M5.5 20.5c.6-3.4 3.2-5.5 6.5-5.5s5.9 2.1 6.5 5.5"/></svg></span><span class="neuro-card-title">Neuropsicología y cognición</span><span class="neuro-card-desc">Relación entre función cerebral y conducta.</span></a>
              <a class="neuro-card neuro-rv" href="/Web/temas/otoneurologia-audicion/"><span class="neuro-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6.5a7.2 7.2 0 0 1 13.5 1.5M6.5 9.5a4.3 4.3 0 0 1 8-1.2M9 12a1.6 1.6 0 0 1 3 .2"/><path d="M6 14a6 6 0 0 0 6 6"/></svg></span><span class="neuro-card-title">Otoneurología y audición</span><span class="neuro-card-desc">Sistema auditivo y vestibular, del oído a la corteza.</span></a>
              <a class="neuro-card neuro-rv" href="/Web/temas/envejecimiento-neurodegeneracion/"><span class="neuro-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h12M6 21h12M8 3v3l4 4 4-4V3M8 21v-3l4-4 4 4v3"/></svg></span><span class="neuro-card-title">Envejecimiento y neurodegeneración</span><span class="neuro-card-desc">Mecanismos del envejecimiento y enfermedades neurodegenerativas.</span></a>
            </div>
          </div>
        </div>
    design:
      spacing:
        padding: ['0', '0', '0', '0']

  # ─────────────────────────────────────────────────────────────
  # 3. ÚLTIMAS NOTICIAS — blox personalizado (sin cambios)
  # ─────────────────────────────────────────────────────────────
  - block: news-grid
    id: noticias

  # ─────────────────────────────────────────────────────────────
  # 4. PRÓXIMO SEMINARIO — blox personalizado (sin cambios)
  # ─────────────────────────────────────────────────────────────
  - block: evento-card
    id: seminario

  # ─────────────────────────────────────────────────────────────
  # 5. REDES SOCIALES — cuadro ancho al final (sin cambios)
  # ─────────────────────────────────────────────────────────────
  - block: markdown
    id: redes
    content:
      title: ''
      subtitle: ''
      text: |
        <div style="width:100%; background:#1a1a2e; padding:3rem 2rem; text-align:center; margin:0;">
          <h2 style="color:#fff; font-size:1.5rem; font-weight:700; margin-bottom:1.8rem; letter-spacing:0.03em;">Síguenos</h2>
          <div style="display:flex; flex-wrap:nowrap; gap:14px; justify-content:center; align-items:center; max-width:900px; margin:0 auto;">
            <a href="https://twitter.com/neurocienciauch" target="_blank" rel="noopener"
               style="display:inline-flex;align-items:center;justify-content:center;width:160px;padding:12px 0;background:#000;color:#fff;border:1.5px solid rgba(255,255,255,0.15);border-radius:8px;text-decoration:none;font-weight:600;font-size:0.95rem;">
              Twitter / X
            </a>
            <a href="https://www.instagram.com/neurocienciauchile/" target="_blank" rel="noopener"
               style="display:inline-flex;align-items:center;justify-content:center;width:160px;padding:12px 0;background:linear-gradient(45deg,#f09433,#dc2743,#bc1888);color:#fff;border:1.5px solid rgba(255,255,255,0.15);border-radius:8px;text-decoration:none;font-weight:600;font-size:0.95rem;">
              Instagram
            </a>
            <a href="https://www.youtube.com/@neurocienciauchile" target="_blank" rel="noopener"
               style="display:inline-flex;align-items:center;justify-content:center;width:160px;padding:12px 0;background:#CC0000;color:#fff;border:1.5px solid rgba(255,255,255,0.15);border-radius:8px;text-decoration:none;font-weight:600;font-size:0.95rem;">
              YouTube
            </a>
            <a href="https://www.linkedin.com/company/neurociencia-uchile/" target="_blank" rel="noopener"
               style="display:inline-flex;align-items:center;justify-content:center;width:160px;padding:12px 0;background:#0A66C2;color:#fff;border:1.5px solid rgba(255,255,255,0.15);border-radius:8px;text-decoration:none;font-weight:600;font-size:0.95rem;">
              LinkedIn
            </a>
          </div>
        </div>
    design:
      background:
        color: '#1a1a2e'
      spacing:
        padding: ['0', '0', '0', '0']
---
