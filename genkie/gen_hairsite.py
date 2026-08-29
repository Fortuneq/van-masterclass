# -*- coding: utf-8 -*-
"""
Генерация фото-ассетов для сайта Hair Academy / Hair Masterclass
через kie.ai (Grok Imagine). Правила — см. KIE_GROK_SYSTEM.md:
единый стиль серии, всегда суффикс no text / no watermark.

Запуск:
  export KIE_API_KEY=...
  python3 genkie/gen_hairsite.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from kie_grok import gen_images  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..", "img")

# Единые стили двух страниц
BEIGE = (", minimal fashion editorial photography, soft diffused studio "
         "light, muted warm beige and ivory tones, photorealistic, shot on "
         "85mm, no text, no watermark, no typography")
PINK = (", minimal fashion editorial photography, soft diffused studio "
        "light, pale dusty pink and rose tones, photorealistic, shot on "
        "85mm, no text, no watermark, no typography")

# ---------------------------------------------------------------- academy ---
ACADEMY_TALL = {
    "hero": "young beautiful woman with very long dark brown hair flying in "
            "motion across her face, black tank top, head tilted down, warm "
            "cream beige seamless studio background, hair in dynamic "
            "movement" + BEIGE,
    "dir-cuts": "back view of a woman with a short precise dark brown french "
                "bob haircut, black turtleneck, dark charcoal studio "
                "background, dramatic soft light" + BEIGE,
    "dir-color": "back view of a woman with long wavy blonde balayage hair, "
                 "seamless color melt, black top, warm beige studio "
                 "background" + BEIGE,
    "dir-care": "still life of minimalist hair care products, amber glass "
                "bottles and white pump dispensers on a beige table, soft "
                "window light, shallow depth of field" + BEIGE,
    "cta": "young woman with long dark brown hair flowing in the wind, black "
           "top, dusty rose pink seamless background, side view, hair in "
           "motion" + PINK,
}

ACADEMY_WIDE = {
    "about": "black and white portrait of an elegant confident female "
             "hairstylist in a black blazer, holding a tail comb near her "
             "face, looking at camera, grey studio backdrop, editorial",
}

ACADEMY_SQUARE = {
    "avatar-1": "portrait headshot of a young woman with dark brown wavy "
                "hair, gentle smile, looking at camera" + BEIGE,
    "avatar-2": "portrait headshot of a young woman with blonde straight "
                "hair, gentle smile, looking at camera" + BEIGE,
    "avatar-3": "portrait headshot of a young woman with light brown curly "
                "hair, gentle smile, looking at camera" + BEIGE,
    "result-1": "close-up of long blonde balayage hair waves, back of head, "
                "perfect glossy color" + BEIGE,
    "result-2": "close-up of dark cherry brunette glossy hair waves, back of "
                "head" + BEIGE,
    "result-3": "close-up of honey golden blonde wavy hair, back of head, "
                "glossy" + BEIGE,
    "result-4": "close-up of ash blonde hair with soft waves, back of head" + BEIGE,
    "result-5": "close-up of caramel brown wavy hair with highlights, back "
                "of head" + BEIGE,
    "result-6": "close-up of dark glossy straight brown hair, back of "
                "head" + BEIGE,
}

# ------------------------------------------------------------ masterclass ---
MC_TALL = {
    "hero": "two beautiful female models standing close together back to "
            "back, one with short dark brown wavy bob haircut, the other "
            "with long blonde waves, both wearing black turtlenecks, pale "
            "dusty pink seamless studio background" + PINK,
    "mc-cut": "young woman with short dark brown wavy french bob haircut, "
              "black turtleneck, three quarter view, light beige studio "
              "background" + PINK,
    "mc-color": "young woman with long blonde beach waves balayage hair, "
                "beige top, back three quarter view, light studio "
                "background" + PINK,
    "mc-style": "young woman with very long sleek straight dark glossy "
                "hair, back three quarter view, black top, light beige "
                "studio background" + PINK,
    "mc-updo": "blonde woman with an elegant collected low bun updo "
               "hairstyle with loose face-framing strands, back view, beige "
               "top, light studio background" + PINK,
    "program": "moody portrait of a young woman with wet look tousled dark "
               "hair, black top, looking at camera, dark warm brown "
               "background, cinematic light, no text, no watermark",
    "quote": "black and white portrait of an elegant female top hairstylist "
             "in a black blazer, slicked back dark hair, looking aside, "
             "light studio backdrop, editorial, no text, no watermark",
    "story-1": "back view of a woman with long chestnut brown waves, "
               "hairstylist hands curling a strand with a curling iron" + PINK,
    "story-2": "hairstylist hands pinning an elegant blonde updo hairstyle, "
               "close-up from behind" + PINK,
    "story-3": "back view of a woman with very long dark straight glossy "
               "hair, salon interior blurred" + PINK,
}

MC_SQUARE = {
    "teacher-1": "portrait headshot of an elegant woman stylist with dark "
                 "hair in a bun, black top, confident look" + PINK,
    "teacher-2": "portrait headshot of a woman stylist with short blonde "
                 "hair, black top, soft smile" + PINK,
    "teacher-3": "portrait headshot of a woman stylist with long auburn "
                 "hair, black top" + PINK,
    "teacher-4": "portrait headshot of a woman stylist with dark wavy hair, "
                 "black top, gentle smile" + PINK,
    "s-avatar-1": "portrait headshot of a young woman with dark long hair, "
                  "warm smile" + PINK,
    "s-avatar-2": "portrait headshot of a young woman with blonde hair in a "
                  "ponytail, warm smile" + PINK,
    "s-avatar-3": "portrait headshot of a young woman with brown wavy hair, "
                  "warm smile" + PINK,
}

MC_WIDE = {
    "cta-bg": "professional hairdressing scissors and a black comb lying on "
              "black silk fabric, dramatic low key lighting, macro "
              "photography, dark moody, no text, no watermark",
}

def gen_with_fallback(prompts, out_dir, ratios):
    """Пробует форматы по очереди: kie.ai принимает не все aspect_ratio.
    Отказ по формату случается на самом первом createTask (до создания
    задач), поэтому повторный вызов группы безопасен."""
    for ar in ratios:
        try:
            return gen_images(prompts, out_dir=out_dir, aspect_ratio=ar)
        except RuntimeError as e:
            if "aspect_ratio" in str(e):
                print(f"aspect_ratio {ar} отклонён, пробую следующий")
                continue
            raise
    raise RuntimeError(f"ни один формат не подошёл: {ratios}")


if __name__ == "__main__":
    if not os.environ.get("KIE_API_KEY"):
        sys.exit("KIE_API_KEY не задан")
    paths = {}
    a = os.path.join(ROOT, "academy")
    m = os.path.join(ROOT, "masterclass")
    paths.update(gen_with_fallback(ACADEMY_TALL, a, ["2:3", "9:16"]))
    paths.update(gen_with_fallback(ACADEMY_WIDE, a, ["3:2", "16:9"]))
    paths.update(gen_with_fallback(ACADEMY_SQUARE, a, ["1:1"]))
    paths.update(gen_with_fallback(MC_TALL, m, ["2:3", "9:16"]))
    paths.update(gen_with_fallback(MC_SQUARE, m, ["1:1"]))
    paths.update(gen_with_fallback(MC_WIDE, m, ["16:9"]))
    total = (len(ACADEMY_TALL) + len(ACADEMY_WIDE) + len(ACADEMY_SQUARE)
             + len(MC_TALL) + len(MC_SQUARE) + len(MC_WIDE))
    print(f"\nготово: {len(paths)}/{total}")
    missing = ({*ACADEMY_TALL, *ACADEMY_WIDE, *ACADEMY_SQUARE,
                *MC_TALL, *MC_SQUARE, *MC_WIDE} - set(paths))
    if missing:
        print(f"НЕ сгенерировались: {sorted(missing)}")
