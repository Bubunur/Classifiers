# Classifiers

Веб-приложение с двумя классификаторами:

- **Животные** — классификация изображений (`Bubunur/animals-classifier`)
- **Новости** — классификация текстов по категориям Business, Sports, Sci/Tech (`Bubunur/ag-news-classifier`)

Бэкенд на FastAPI, модели загружаются с Hugging Face, интерфейс — статическая страница в `static/`.

## Запуск через Docker (рекомендуется)

Нужен установленный [Docker](https://docs.docker.com/get-docker/) с Docker Compose.

```bash
git clone https://github.com/Bubunur/Classifiers.git
cd Classifiers
docker compose up --build
```

Откройте http://localhost:8000.

При первом запуске контейнер скачивает модели с Hugging Face, поэтому нужен интернет, а старт занимает несколько минут. Модели сохраняются в томе `hf_cache`, и дальше запуск быстрый.

Полезные команды:

```bash
docker compose up -d      # запуск в фоне
docker compose logs -f    # логи
docker compose down       # остановка
```

Если порт 8000 занят, измените в `docker-compose.yml` строку `"8000:8000"`, например на `"8080:8000"`.

## Запуск без Docker

Нужен Python 3.10+.

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Откройте http://127.0.0.1:8000. Документация API: http://127.0.0.1:8000/docs.

## API

| Метод | Путь                  | Параметры                    |
|-------|-----------------------|------------------------------|
| POST  | `/api/classify/text`  | `text` (form-data)           |
| POST  | `/api/classify/image` | `file` (form-data, картинка) |

Ответ — список объектов `{"label": "...", "score": 0.0–1.0}`.

Пример:

```bash
curl -F "text=The stock market rallied after the central bank's decision" \
     http://localhost:8000/api/classify/text
```

## Структура проекта

```
main.py              # FastAPI-приложение
static/              # index.html, style.css, скриншоты
requirements.txt     # зависимости Python
Dockerfile
docker-compose.yml
```
