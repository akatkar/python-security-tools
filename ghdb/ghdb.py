from urllib.request import urlopen, Request
import time
from bs4 import BeautifulSoup
import html


def extract_google_dorks(start_item_number, latest_item_number):
    # log file
    log_file_name = "GhdbResults_" + str(start_item_number) + "_" + str(latest_item_number) + ".txt"
    log_file = open(log_file_name, "a")
    # failed attempts counter
    failed_attempts_counter = 0

    for page_number in range(start_item_number, latest_item_number):

        current_url = 'http://www.exploit-db.com/ghdb/' + str(page_number) + '/'

        print("Downloading " + current_url)

        try:
            # Construct the HTTP Request
            item_request = Request(current_url)
            item_request.add_header('user-agent',
                                    'Mozilla/5.0 (X11; Linux i686; rv:43.0) Gecko/20100101 Firefox/43.0 Iceweasel/43.0.4')

            # Get the HTTP Response aka HTML page
            item_response = urlopen(current_url, timeout=7)
            item_content = item_response.read()

            parsed_html = BeautifulSoup(item_content,'html.parser')
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

            item_date = items[4]
            item_dork = items[2]

            desc_div = parsed_html.body.find('div', {'id': 'container'})
            item_desc = html.unescape(desc_div.text).strip()

            item = "{}\nDescription: {}\nGoogle Dork: {}\n-----------------------------\n"\
                       .format(item_date, item_desc, item_dork)
            log_file.write(item)

            item_response.close()

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

    log_file.close()
    print("[+] Congrats! the application report is saved: " + log_file_name)


def main():
    extract_google_dorks(900, 906)

if __name__ == '__main__':
    main()