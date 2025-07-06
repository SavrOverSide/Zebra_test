# Food-Detection-YOLOv11

> Детекция блюд (soup, salad, meat, flatbread) в ресторанном видео. <br>
> **Датасет:** 238 кадров, из них 22 размеченных :) 6 классов, YOLO‑формат. <br>
> **Модель:** Ultralytics YOLOv11s, mAP\@0.5-90 = 0.72.

---

## 1. Быстрый старт

```bash
# 1. Клонируем
git clone https://github.com/SavrOverSide/Zebra_test.git

# 2. Виртуальное окружение
python3 -m venv venv && source venv/bin/activate

# 3. Установка зависимостей
pip install -r requirements.txt

# ВАЖНО. Скачиваем датасет по адресу:
https://app.roboflow.com/project-w5hz4/zebra-testovoe/2

# ВАЖНО. Скачиваем веса по адресу:
https://disk.yandex.ru/d/r_13ZeYk_PPTfg

# Далее пункты 4-9 НЕОБЯЗАТЕЛЬНЫЕ!! Пункты 4-9 показывают как можно обработать датасет и подготовить данные для обученмя!

# 4. Скачиваем видео тестовые из яндекс диска

# 5. Запускаем скрипт extract_frames по разбиению видео на кадры

# 6. Запускаем скрипт filter_frames для фильтра кадров на релевантные

# 7.  (опционально) тестим модели из HF

# 8. Обучаем модель Yolo11 нв получившемся датасете

# 9. (опционально) использьуем гиперы для тюнинга модели

# 10. Инференсим получившуюся модель :)
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

Демо здесь
https://www.transferxl.com/download/08vPyhR07GsSbp


## 7. Трудозатраты и опыт

| Этап                 | Время, ч |
| -------------------- | -------- |
| Подготовка/аннотация | 2.1      |
| Обучение + тюнинг    | 1.1      |
| Отчёт + репо         | 0.8      |
| **Итого**            | **4.0**  |

