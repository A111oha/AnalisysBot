
from bs4 import BeautifulSoup
import requests
from selenium import webdriver


class Parser:
    def parse_website(self, page_url, max_elements=5):
        driver = webdriver.Chrome()  # Потрібно встановити chromedriver
        driver.get(page_url)
        driver.implicitly_wait(10)

        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        links = soup.find_all('div', class_='goods-tile ng-star-inserted')

        parsed_data = []  # Створюємо список для збереження даних

        for i, link in enumerate(links):
            if i >= max_elements:
                break

            product_link = link.find('a', class_='goods-tile__heading')
            if product_link:
                product_url = product_link.get("href")
                name = link.find('span', class_='goods-tile__title').text.strip()
                price = link.find("div", class_="goods-tile__prices").text

                # Зберігаємо дані у список
                parsed_data.append({
                    "url": product_url,
                    "name": name,
                    "price": price
                })
            else:
                print("No link found for this product.\n")

        driver.quit()

        return parsed_data  # Повертаємо список зі збереженими даними






