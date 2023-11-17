import requests
from bs4 import BeautifulSoup
import os

class ArbitrCourtScraper:

    HEADER = {
    'Cookie' : '__ddg1_=eInGhWOB8WYDB749ODos; ASP.NET_SessionId=kenxbpnnvjwvkppwagtdqrjy; CUID=98e58dce-8af2-43a0-8583-928be89757c7:MMQhLpiJ4VdqrPeDpp+hVQ==; pr_fp=561556d32115512f3f3224a0b2a49340626012691234d5441c486ef030ec323d; KadLVCards=%d0%9041-17787%2f2023; _ga=GA1.2.1518033350.1700187076; _gid=GA1.2.1814489023.1700187076; tmr_lvid=d8eeee86d6137acffc21c4141a830a3b; tmr_lvidTS=1700187077633; _ym_uid=1700187078411911694; _ym_d=1700187078; _ym_isad=1; _ga_5C6XL8NQPW=GS1.2.1700188654.1.0.1700188654.0.0.0; rcid=d516bda6-320c-4ef7-bebd-75eb48d99d18; _ga_EYS41HMRV3=GS1.2.1700199151.3.1.1700199153.58.0.0; _ga_Q2V7P901XE=GS1.2.1700199151.3.1.1700199153.0.0.0; tmr_detect=1%7C1700199154004; _ga_9582CL89Y6=GS1.2.1700201567.4.0.1700201567.60.0.0; wasm=d877bae54dd0a04b54133a8c7c8970f3',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

    def __init__(self, base_url='https://kad.arbitr.ru/'):
        self.base_url = base_url

    def download_pdfs(self, case_number):
        search_url = f'https://kad.arbitr.ru/Card/{case_number}'

        response = requests.post(search_url, headers=self.HEADER)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml.parser')

            pdf_links = []
            for link in soup.find_all('a', {'class': 'file'}):
                pdf_links.append(self.base_url + link.get('href'))

            if pdf_links:
                download_folder = f'pdfs_{case_number}'
                os.makedirs(download_folder, exist_ok=True)

                for i, pdf_link in enumerate(pdf_links, start=1):
                    pdf_response = requests.get(pdf_link)
                    if pdf_response.status_code == 200:
                        pdf_filename = f'{download_folder}/document_{i}.pdf'
                        with open(pdf_filename, 'wb') as pdf_file:
                            pdf_file.write(pdf_response.content)
                            print(f'Downloaded: {pdf_filename}')
            else:
                print('No PDFs found on the case page.')
        else:
            print(f'Error accessing the case page. Status code: {response.status_code}')

if __name__ == '__main__':
    arbitr_scraper = ArbitrCourtScraper()
    case_number = 'А41-17787/2023'
    arbitr_scraper.download_pdfs(case_number)
