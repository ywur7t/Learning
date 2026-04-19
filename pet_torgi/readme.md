# SPIMEX Data Pipeline

## Обзор

Данный проект реализует data pipeline для извлечения, трансформации и загрузки торговых данных с сайта SPIMEX (Санкт-Петербургская международная товарно-сырьевая биржа).

### Pipeline выполняет:

* Парсинг PDF-отчетов с SPIMEX
* Извлечение табличных данных
* Очистку и нормализацию данных
* Сохранение в формате Parquet (промежуточные слои)
* Загрузку в ClickHouse для аналитической обработки
* Построение аналитических витрин (gold слой) с использованием SQL

## Архитектура

Pipeline построен по слоистой архитектуре:

* PDF (источник)
* Raw (PDF-файлы)
* Landing (Parquet, необработанные таблицы)
* Staging (очищенные и типизированные данные)
* ClickHouse (staging таблица)
* Analytical Layer (витрины на основе SQL)

## Технологии

* Python==3.14
* beautifulsoup4==4.14.3
* numpy==2.4.4
* pandas==3.0.2
* pyarrow==23.0.1
* PyMuPDF==1.27.2.2
* requests==2.33.1
* ClickHouse
* Docker

### Извлечение данных

Pipeline получает торговые отчеты с:
https://spimex.com/markets/oil_products/trades/results/

Шаги:

* Парсинг веб-страницы для получения ссылки на последний PDF
* Загрузка PDF
* Извлечение таблиц с помощью PyMuPDF
* Преобразование таблиц в pandas DataFrame

### Обработка данных

* Удаление пустых и некорректных строк
* Нормализация названий колонок
* Приведение типов данных:
* * числовые поля → float / int
* * дата → Date
* * Замена пропущенных значений
* Удаление артефактов форматирования (переносы строк, запятые)

### Хранение данных

* Промежуточные слои
* Landing → сырые извлечённые таблицы
* Staging → очищенный и структурированный датасет

Хранение в формате Parquet обеспечивает:

* эффективное использование памяти
* высокую скорость чтения/записи
* согласованность схемы

#### Интеграция с ClickHouse

Данные загружаются в staging-таблицу:

* instrument_code
* instrument_name
* delivery_basis
* volume_import_units
* volume_import_rub
* changes_to_previous_rub
* changes_to_previous_pers
* price_min
* price_avg
* price_max
* price_market
* price_best_offer
* price_best_demand
* count_contracts
* date

Движок:

* MergeTree
* ORDER BY (date, instrument_code)

### Аналитический слой

Аналитические запросы строятся непосредственно в ClickHouse с использованием SQL.

Примеры:

* Дневная сводка рынка
* Статистика по инструментам
