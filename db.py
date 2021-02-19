from datetime import datetime
from urllib.parse import urljoin
from peewee import (
    Model,
    CharField,
    DateTimeField,
    IntegrityError,
    SqliteDatabase,
)

db = SqliteDatabase('sitemap.db')


class Link(Model):
    link = CharField(unique=True)
    date = DateTimeField(default=datetime.now)

    class Meta:
        database = db


def create_db_and_save_links(crawler):
    """
    Создает базу sqlite и записывает в нее все линки кравлера.\n
    Если линк уже записан в БД - обновляет время записи.
    :param crawler:
    :return:
    """
    global db
    db.connect()
    db.create_tables([Link])
    print('Начинаю запись в базу данных...')
    for url in crawler:
        try:
            Link.create(link=urljoin(crawler.url, url))
        except IntegrityError:
            query = Link.update(
                date=datetime.now()
            ).where(
                Link.link == urljoin(crawler.url, url)
            )
            query.execute()
    db.commit()
    db.close()
    print('Готово. \n')

