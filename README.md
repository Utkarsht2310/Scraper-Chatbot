# 🌐 Web Scraping and Chatbot Integration App

This project is a **Flask-based web application** that allows users to scrape website content, store it in a **PostgreSQL** database, and interact with the scraped data through an intelligent **chatbot interface**.  

It combines web scraping, structured data storage, and natural language querying for a complete web intelligence workflow.

---

## 🚀 Features

- 🕸️ **Web Scraping:** Extracts text, links, images, videos, and document URLs from any webpage.
- 💾 **Database Integration:** Stores structured scraped data into a PostgreSQL database.
- 💬 **Chatbot Interface:** Interact with the stored data using simple queries.
- 📂 **Selective Scraping:** Choose which content categories to scrape (Text, Links, Images, Videos, Documents).
- 🧠 **Data Normalization:** Prepares and chunks scraped data for easier processing and LLM parsing.
- 🧩 **Modular Architecture:** Core scraping logic is abstracted in the `doc.py` module.

---

## 🧰 Tech Stack

| Component | Technology |
|------------|-------------|
| **Backend Framework** | Flask |
| **Database** | PostgreSQL |
| **Language** | Python 3.8+ |
| **Libraries** | requests, BeautifulSoup, psycopg2, Flask, JSON, etc. |

---

## ⚙️ Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/web-scraper-chatbot.git
cd web-scraper-chatbot
```

### 2️⃣ Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate      # For Linux/Mac
venv\Scripts\activate         # For Windows
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

Example `requirements.txt`:
```
Flask
psycopg2
requests
beautifulsoup4
```
*(Include other libraries you use inside `doc.py` if needed.)*

---

## 🗄️ Database Setup

1. Open PostgreSQL and create a new database:
   ```sql
   CREATE DATABASE your_database_name;
   ```

2. Create a table for storing scraped data:
   ```sql
   CREATE TABLE scraped_data (
       url TEXT PRIMARY KEY,
       content JSONB
   );
   ```

3. Update the following credentials in your Python file:
   ```python
   hostname = 'localhost'
   database = 'your_database_name'
   username = 'postgres'
   pwd = 'your_password'
   port_id = 5432
   ```

---

## 🧩 App Structure

```
web-scraper-chatbot/
│
├── app.py                 # Main Flask application
├── doc.py                 # Contains scraping, downloading, and chatbot logic
├── templates/             # HTML templates (home, categories, chatbot pages)
│   ├── home.html
│   ├── categories.html
│   └── chatbot.html
├── static/                # (Optional) CSS/JS files for frontend
├── requirements.txt       # Dependencies
└── README.md              # Project documentation
```

---

## 🖥️ Usage

1. Run the Flask app:
   ```bash
   python app.py
   ```

2. Open your browser and go to:
   ```
   http://127.0.0.1:5000/
   ```

3. Enter a **base URL** to scrape.

4. Select which **categories** you want to extract:
   - ✅ Text
   - ✅ Links
   - ✅ Images
   - ✅ Videos
   - ✅ Documents

5. Once scraped, interact with the **chatbot** to query the data.  
   Example:
   > “Summarize the content from this website.”  
   > “List all image links.”  
   > “Find PDF documents available on the page.”

---

## 💾 Data Normalization for LLMs

The app automatically:
- Splits long text into smaller chunks.
- Limits the number of stored images/videos (to improve performance).
- Converts all content into a clean JSON format before saving to PostgreSQL.

---

## 💬 Chatbot Querying

The chatbot retrieves stored data from the database and processes user queries using the `handle_chatbot_query()` function in `doc.py`.  
It allows natural language search and summarization on top of the scraped dataset.

---

## 🔒 Error Handling

- Handles invalid URLs or pages without accessible content.
- Updates existing entries in the database if the same URL is scraped again.
- Displays user-friendly messages if no data is found.

---

## 🔮 Future Enhancements

- 🤖 Integrate GPT-based LLM for advanced query responses.
- 📊 Add a dashboard for analyzing scraped data.
- 🌐 Support batch scraping of multiple URLs.
- 💬 Enhance chatbot context understanding.

---

## 🤝 Contributing

Pull requests are welcome!  
If you'd like to improve scraping speed, add AI enhancements, or improve the chatbot, open an issue or submit a PR.

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Utkarsh Tripathi**  
🔗 [GitHub](https://github.com/<your-username>) • ✉️ [Email](mailto:<your-email>)
