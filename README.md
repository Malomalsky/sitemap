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

Результаты работы записываются в [table.md](https://github.com/Malomalsky/sitemap/blob/master/table.md). В таблице лежат запрашиваемые в тестовом задании значения. 
Сам файл sitemap - в директории [sitemaps](https://github.com/Malomalsky/sitemap/tree/master/sitemaps)

--- 
## Пояснения 

* Файл [crawler.py](https://github.com/Malomalsky/sitemap/blob/master/crawler.py) содержит класс Crawler. 
* Файл [db.py](https://github.com/Malomalsky/sitemap/blob/master/db.py) содержит логику работы с базой даных. В качестве интерфейса был выбран peewee - Django-like ORM.
* Файл [utils.py](https://github.com/Malomalsky/sitemap/blob/master/utils.py) содержит дополнительные функции - создание sitemap.xml и markdown-таблицы с результатами. 

## Сложности и доработки

### Визуализация

Для визуализации sitemap можно прибегнуть к [этому](https://github.com/Ayima/sitemap-visualization-tool) репозиторию. Я не стал копировать код. 

### 429.
Во время многопоточного парсинга довольно часто возникает превышение лимита запросов. Такая ситуация случается со стаковерфлоу: 

![stack](https://raw.githubusercontent.com/Malomalsky/knowledge_base/master/g-book/stackoverflow.PNG?token=AGSNIZ6YTM6FF3VP7RTSGITAHDECI)

Решается это проксированием трафика. 
Stackoverflow пришлось парсить без многопоточности. 

### Яндекс и избыточность
В яндексе неимоверно много ссылок! На тот момент, когда я остановил скрипт, значение найденных ссылок превышало 270000, а время работы скрипта - 40 минут. 
В любом случае, стандарт sitemap приписывает не добавлять в файл более 50к URL и не превышать его размер в 50мб. В противном случае sitemap-ов должно быть несколько. 
Выходов в данной ситуации может стать более умный парсинг, или парсинг с заданием 'глубины' - числа, отвечающего за количество поддоменов в исследуемом URL. 

### Мнопоточность и многопроцессорность 
Я знаю, что сейчас скрипт рекурсивно плодит потоки, и я знаю что это плохо. Выходом я вижу использование ассинхронности, но ее в тестовом задании заявлено не было. 

### crawler-test
Во время парсинга http://crawler-test.com/ сайт начинает генерировать бесконечные рекурсивные страницы со списком таких же случайных страниц. Для их исключения было захардкожено условие с пропуском ссылок с поддоменом '/infinite/'.  

### Результаты google 
По таблице можно заметить, что результаты гугла различаются. Это - последствия запуска скрипта с локальной машины и с repl.it. Локальную машину гугл быстро ограничивает в реквестах. 

### Валидация
Все полученные sitemap были провалидированы с помощью [Яндекс.Вебмастера](https://webmaster.yandex.ru/tools/sitemap/)
