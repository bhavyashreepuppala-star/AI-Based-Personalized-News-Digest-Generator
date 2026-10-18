# 📰 AI-Based Personalized News Digest Generator

An AI-powered news digest application that fetches news based on users' interests, removes duplicate and previously viewed articles, and generates concise AI summaries.

## ✨ Features

- **Personalized News:** Select multiple interests, including Artificial Intelligence, Technology, Science, Business, Sports, and Education.
- **News Fetching:** Retrieve news articles using the NewsAPI.
- **Duplicate Detection:** Identify and remove similar headlines.
- **Persistent News History:** Store previously seen articles using SQLite to reduce repetition across sessions.
- **AI-Powered Summarization:** Generate concise news summaries using Google's Gemini API.
- **Category Filtering:** Browse articles by selected interests.
- **Article Links:** Open the original news articles.
- **Interactive Dashboard:** View article counts and digest statistics through Streamlit.

## 🛠️ Tech Stack

- **Language:** Python
- **Frontend:** Streamlit
- **News API:** NewsAPI
- **AI Model:** Google Gemini
- **Database:** SQLite
- **Libraries:** Requests, python-dotenv, google-genai

## 📁 Project Structure

```text
AI-News-Digest-Generator/
├── app.py
├── news_fetcher.py
├── deduplicator.py
├── summarizer.py
├── history.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

The `.env` file contains API keys and should never be uploaded to GitHub.

## ⚙️ Setup and Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd AI-News-Digest-Generator
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file in the project root:

```env
NEWS_API_KEY=your_newsapi_key
GEMINI_API_KEY=your_gemini_api_key
```

Replace the placeholder values with your own API keys. Never publish your actual keys.

- NewsAPI: https://newsapi.org/
- Google AI Studio: https://aistudio.google.com/

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🚀 How It Works

1. The user selects one or more news categories.
2. The application fetches articles for each selected category.
3. Similar headlines are detected and duplicates are removed.
4. Previously seen articles are filtered using the SQLite history database.
5. New articles are displayed in a personalized digest.
6. Users can request concise AI summaries for individual articles.

## 🔐 API Keys and Privacy

API keys are loaded from environment variables using `python-dotenv`. Keep the `.env` file private and exclude it from version control.

## 🔮 Future Improvements

- User accounts and individual reading histories
- Scheduled daily email digests
- Additional news sources
- Improved semantic duplicate detection
- Saved articles and personalized recommendations

## 👩‍💻 Author

Developed as an AI-based personalized news digest project.
