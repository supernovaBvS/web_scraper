import httpx 
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict
import csv
from datetime import datetime
d = datetime.now().date()


@dataclass
class Product:
    manufacturer: str
    title: str
    price: str


def get_html(page):
    url = f"https://www.thomann.de/gb/search_GF_electric_guitars.html?ls=100&pg={page}&hl=BLOWOUT"
    resp = httpx.get(url)
    return HTMLParser(resp.text)


def parse_products(html):
    products = html.css("div.product")

    results = []
    for product in products:
        new = Product(
            manufacturer=product.css_first('span.title__manufacturer').text(),
            title=product.css_first('span.title__name').text(),
            price=product.css_first('div.product__price').text().strip()
        )
        results.append(asdict(new))
    return results


def to_csv(res):
    with open(f'{d} results.csv', 'w') as f:
        fieldnames = ['manufacturer', 'title', 'price']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerows(res)


def main():
    for x in range(1, 4):
        html = get_html(x)
        res = parse_products(html)
        print(html.css_first('title').text(), f'(nums of data {len(res)})')
        to_csv(res)


if __name__ == "__main__":
    main()