from bs4 import BeautifulSoup
import requests
from smtplib import *

email = "YOUR_EMAIL"
password = "YOUR_PASSWORD"

serial_number = input("Введіть свій пошуковий запит: ")
target_url = f"https://prom.ua/ua/search?search_term={serial_number}&exact_match=true&sort=price&binary_filters=presence_available"

response = requests.get(target_url).text

sp = BeautifulSoup(response, 'html.parser')
gallery_results = sp.find(name='span', class_='_3Trjq htldP _7NHpZ h97_n')
gallery_price = sp.find(name='span', class_='yzKb6')
gallery_href = 'https://prom.ua' + sp.find(name='a', class_='_0cNvO jwtUM').get('href')


for result_price in range(1):
    with SMTP(host='smtp.gmail.com', port=587) as server:
            server.starttls()
            server.login(email, password)
            try:
                message = f'Subject:Найдешевший варіант по запиту {serial_number}\n\n{gallery_results.text}, вартістю {gallery_price.text} грн. Посилання на пошук: {gallery_href}'.encode('utf-8')
                server.sendmail(from_addr=email, to_addrs=email, msg=message)
            except AttributeError:
                message = f'Subject:Результат запиту по {serial_number}\n\nПо запиту {serial_number} нічого не знайдено'.encode('utf-8')
                server.sendmail(from_addr=email, to_addrs=email, msg=message)
        