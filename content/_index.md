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
        <div style="display:inline-block; background:rgba(255,255,255,0.82); backdrop-filter:blur(4px); border-radius:12px; padding:2rem 3rem; text-align:center;">
          <h1 style="color:#1a1a2e; font-size:clamp(2rem,5vw,3.5rem); font-weight:800; line-height:1.15; margin:0 0 0.5rem;">
            Departamento de<br>Neurociencia
          </h1>
          <p style="color:#333; font-size:1.1rem; margin:0;">
            Universidad de Chile · Facultad de Medicina
          </p>
          <div style="display:flex; gap:12px; justify-content:center; margin-top:1.5rem; flex-wrap:wrap;">
            <a href="/Web/quienes-somos" style="background:#1565C0; color:#fff; padding:10px 24px; border-radius:7px; text-decoration:none; font-weight:600;">Conócenos</a>
            <a href="/Web/blog" style="background:transparent; color:#1a1a2e; border:2px solid #1a1a2e; padding:10px 24px; border-radius:7px; text-decoration:none; font-weight:600;">Ver noticias</a>
          </div>
        </div>
      cta:
        label: ''
        url: ''
    design:
      background:
        image:
          filename: brain.jpg
          filters:
            brightness: 0.6        # un poco más claro que antes, el recuadro ya oscurece menos
          parallax: false
          position: center
          size: cover
        text_color_light: false    # ← cambia a false porque ahora el texto es oscuro
      spacing:
        padding: ['14px', '0', '14px', '0']
  # ─────────────────────────────────────────────────────────────
  # 2. ÚLTIMAS NOTICIAS (desde content/blog)
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
      columns: 2

  # ─────────────────────────────────────────────────────────────
  # 3. PRÓXIMO SEMINARIO (desde content/events)
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
          - events
      order: desc
    design:
      view: card
      columns: '1'

  # ─────────────────────────────────────────────────────────────
  # 4. REDES SOCIALES
  # Actualiza las URLs con los perfiles reales del departamento.
  # ─────────────────────────────────────────────────────────────
  - block: markdown
    id: redes
    content:
      title: Síguenos
      subtitle: ''
      text: |
        <div style="display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin:1.5rem 0;">
          <a href="https://twitter.com/neurocienciauch" target="_blank" rel="noopener"
             style="display:inline-flex;align-items:center;gap:8px;padding:10px 20px;background:#000;color:#fff;border-radius:8px;text-decoration:none;font-weight:600;font-size:0.9rem;">
            Twitter / X
          </a>
          <a href="https://www.instagram.com/neurocienciauchile/" target="_blank" rel="noopener"
             style="display:inline-flex;align-items:center;gap:8px;padding:10px 20px;background:linear-gradient(45deg,#f09433,#e6683c,#dc2743,#cc2366,#bc1888);color:#fff;border-radius:8px;text-decoration:none;font-weight:600;font-size:0.9rem;">
            Instagram
          </a>
          <a href="https://www.youtube.com/@neurocienciauchile" target="_blank" rel="noopener"
             style="display:inline-flex;align-items:center;gap:8px;padding:10px 20px;background:#FF0000;color:#fff;border-radius:8px;text-decoration:none;font-weight:600;font-size:0.9rem;">
            YouTube
          </a>
          <a href="https://www.linkedin.com/company/neurociencia-uchile/" target="_blank" rel="noopener"
             style="display:inline-flex;align-items:center;gap:8px;padding:10px 20px;background:#0A66C2;color:#fff;border-radius:8px;text-decoration:none;font-weight:600;font-size:0.9rem;">
            LinkedIn
          </a>
        </div>
    design:
      columns: '1'
      spacing:
        padding: ['20px', '0', '40px', '0']
---