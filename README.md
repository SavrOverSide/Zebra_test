# Food-Detection-YOLOv11

> Детекция блюд (soup, salad, meat, flatbread) в ресторанном видео. <br>
> **Датасет:** 238 кадров, из них 22 размеченных :) 6 классов, YOLO‑формат. <br>
> **Модель:** Ultralytics YOLOv11s, mAP\@0.5-90 = 0.72.

---

## 1. Быстрый старт

```bash
# 1. Клонируем
git clone https://github.com/YOUR-NICK/food-detection-yolov11.git && cd food-detection-yolov11

# 2. Виртуальное окружение
python3 -m venv venv && source venv/bin/activate

# 3. Установка зависимостей
pip install -r requirements.txt

# 5. Обучение лучшей конфигурации (exp00)
make train

# 6. Делаем инференс модели
```

## 2. Структура репозитория

```
.
├── dataset/                  # (git‑ignored тяжёлые файлы)
│   ├── images/{train,val,test}/*.jpg
│   └── labels/{train,val,test}/*.txt
├── data.yaml                 # пути + список классов
├── requirements.txt          # pinned deps
├── hyp_v1.yaml               # изменённые гиперпараметры (exp01)
├── scripts/
│   ├── extract_frames.sh     # ffmpeg → кадры (fps=5)
│   ├── filter_frames.py      # stride+diff+proxy‑food фильтр
│   └── test_models.py        # быстрый прогон сторонних весов
├── Makefile                  # make train / val / demo
├── README.md                 # (этот файл)
└── report.md                 # финальный отчёт
```

## 3. Ключевые скрипты

| Файл                        | Назначение                                                                       |
| --------------------------- | -------------------------------------------------------------------------------- |
| `scripts/extract_frames.sh` | Разрезает все видео в папке `videos/` на кадры в `dataset/raw`                   |
| `scripts/filter_frames.py`  | Удаляет дубли и оставляет кадры, где детектор видит еду (stride+diff+proxy‑food) |
| `scripts/test_models.py`    | Быстрое тестирование моделей с HF/Roboflow на кадрах (сохраняет `vis/`)          |
| `Makefile`                  | `make train` (YOLOv11s exp02), `make val`, `make demo`                           |
| `hyp_v1.yaml`               | Конфиг гиперпараметров для exp01 (lr0 уменьшен, Mosaic 0.7, MixUp 0.2)           |

## 4. Датасет (YOLO‑формат). Ключевые скрипты

| скрипт                      | назначение                                           |
| --------------------------- | ---------------------------------------------------- |
| `scripts/extract_frames.sh` | разрезает видео в `videos/` на кадры (`dataset/raw`) |
| `scripts/filter_frames.py`  | удаляет дубли и оставляет кадры с едой               |
| `scripts/augment.py`        | copy‑paste / mosaic доп. аугментации                 |
| `make train`                | `yolo train …` 60 эпох, exp02‑гиперы                 |
| `make val`                  | валидирует веса `runs/exp02/best.pt`                 |
| `make demo`                 | детекция на видео‑клипе с overlay                    |

## 4. Датасет (YOLO‑формат)

* 238 кадров, из них 22 размеченных :) 6 классов, YOLO‑формат. <br>
* Сплит: 70 % train / 20 % val / 10 % test. См. `data.yaml`.

> **Пример строки label.txt**
> `2 0.523 0.612 0.245 0.251` ⇢ `meat`,   `xc yc w h` (норм.)

## 5. Обучение и гиперы

* `imgsz = 768`, `batch = 8`, `optimizer = AdamW`, `lr0 = 0.003`.
* Мозаика 0.7, MixUp 0.2, Cutout p 0.3.
* Итерации гиперов: см. `report.md §4`.

## 6. Результаты

| Metric (test) | Value    |
| ------------- | -------- |
| mAP\@0.5-90      | **0.72** |
| Precision     | 0.97     |
| Recall        | 1     |


![mAP/loss](runs/exp02/results.png)

## 7. Трудозатраты и опыт

| Этап                 | Время, ч |
| -------------------- | -------- |
| Подготовка/аннотация | 2.1      |
| Обучение + тюнинг    | 1.1      |
| Отчёт + репо         | 0.8      |
| **Итого**            | **4.0**  |

*Опыт с YOLO: использую v5‑v8 два года (manufacturing QA, people‑count).*
