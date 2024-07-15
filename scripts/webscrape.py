import requests
import datetime
from bs4 import BeautifulSoup

def scrape():
    month = datetime.datetime.now().strftime("%B")
    table = None
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
    }
    url = "https://en.wikipedia.org/wiki/List_of_2024_albums"
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")


    for caption in soup.find_all('caption'):
        caption_text = caption.get_text().strip()
        if caption_text == f"List of albums released or to be released in {month} 2024":
            table = caption.find_parent('table', {'class': 'wikitable plainrowheaders'})
            break
    rows = table.find_all('tr')
    hashmap = {}
    current_date = ""

    for row in rows:
        date_header = row.find('th', class_='head head_type_1')
        if date_header:
            current_date = date_header.text.strip()
            if current_date not in hashmap:
                hashmap[current_date] = []
            continue

        artist_cell = row.find('td', class_='artistName')
        album_cell = row.find('td', class_='albumTitle')

        if artist_cell and album_cell:
            artist_name = artist_cell.get_text(strip=True)
            album_title = album_cell.get_text(strip=True)

            hashmap[current_date].append({
                'artist': artist_name,
                'album': album_title,
            })

    print(hashmap)



def main():
    scrape()

if __name__ == "__main__":
    main()