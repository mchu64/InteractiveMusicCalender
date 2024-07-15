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
        th = row.find('th', scope='row')
        if th:
            current_date = th.get_text(strip=True)
            if current_date not in hashmap:
                hashmap[current_date] = []
        
        cells = row.find_all('td')
        if len(cells) >= 3:
            artist = cells[0].get_text(strip=True)
            album = cells[1].get_text(strip=True)
            genre = cells[2].get_text(strip=True) if len(cells) > 2 else ""
            label = cells[3].get_text(strip=True) if len(cells) > 3 else ""

            hashmap[current_date].append({
                'artist': artist,
                'album': album,
                'genre': genre,
                'label': label
            })

    print(hashmap)

def main():
    scrape()

if __name__ == "__main__":
    main()