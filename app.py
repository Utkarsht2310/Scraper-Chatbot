import json


from flask import Flask, render_template, request, redirect, url_for, jsonify
from doc import (
    scrape_page_content,
   
    scrape_and_download_files,
    handle_chatbot_query,
    scrape_full_page,
)

app = Flask(__name__)

#Creating database
import psycopg2

hostname = 'localhost'
database = 'your_database_name'
username = 'postgres'
pwd = 'your_password'
port_id = 5432

def save_to_db():
    conn = psycopg2.connect(
        host=hostname,
        database=database,
        user=username,
        password=pwd,
        port=port_id
    )
    return conn


import json

def normalize_data_for_llm(content):
    """
    Normalize and chunk data for LLM parsing and database storage.
    """
    def chunk_text(text, max_length=500):
        """
        Split text into smaller chunks of `max_length`.
        """
        lines = text.split("\n")
        chunks = []
        current_chunk = ""
        
        for line in lines:
            if len(current_chunk) + len(line) < max_length:
                current_chunk += line + " "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = line
        if current_chunk:
            chunks.append(current_chunk.strip())
        return chunks

    # Process Text
    text_chunks = chunk_text(content.get("Text", ""), max_length=500)

    # Process Links
    links = content.get("Links", {})
    normalized_links = [{"url": url, "description": desc[:500]} for url, desc in links.items()]

    # Process Images, Videos, and Documents
    images = content.get("Images", [])[:50]  # Limit to 50 images
    videos = content.get("Videos", [])[:50]  # Limit to 50 videos
    documents = content.get("Documents", {})

    return {
        "TextChunks": text_chunks,
        "Links": normalized_links,
        "Images": images,
        "Videos": videos,
        "Documents": documents,
    }



def store_to_db(url, content):
    conn = save_to_db()
    cur = conn.cursor()

    # chunk_content = normalize_data_for_llm(content)

    content_json = json.dumps(content)
    insert_script = '''
        INSERT INTO scraped_data (url, content) 
        VALUES (%s, %s) 
        ON CONFLICT (url) 
        DO UPDATE SET content = EXCLUDED.content
    '''
    insert_values = (url, content_json)
    cur.execute(insert_script, insert_values)
    conn.commit()
    cur.close()
    conn.close()



# def store_to_db(url, content):
#     conn = save_to_db()
#     cur = conn.cursor()

#     chunk_content = normalize_data_for_llm(content)

#     content_json = json.dumps(chunk_content)
#     insert_script = 'INSERT INTO scraped_data (url, content) VALUES (%s, %s) ON CONFLICT (url) DO NOTHING'
#     insert_values = (url, content_json)
#     cur.execute(insert_script, insert_values)
#     conn.commit()
#     cur.close()
#     conn.close()


# Route: Home (Base URL form)
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        base_url = request.form["base_url"]
        return redirect(url_for("scrape_categories", base_url=base_url))
        
    return render_template("home.html")

# Route: Scrape Categories
@app.route("/scrape_categories")
def scrape_categories():
    base_url = request.args.get("base_url")
    print("Scraping Categories From given URL....")
    text_content, images, videos, links, file_links = scrape_page_content(base_url)

    # Store scraped content temporarily in session-like variables
    categories = {
        "1": {"name": f"Text ({len(text_content.splitlines())})", "data": text_content},
        "2": {"name": f"Links ({len(links)})", "data": links},
        "3": {"name": f"Images ({len(images)})", "data": images},
        "4": {"name": f"Videos ({len(videos)})", "data": videos},
        "5": {"name": f"Documents ({sum(len(v) for v in file_links.values())})", "data": file_links},
    }
    return render_template("categories.html", base_url=base_url, categories=categories)

# Route: Scrape Data
@app.route("/scrape_data", methods=["POST"])
def scrape_data():
    base_url = request.form["base_url"]
    selected_categories = request.form.getlist("categories")
    scraped_data = {"Text": "", "Images": [], "Videos": [], "Links": {}, "Documents": {}}

    # Process selected categories
    print("Scraping Selected Categories data....")
    if "1" in selected_categories:
        scraped_data["Text"] = scrape_page_content(base_url)[0]
    if "2" in selected_categories:
        links = scrape_page_content(base_url)[3]
        scraped_data["Links"] = scrape_full_page(links)
    if "3" in selected_categories:
        scraped_data["Images"] = scrape_page_content(base_url)[1]
    if "4" in selected_categories:
        scraped_data["Videos"] = scrape_page_content(base_url)[2]
    if "5" in selected_categories:
        file_links = scrape_page_content(base_url)[4]
        scraped_data["Documents"] = scrape_and_download_files(base_url, file_links)
    store_to_db(base_url,scraped_data)
    
    return redirect(f"/chatbot?base_url={base_url}")
    


# Route: Chatbot Interaction

@app.route("/chatbot", methods=["GET","POST"])
def chatbot():
    
    if request.method == "POST":
        user_query = request.form.get("query")
        base_url = request.args.get("base_url")
        print(user_query)
        conn = save_to_db()
        cur = conn.cursor()
        sql_query = "SELECT content FROM scraped_data WHERE url = %s;"
        cur.execute(sql_query, (base_url,))
        result = cur.fetchall()
        # print("yaha hu mei bahiiiiiiiiiiiii")
        # print(result)

        if result:
            # content = str(result)  
            content = json.loads(result[0][0]) if result else ""

            
            response = handle_chatbot_query(content, user_query)
            return render_template("chatbot.html", result=response)
        else:
            return render_template("chatbot.html", result="No data found for this URL.")
    
    return render_template("chatbot.html")




if __name__ == "__main__":
    app.run(debug=True)
