# Инструкция по запуску задания 2: Experiment Tracking с MLflow

## 📋 Варианты выполнения

Есть **два способа** выполнить это задание:

### Способ 1: Jupyter ноутбук (Рекомендуется)
Откройте ноутбук `homework/mlops_homework_2.ipynb` и выполняйте ячейки последовательно.

Все шаги (Q1-Q6) уже реализованы в ноутбуке с подробными комментариями.

### Способ 2: Python скрипты
Запускайте скрипты из папки `homework/` по очереди через командную строку.

---

## Предварительные требования

- Python 3.8+
- pip или conda

---

## Шаг 1: Установка зависимостей

```bash
cd C:\Users\Alfa\Documents\MLops\mlops-zoomcamp\cohorts\2025\02-experiment-tracking

# Создать виртуальное окружение (опционально)
python -m venv venv
venv\Scripts\activate  # Windows

# Установить зависимости
pip install mlflow scikit-learn pandas seaborn hyperopt xgboost fastparquet pyarrow click
```

Проверить версию MLflow:
```bash
mlflow --version
```

---

## Шаг 2: Скачать данные (автоматически)

```bash
python download_data.py
```

Или вручную скачать с https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page:
- green_tripdata_2023-01.parquet
- green_tripdata_2023-02.parquet
- green_tripdata_2023-03.parquet

Сохранить в папку `data/`

---

## Шаг 3: Предобработка данных (Q2)

```bash
cd homework
python preprocess_data.py --raw_data_path ../data --dest_path ./output
```

**Результат:** В папке `output/` появятся 4 файла:
- `dv.pkl` — DictVectorizer
- `train.pkl` — тренировочные данные
- `val.pkl` — валидационные данные
- `test.pkl` — тестовые данные

**Ответ на Q2:** 4 файла

---

## Шаг 4: Запуск MLflow Tracking Server (Q4)

В НОВОМ терминале (сервер должен работать постоянно):

```bash
cd C:\Users\Alfa\Documents\MLops\mlops-zoomcamp\cohorts\2025\02-experiment-tracking

mlflow server ^
  --backend-store-uri sqlite:///mlflow.db ^
  --default-artifact-root ./artifacts ^
  --host 127.0.0.1 ^
  --port 5000
```

Открыть MLflow UI в браузере: http://localhost:5000

**Ответ на Q4:** Нужно передать `--backend-store-uri` и `--default-artifact-root`

---

## Шаг 5: Обучение модели с autolog (Q3)

```bash
cd homework
python train.py --data_path ./output
```

Проверить в MLflow UI эксперимент "random-forest-training".

**Ответ на Q3:** `min_samples_split` = 2 (значение по умолчанию RandomForestRegressor)

---

## Шаг 6: Оптимизация гиперпараметров (Q5)

```bash
python hpo.py --data_path ./output --num_trials 15
```

Проверить в MLflow UI эксперимент "random-forest-hyperopt".

**Ответ на Q5:** Лучший RMSE ≈ 4.817 (одно из значений в вариантах)

---

## Шаг 7: Регистрация модели (Q6)

```bash
python register_model.py --data_path ./output --top_n 5
```

Проверить в MLflow UI:
- Эксперимент "random-forest-best-models"
- Model Registry → random-forest-model

**Ответ на Q6:** Test RMSE ≈ 5.060 (одно из значений в вариантах)

---

## Итоговые артефакты

### Файлы данных:
```
data/
├── green_tripdata_2023-01.parquet
├── green_tripdata_2023-02.parquet
└── green_tripdata_2023-03.parquet
```

### Обработанные данные:
```
homework/output/
├── dv.pkl
├── train.pkl
├── val.pkl
└── test.pkl
```

### MLflow артефакты:
```
artifacts/
└── <experiment_id>/
    └── <run_id>/
        └── artifacts/
            └── model/  # сериализованные модели
```

### База данных MLflow:
```
mlflow.db  # SQLite с метаданными экспериментов
```

---

## Как посмотреть результаты

1. **MLflow UI:** http://localhost:5000
   - Эксперименты: random-forest-training, random-forest-hyperopt, random-forest-best-models
   - Model Registry: random-forest-model

2. **Файлы моделей:** В папке `artifacts/`

3. **Метаданные:** В базе `mlflow.db`

---

## 📓 Jupyter ноутбук

Ноутбук `homework/mlops_homework_2.ipynb` содержит все шаги задания:

| Ячейка | Описание |
|--------|----------|
| 1-2 | Импорт библиотек |
| 3-4 | Q1: Проверка версии MLflow |
| 5-8 | Q2: Загрузка и предобработка данных |
| 9-10 | Q3: Обучение с autolog |
| 11-12 | Q4: Инструкция по запуску сервера |
| 13-14 | Q5: HPO оптимизация |
| 15-16 | Q6: Регистрация модели |
| 17 | Итоговые результаты |

### Как запустить ноутбук:

```bash
cd homework
jupyter notebook mlops_homework_2.ipynb
```

Или через VS Code:
1. Откройте файл `mlops_homework_2.ipynb` в VS Code
2. Выберите Python interpreter с установленными зависимостями
3. Выполняйте ячейки последовательно (Shift+Enter)
