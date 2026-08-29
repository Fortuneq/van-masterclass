# -*- coding: utf-8 -*-
"""
Генерация фото-ассетов интерфейса Atelier через kie.ai (Grok Imagine).

Это ДЕКОРАТИВНЫЙ слой (§7.4 ТЗ): фото для hero, 3D-превью, тканей, шагов
инструкции. В геометрию эти изображения не попадают.

Правила из KIE_GROK_SYSTEM.md:
- единый персонаж серии — один гардероб-префикс во всех промптах;
- всегда суффикс no text / no watermark / no typography;
- схемы и анатомические диаграммы не генерим (BodyMap остаётся SVG).

Запуск:
  export KIE_API_KEY=...
  python3 grok/gen_atelier.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from kie_grok import gen_images  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "apps", "web", "public", "img")

# Единый стиль: тёплый монохром бумажной системы Atelier
STYLE = (
    "minimal fashion editorial photography, warm off-white seamless studio "
    "background, soft diffused daylight, muted beige and ivory tones, "
    "no text, no watermark, no typography"
)
# Единый персонаж для всех кадров с моделью
MODEL = (
    "young woman with dark hair in a low bun, wearing an oversized white "
    "cotton shirt and loose beige trousers"
)

SQUARE = {
    "fabric-linen": f"extreme close-up of natural linen fabric, visible weave texture, flat lay, even soft light, warm beige, {STYLE}",
    "fabric-cotton": f"extreme close-up of smooth white cotton poplin fabric, subtle weave, flat lay, even soft light, {STYLE}",
    "fabric-denim": f"extreme close-up of dark indigo denim fabric, diagonal twill texture, flat lay, even soft light, {STYLE}",
    "fabric-silk": f"extreme close-up of ivory silk satin fabric with soft folds and gentle sheen, flat lay, {STYLE}",
    "step-cutting": f"hands cutting white paper sewing pattern pieces with fabric scissors on a large table, top view, {STYLE}",
    "step-seams": f"hands guiding white cotton fabric under a sewing machine needle, close-up, {STYLE}",
    "step-collar": f"hands pinning a white shirt collar to a neckline with sewing pins, close-up on tailor table, {STYLE}",
    "step-sleeve": f"white shirt sleeve being eased into an armhole with pins, close-up, tailor workshop, {STYLE}",
    "profile-anna": f"portrait of a young woman with dark hair, gentle smile, looking at camera, head and shoulders, {STYLE}",
    "hero-dressform": f"professional tailor's dress form mannequin on a wooden tripod stand, draped with white muslin fabric and a measuring tape, {STYLE}",
}

TALL = {
    "preview-front": f"full body photo of {MODEL}, standing straight facing the camera, arms relaxed, {STYLE}",
    "preview-back": f"full body photo of {MODEL}, standing straight with her back to the camera, {STYLE}",
    "preview-side": f"full body photo of {MODEL}, standing in profile side view, {STYLE}",
    "avatar-body": f"neutral 3d body scan avatar of a woman in a plain light grey seamless bodysuit, A-pose, clean minimal 3d render, matte studio lighting, {STYLE}",
    "sim-linen": f"full body photo of {MODEL.replace('white cotton shirt', 'flowing natural linen shirt')}, standing facing the camera, fabric draping softly, {STYLE}",
}

if __name__ == "__main__":
    if not os.environ.get("KIE_API_KEY"):
        sys.exit("KIE_API_KEY не задан")
    os.makedirs(OUT, exist_ok=True)
    paths = {}
    paths.update(gen_images(SQUARE, out_dir=OUT, aspect_ratio="1:1"))
    paths.update(gen_images(TALL, out_dir=OUT, aspect_ratio="9:16"))
    print(f"\nготово: {len(paths)} файлов в {OUT}")
    missing = (set(SQUARE) | set(TALL)) - set(paths)
    if missing:
        print(f"НЕ сгенерировались: {sorted(missing)}")
