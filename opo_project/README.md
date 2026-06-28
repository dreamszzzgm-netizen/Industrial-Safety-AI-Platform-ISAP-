# OPO Export Project

Генерация документа «Сведения об ОПО» в форматах DOCX и PDF через Flask + docxtpl.

## Быстрый старт

### 1. Установите зависимости

```bash
pip install -r requirements.txt
```

Для PDF-экспорта также нужен LibreOffice:
```bash
# Ubuntu/Debian
sudo apt install libreoffice

# или скачайте с https://www.libreoffice.org/download/
```

### 2. Запустите сервер

```bash
python app.py
```

Откройте браузер: http://localhost:5000

### 3. Экспорт

- Заполните форму
- Нажмите «Скачать DOCX» или «Скачать PDF»

## Структура проекта

```
project/
├── app.py                     # Flask-приложение (маршруты)
├── requirements.txt
├── exports/
│   └── exporter.py            # ExportEngine: сборка контекста + docxtpl
├── word_templates/
│   └── opo_template.docx      # Шаблон с тегами {{ }} для docxtpl
├── generated/
│   ├── docx/                  # Сюда пишутся сгенерированные DOCX
│   └── pdf/                   # Сюда пишутся сгенерированные PDF
└── static/
    └── forma_OPO.html         # HTML-форма
```

## Переменные шаблона (docxtpl)

### Одиночные поля
| Переменная | Описание |
|---|---|
| `{{ opo_name }}` | 1.1. Полное наименование ОПО |
| `{{ object_type }}` | 1.2. Типовое наименование |
| `{{ industry_code }}` | 1.3. Отраслевой код |
| `{{ address }}` | 1.4. Адрес ОПО |
| `{{ oktmo }}` | 1.5. Код ОКТМО |
| `{{ commissioning_date }}` | 1.6. Дата ввода в эксплуатацию |
| `{{ owner_name }}` | 1.7.1. Собственник |
| `{{ owner_inn }}` | 1.7.2. ИНН собственника |
| `{{ processes_text }}` | Раздел 2 — перечень процессов |
| `{{ danger_class }}` | Раздел 3 — класс опасности |
| `{{ classification_text }}` | Раздел 4 — классификация |
| `{{ licenses_text }}` | Раздел 5 — лицензии |
| `{{ total_amount }}` | Итого опасного вещества, т |
| `{{ nearby_substances }}` | Раздел 7 |
| `{{ applicant_full }}` ... | Разделы 8, 9 |

### Таблица состава (цикл)
```
{% for row in composition %}
{{ row.number }} {{ row.name }} {{ row.danger }}
{{ row.substance }} {{ row.characteristics }} {{ row.processes }}
{% endfor %}
```

## Добавление новых шаблонов

1. Создайте `.docx` с тегами `{{ }}` и положите в `word_templates/`
2. Вызовите `ExportEngine.export_docx('new_template.docx', context)`
