# -*- coding: utf-8 -*-
"""
kie_grok.py — система генерации картинок и видео через kie.ai (Grok Imagine).

Восстановлено из рабочего конвейера сессии «Кегель-карусели» (Stretcher)
и дополнено видео-эндпоинтами по документации kie.ai.

Эндпоинты:
  POST https://api.kie.ai/api/v1/jobs/createTask
  GET  https://api.kie.ai/api/v1/jobs/recordInfo?taskId=...

Модели Grok Imagine на kie.ai:
  grok-imagine/text-to-image   — картинка из текста
  grok-imagine/text-to-video   — видео из текста
  grok-imagine/image-to-video  — оживление картинки (по URL или по task_id грок-картинки)
  grok-imagine/upscale         — апскейл видео (по task_id)

Использование:
  python3 kie_grok.py                          # демо: одна картинка
  или как модуль:
    from kie_grok import gen_images, gen_video_from_text, gen_video_from_image

Ключ: возьми из личного кабинета kie.ai (в прошлой сессии использовался ключ
проекта Stretcher — он лежит в переписке; сюда не зашит, чтобы файл можно
было безопасно класть в репозиторий). Задай через переменную окружения:
  export KIE_API_KEY=...
"""

import json
import os
import sys
import time

import requests

API = "https://api.kie.ai/api/v1"
KEY = os.environ.get("KIE_API_KEY", "")
HDR = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}


# ----------------------------------------------------------------------------
# Ядро: создать задачу / дождаться / скачать
# ----------------------------------------------------------------------------

def create_task(model: str, inp: dict) -> str:
    """Создаёт задачу генерации, возвращает taskId. Бросает RuntimeError при отказе."""
    r = requests.post(f"{API}/jobs/createTask", headers=HDR,
                      json={"model": model, "input": inp}, timeout=60).json()
    if r.get("code") != 200:
        raise RuntimeError(f"createTask failed: {r}")
    return r["data"]["taskId"]


def poll_task(task_id: str, timeout_s: int = 600, every_s: int = 8) -> list[str]:
    """Ждёт завершения задачи, возвращает список URL результата (картинки или видео)."""
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        r = requests.get(f"{API}/jobs/recordInfo", headers=HDR,
                         params={"taskId": task_id}, timeout=30).json()
        st = r.get("data", {}).get("state")
        if st == "success":
            res = json.loads(r["data"]["resultJson"])
            return res["resultUrls"]
        if st == "fail":
            raise RuntimeError(f"task {task_id} failed: {r['data'].get('failMsg')}")
        time.sleep(every_s)
    raise TimeoutError(f"task {task_id} not done in {timeout_s}s")


def download(url: str, path: str) -> str:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    data = requests.get(url, timeout=300).content
    with open(path, "wb") as f:
        f.write(data)
    print(f"saved {path} ({len(data)} bytes)")
    return path


# ----------------------------------------------------------------------------
# Картинки (grok-imagine/text-to-image)
# ----------------------------------------------------------------------------

def gen_images(prompts: dict[str, str], out_dir: str = "out",
               aspect_ratio: str = "9:16") -> dict[str, str]:
    """
    Пакетная генерация картинок. prompts = {имя_файла: промпт}.
    Все задачи создаются сразу, затем опрашиваются вместе (как в боевом poll.py).
    Возвращает {имя: путь}; упавшие задачи печатаются и пропускаются.
    """
    tasks, paths_skip = {}, {}
    for name, p in prompts.items():
        existing = os.path.join(out_dir, f"{name}.png")
        if os.path.exists(existing) and os.path.getsize(existing) > 0:
            print(f"skip {name}: уже есть")
            paths_skip[name] = existing
            continue
        tasks[name] = create_task("grok-imagine/text-to-image",
                                  {"prompt": p, "aspect_ratio": aspect_ratio})
        print(f"created {name}: {tasks[name]}")
        time.sleep(1)  # не душим API
    if not tasks:
        return paths_skip

    done, paths = {}, {}
    for _ in range(80):
        for name, tid in tasks.items():
            if name in done:
                continue
            try:
                r = requests.get(f"{API}/jobs/recordInfo", headers=HDR,
                                 params={"taskId": tid}, timeout=60).json()
            except requests.RequestException as e:
                print(f"{name}: сеть моргнула ({e.__class__.__name__}), повтор позже")
                continue
            st = r.get("data", {}).get("state")
            if st == "success":
                url = json.loads(r["data"]["resultJson"])["resultUrls"][0]
                paths[name] = download(url, os.path.join(out_dir, f"{name}.png"))
                done[name] = True
            elif st == "fail":
                print(f"{name} FAIL: {r['data'].get('failMsg')}")
                done[name] = False
        if len(done) == len(tasks):
            break
        time.sleep(8)
    paths.update(paths_skip)
    return paths


# ----------------------------------------------------------------------------
# Видео
# ----------------------------------------------------------------------------

def gen_video_from_text(prompt: str, out_path: str = "out/video.mp4",
                        aspect_ratio: str = "9:16", duration: str = "6",
                        resolution: str = "480p", mode: str = "normal") -> str:
    """Текст → видео (grok-imagine/text-to-video). duration в секундах строкой."""
    tid = create_task("grok-imagine/text-to-video", {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "mode": mode,
        "duration": duration,
        "resolution": resolution,
    })
    print("video task", tid)
    return download(poll_task(tid, timeout_s=900)[0], out_path)


def gen_video_from_image(prompt: str, out_path: str = "out/video.mp4",
                         image_url: str | None = None,
                         image_task_id: str | None = None, index: int = 0,
                         aspect_ratio: str = "9:16", duration: str = "6",
                         resolution: str = "480p", mode: str = "normal") -> str:
    """
    Картинка → видео (grok-imagine/image-to-video).
    ЛИБО image_url (один внешний URL), ЛИБО image_task_id (taskId грок-картинки) —
    одновременно оба передавать нельзя, API это запрещает.
    При image_url ссылайся на него в промпте как «@image1 ...».
    """
    inp: dict = {"prompt": prompt, "aspect_ratio": aspect_ratio,
                 "mode": mode, "duration": duration, "resolution": resolution}
    if image_url and image_task_id:
        raise ValueError("передай либо image_url, либо image_task_id, не оба")
    if image_url:
        inp["image_urls"] = [image_url]
    elif image_task_id:
        inp["task_id"] = image_task_id
        inp["index"] = index
    else:
        raise ValueError("нужен image_url или image_task_id")
    tid = create_task("grok-imagine/image-to-video", inp)
    print("video task", tid)
    return download(poll_task(tid, timeout_s=900)[0], out_path)


def upscale_video(video_task_id: str, out_path: str = "out/video_hd.mp4") -> str:
    """Апскейл ранее сгенерённого видео по его taskId (grok-imagine/upscale)."""
    tid = create_task("grok-imagine/upscale", {"task_id": video_task_id})
    return download(poll_task(tid, timeout_s=900)[0], out_path)


# ----------------------------------------------------------------------------
# Промпт-заготовки из боевых прогонов (Stretcher)
# ----------------------------------------------------------------------------

# Единый персонаж во всех кадрах серии — гардероб зашивается в префикс,
# иначе Grok рисует разных людей:
CHAR = ("young athletic man with short dark hair, grey open windbreaker over "
        "bare torso, beige athletic shorts, magenta crew socks, cream white sneakers, ")

# Единая сцена/свет — суффикс. Всегда завершай запретом текста:
SCENE = (", on an urban rooftop basketball court, city skyline in background, "
         "bright blue sky, harsh direct sunlight, hard shadows, dynamic sports "
         "fashion editorial photography, shot on 35mm, vivid color, "
         "no text, no watermark, no typography")

# Пустые фоны под последующую склейку с фигурой:
BG_SUFFIX = (", empty scene with no people, wide symmetric composition, clear open "
             "space in the center of frame, cinematic soft light, photorealistic, "
             "no text, no watermark")

# Стикер-фигура на белом (под вырез хромакеем по белому, а не rembg):
FIG_PREFIX = ("simple flat 2D vector-style sticker: one single human silhouette, "
              "dark brown scribble crayon fill, thick rough golden-yellow outline, "
              "featureless no face, centered on a completely plain solid pure white "
              "background, nothing else in frame, no shadow, no floor, no scenery, "
              "no text, no watermark")


if __name__ == "__main__":
    if not KEY:
        sys.exit("Задай KIE_API_KEY: export KIE_API_KEY=...")
    demo = {"demo": CHAR + "standing tall, tilting his head to the right side, "
                            "deep side neck stretch, eyes closed calm" + SCENE}
    print(gen_images(demo, out_dir="out"))
