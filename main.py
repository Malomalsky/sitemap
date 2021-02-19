from crawler import *
from db import *
from utils import create_sitemap_xml, make_md_table
from datetime import datetime
import click



@click.command()
@click.option('--url', help='URL для составления sitemap.')
@click.option('--threads', default=5, help='Количество потоков.')
@click.option('--db', '-d', is_flag=True, help='Запись в базу данных.')
@click.option('--s', '-s', is_flag=False,  help='Отключить уведомления в консоли. ')
def main(url, threads, s, db):
    crawler = Crawler(url=url, silence=s, threads=threads)
    start_time = datetime.now()
    crawler.run()
    end_time = datetime.now()
    runtime = end_time-start_time

    print(f'\nПарсинг занял {runtime}')

    create_sitemap_xml(crawler)
    make_md_table(crawler, runtime)

    if db:
        create_db_and_save_links(crawler)


if __name__ == '__main__':
    main()


