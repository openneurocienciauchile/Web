---
title: ''
summary: ''
date: 2022-10-24
type: landing

design:
  spacing: '6rem'

sections:

  # ─────────────────────────────────────────────────────────────
  # 1. HERO — Banner institucional
  # ─────────────────────────────────────────────────────────────
  - block: hero
    content:
      title: ''
      text: |
        <div style="display:inline-block; background:rgba(255,255,255,0.82); backdrop-filter:blur(4px); border-radius:12px; padding:1.2rem 2.5rem; text-align:center;">
          <h1 style="color:#1a1a2e; font-size:clamp(1.5rem,4vw,2.8rem); font-weight:300; line-height:1.2; margin:0 0 0.4rem; letter-spacing:0.04em;">
            Departamento de Neurociencia
          </h1>
          <p style="color:#555; font-size:1rem; margin:0; font-weight:300;">
            Universidad de Chile · Facultad de Medicina
          </p>
          <div style="display:flex; gap:12px; justify-content:center; margin-top:1.2rem; flex-wrap:wrap;">
            <a href="/Web/academicos" style="background:#1565C0; color:#fff; padding:9px 22px; border-radius:7px; text-decoration:none; font-weight:500; font-size:0.95rem;">Nuestro equipo</a>
            <a href="/Web/temas" style="background:transparent; color:#1a1a2e; border:2px solid #1a1a2e; padding:9px 22px; border-radius:7px; text-decoration:none; font-weight:500; font-size:0.95rem;">Temas</a>
          </div>
        </div>
      cta:
        label: ''
        url: ''
    design:
      background:
        image:
          filename: facultad.png
          filters:
            brightness: 0.6
          parallax: false
          position: center
          size: cover
        text_color_light: false
      spacing:
        padding: ['60px', '0', '60px', '0']

  # ─────────────────────────────────────────────────────────────
  # 2. ÚLTIMAS NOTICIAS — 2 columnas, solo imagen y título
  # ─────────────────────────────────────────────────────────────
  - block: collection
    id: noticias
    content:
      title: Últimas Noticias
      subtitle: ''
      text: ''
      count: 4
      filters:
        folders:
          - blog
        exclude_featured: false
      order: desc
    design:
      view: article-grid
      columns: '2'

  # ─────────────────────────────────────────────────────────────
  # 3. PRÓXIMO SEMINARIO (desde content/eventos)
  # ─────────────────────────────────────────────────────────────
  - block: collection
    id: seminario
    content:
      title: Próximo Seminario
      subtitle: ''
      text: ''
      count: 1
      filters:
        folders:
          - eventos
      order: desc
    design:
      view: card
      columns: '1'

  # ─────────────────────────────────────────────────────────────
  # 4. REDES SOCIALES — cuadro ancho al final
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