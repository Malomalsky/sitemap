from urllib.parse import urljoin, urlsplit
import os

XML_HEAD_TEMPLATE = '<?xml version="1.0" encoding="UTF-8"?>\n\t<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
XML_ROW_TEMPLATE = "\n\t\t<url>\n\t\t\t<loc>\n\t\t\t\t{0}/\n\t\t\t</loc>\n\t\t</url>"
MARKDOWN_TEMPLATE = " {} | {} | {} | {} | {} "



def create_sitemap_xml(crawler):
    print(f"\nСоздание {crawler.output}...")
    with open(
            urlsplit(crawler.url).netloc + '-' + crawler.output,
            'w'
    ) as file:
        file.write(XML_HEAD_TEMPLATE)

        # Стандарт предписывает не превышать количество URL в 50000.
        for link in crawler[:50000]:
            file.write(XML_ROW_TEMPLATE.format(
                urljoin(
                    crawler.url,
                    link.replace('&', '&amp;')
                )  # Для успешной валидации XML экранируем символ &.
            ))
        file.write('</urlset>')
    print('Готово.\n')


def make_md_table(crawler, time):
    sitemap_name = f""
    if os.path.exists('table.md'):
        with open('table.md', 'a') as f:
            f.write(MARKDOWN_TEMPLATE.format(
                crawler.url,
                crawler.threads,
                time,
                len(crawler),
                crawler.output
                )
            )
