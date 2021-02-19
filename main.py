from crawler import *
from db import *
from utils import create_sitemap_xml
from datetime import datetime
import click

# c = Crawler('https://yandex.ru')
#
# c.run()
#
# create_db_and_save_links(c)
# create_sitemap_xml(c)
#
# print(len(c.founded_links))

@click.command()
@click.option('--url', help='URL для составления sitemap.')
@click.option('--threads', default=5, help='Количество потоков.')
@click.option('--db', '-d', is_flag=True, help='Запись в базу данных.')
@click.option('--o', default='sitemaps/sitemap.xml', help='Имя файла с sitemap.')
@click.option('--s', '-s', is_flag=False,  help='Отключить уведомления в консоли. ')
def main(url, threads, s, db, o):
    crawler = Crawler(url=url, silence=s, output=o, threads=threads)
    start_time = datetime.now()
    crawler.run()
    end_time = datetime.now()
    runtime = end_time-start_time

    print(f'\nПарсинг занял {runtime}')

    create_sitemap_xml(crawler)

    if db:
        create_db_and_save_links(crawler)


if __name__ == '__main__':
    main()

