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
            <h1 class="neuro-h1 neuro-rv"><span class="neuro-h1-main">Comprender el <span class="neuro-glow">cerebro</span>:</span><span class="neuro-h1-sub">de la molécula a la conducta, de la sinapsis a la sociedad — y de la ciencia a la salud.</span></h1>
            <p class="neuro-lead neuro-rv">Tradición que investiga, ciencia que se renueva: una red amplia de investigación en neurociencia, del laboratorio a la clínica.</p>
            <div class="neuro-cta neuro-rv">
              <a class="neuro-btn neuro-btn-primary" href="/Web/academicos/">Conoce nuestro equipo
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
              </a>
              <a class="neuro-btn neuro-btn-ghost" href="/Web/temas/">Nuestros temas</a>
            </div>
          </div>
          <a class="neuro-hero-scroll" href="#noticias" aria-label="Ir a Noticias"><span>Noticias</span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg></a>
        </div>
    design:
      spacing:
        padding: ['0', '0', '0', '0']

  # ─────────────────────────────────────────────────────────────
  # 3. ÚLTIMAS NOTICIAS — blox personalizado (sin cambios)
  # ─────────────────────────────────────────────────────────────
  - block: news-grid
    id: noticias
    design:
      spacing:
        padding: ['0', '0', '0', '0']

  # ─────────────────────────────────────────────────────────────
  # 3b. PRÓXIMO SEMINARIO — destacado + link a Eventos (blox propio)
  # ─────────────────────────────────────────────────────────────
  - block: proximo-seminario
    id: proximo-seminario
    design:
      spacing:
        padding: ['0', '0', '0', '0']

  # ─────────────────────────────────────────────────────────────
  # 4. LABORATORIOS — tira de logos (blox propio labs-strip)
  # ─────────────────────────────────────────────────────────────
  - block: labs-strip
    id: laboratorios
    design:
      spacing:
        padding: ['0', '0', '0', '0']

  # ─────────────────────────────────────────────────────────────
  # 5. INSTITUCIONES Y COLABORADORES — blox propio (data/colaboradores.yaml)
  # ─────────────────────────────────────────────────────────────
  - block: colaboradores
    id: colaboradores
    design:
      spacing:
        padding: ['0', '0', '0', '0']

  # ─────────────────────────────────────────────────────────────
  # REDES SOCIALES — cuadro ancho al final (sin cambios)
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
            <a href="https://x.com/NeuroUChile" target="_blank" rel="noopener"
               style="display:inline-flex;align-items:center;justify-content:center;width:160px;padding:12px 0;background:#000;color:#fff;border:1.5px solid rgba(255,255,255,0.15);border-radius:8px;text-decoration:none;font-weight:600;font-size:0.95rem;">
              Twitter / X
            </a>
            <a href="https://www.instagram.com/neuro_uchile/" target="_blank" rel="noopener"
               style="display:inline-flex;align-items:center;justify-content:center;width:160px;padding:12px 0;background:linear-gradient(45deg,#f09433,#dc2743,#bc1888);color:#fff;border:1.5px solid rgba(255,255,255,0.15);border-radius:8px;text-decoration:none;font-weight:600;font-size:0.95rem;">
              Instagram
            </a>
            <a href="https://www.youtube.com/@neurocienciauchile6900" target="_blank" rel="noopener"
               style="display:inline-flex;align-items:center;justify-content:center;width:160px;padding:12px 0;background:#CC0000;color:#fff;border:1.5px solid rgba(255,255,255,0.15);border-radius:8px;text-decoration:none;font-weight:600;font-size:0.95rem;">
              YouTube
            </a>
          </div>
        </div>
    design:
      background:
        color: '#1a1a2e'
      spacing:
        padding: ['0', '0', '0', '0']
---
