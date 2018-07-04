from urllib.request import urlopen, Request
import time
from bs4 import BeautifulSoup
import html
import contextlib


class Dork:
    def __init__ (self, content):
        items = self._parse_html(content)
        self.date = items[4]
        self.dork = items[2]
        self.desc = items[-1]

    @staticmethod
    def _parse_html(content):
        parsed_html = BeautifulSoup(content, 'html.parser')
        dork_table = parsed_html.body.find('table', {'class': 'category-list'})

        first_td = dork_table.findChild('td')
        items = []
        for i in range(5):
            if i == 1 or i == 2:
                item = first_td.find('a').get('href')
            else:
                item = html.unescape(first_td.text)
            items.append(item.strip())
            first_td = first_td.findNext('td')

        # parse description
        desc_div = parsed_html.body.find('div', {'id': 'container'})
        items.append(html.unescape(desc_div.text).strip())
        return items

    def __str__(self):
        return f"{self.date}\nDescription: {self.desc}\nGoogle Dork: {self.dork}\n-----------------------------\n";


def fetch_and_save_the_dork(current_url, log_file):
    print("Downloading " + current_url)

    # failed attempts counter
    failed_attempts_counter = 0
    try:
        # Construct the HTTP Request
        dork_request = Request(current_url)
        dork_request.add_header('user-agent',
                                'Mozilla/5.0 (X11; Linux i686; rv:43.0) Gecko/20100101 Firefox/43.0 Iceweasel/43.0.4')

        with contextlib.closing(urlopen(current_url, timeout=7)) as dork_response:
            # Get the HTTP Response aka HTML page
            dork = Dork(dork_response.read())
            log_file.write(str(dork))

        # reset counter
        failed_attempts_counter = 0
        print("[+]FINISHED")

    except Exception as e:
        print("Exception:" + str(e))
        print("Error retrying in 3 seconds.")
        time.sleep(3)
        failed_attempts_counter += 1

        if failed_attempts_counter == 5:
            print("Something is wrong,exiting...")
            log_file.close()
            exit(0)


def extract_google_dorks(start_item_number, latest_item_number):
    # log file
    log_file_name = "GhdbResults_" + str(start_item_number) + "_" + str(latest_item_number) + ".txt"

    with open(log_file_name, "a") as log_file:
        for page_number in range(start_item_number, latest_item_number):
            current_url = 'http://www.exploit-db.com/ghdb/' + str(page_number) + '/'
            fetch_and_save_the_dork(current_url, log_file)

    print("[+] Congrats! the application report is saved: " + log_file_name)


def main():
    extract_google_dorks(900, 906)

if __name__ == '__main__':
    main()