from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
from docx import Document
from PyPDF2 import PdfReader
import os
from ollamaparse import parse_with_ollama

# FILE HANDLING FUNCTIONS
def extract_docx_content(file_path):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_pdf_content(file_path):
    reader = PdfReader(file_path)
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

def download_file(url, file_path):
    response = requests.get(url)
    with open(file_path, "wb") as f:
        f.write(response.content)

# SCRAPING FUNCTIONS
def scrape_page_content(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto(url)
        content = page.content()

        soup = BeautifulSoup(content, "html.parser")
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        text_content = soup.get_text(separator="\n", strip=True)

        images = [urljoin(url, img['src']) for img in soup.find_all('img', src=True)]
        videos = [urljoin(url, video['src']) for video in soup.find_all('video', src=True)]
        links = [urljoin(url, link['href']) for link in soup.find_all('a', href=True)]

        file_links = {
            "pdf": [link for link in links if link.lower().endswith(".pdf")],
            "docx": [link for link in links if link.lower().endswith(".docx")],
            "doc": [link for link in links if link.lower().endswith(".doc")]
        }

        browser.close()
        return text_content, images, videos, links, file_links

def scrape_and_download_files(base_url, file_links):
    content = {}
    temp_dir = "temp_files"
    os.makedirs(temp_dir, exist_ok=True)

    for file_type, links in file_links.items():
        for link in links:
            file_name = os.path.basename(link)
            file_path = os.path.join(temp_dir, file_name)
            try:
                download_file(link, file_path)
                if file_type == "docx":
                    content[file_name] = extract_docx_content(file_path)
                elif file_type == "pdf":
                    content[file_name] = extract_pdf_content(file_path)
                elif file_type == "doc":
                    content[file_name] = extract_docx_content(file_path)  # For .doc, treat as .docx
            except Exception as e:
                print(f"Error processing file {file_name}: {e}")

    return content

# def scrape_links_and_content(links):
#     link_data = {}
#     for link in links:
#         print(f"Scraping linked page: {link}")
#         try:
#             page_text, _, _, _, _ = scrape_page_content(link)
#             link_data[link] = page_text
#         except Exception as e:
#             print(f"Failed to scrape link {link}: {e}")
#     # print(link_data)        
#     return link_data


def scrape_full_page(links):
    link_data = []
    for url in links:
        print(f"Scraping linked page: {url}")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            page.goto(url)
            content = page.content()
            # print("contenen hooooooooooooooooooooooooooooooo maiiiiiiiiiiii")
            # print (content)

            soup = BeautifulSoup(content, "html.parser")
            for script_or_style in soup(["script", "style"]):
                script_or_style.decompose()

            cleaned_content = soup.get_text(separator="\n", strip=True)
            # print("maiiiiiiiiiiiiiiinnnnnnnnnnnnnnn hooooooooooooooooooooooooooooooo")
            # print(cleaned_content)
            link_data.append(cleaned_content)
            # print(link_data)
            browser.close()
    
    return link_data
    




# def split_down_content(dom_content, max_length=6000):
#     return [dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)]

# CHATBOT QUERYING
# def handle_chatbot_query(dom_content, user_query):
#     # Split the content into smaller chunks if necessary
#     content_chunks = split_down_content(dom_content)
#     # Send chunks to Ollama (or other processing logic)
#     combined_content = " ".join(content_chunks)  

#     return parse_with_ollama(user_query, combined_content)

#changes in the function to handle the chatbot query

import textwrap

def split_down_content(dom_content, max_length=6000):
    return textwrap.wrap(dom_content, width=max_length)

def handle_chatbot_query(dom_content, user_query):
    # Extract only meaningful text
    text_content = extract_text_from_dom(dom_content)
    
    if not text_content.strip():
        return "No meaningful text found for processing."

    # Split text content into chunks
    content_chunks = split_down_content(text_content)
    
    # Send chunks to LLaMA 3.2
    return parse_with_ollama(content_chunks, user_query)

def extract_text_from_dom(dom_content):
    # Extract only text, ignoring images and empty fields
    return " ".join(dom_content.get("TextChunks", [])).strip()



# MAIN FUNCTIONALITY
def main():
    base_url = input("Enter the base URL to scrape: ")

    # Initial scraping of base URL to fetch categories
    print("Fetching categories from the webpage...")
    text_content, images, videos, links, file_links = scrape_page_content(base_url)

    # Display categories with counts
    categories = {
        "1": f"Text ({len(text_content.splitlines())})",
        "2": f"Links ({len(links)})",
        "3": f"Images ({len(images)})",
        "4": f"Videos ({len(videos)})",
        "5": f"Documents ({sum(len(v) for v in file_links.values())})"
    }

    print("\nAvailable categories on the page:")
    print(f"links are: - {links}, text: - {text_content}")
    for key, value in categories.items():
        print(f"{key}. {value}")

    # User selects categories to scrape
    selected_categories = input("\nEnter the numbers of categories to scrape (comma-separated): ").split(",")

    # Collect data based on user-selected categories
    final_data = {"Text": "", "Images": [], "Videos": [], "Links": {}, "Documents": {}}

    if "1" in selected_categories:
        final_data["Text"] = text_content

    if "2" in selected_categories:
        # If 'Links' is selected, scrape all linked pages and collect their content
        final_data["Links"] = scrape_full_page(links)

    if "3" in selected_categories:
        final_data["Images"] = images

    if "4" in selected_categories:
        final_data["Videos"] = videos

    if "5" in selected_categories:
        final_data["Documents"] = scrape_and_download_files(base_url, file_links)

    # User queries chatbot
    print("\nData scraped successfully. You can now query the chatbot.")
    while True:
        query = input("Ask a question (or type 'exit' to quit): ")
        if query.lower() == "exit":
            break
        response = handle_chatbot_query(final_data, query)  # Use the Text content for query
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    main()
