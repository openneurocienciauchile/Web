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
  # ─────────────────────────────────────────────────────────────
  # 2. REDES — franja compacta bajo el Hero
  # ─────────────────────────────────────────────────────────────
  - block: markdown
    id: rrss-top
    content:
      title: ''
      text: |
        <div style="position:relative;left:50%;right:50%;margin-left:-50vw;margin-right:-50vw;width:100vw;max-width:100vw;background:#0A1533;padding:14px 24px;display:flex;flex-wrap:wrap;gap:12px;justify-content:center;align-items:center;">
          <span style="color:#cdd6f4;font-family:'Roboto Condensed',sans-serif;font-size:.82rem;letter-spacing:.14em;text-transform:uppercase;font-weight:700;">Síguenos en redes</span>
          <a href="https://x.com/NeuroUChile" target="_blank" rel="noopener" aria-label="X (Twitter)" style="display:inline-flex;align-items:center;gap:7px;padding:7px 16px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.18);border-radius:999px;color:#fff;text-decoration:none;font-family:'IBM Plex Sans',sans-serif;font-size:.86rem;font-weight:600;"><svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg><span>X</span></a>
          <a href="https://www.instagram.com/neuro_uchile/" target="_blank" rel="noopener" aria-label="Instagram" style="display:inline-flex;align-items:center;gap:7px;padding:7px 16px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.18);border-radius:999px;color:#fff;text-decoration:none;font-family:'IBM Plex Sans',sans-serif;font-size:.86rem;font-weight:600;"><svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.2c3.2 0 3.58.01 4.85.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.43.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.43.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.23-.41a3.66 3.66 0 0 1-1.38-.9 3.66 3.66 0 0 1-.9-1.38c-.16-.43-.36-1.06-.41-2.23-.06-1.27-.07-1.65-.07-4.85s.01-3.58.07-4.85c.05-1.17.25-1.8.41-2.23.21-.56.48-.96.9-1.38.42-.42.82-.69 1.38-.9.43-.16 1.06-.36 2.23-.41C8.42 2.21 8.8 2.2 12 2.2zm0 1.62c-3.15 0-3.52.01-4.76.07-.86.04-1.33.18-1.64.3-.41.16-.71.35-1.02.66-.31.31-.5.61-.66 1.02-.12.31-.26.78-.3 1.64-.06 1.24-.07 1.61-.07 4.76s.01 3.52.07 4.76c.04.86.18 1.33.3 1.64.16.41.35.71.66 1.02.31.31.61.5 1.02.66.31.12.78.26 1.64.3 1.24.06 1.61.07 4.76.07s3.52-.01 4.76-.07c.86-.04 1.33-.18 1.64-.3.41-.16.71-.35 1.02-.66.31-.31.5-.61.66-1.02.12-.31.26-.78.3-1.64.06-1.24.07-1.61.07-4.76s-.01-3.52-.07-4.76c-.04-.86-.18-1.33-.3-1.64a2.75 2.75 0 0 0-.66-1.02 2.75 2.75 0 0 0-1.02-.66c-.31-.12-.78-.26-1.64-.3-1.24-.06-1.61-.07-4.76-.07zm0 2.76a5.42 5.42 0 1 1 0 10.84 5.42 5.42 0 0 1 0-10.84zm0 1.62a3.8 3.8 0 1 0 0 7.6 3.8 3.8 0 0 0 0-7.6zm5.6-2.91a1.27 1.27 0 1 1 0 2.54 1.27 1.27 0 0 1 0-2.54z"/></svg><span>Instagram</span></a>
          <a href="https://www.youtube.com/@neurocienciauchile6900" target="_blank" rel="noopener" aria-label="YouTube" style="display:inline-flex;align-items:center;gap:7px;padding:7px 16px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.18);border-radius:999px;color:#fff;text-decoration:none;font-family:'IBM Plex Sans',sans-serif;font-size:.86rem;font-weight:600;"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M23.5 6.2a3.02 3.02 0 0 0-2.12-2.14C19.5 3.55 12 3.55 12 3.55s-7.5 0-9.38.51A3.02 3.02 0 0 0 .5 6.2 31.5 31.5 0 0 0 0 12a31.5 31.5 0 0 0 .5 5.8 3.02 3.02 0 0 0 2.12 2.14c1.88.51 9.38.51 9.38.51s7.5 0 9.38-.51a3.02 3.02 0 0 0 2.12-2.14A31.5 31.5 0 0 0 24 12a31.5 31.5 0 0 0-.5-5.8zM9.55 15.57V8.43L15.82 12z"/></svg><span>YouTube</span></a>
        </div>
    design:
      spacing:
        padding: ['0', '0', '0', '0']
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
