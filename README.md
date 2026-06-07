# DataMatrix Recognition API

HTTP-сервис для распознавания DataMatrix-кодов из изображений. Принимает изображение в формате base64, выполняет распознавание и возвращает результат в JSON.

## Особенности

- HTTP API на базе FastAPI
- Принимает изображение в base64 и UUID операции
- Возвращает распознанный текст DataMatrix в JSON
- Корректные HTTP-статусы: 200, 400, 500
- Docker-образ на Python 3.10
- Эндпоинт доступен извне на порту 8000

## API

### POST /recognize

Распознавание DataMatrix-кода из изображения.

**Запрос:**

```json
{
  "file_data": "<изображение в base64>",
  "operation_uuid": "550e8400-e29b-41d4-a716-446655440000"
}
```

| Параметр | Тип | Описание |
|----------|-----|----------|
| `file_data` | string | Изображение, закодированное в base64 |
| `operation_uuid` | string | UUID операции для идентификации запроса |

**Ответ 200 — успех:**

```json
{
  "operation_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "status": "success",
  "data": "0104607024328011210000012345\u001d911234"
}
```

**Ответ 400 — штрихкод не найден:**

```json
{
  "operation_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "status": "error",
  "message": "ШТРИХКОД НЕ РАСПОЗНАН. Ошибка типа ValueError"
}
```

**Ответ 500 — внутренняя ошибка:**

```json
{
  "operation_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "status": "error",
  "message": "ШТРИХКОД НЕ РАСПОЗНАН. Ошибка типа <ТипИсключения>"
}
```

### GET /health

Проверка работоспособности сервиса.

**Ответ:**

```json
{
  "status": "ok"
}
```

## Развёртывание Docker на Ubuntu

### 1. Установка Docker

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

### 2. Клонирование репозитория

```bash
git clone <repository-url>
cd datamatrixRecognitionAPI
```

### 3. Запуск

```bash
sudo docker compose up -d --build
```

Сервис будет доступен по адресу: `http://<IP-сервера>:8000`

### 4. Проверка

```bash
curl http://localhost:8000/health
```

### 5. Остановка

```bash
sudo docker compose down
```

## Развёртывание Docker на Windows

### 1. Установка Docker Desktop

Скачайте и установите [Docker Desktop для Windows](https://www.docker.com/products/docker-desktop/).

### 2. Клонирование репозитория

Откройте терминал (PowerShell или CMD):

```cmd
git clone <repository-url>
cd datamatrixRecognitionAPI
```

### 3. Запуск

```cmd
docker compose up -d --build
```

Сервис будет доступен по адресу: `http://localhost:8000`

### 4. Проверка

```cmd
curl http://localhost:8000/health
```

### 5. Остановка

```cmd
docker compose down
```

## Локальная разработка

### 1. Создание виртуального окружения (Python 3.10)

**Windows:**

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Запуск сервера

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Запуск тестов

```bash
pip install pytest httpx
pytest app/test_main.py -v
```

## Подготовка тестовых данных

Для конвертации файла изображения в JSON-формат, готовый для отправки в API, используйте утилиту `myfileinbase64.py`:

```bash
python myfileinbase64.py <входной_файл> <выходной_json>
```

**Пример:**

```bash
python myfileinbase64.py pic.jpg result.json
```

Результат в `result.json`:

```json
{
  "file_data": "<base64-строка содержимого pic.jpg>",
  "operation_uuid": "550e8400-e29b-41d4-a716-446655440000"
}
```

Полученный файл можно использовать как тело запроса для Postman или curl.

## Вызов эндпоинта из Postman

1. Откройте Postman
2. Создайте новый запрос:
   - **Метод:** `POST`
   - **URL:** `http://<host>:8000/recognize`
3. Перейдите на вкладку **Headers** и добавьте:
   - `Content-Type`: `application/json`
4. Перейдите на вкладку **Body**, выберите **raw** и тип **JSON**:
```json
{
  "file_data": "<base64-строка изображения>",
  "operation_uuid": "550e8400-e29b-41d4-a716-446655440000"
}
```
5. Нажмите **Send**
6. В ответе получите JSON с результатом распознавания

Для быстрой подготовки `file_data` используйте утилиту `myfileinbase64.py`, затем скопируйте значение из полученного JSON.

## Вызов эндпоинта из кода 1С:Предприятие 8.3

Пример функции на BSL для вызова API распознавания DataMatrix:

```bsl
Функция РаспознатьDataMatrix(ДанныеФайлаБаз64, UUIDОперации, АдресСервера = "localhost", ПортСервера = 8000) Экспорт
    
    ПараметрыПодключения = Новый ПараметрыПодключенияHTTP;
    ПараметрыПодключения.Сервер = АдресСервера;
    ПараметрыПодключения.Порт = ПортСервера;
    
    HTTPСоединение = Новый HTTPСоединение(ПараметрыПодключения);
    
    ЗаписьJSON = Новый ЗаписьJSON;
    ЗаписьJSON.УстановитьСтроку();
    ЗаписьJSON.ЗаписатьНачалоОбъекта();
    ЗаписьJSON.ЗаписатьИмяСвойства("file_data");
    ЗаписьJSON.ЗаписатьЗначение(ДанныеФайлаБаз64);
    ЗаписьJSON.ЗаписатьИмяСвойства("operation_uuid");
    ЗаписьJSON.ЗаписатьЗначение(UUIDОперации);
    ЗаписьJSON.ЗаписатьКонецОбъекта();
    ТелоЗапроса = ЗаписьJSON.Закрыть();
    
    HTTPЗапрос = Новый HTTPЗапрос("/recognize");
    HTTPЗапрос.Заголовки.Вставить("Content-Type", "application/json");
    HTTPЗапрос.УстановитьТелоИзСтроки(ТелоЗапроса, КодировкаТекста.UTF8);
    
    HTTPОтвет = HTTPСоединение.Отправить(HTTPЗапрос, "POST");
    
    ЧтениеJSON = Новый ЧтениеJSON;
    ЧтениеJSON.УстановитьСтроку(HTTPОтвет.ПолучитьТелоКакСтроку());
    Результат = ПрочитатьJSON(ЧтениеJSON);
    ЧтениеJSON.Закрыть();
    
    Возврат Результат;
    
КонецФункции
```

**Пример вызова:**

```bsl
ДвоичныеДанные = Новый ДвоичныеДанные("C:\images\datamatrix.jpg");
ДанныеФайлаБаз64 = Base64Строка(ДвоичныеДанные);
UUIDОперации = Строка(Новый УникальныйИдентификатор);

Результат = РаспознатьDataMatrix(ДанныеФайлаБаз64, UUIDОперации, "192.168.1.100", 8000);

Если Результат.status = "success" Тогда
    Сообщить("Распознанный код: " + Результат.data);
Иначе
    Сообщить("Ошибка: " + Результат.message);
КонецЕсли;
```

## Обработка ошибок

| HTTP-статус | Условие | Описание |
|-------------|---------|----------|
| 200 | Успех | DataMatrix-код успешно распознан, текст в поле `data` |
| 400 | Код не найден | На изображении не найден DataMatrix-код или данные не являются изображением |
| 422 | Неверный запрос | Отсутствуют обязательные поля `file_data` или `operation_uuid` |
| 500 | Внутренняя ошибка | Непредвиденная ошибка при обработке (невалидный base64, ошибка декодирования и т.д.) |

Во всех ответах с ошибкой формат одинаков:

```json
{
  "operation_uuid": "<переданный UUID>",
  "status": "error",
  "message": "ШТРИХКОД НЕ РАСПОЗНАН. Ошибка типа <ТипИсключения>"
}
```

## Структура проекта

```
datamatrixRecognitionAPI/
├── app/
│   ├── main.py            # FastAPI-приложение
│   └── test_main.py       # Тесты
├── datamatrix2.py          # Оригинальный CLI-скрипт (справочный)
├── myfileinbase64.py       # Утилита конвертации файла в base64-JSON
├── requirements.txt        # Зависимости Python
├── Dockerfile              # Docker-образ
├── docker-compose.yml      # Docker Compose
├── .gitignore              # Исключения Git
└── README.md               # Этот файл
```

## Зависимости

- `numpy==2.2.6` — работа с массивами изображений
- `opencv-python-headless==4.13.0.92` — обработка изображений (без GUI)
- `zxing-cpp>=2.2.0` — распознавание DataMatrix-кодов
- `fastapi>=0.100.0` — HTTP-фреймворк
- `uvicorn[standard]>=0.23.0` — ASGI-сервер
- `python-multipart>=0.0.6` — парсинг тела запроса

## Лицензия

Проект распространяется под лицензией Apache 2.0 (как ZXing-CPP).