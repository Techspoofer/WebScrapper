from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque        # to deque the original url
import re
from pyfiglet import Figlet          # To print Welcome Text


f = Figlet(font='slant')
print(f.renderText('EMAIL SCRAPPER           -by Techspoofer & Techbooffer'))



user_url = str(input('[+] Enter Target URL to scan: ')) # url that needs to be scan
urls = deque([user_url])    #deques original url and extends new hyperlink from the existing one

scrapped_url = set()
emails = set()

count = 0    #the process will start from 0 and then so on.
try:
    while len(urls):
        count += 1
        if count == 80:
            break
        
        url = urls.popleft()
        scrapped_url.add(url)
        
        parts = urllib.parse.urlsplit(url)
        base_url = f"{parts.scheme}://{parts.netloc}"
        
        path = url[:url.rfind('/') + 1] if '/' in parts.path else url
        print(f'[{count}] Processing {url}')
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
            continue
        
        new_emails = set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', response.text, re.I))
        emails.update(new_emails)

        soup = BeautifulSoup(response.text, 'lxml')
        for anchor in soup.find_all("a"):
            link = anchor.get('href', '')
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
            
            if link not in urls and link not in scrapped_url:
                urls.append(link)

except KeyboardInterrupt:
    print('[-] Closing!')  #closing window


print('Found emails:')   #to print all found emails
for mail in emails:
    print(mail)
