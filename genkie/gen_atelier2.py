# -*- coding: utf-8 -*-
"""
Вторая партия ассетов Atelier: line-art одежды для карточек, иллюстрация
обмера (как в утверждённом макете), фигура для body map, фото для интро.

Точки/подписи (Bust/Waist/Hips, номера мерок) НЕ генерим — рисуем сами
поверх (правило 2 KIE_GROK_SYSTEM.md).

  export KIE_API_KEY=...
  python3 grok/gen_atelier2.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from kie_grok import gen_images  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "..", "apps", "web", "public", "img")

LINE = (
    "thin uniform black outline on pure white background, minimal flat "
    "technical fashion sketch, clean elegant vector style, no shading, "
    "no text, no watermark, no typography"
)
PHOTO = (
    "minimal fashion editorial photography, warm off-white background, soft "
    "diffused daylight, muted beige and ivory tones, no text, no watermark, "
    "no typography"
)

SQUARE = {
    "icon-shirt": f"classic button-up shirt with collar and long sleeves, front view, {LINE}",
    "icon-dress": f"sleeveless summer dress with fitted waist and gently flared skirt, front view, {LINE}",
    "icon-pants": f"straight-leg tailored trousers, front view, {LINE}",
    "icon-jacket": f"tailored blazer jacket with lapels, front view, {LINE}",
    "icon-skirt": f"straight midi skirt with waistband, front view, {LINE}",
    "illu-measure": (
        "elegant minimal line illustration of a woman with dark hair in a bun "
        "wearing a black sports bra, eyes gently closed, measuring her waist "
        "with a measuring tape held in both hands, thin black lines on white "
        "background, flat vector illustration with solid black hair and top, "
        "no text, no watermark, no typography"
    ),
    "intro-measure": f"close-up of a tailor measuring a woman's waist over a white shirt with a cream tape measure, hands visible, {PHOTO}",
    "intro-adjust": f"top view of a paper sewing pattern being drafted with a wooden french curve ruler and a pencil on a large white table, {PHOTO}",
}

TALL = {
    "illu-body": (
        "minimal line illustration of a standing woman figure, front view, "
        "arms relaxed slightly away from the body, thin clean black outline "
        "on white background, flat vector style, simple neutral silhouette, "
        "no face details, no text, no watermark, no typography"
    ),
}

if __name__ == "__main__":
    if not os.environ.get("KIE_API_KEY"):
        sys.exit("KIE_API_KEY не задан")
    os.makedirs(OUT, exist_ok=True)
    paths = {}
    paths.update(gen_images(SQUARE, out_dir=OUT, aspect_ratio="1:1"))
    paths.update(gen_images(TALL, out_dir=OUT, aspect_ratio="9:16"))
    print(f"\nготово: {len(paths)} файлов")
    missing = (set(SQUARE) | set(TALL)) - set(paths)
    if missing:
        print(f"НЕ сгенерировались: {sorted(missing)}")
