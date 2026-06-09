Manchester United Soccer Culture Project — generated asset bundle
=====================================================================

Generated original assets
-------------------------
- generated/site-mark.svg
- generated/site-logo.svg
- generated/favicon.svg
- generated/favicon.ico
- generated/favicon-16.png, favicon-32.png, favicon-48.png, favicon-64.png, favicon-128.png, favicon-180.png, favicon-192.png, favicon-512.png
- generated/apple-touch-icon.png
- generated/social-card.png
- generated/hero-stadium-abstract.svg

These logo/icon assets are original, non-official project branding. They intentionally do not copy the official Manchester United crest, mascot, ship, shield layout, or typography.

Photo assets included and optimized
-----------------------------------
- photos/stretford-end-exterior-original.jpg
- photos/stretford-end-exterior-1600.jpg / .webp
- photos/stretford-end-exterior-hero.jpg / .webp
- photos/old-trafford-aerial-original.jpg
- photos/old-trafford-aerial-1600.jpg / .webp
- photos/old-trafford-aerial-hero.jpg / .webp
- photos/stretford-end-crowd-original.jpg
- photos/stretford-end-crowd-1600.jpg / .webp
- photos/stretford-end-crowd-hero.jpg / .webp

Photo source notes
------------------
The bundled photos were downloaded from Pexels and should be credited in your project even when attribution is not strictly required:
- Stretford End exterior — Cláudio Castro / Pexels
- Old Trafford aerial — Mylo Kaye / Pexels
- Stretford End crowd — Biswash Lamichhane / Pexels

Patch files
-----------
- generated/mu-focus-card-assets-patch.css
- generated/template-head-asset-patch.html
- generated/photo-figure-snippet.html

Suggested project location
--------------------------
Copy the `generated/` and `photos/` directories into the same static asset directory that serves `mu.css`. The template snippets assume paths like:
- {{ asset_url('generated/favicon.svg') }}
- {{ asset_url('photos/stretford-end-exterior-hero.webp') }}
