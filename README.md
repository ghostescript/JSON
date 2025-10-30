# JSON
Retrieve website data, parse and save to a JSON formatted file. Use flags to specify which data to retrieve.

<br>

# Installation 
```bash
git clone https://github.com/ghostescript/JSON
cd JSON
python get.json.py -h
```

<br>

# Help Message 
![alt text](https://raw.githubusercontent.com/ghostescript/JSON/refs/heads/main/files/20251030_002620.jpg)

<br>

```
┌──(kali㉿localhost)-[~/JSON]
└─$ python get.json.py -h
usage: get.json.py [-h] [--cookies-to-json] [--headers-to-json] [--html-to-json] [--javascript-to-json] [--text-to-json] [--image-links-to-json]
                   [--structured-data-to-json] [--metadata-to-json] [--extracted-links-to-json] [--media-files-to-json] [--emails-usernames-to-json]
                   [--phonenumbers-to-json] [--all-to-json] [--all-separate-to-json]
                   url

Retrieve website data, parse and save to a JSON formatted file. Use flags to specify which data to retrieve.

positional arguments:
  url                   The URL to retrieve data from.

options:
  -h, --help            show this help message and exit
  --cookies-to-json     Retrieve cookies and save them as JSON.
  --headers-to-json     Retrieve response headers and save them as JSON.
  --html-to-json        Retrieve HTML content, parse it, and save as JSON.
  --javascript-to-json  Retrieve JavaScript content from script tags, parse it, and save as JSON.
  --text-to-json        Retrieve all visible text content from a URL and save as JSON.
  --image-links-to-json
                        Retrieve all image links (src attributes) from a URL and save as JSON.
  --structured-data-to-json
                        Retrieve structured data (JSON-LD) from a URL and save as JSON.
  --metadata-to-json    Retrieve metadata (title, meta tags) from a URL and save as JSON.
  --extracted-links-to-json
                        Retrieve all extracted links (href attributes of <a> tags) from a URL and save as JSON.
  --media-files-to-json
                        Retrieve all media file links (audio, video, common extensions) from a URL and save as JSON.
  --emails-usernames-to-json
                        Retrieve emails and potential usernames from a URL and save as JSON.
  --phonenumbers-to-json
                        Retrieve phone numbers from a URL and save as JSON.
  --all-to-json         Retrieve all available data (HTML, JS, Text, Images, Structured Data, Metadata, Links, Emails/Usernames, Phone Numbers) and
                        save to a single JSON file.
  --all-separate-to-json
                        Retrieve all available data and save each type to its own separate JSON file.
```

<br>

# Updated On
``Oct 30, 2025``

<br>
