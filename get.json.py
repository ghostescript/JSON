import requests
import json
import argparse
import re
from bs4 import BeautifulSoup

# ANSI color codes
COLOR_GREEN = '\033[92m'
COLOR_CYAN = '\033[96m'
COLOR_YELLOW = '\033[93m'
COLOR_WHITE = '\033[97m'
COLOR_ORANGE = '\033[38;5;208m'
COLOR_BLUE = '\033[94m'
COLOR_GRAY = '\033[90m'
COLOR_RED = '\033[91m'
COLOR_MAGENTA = '\033[95m'
COLOR_PURPLE = '\033[35m'
COLOR_LIGHT_BLUE = '\033[96m'
COLOR_LIGHT_GRAY = '\033[37m'
COLOR_LIGHT_GREEN = '\033[92m'
COLOR_BOLD_GREEN = '\033[1m\033[92m'
COLOR_BOLD_WHITE = '\033[1m\033[97m'
COLOR_RESET = '\033[0m'

def get_response(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

def get_cookies_data(cookies):
    if cookies:
        return {cookie.name: cookie.value for cookie in cookies}
    return None

def save_cookies_to_json(cookies, filename):
    cookie_dict = get_cookies_data(cookies)
    if cookie_dict:
        with open(filename, 'w') as f:
            json.dump(cookie_dict, f, indent=4)
        print(f"{COLOR_BOLD_WHITE}Cookies parsed and saved to {COLOR_BOLD_GREEN}{filename}{COLOR_RESET}")
    else:
        print(f"{COLOR_YELLOW}No cookies found.{COLOR_RESET}")

def get_headers_data(headers):
    if headers:
        return dict(headers)
    return None

def save_headers_to_json(headers, filename):
    header_dict = get_headers_data(headers)
    if header_dict:
        with open(filename, 'w') as f:
            json.dump(header_dict, f, indent=4)
        print(f"{COLOR_BOLD_WHITE}Headers parsed and saved to {COLOR_BOLD_GREEN}{filename}{COLOR_RESET}")

def get_html_data(html_content):
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract title
        title = soup.title.string if soup.title else "No Title"

        # Extract all text
        for script in soup(["script", "style"]):
            script.extract()    # rip it out
        text = soup.get_text()
        # break into lines and remove leading/trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a single line
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        # Extract all links
        links = [a['href'] for a in soup.find_all('a', href=True)]

        return {
            "title": title,
            "text_content": text,
            "links": links
        }
    return None

def save_html_to_json(html_content, filename):
    html_data = get_html_data(html_content)
    if html_data:
        with open(filename, 'w') as f:
            json.dump(html_data, f, indent=4)
        print(f"{COLOR_BOLD_WHITE}HTML content parsed and saved to {COLOR_BOLD_GREEN}{filename}{COLOR_RESET}")
    else:
        print(f"{COLOR_YELLOW}No HTML content to save.{COLOR_RESET}")

def get_javascript_data(html_content):
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        script_data = []
        for script in soup.find_all('script'):
            script_info = {
                "type": script.get('type', 'text/javascript'),
                "src": script.get('src'),
                "content": script.string
            }
            script_data.append(script_info)
        return script_data
    return None

def save_javascript_to_json(html_content, filename):
    script_data = get_javascript_data(html_content)
    if script_data:
        with open(filename, 'w') as f:
            json.dump(script_data, f, indent=4)
        print(f"{COLOR_BOLD_WHITE}JavaScript content parsed and saved to {COLOR_BOLD_GREEN}{filename}{COLOR_RESET}")
    else:
        print(f"{COLOR_YELLOW}No JavaScript content to save.{COLOR_RESET}")

def get_text_data(html_content):
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        # Extract all text
        for script in soup(["script", "style"]):
            script.extract()    # rip it out
        text = soup.get_text()
        # break into lines and remove leading/trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a single line
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return {
            "text_content": text
        }
    return None

def save_text_to_json(html_content, filename):
    text_data = get_text_data(html_content)
    if text_data:
        with open(filename, 'w') as f:
            json.dump(text_data, f, indent=4)
        print(f"{COLOR_BOLD_WHITE}Text content parsed and saved to {COLOR_BOLD_GREEN}{filename}{COLOR_RESET}")
    else:
        print(f"{COLOR_YELLOW}No text content to save.{COLOR_RESET}")

def get_image_links_data(html_content):
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        image_links = [img['src'] for img in soup.find_all('img', src=True)]

        return {
            "image_links": image_links
        }
    return None

def save_image_links_to_json(html_content, filename):
    image_data = get_image_links_data(html_content)
    if image_data:
        with open(filename, 'w') as f:
            json.dump(image_data, f, indent=4)
        print(f"{COLOR_BOLD_WHITE}Image links parsed and saved to {COLOR_BOLD_GREEN}{filename}{COLOR_RESET}")
    else:
        print(f"{COLOR_YELLOW}No image links to save.{COLOR_RESET}")

def get_structured_data(html_content):
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        structured_data = []
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                json_data = json.loads(script.string)
                structured_data.append(json_data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON-LD: {e}")
        return structured_data if structured_data else None
    return None

def save_structured_data_to_json(html_content, filename):
    structured_data = get_structured_data(html_content)
    if structured_data:
        with open(filename, 'w') as f:
            json.dump(structured_data, f, indent=4)
        print(f"{COLOR_BOLD_WHITE}Structured data parsed and saved to {COLOR_BOLD_GREEN}{filename}{COLOR_RESET}")
    else:
        print(f"{COLOR_YELLOW}No structured data found to save.{COLOR_RESET}")

def get_metadata(html_content):
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        metadata = {}

        # Extract title
        if soup.title:
            metadata["title"] = soup.title.string

        # Extract meta tags
        meta_tags = soup.find_all('meta')
        for tag in meta_tags:
            if tag.get('name'):
                metadata[tag['name']] = tag.get('content')
            elif tag.get('property'):
                metadata[tag['property']] = tag.get('content')
            elif tag.get('http-equiv'):
                metadata[tag['http-equiv']] = tag.get('content')
        return metadata if metadata else None
    return None

def save_metadata_to_json(html_content, filename):
    metadata = get_metadata(html_content)
    if metadata:
        with open(filename, 'w') as f:
            json.dump(metadata, f, indent=4)
        print(f"{COLOR_BOLD_WHITE}Metadata parsed and saved to {COLOR_BOLD_GREEN}{filename}{COLOR_RESET}")
    else:
        print(f"{COLOR_YELLOW}No metadata found to save.{COLOR_RESET}")

def get_extracted_links_data(html_content):
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        extracted_links = [a['href'] for a in soup.find_all('a', href=True)]

        return {
            "extracted_links": extracted_links
        }
    return None

def save_extracted_links_to_json(html_content, filename):
    links_data = get_extracted_links_data(html_content)
    if links_data:
        with open(filename, 'w') as f:
            json.dump(links_data, f, indent=4)
        print(f"{COLOR_BOLD_WHITE}Extracted links parsed and saved to {COLOR_BOLD_GREEN}{filename}{COLOR_RESET}")
    else:
        print(f"{COLOR_YELLOW}No extracted links to save.{COLOR_RESET}")

def get_media_files_data(html_content):
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        media_files = []

        # Find audio and video sources
        for tag in soup.find_all(['audio', 'video']):
            if tag.get('src'):
                media_files.append(tag['src'])
            for source in tag.find_all('source'):
                if source.get('src'):
                    media_files.append(source['src'])

        # Find links to common media file extensions
        media_extensions = ('.mp3', '.mp4', '.ogg', '.wav', '.webm', '.avi', '.mov', '.flv')
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if href.lower().endswith(media_extensions):
                media_files.append(href)

        return {"media_files": list(set(media_files))} if media_files else None
    return None

def save_media_files_to_json(html_content, filename):
    media_files_data = get_media_files_data(html_content)
    if media_files_data:
        with open(filename, 'w') as f:
            json.dump(media_files_data, f, indent=4)
        print(f"{COLOR_BOLD_WHITE}Media files parsed and saved to {COLOR_BOLD_GREEN}{filename}{COLOR_RESET}")
    else:
        print(f"{COLOR_YELLOW}No media files found to save.{COLOR_RESET}")

def get_emails_usernames_data(html_content):
    if html_content:
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', html_content)
        # A very basic regex for potential usernames. This is highly heuristic.
        # It looks for sequences of word characters, possibly with dots or hyphens, not followed by @.
        usernames = re.findall(r'(?<!@)([a-zA-Z0-9._-]+)(?!@)(?=\s|<|\Z)', html_content)
        # Filter out common words or very short strings that are unlikely to be usernames
        usernames = [u for u in usernames if len(u) > 2 and not u.lower() in ['the', 'and', 'for', 'with', 'from', 'http', 'https', 'www']]

        # Remove duplicates and sort
        emails = sorted(list(set(emails)))
        usernames = sorted(list(set(usernames)))

        data = {
            "emails": emails,
            "usernames": usernames
        }
        return data if emails or usernames else None
    return None

def save_emails_usernames_to_json(html_content, filename):
    data = get_emails_usernames_data(html_content)
    if data:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"{COLOR_BOLD_WHITE}Emails and potential usernames parsed and saved to {COLOR_BOLD_GREEN}{filename}{COLOR_RESET}")
    else:
        print(f"{COLOR_YELLOW}No emails or potential usernames found to save.{COLOR_RESET}")

def get_phonenumbers_data(html_content):
    if html_content:
        # This regex attempts to capture various phone number formats.
        # It's a heuristic and might not catch all or might catch false positives.
        phonenumbers = re.findall(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{2,4}[-.\s]?\d{2,4}[-.\s]?\d{2,4}\b', html_content)
        phonenumbers = sorted(list(set(phonenumbers))) # Remove duplicates and sort

        return {"phonenumbers": phonenumbers} if phonenumbers else None
    return None

def save_phonenumbers_to_json(html_content, filename):
    phonenumbers_data = get_phonenumbers_data(html_content)
    if phonenumbers_data:
        with open(filename, 'w') as f:
            json.dump(phonenumbers_data, f, indent=4)
        print(f"{COLOR_BOLD_WHITE}Phone numbers parsed and saved to {COLOR_BOLD_GREEN}{filename}{COLOR_RESET}")
    else:
        print(f"{COLOR_YELLOW}No phone numbers found to save.{COLOR_RESET}")

def save_all_to_json(response, filename):
    all_data = {}

    # Cookies and Headers (from response object)
    cookies_data = get_cookies_data(response.cookies)
    if cookies_data: all_data["cookies"] = cookies_data

    headers_data = get_headers_data(response.headers)
    if headers_data: all_data["headers"] = headers_data

    # HTML content based extractions
    html_content = response.text
    if html_content:
        html_data = get_html_data(html_content)
        if html_data: all_data["html_content"] = html_data

        javascript_data = get_javascript_data(html_content)
        if javascript_data: all_data["javascript_content"] = javascript_data

        text_data = get_text_data(html_content)
        if text_data: all_data["text_content"] = text_data

        image_links_data = get_image_links_data(html_content)
        if image_links_data: all_data["image_links"] = image_links_data

        structured_data = get_structured_data(html_content)
        if structured_data: all_data["structured_data"] = structured_data

        metadata = get_metadata(html_content)
        if metadata: all_data["metadata"] = metadata

        extracted_links_data = get_extracted_links_data(html_content)
        if extracted_links_data: all_data["extracted_links"] = extracted_links_data

        media_files_data = get_media_files_data(html_content)
        if media_files_data: all_data["media_files"] = media_files_data

        emails_usernames_data = get_emails_usernames_data(html_content)
        if emails_usernames_data: all_data["emails_usernames"] = emails_usernames_data

        phonenumbers_data = get_phonenumbers_data(html_content)
        if phonenumbers_data: all_data["phonenumbers"] = phonenumbers_data

    if all_data:
        with open(filename, 'w') as f:
            json.dump(all_data, f, indent=4)
        print(f"{COLOR_BOLD_WHITE}All data extracted and saved to {COLOR_BOLD_GREEN}{filename}{COLOR_RESET}")
    else:
        print(f"{COLOR_YELLOW}No data found to save for --all-to-json.{COLOR_RESET}")

def run_all_separate_extractions(response, url):
    # Cookies and Headers
    cookie_filename = sanitize_filename(url, "cookies")
    save_cookies_to_json(response.cookies, cookie_filename)

    header_filename = sanitize_filename(url, "headers")
    save_headers_to_json(response.headers, header_filename)

    html_content = response.text

    # HTML content based extractions
    html_filename = sanitize_filename(url, "html_content")
    save_html_to_json(html_content, html_filename)

    js_filename = sanitize_filename(url, "javascript_content")
    save_javascript_to_json(html_content, js_filename)

    text_filename = sanitize_filename(url, "text_content")
    save_text_to_json(html_content, text_filename)

    image_links_filename = sanitize_filename(url, "image_links")
    save_image_links_to_json(html_content, image_links_filename)

    structured_data_filename = sanitize_filename(url, "structured_data")
    save_structured_data_to_json(html_content, structured_data_filename)

    metadata_filename = sanitize_filename(url, "metadata")
    save_metadata_to_json(html_content, metadata_filename)

    extracted_links_filename = sanitize_filename(url, "extracted_links")
    save_extracted_links_to_json(html_content, extracted_links_filename)

    media_files_filename = sanitize_filename(url, "media_files")
    save_media_files_to_json(html_content, media_files_filename)

    emails_usernames_filename = sanitize_filename(url, "emails_usernames")
    save_emails_usernames_to_json(html_content, emails_usernames_filename)

    phonenumbers_filename = sanitize_filename(url, "phonenumbers")
    save_phonenumbers_to_json(html_content, phonenumbers_filename)

def sanitize_filename(url, prefix):
    # Remove protocol and replace special characters with underscores
    sanitized_url = re.sub(r'https?://', '', url)
    sanitized_url = re.sub(r'[^a-zA-Z0-9_.-]', '_', sanitized_url)
    return f"{prefix}_for_{sanitized_url}.json"

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Retrieve website data, parse and save to a JSON formatted file. Use flags to specify which data to retrieve.")

    parser.add_argument("url", help="The URL to retrieve data from.")

    parser.add_argument("--cookies-to-json", action="store_true", help="Retrieve cookies and save them as JSON.")

    parser.add_argument("--headers-to-json", action="store_true", help="Retrieve response headers and save them as JSON.")

    parser.add_argument("--html-to-json", action="store_true", help="Retrieve HTML content, parse it, and save as JSON.")

    parser.add_argument("--javascript-to-json", action="store_true", help="Retrieve JavaScript content from script tags, parse it, and save as JSON.")

    parser.add_argument("--text-to-json", action="store_true", help="Retrieve all visible text content from a URL and save as JSON.")

    parser.add_argument("--image-links-to-json", action="store_true", help="Retrieve all image links (src attributes) from a URL and save as JSON.")

    parser.add_argument("--structured-data-to-json", action="store_true", help="Retrieve structured data (JSON-LD) from a URL and save as JSON.")

    parser.add_argument("--metadata-to-json", action="store_true", help="Retrieve metadata (title, meta tags) from a URL and save as JSON.")

    parser.add_argument("--extracted-links-to-json", action="store_true", help="Retrieve all extracted links (href attributes of <a> tags) from a URL and save as JSON.")

    parser.add_argument("--media-files-to-json", action="store_true", help="Retrieve all media file links (audio, video, common extensions) from a URL and save as JSON.")

    parser.add_argument("--emails-usernames-to-json", action="store_true", help="Retrieve emails and potential usernames from a URL and save as JSON.")

    parser.add_argument("--phonenumbers-to-json", action="store_true", help="Retrieve phone numbers from a URL and save as JSON.")

    parser.add_argument("--all-to-json", action="store_true", help="Retrieve all available data (HTML, JS, Text, Images, Structured Data, Metadata, Links, Emails/Usernames, Phone Numbers) and save to a single JSON file.")

    parser.add_argument("--all-separate-to-json", action="store_true", help="Retrieve all available data and save each type to its own separate JSON file.")

    args = parser.parse_args()



    # Check if any action flag is provided

    if not any([args.cookies_to_json, args.headers_to_json, args.html_to_json, args.javascript_to_json, args.text_to_json, args.image_links_to_json, args.structured_data_to_json, args.metadata_to_json, args.extracted_links_to_json, args.media_files_to_json, args.emails_usernames_to_json, args.phonenumbers_to_json, args.all_to_json, args.all_separate_to_json]):

        print("No action requested. Please specify at least one flag: --cookies-to-json, --headers-to-json, --html-to-json, --javascript-to-json, --text-to-json, --image-links-to-json, --structured-data-to-json, --metadata-to-json, --extracted-links-to-json, --media-files-to-json, --emails-usernames-to-json, --phonenumbers-to-json, --all-to-json, and/or --all-separate-to-json.")

        parser.print_help()

    else:

        response = get_response(args.url)



        if response:

            if args.all_to_json:

                all_data_filename = sanitize_filename(args.url, "all_extracted_data")

                save_all_to_json(response, all_data_filename)

            elif args.all_separate_to_json:

                run_all_separate_extractions(response, args.url)

            else:
                if args.cookies_to_json:
                    cookie_filename = sanitize_filename(args.url, "cookies")
                    save_cookies_to_json(response.cookies, cookie_filename)

                if args.headers_to_json:
                    header_filename = sanitize_filename(args.url, "headers")
                    save_headers_to_json(response.headers, header_filename)

                # For HTML content based extractions, ensure response.text is available
                html_content = response.text

                if args.html_to_json:
                    html_filename = sanitize_filename(args.url, "html_content")
                    save_html_to_json(html_content, html_filename)

                if args.javascript_to_json:
                    js_filename = sanitize_filename(args.url, "javascript_content")
                    save_javascript_to_json(html_content, js_filename)

                if args.text_to_json:
                    text_filename = sanitize_filename(args.url, "text_content")
                    save_text_to_json(html_content, text_filename)

                if args.image_links_to_json:
                    image_links_filename = sanitize_filename(args.url, "image_links")
                    save_image_links_to_json(html_content, image_links_filename)

                if args.structured_data_to_json:
                    structured_data_filename = sanitize_filename(args.url, "structured_data")
                    save_structured_data_to_json(html_content, structured_data_filename)

                if args.metadata_to_json:
                    metadata_filename = sanitize_filename(args.url, "metadata")
                    save_metadata_to_json(html_content, metadata_filename)

                if args.extracted_links_to_json:
                    extracted_links_filename = sanitize_filename(args.url, "extracted_links")
                    save_extracted_links_to_json(html_content, extracted_links_filename)

                if args.media_files_to_json:
                    media_files_filename = sanitize_filename(args.url, "media_files")
                    save_media_files_to_json(html_content, media_files_filename)

                if args.emails_usernames_to_json:
                    emails_usernames_filename = sanitize_filename(args.url, "emails_usernames")
                    save_emails_usernames_to_json(html_content, emails_usernames_filename)

                if args.phonenumbers_to_json:
                    phonenumbers_filename = sanitize_filename(args.url, "phonenumbers")
                    save_phonenumbers_to_json(html_content, phonenumbers_filename)
