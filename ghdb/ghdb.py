from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import contextlib


class Dork:
    def __init__ (self, html_page):
        self.result = self._parse_html(html_page)

    @staticmethod
    def _parse_html(html_page):
        def card_body(page, result):
            row = page.body.find(class_=['card-body'])
            for div in row.find_all('div'):
                title = div.find(class_=['info-title'])
                value = div.find(class_=['stats-title'])

                if title and value:
                    result[title.string.strip().split(':')[0]] = value.string.strip()

        def card_footer(page, result):
            row = page.body.find(class_=['card-footer'])
            for div in row.find_all(lambda tag: tag.name == 'div', class_="stats text-center"):
                title = div.find('strong')
                if title:
                    data = div.text.strip().split(':')
                    result[data[0]] = data[1].strip()

            row = row.find_next(class_=['card-footer'])
            for div in row.find_all(lambda tag: tag.name == 'div', class_='stats text-center'):
                dork_ref = div.find('a')
                if dork_ref:
                    result['Dork'] = dork_ref.text.strip()
                    result['Link'] = dork_ref.get('href').replace(' ','%20')

        def card_toolbar(page, result):
            item = page.body.find(lambda tag: tag.name == 'code', class_='language-text')
            result['Description'] = item.text.strip()

        parsed_html = BeautifulSoup(html_page, 'html.parser')
        result = {}
        card_body(parsed_html, result)
        card_footer(parsed_html, result)
        card_toolbar(parsed_html, result)
        return result

    def __str__(self):
        data = '\n'.join(f'{key:12}: {value}' for (key, value) in self.result.items())
        return f'{data}\n{"-"*40}\n'


def process_dork(url, log_file):
    print('Downloading', url)
    # Construct the HTTP Request
    dork_request = Request(url)
    dork_request.add_header('user-agent',
                                'Mozilla/5.0 (X11; Linux i686; rv:43.0) Gecko/20100101 Firefox/43.0 Iceweasel/43.0.4')

    with contextlib.closing(urlopen(url, timeout=7)) as response:
        # Get the HTTP Response aka HTML page
        dork = Dork(response.read())
        log_file.write(str(dork))

    print('[+]FINISHED')


def extract_google_dorks(start, stop):
    # log file
    log_file_name = f'GhdbResults_{str(start)}_{str(stop)}.txt'

    with open(log_file_name, 'a') as log_file:
        for page_number in range(start, stop):
            current_url = f'http://www.exploit-db.com/ghdb/{str(page_number)}/'
            try:
                process_dork(current_url, log_file)
            except Exception as e:
                print('Exception:', str(e))
                exit(0)

    print("[+] Congrats! the application report is saved: " + log_file_name)


def main():
    extract_google_dorks(900, 910)

if __name__ == '__main__':
    main()