# 🚀 InsightSQL AI  
### AI-Powered Business Intelligence Platform  

🔗 **Live Project:** https://insightsql-ai.onrender.com  

---

## 📌 Problem Statement

In real-world businesses, decision-makers often struggle to extract insights from databases because:

- SQL knowledge is required to query data
- Business teams depend on technical teams for reports
- Data insights are slow and inefficient
- Ad-hoc analysis takes time and effort

This creates a gap between **business questions** and **technical execution**.

---

## 💡 Solution

**InsightSQL AI** bridges that gap.

It allows users to:

- Ask business questions in plain English
- Automatically generate optimized SQL queries
- Execute queries securely
- Get business-friendly explanations
- View structured results instantly

This transforms raw database access into an **AI-powered analytics assistant**.

---

## 🧠 What the System Does

1. User asks a business question  
   Example:  
   > What is the average order value?

2. AI converts natural language → SQL

3. SQL is executed against PostgreSQL

4. Results are returned with:
   - Generated SQL
   - Business explanation
   - Execution time
   - Result table
   - Export to CSV option

---

## 🏗️ Tech Stack

### Backend
- FastAPI
- Python 3.11
- SQLAlchemy
- PostgreSQL
- Uvicorn

### AI Layer
- Google Gemini API
- Mock LLM mode for testing

### Frontend
- HTML
- CSS
- Vanilla JavaScript

### DevOps & Deployment
- Docker
- Render
- Git & GitHub

---

## 📂 Project Structure

```
insightsql-ai/
│
├── app/
│   ├── main.py
│   ├── routes.py
│   └── __init__.py
│
├── core/
│   ├── db_connection.py
│   ├── executor.py
│   └── config.py
│
├── llm/
│   ├── gemini_config.py
│   ├── explanation.py
│   └── __init__.py
│
├── database/
├── utils/
│
├── static/
│   └── images/
│       └── bg1.jpg
│
├── templates/
│   └── index.html
│
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 🛠️ Development Summary

### 1️⃣ Backend Development
- Built FastAPI server
- Created API routes
- Connected PostgreSQL using SQLAlchemy

### 2️⃣ AI Integration
- Integrated Google Gemini API
- Designed structured business prompts
- Added mock mode for testing

### 3️⃣ Query Execution Layer
- Secure SQL execution
- Result formatting
- Execution time tracking
- Error handling

### 4️⃣ Frontend UI
- KPI dashboard
- Query input box
- Generated SQL display
- Business explanation
- Results table
- CSV export
- Query history

### 5️⃣ Dockerization
- Created Dockerfile
- Containerized FastAPI app
- Exposed port 8000

### 6️⃣ Deployment
- Connected GitHub to Render
- Configured environment variables
- Linked PostgreSQL database
- Deployed production app

Live URL:
👉 https://insightsql-ai.onrender.com

---

## 📊 Example

User Question:
```
What is the average order value?
```

Generated SQL:
```sql
SELECT AVG(total_amount) AS avg_order_value FROM orders;
```

---

## 🌍 Business Impact

- Enables non-technical users to access database insights
- Reduces dependency on data teams
- Speeds up decision-making
- Improves data-driven culture

---

## 🔐 Environment Variables

```
DATABASE_URL=
GOOGLE_API_KEY=
GEMINI_API_KEY=
USE_MOCK_LLM=
```

---

## 🐳 Docker Usage

Build:
```
docker build -t insightsql-ai .
```

Run:
```
docker run -p 8000:8000 insightsql-ai
```

---

## 🧪 Local Development

Activate environment:
```
venv\Scripts\activate
```

Run server:
```
uvicorn app.main:app --reload
```

Open:
```
http://127.0.0.1:8000
```

---

## 🚀 Future Improvements

- Role-based authentication
- Data visualizations (charts)
- Multi-database support
- Query caching
- SaaS version
- AI anomaly detection
- Saved dashboards & reports

---

## 👨‍💻 Author

Developed by Shaheensha  
AI & Backend Enthusiast  

---

# ⭐ Project Status: LIVE & PRODUCTION READY

🔗 https://insightsql-ai.onrender.com