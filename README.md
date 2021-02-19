# sitemap
Тестовое задание АВСОФТ

--- 

## Установка: 

```bash
git clone https://github.com/Malomalsky/sitemap.git
cd sitemap
pip install -r requirements.txt
```

--- 
## Запуск
Скрипт запускается из консоли командой:

```bash
python main.py [OPTIONS]
```

Сигнатура: 

```bash
Usage: main.py [OPTIONS]

Options:
  --url TEXT         URL для составления sitemap.
  --threads INTEGER  Количество потоков.
  -d, --db           Запись в базу данных.
  -s, --s TEXT       Отключить уведомления в консоли.
  --help             Show this message and exit.
```

Например, для парсинга google.com в 10 потоков и последующей записи результатов в бд необходимо выполнить команду: 

```bash
python main.py --url=https://google.com --threads=10 -d
```

--- 
## Пояснения 

* Файл [crawler.py](https://github.com/Malomalsky/sitemap/blob/master/crawler.py) содержит класс Crawler. 
* Файл [db.py](https://github.com/Malomalsky/sitemap/blob/master/db.py) содержит логику работы с базой даных. В качестве интерфейса был выбран peewee - Django-like OR<.
* Файл [utils.py](https://github.com/Malomalsky/sitemap/blob/master/utils.py) содержит дополнительные функции - создание sitemap.xml и markdown-таблицы с результатами. 

## Сложности и доработки

### Визуализация. 

Для визуализации sitemap можно прибегнуть к [этому](https://github.com/Ayima/sitemap-visualization-tool) репозиторию. Я не стал копировать код. 

### 429.
Во время многопоточного парсинга довольно часто возникает превышение лимита запросов. Такая ситуация случается со стаковерфлоу: 

![stack](https://raw.githubusercontent.com/Malomalsky/knowledge_base/master/g-book/stackoverflow.PNG?token=AGSNIZ6YTM6FF3VP7RTSGITAHDECI)

Решается это проксированием трафика. 
Кстати, из-за этого составить полную карту stackoverflow не вышло. 

### Яндекс и избыточность. 
В яндексе неимоверно много ссылок! На тот момент, когда я остановил скрипт, значение найденных ссылок превышало 270000, а время работы скрипта - 40 минут. 
В любом случае, стандарт sitemap приписывает не добавлять в файл более 50к URL и не превышать его размер в 50мб. В противном случае sitemap-ов должно быть несколько. 
Выходов в данной ситуации может стать более умный парсинг, или парсинг с заданием 'глубины' - числа, отвечающего за количество поддоменов в исследуемом URL. 

### Мнопоточность и многопроцессорность. 
Я знаю, что сейчас скрипт бесконечно и рекурсивно плодит потоки, и я знаю что это плохо. Выходом я вижу использование ассинхронности, но ее в тестовом задании заявлено не было. 
