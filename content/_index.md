---
title: ''
summary: ''
date: 2022-10-24
type: landing

design:
  spacing: '0rem'

sections:

  # ─────────────────────────────────────────────────────────────
  # 1. HERO — Frontis + nodos animados (texto sobrio + indicador a noticias)
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
            <p class="neuro-eyebrow neuro-rv">Universidad de Chile · Facultad de Medicina</p>
            <h1 class="neuro-h1 neuro-rv">Una comunidad amplia para la <span class="neuro-glow">neurociencia</span>, del laboratorio a la clínica.</h1>
            <p class="neuro-lead neuro-rv">Reunimos a investigadoras, investigadores y académicos de distintas facultades, sedes y hospitales de la Universidad de Chile, junto a una red de colaboradores. Unimos la neurociencia básica y la clínica, recogiendo una larga tradición y abriendo camino a la innovación al servicio de la salud.</p>
            <div class="neuro-cta neuro-rv">
              <a class="neuro-btn neuro-btn-primary" href="/Web/academicos/">Conoce nuestro equipo
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
              </a>
              <a class="neuro-btn neuro-btn-ghost" href="/Web/quienes-somos/">Quiénes somos</a>
            </div>
          </div>
          <a class="neuro-scroll" href="#noticias" aria-label="Ver noticias">
            <span>Noticias</span>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>
          </a>
        </div>
    design:
      spacing:
        padding: ['0', '0', '0', '0']

  # ─────────────────────────────────────────────────────────────
  # 2. ÚLTIMAS NOTICIAS — primer contenido del home
  # ─────────────────────────────────────────────────────────────
  - block: news-grid
    id: noticias

  # ─────────────────────────────────────────────────────────────
  # 3. PRÓXIMO SEMINARIO — blox personalizado (sin cambios)
  # ─────────────────────────────────────────────────────────────
  - block: evento-card
    id: seminario

  # ─────────────────────────────────────────────────────────────
  # 4. REDES SOCIALES — cuadro ancho al final (sin cambios)
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
