# 🎮 Clash Royale AI

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.8+-orange.svg)
![YOLO](https://img.shields.io/badge/YOLO-v8-green.svg)
![License](https://img.shields.io/badge/License-MIT-purple.svg)

**🏆AI для игры в Clash Royale**

*Объединение лучших технологий*

[🚀 Быстрый старт](#-быстрый-старт) • [🌟 Возможности](#-основные-возможности) • [⚙️ Настройка](#-настройка) • [📁 Структура](#-детальная-структура-проекта)

</div>

---

## 📖 О проекте

**Clash Royale AI** — это мощная система искусственного интеллекта для автоматизации игры в Clash Royale. Проект объединяет лучшие технологии компьютерного зрения, машинного обучения и игровой автоматизации в единую, высокопроизводительную платформу.

Система использует:
- 🧠 **Deep Learning** для распознавания карт и войск
- 🎯 **Reinforcement Learning** для обучения оптимальной стратегии
- 👁️ **Computer Vision** для анализа игрового поля в реальном времени
- 📊 **Advanced Analytics** для анализа паттернов и улучшения игры
- 🔧 **Модульная архитектура** для легкого расширения

---

## 🌟 Основные возможности

### 🃏 Распознавание карт
- **CNN нейросеть** для точного определения карт в руке и колоде противника
- **Отслеживание цикла** — знает, какие карты уже сыграны и что осталось
- **Предсказание руки противника** на основе паттернов
- **Поддержка всех карт** игры с высоким процентом точности

### 👁️ Обнаружение войск
- **YOLO v8** для обнаружения всех единиц на поле боя
- **Распознавание союзных и вражеских войск** с классификацией
- **Детекция башен и зданий** для точного расчета урона
- **Трекинг движущихся целей** в реальном времени

### 🧠 Машинное обучение
- **PDQN (Parameterized Deep Q-Network)** агент для принятия решений
- **VAE (Variational Autoencoder)** для сжатия состояний игры
- **Experience Replay** с приоритизацией для эффективного обучения
- **Онлайн обучение** — AI учится в процессе игры

### 🎯 Умные стратегии
- **Анализ угроз** — определение уровня опасности ситуации
- **Выбор оптимального действия** на основе множества факторов
- **Контрпики** — автоматический подбор карт против угроз
- **Управление эликсиром** — точный подсчет и планирование
- **Циклирование карт** — оптимальное использование колоды

### 📹 Анализ реплеев
- **Парсинг записанных матчей** для детального анализа
- **Визуализация** с наложением информации о состоянии игры
- **Анализ ошибок** с конкретными рекомендациями
- **Экспорт в видео** с комментариями и аннотациями
- **Интерактивный просмотр** с возможностью перемотки

### ⚡ Оптимизация производительности
- **Многопоточная обработка** кадров для максимальной скорости
- **Быстрый захват экрана** (60+ FPS) через dxcam/mss
- **Умное кэширование** результатов распознавания
- **Оптимизация моделей** (ONNX, TensorRT) для GPU
- **Асинхронные операции** для параллельной обработки

### 🧪 Тестирование
- **Unit тесты** для каждого модуля
- **Integration тесты** для проверки взаимодействия
- **Симулятор стратегий** для тестирования без реальной игры
- **Бенчмарки производительности** для оптимизации

### ⚙️ Гибкая настройка
- **GUI интерфейс настроек** для удобной конфигурации
- **Профили** (быстрый/сбалансированный/точный/слабый ПК/обучение)
- **Калибровка экрана** для автоматического определения координат
- **Горячие клавиши** для управления во время игры

### 📚 База знаний
- **Оптимальные позиции** размещения для каждой карты
- **Таблица контрпиков** для всех популярных карт
- **Мета колоды** с описаниями и советами
- **Гайды по стратегиям** для разных архетипов

### 🔌 Система плагинов
- **Легкое расширение** функционала через плагины
- **Кастомные стратегии** для экспериментов
- **Дополнительные детекторы** для новых типов объектов
- **Метрики и аналитика** через плагины

### 📊 Расширенная аналитика
- **Статистика по картам** — винрейт, использование, комбо
- **Анализ архетипов** — эффективность разных стилей игры
- **Тайминг аналитика** — оптимальное время для атак
- **Паттерны противника** — предсказание следующих ходов

### 🎓 Система обучения
- **Сбор данных** автоматически во время игры
- **Обучение CNN** для распознавания карт
- **Дообучение YOLO** для лучшего обнаружения
- **Обучение RL агента** на собранных данных
- **Версионирование моделей** и автозагрузка из облака

### 🔄 Автоматический перезапуск
- **Отказоустойчивость** — автоматическое восстановление после сбоев
- **Мониторинг здоровья** системы в реальном времени
- **Логирование ошибок** для диагностики
- **Умные лимиты** перезапусков для предотвращения циклов

---

## 📁 Детальная структура проекта

```
unified_clash_royale_ai/
│
├── 🃏 card_recognition/          # Распознавание карт
│   ├── card_detector.py         # CNN модель для распознавания
│   └── __init__.py
│
├── 👁️ troop_detection/           # Обнаружение войск
│   ├── troop_detector.py        # YOLO детектор
│   └── __init__.py
│
├── 🧠 rl/                        # Reinforcement Learning
│   ├── pdqn_agent.py           # PDQN агент
│   ├── environment.py          # Игровое окружение
│   ├── utils.py                # Вспомогательные функции (Replay Buffer, OU Noise)
│   └── __init__.py
│
├── 🎯 strategies/                # Стратегии игры
│   ├── bot_brain.py            # Главный мозг бота
│   ├── deck_analyzer.py        # Анализ колод
│   ├── advanced/               # Продвинутые стратегии
│   │   ├── deck_builder.py     # Создание оптимальных колод
│   │   ├── meta_tracker.py     # Отслеживание меты
│   │   ├── matchup_analyzer.py # Анализ матчапов
│   │   ├── elixir_tracker.py   # Точный подсчет эликсира
│   │   └── cycle_counter.py    # Подсчет циклов карт
│   └── __init__.py
│
├── 🎮 game_automation/           # Автоматизация игры
│   ├── screen_capture.py       # Захват экрана
│   ├── game_state.py           # Управление состоянием игры
│   ├── action_executor.py      # Выполнение действий (клики, свайпы)
│   └── __init__.py
│
├── 📹 replay_analyzer/           # Анализ реплеев
│   ├── replay_parser.py        # Парсинг реплеев
│   ├── match_visualizer.py     # Визуализация матчей
│   ├── error_analyzer.py       # Анализ ошибок
│   ├── improvement_advisor.py  # Рекомендации по улучшению
│   ├── video_exporter.py       # Экспорт в видео
│   └── __init__.py
│
├── ⚡ performance/               # Оптимизация производительности
│   ├── frame_processor.py      # Параллельная обработка кадров
│   ├── screen_optimizer.py     # Оптимизация захвата экрана
│   ├── cache_manager.py        # Кэширование результатов
│   ├── async_operations.py     # Асинхронные операции
│   ├── neural_optimizer.py     # Оптимизация моделей (ONNX/TensorRT)
│   └── __init__.py
│
├── 🧪 tests/                     # Тестирование
│   ├── test_runner.py          # Запускатор тестов
│   ├── unit_tests.py           # Unit тесты модулей
│   ├── integration_tests.py    # Integration тесты
│   ├── strategy_tests.py       # Тесты стратегий с симулятором
│   ├── benchmarks.py           # Бенчмарки производительности
│   └── __init__.py
│
├── ⚙️ settings/                  # Настройки
│   ├── settings_manager.py     # Менеджер настроек
│   ├── profiles.py             # Профили конфигурации
│   ├── screen_calibration.py   # Калибровка экрана
│   ├── settings_gui.py         # GUI для настроек
│   └── __init__.py
│
├── 📚 knowledge_base/            # База знаний
│   ├── placement_guide.py      # Оптимальные позиции размещения
│   ├── counterpicks.py         # Таблица контрпиков
│   ├── meta_decks.py           # База мета колод
│   ├── strategy_guides.py      # Гайды по стратегиям
│   └── __init__.py
│
├── 🔌 plugins/                   # Система плагинов
│   ├── plugin_manager.py       # Менеджер плагинов
│   ├── plugin_base.py          # Базовые классы плагинов
│   ├── examples/               # Примеры плагинов
│   │   ├── sample_strategy.py  # Пример стратегии
│   │   └── sample_metrics.py   # Пример метрик
│   └── __init__.py
│
├── 📊 analytics/                 # Аналитика
│   ├── card_analytics.py       # Статистика по картам
│   ├── archetype_analytics.py  # Анализ архетипов
│   ├── timing_analytics.py     # Анализ тайминга
│   ├── opponent_patterns.py    # Паттерны противника
│   └── __init__.py
│
├── 🖥️ gui/                       # Графический интерфейс
│   ├── main_window.py          # Главное окно с информацией
│   └── __init__.py
│
├── 📚 data/                      # База данных
│   ├── cards_database.py       # Информация о всех картах
│   └── __init__.py
│
├── 🎓 training/                  # Обучение моделей
│   ├── train_card_detector.py  # Обучение CNN для карт
│   ├── train_yolo.py           # Обучение YOLO
│   ├── train_rl.py             # Обучение RL агента
│   ├── data_collection.py      # Сбор данных
│   ├── model_manager.py        # Управление моделями (версионирование, загрузка)
│   └── __init__.py
│
├── 🛠️ utils/                     # Утилиты
│   ├── logger.py               # Система логирования
│   ├── match_recorder.py       # Запись матчей
│   ├── statistics.py           # Сбор статистики
│   ├── auto_restart.py         # Автоматический перезапуск
│   └── __init__.py
│
├── config.py                    # Основной конфигурационный файл
├── main.py                      # Главный файл запуска
└── __init__.py
```

---

## 🚀 Быстрый старт

### Требования

- **Python 3.8+** (рекомендуется 3.10+)
- **Windows 10/11**
- **4+ GB RAM** (рекомендуется 16 GB)
- **Эмулятор** LDPlayer или BlueStacks
- **GPU** (опционально, но рекомендуется для лучшей производительности)

### Установка

```bash
# 1. или скачайте архив

# 2. Установите зависимости
pip install -r requirements.txt

# 3. (Опционально) Установите модели или обучите свои
# Модели можно скачать автоматически при первом запуске
```

### Первый запуск

```bash
# Запуск с графическим интерфейсом
python run_ai.py --mode smart --gui

# Или без GUI (быстрее)
python run_ai.py --mode rule_based
```

### Настройка

1. **Откройте настройки**: `python run_ai.py --settings`
2. **Калибруйте экран**: Автоматически при первом запуске или через `--calibrate`
3. **Выберите профиль**: `--profile balanced` (рекомендуется)

---

## 🎮 Режимы работы

| Режим | Описание | Скорость | Точность | Когда использовать |
|-------|----------|----------|----------|-------------------|
| **`smart`** | Гибридный: правила + ML | ⭐⭐⭐ | ⭐⭐⭐⭐ | **Рекомендуется** для лучшего баланса |
| **`hybrid`** | RL + правила с приоритетом RL | ⭐⭐ | ⭐⭐⭐⭐⭐ | Когда есть обученная модель RL |
| **`rl`** | Чистое RL без правил | ⭐⭐ | ⭐⭐⭐ | Для экспериментов и обучения |
| **`rule_based`** | Только правила, без ML | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | На слабом ПК или без GPU |

### Выбор режима

```bash
# Умный режим (рекомендуется)
python run_ai.py --mode smart

# Только правила (быстро, не требует ML)
python run_ai.py --mode rule_based

# С RL обучением
python run_ai.py --mode hybrid --rl-model path/to/model
```

---

## ⚙️ Профили настроек

Профили оптимизируют производительность под разные задачи:

### 🚀 `fast` — Максимальная скорость
- **FPS**: 60
- **Порог уверенности**: 0.5 (низкий)
- **Параллельная обработка**: 8 потоков
- **Использование**: Мощный ПК, фарм трофеев

```bash
python run_ai.py --profile fast
```

### ⚖️ `balanced` — Сбалансированный (рекомендуется)
- **FPS**: 30
- **Порог уверенности**: 0.7 (средний)
- **Параллельная обработка**: 4 потока
- **Использование**: Большинство случаев

```bash
python run_ai.py --profile balanced
```

### 🎯 `accurate` — Максимальная точность
- **FPS**: 15
- **Порог уверенности**: 0.9 (высокий)
- **Параллельная обработка**: Отключена
- **Использование**: Важные матчи, анализ

```bash
python run_ai.py --profile accurate
```

### 💻 `low_end` — Для слабого ПК
- **FPS**: 15
- **Метод захвата**: MSS (стабильнее)
- **GPU**: Отключен
- **Кэширование**: Включено
- **Использование**: Старые компьютеры

```bash
python run_ai.py --profile low_end
```

### 🎓 `training` — Для обучения
- **FPS**: 10
- **Запись**: Все кадры и действия
- **Автоигра**: Отключена (ручное управление)
- **Использование**: Сбор данных для обучения

```bash
python run_ai.py --profile training --collect-data
```

---

## 📊 Аналитика и статистика

### Просмотр статистики

```bash
# Общая статистика
python run_ai.py --stats

# Детальный отчет
python -m unified_clash_royale_ai.analytics --report

# Анализ карт
python -m unified_clash_royale_ai.analytics --cards

# Анализ матчапов
python -m unified_clash_royale_ai.analytics --matchups

# Анализ тайминга
python -m unified_clash_royale_ai.analytics --timing
```

### Пример отчета

```
📊 АНАЛИТИКА КАРТ
============================================================
Всего игр: 100
Общий винрейт: 65.0%
Уникальных карт использовано: 24

ТОП ИСПОЛЬЗУЕМЫХ КАРТ:
  1. hog_rider: 234 раза (WR: 68%)
  2. fireball: 189 раз (WR: 72%)
  3. knight: 156 раз (WR: 65%)
  4. musketeer: 134 раза (WR: 70%)
  5. log: 98 раз (WR: 71%)

ЛУЧШИЕ КОМБО:
  1. hog_rider + ice_golem: 82% успешность
  2. fireball + log: 75% успешность
  3. pekka + electro_wizard: 73% успешность

ОПТИМАЛЬНЫЕ УСЛОВИЯ:
  Лучшее время для атаки: 1:30 (78% успех)
  Оптимальный эликсир: 8 (75% успех)
```

---

## 📹 Анализ реплеев

### Просмотр и анализ

```bash
# Список доступных реплеев
python -m unified_clash_royale_ai.replay_analyzer --list

# Просмотр реплея
python -m unified_clash_royale_ai.replay_analyzer --view match_001

# Анализ ошибок
python -m unified_clash_royale_ai.replay_analyzer --analyze match_001

# Экспорт в видео
python -m unified_clash_royale_ai.replay_analyzer --export match_001

# С рекомендациями по улучшению
python -m unified_clash_royale_ai.replay_analyzer --export match_001 --analyzed
```

### Функции анализатора

- ✅ **Интерактивный просмотр** с перемоткой и паузами
- ✅ **Визуализация** состояния игры на кадрах
- ✅ **Тепловая карта** размещений карт
- ✅ **Временная шкала** всех действий
- ✅ **Обнаружение ошибок** с приоритетами
- ✅ **Рекомендации** по улучшению игры
- ✅ **Экспорт в видео** с комментариями

---

## 🧪 Тестирование

### Запуск тестов

```bash
# Все тесты
python -m pytest unified_clash_royale_ai/tests/

# Только unit тесты
python -m pytest unified_clash_royale_ai/tests/unit_tests.py -v

# Integration тесты
python -m pytest unified_clash_royale_ai/tests/integration_tests.py -v

# С покрытием кода
python -m pytest unified_clash_royale_ai/tests/ --cov=unified_clash_royale_ai

# Бенчмарки производительности
python -m unified_clash_royale_ai.tests.benchmarks
```

### Типы тестов

- **Unit тесты** — проверка отдельных модулей
- **Integration тесты** — проверка взаимодействия компонентов
- **Strategy tests** — тестирование стратегий на симуляторе
- **Benchmarks** — измерение производительности

---

## 🔌 Система плагинов

### Создание плагина

```python
from unified_clash_royale_ai.plugins import StrategyPlugin

class MyCustomStrategy(StrategyPlugin):
    name = "Моя Кастомная Стратегия"
    version = "1.0.0"
    author = "Ваше имя"
    description = "Описание стратегии"

    def on_load(self):
        print("Плагин загружен!")

    def on_unload(self):
        print("Плагин выгружен!")

    def get_priority(self):
        return 50  # Приоритет (выше = важнее)

    def decide_action(self, game_state):
        # Ваша логика принятия решений
        if game_state['our_elixir'] >= 7:
            return {
                'action': 'play_card',
                'card': 'hog_rider',
                'position': 'bridge_left'
            }
        return None
```

Сохраните в `plugins/my_strategy.py` — плагин автоматически загрузится!

### Типы плагинов

- **StrategyPlugin** — кастомные стратегии
- **DetectorPlugin** — дополнительные детекторы
- **MetricsPlugin** — сбор метрик
- **HookPlugin** — хуки на события игры

---

## 📚 База знаний

### Оптимальные размещения

```python
from unified_clash_royale_ai.knowledge_base import PlacementGuide

guide = PlacementGuide()

# Получить оптимальную позицию
pos = guide.get_optimal_position('hog_rider', 'offensive')
# Возвращает нормализованные координаты (x, y)

# Получить советы
tips = guide.get_placement_tips('golem')
# "Размещайте танков сзади для накопления эликсира"

# Все позиции для карты
all_positions = guide.get_all_positions('xbow')
```

### Контрпики

```python
from unified_clash_royale_ai.knowledge_base import CounterPickTable

table = CounterPickTable()

# Получить контрпики
counters = table.get_counters('balloon')
# ['minion_horde', 'mega_minion', 'musketeer', ...]

# Лучшая контра
best_counter = table.get_best_counter('balloon')
# 'minion_horde'

# Найти контру в нашей колоде
our_counters = table.find_counter_in_deck('balloon', our_deck)
```

### Мета колоды

```python
from unified_clash_royale_ai.knowledge_base import MetaDecksDatabase

db = MetaDecksDatabase()

# Получить колоду
deck = db.get_deck('hog_2.6')
# {'cards': [...], 'archetype': 'cycle', 'tips': [...]}

# Все колоды архетипа
cycle_decks = db.get_decks_by_archetype('cycle')

# Поиск похожих колод
similar = db.search_similar_deck(['hog_rider', 'musketeer', ...])
```

---

## 🎓 Обучение моделей

### Сбор данных

```bash
# Автоматический сбор данных во время игры
python -m unified_clash_royale_ai.training.data_collection

# Или во время обычной игры
python run_ai.py --collect-data
```

Собранные данные сохраняются в:
- `training_data/cards/` — изображения карт
- `training_data/yolo/` — изображения для YOLO
- `training_data/rl/` — состояния для RL

### Обучение моделей

```bash
# Обучение CNN для распознавания карт
python -m unified_clash_royale_ai.training.train_card_detector \
    --epochs 50 --batch-size 32

# Обучение YOLO для обнаружения войск
python -m unified_clash_royale_ai.training.train_yolo \
    --epochs 100 --imgsz 640

# Обучение RL агента
python -m unified_clash_royale_ai.training.train_rl \
    --episodes 1000 --save-freq 100
```

### Управление моделями

```python
from unified_clash_royale_ai.training import ModelManager

manager = ModelManager()

# Автозагрузка необходимых моделей
models = manager.auto_load_models(['card_detector', 'yolo_troops'])

# Регистрация новой версии
manager.register_model('card_detector', 'path/to/model.h5', version='v2.0')

# Загрузка из облака
manager.download_model('card_detector')
```

---

## 🔄 Автоматический перезапуск

Система автоматически перезапускается после сбоев:

```python
from unified_clash_royale_ai.utils.auto_restart import Watchdog

watchdog = Watchdog(
    max_restarts=5,           # Максимум 5 перезапусков
    restart_delay=5.0,        # Задержка 5 секунд
    health_check_interval=30  # Проверка каждые 30 секунд
)

# Добавление проверок здоровья
watchdog.add_health_check(
    lambda: screen_capture.is_working(),
    "Screen capture"
)

# Запуск с защитой
watchdog.run(main_function, arg1, arg2)
```

### Особенности

- ✅ **Лимит перезапусков** — предотвращает бесконечные циклы
- ✅ **Период охлаждения** — пауза после множественных сбоев
- ✅ **Мониторинг здоровья** — обнаружение проблем до краша
- ✅ **Логирование** — все ошибки записываются в файл
- ✅ **Статус** — можно проверить состояние системы

---

## ⚙️ Настройка

### GUI настроек

```bash
python run_ai.py --settings
```

Откроется окно с вкладками:
- **Общие** — язык, тема, автозапуск
- **Захват экрана** — метод, FPS, окно
- **Распознавание** — пороги, GPU
- **Бот** — режим, задержки
- **Производительность** — кэш, потоки
- **Горячие клавиши**
- **Профили**
- **Калибровка**

### Калибровка экрана

```bash
# Автоматическая калибровка
python run_ai.py --calibrate

# Или через GUI настроек
```

Система автоматически определит:
- Размер окна игры
- Масштаб
- Координаты карт, башен, поля боя

---

## 🔧 Все команды

### Запуск

```bash
# Базовый запуск
python run_ai.py

# С интерфейсом
python run_ai.py --gui

# Выбор режима
python run_ai.py --mode smart
python run_ai.py --mode rule_based
python run_ai.py --mode hybrid

# Выбор профиля
python run_ai.py --profile fast
python run_ai.py --profile balanced
python run_ai.py --profile accurate

# С записью
python run_ai.py --record
```

### Настройки

```bash
# Открыть GUI настроек
python run_ai.py --settings

# Калибровка экрана
python run_ai.py --calibrate

# Сброс настроек
python run_ai.py --reset-config
```

### Аналитика

```bash
# Общая статистика
python run_ai.py --stats

# Полный анализ
python run_ai.py --analyze

# Детальные отчеты
python -m unified_clash_royale_ai.analytics --report
python -m unified_clash_royale_ai.analytics --cards
python -m unified_clash_royale_ai.analytics --matchups
python -m unified_clash_royale_ai.analytics --timing
```

### Обучение

```bash
# Сбор данных
python run_ai.py --collect-data
python -m unified_clash_royale_ai.training.data_collection

# Обучение моделей
python run_ai.py --train cards
python run_ai.py --train yolo
python run_ai.py --train rl

# Или напрямую
python -m unified_clash_royale_ai.training.train_card_detector
python -m unified_clash_royale_ai.training.train_yolo
python -m unified_clash_royale_ai.training.train_rl
```

### Тесты

```bash
# Запуск тестов
python run_ai.py --test
python -m pytest unified_clash_royale_ai/tests/

# Бенчмарки
python run_ai.py --benchmark
python -m unified_clash_royale_ai.tests.benchmarks
```

### Реплеи

```bash
# Просмотр
python -m unified_clash_royale_ai.replay_analyzer --view match_id

# Анализ
python -m unified_clash_royale_ai.replay_analyzer --analyze match_id

# Экспорт
python -m unified_clash_royale_ai.replay_analyzer --export match_id
```

---

## 📋 Системные требования

| Компонент | Минимум | Рекомендуется |
|-----------|---------|---------------|
| **ОС** | Windows 10 | Windows 11 |
| **Python** | 3.8 | 3.10+ |
| **RAM** | 4 GB | 16 GB |
| **GPU** | Не обязательно | NVIDIA GTX 1060+ |
| **VRAM** | - | 4+ GB |
| **Эмулятор** | LDPlayer/BlueStacks | LDPlayer 9 |
| **Свободное место** | 2 GB | 10+ GB (с моделями) |

---

## 🎯 Основные фичи

### ✅ Реализовано

- ✅ **Распознавание карт** с помощью CNN
- ✅ **Обнаружение войск** через YOLO v8
- ✅ **Reinforcement Learning** агент (PDQN)
- ✅ **Продвинутые стратегии** (Deck Builder, Meta Tracker, Matchup Analyzer)
- ✅ **Система обучения** моделей
- ✅ **Анализ реплеев** с экспортом в видео
- ✅ **Оптимизация производительности** (многопоточность, кэширование, ONNX/TensorRT)
- ✅ **Полное тестирование** (unit, integration, strategy tests, benchmarks)
- ✅ **Система настроек** с профилями и калибровкой
- ✅ **База знаний** (размещения, контрпики, мета колоды, гайды)
- ✅ **Система плагинов** для расширения
- ✅ **Расширенная аналитика** (карты, архетипы, тайминг, паттерны)
- ✅ **Автоматический перезапуск** и мониторинг здоровья
- ✅ **GUI интерфейс** для мониторинга
- ✅ **Запись матчей** для анализа

---

## 🤝 Вклад в проект

Приветствуются любые вклады! Вы можете:

- 🐛 Сообщать об ошибках
- 💡 Предлагать новые функции
- 🔧 Улучшать код
- 📝 Улучшать документацию
- 🔌 Создавать плагины

---

Автор: legenda  
Telegram: [@LEGENDA_SD](https://t.me/LEGENDA_SD)
