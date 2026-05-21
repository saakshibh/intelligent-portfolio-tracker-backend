# 🚀 Intelligent Portfolio Tracker & Sentiment Analysis Engine

A full-stack, distributed AI-powered financial tracking application. This system allows users to securely track assets, fetch real-time market data, analyze global news sentiment using NLP, and view predictive stock price trends using a deep learning LSTM model.

## 🌐 Live Demo
* **Frontend Application:** [Live Link via Vercel](https://intelligent-portfolio-tracker-front.vercel.app/)
* **Backend API Terminal:** [Live Link via Render](https://intelligent-portfolio-tracker-backend.onrender.com)

---

## 🏗️ System Architecture & Data Flow

The platform relies on a completely decoupled microservices architecture designed to isolate client-side rendering from heavy machine learning computation:

1. **User Request:** The user securely authenticates via Supabase Auth and submits an asset ticker (e.g., `INFY.NS`, `BTC-USD`) on the Next.js frontend dashboard.
2. **AI Engine Trigger:** The frontend dispatches an asynchronous `POST` request across origins to the FastAPI microservice hosted on Render.
3. **Multi-Modal Processing:** * The backend pulls real-time financial metrics and historical trends using `yfinance`.
   * It parallel-scrapes the latest global financial headlines and executes NLP sentiment scoring via NLTK's VADER lexicon.
   * Data arrays are preprocessed using `scikit-learn`'s `MinMaxScaler` and passed into a custom TensorFlow LSTM neural network to evaluate trend vectors.
4. **Cloud Database Sync:** The structured intelligence payload is written directly to the Supabase PostgreSQL database instances.
5. **Real-Time Client Render:** The UI listens for state updates, fetches from the synchronized database, and fluidly projects the trends using interactive Recharts components.

---

## 🛠️ Tech Stack

### Frontend (Client Portal)
* **Framework:** Next.js (App Router) & TypeScript
* **Styling:** Tailwind CSS (Dark Mode Optimization)
* **Data Visualization:** Recharts (Interactive Line Graphs & Trend Vectors)
* **Hosting Platform:** Vercel

### Backend (AI & Microservice Layer)
* **Framework:** FastAPI (Python 3.11 Optimization)
* **Deep Learning Model:** TensorFlow (LSTM Neural Network for sequential data tracking)
* **Data Scrapers & Processors:** Pandas, NumPy, Scipy, Scikit-learn, yfinance
* **Natural Language Processing:** NLTK (VADER Sentiment Engine)
* **Hosting Platform:** Render (Linux Virtual Environment)

### Database & Security (Infrastructure)
* **Database:** Cloud PostgreSQL via Supabase
* **Authentication:** Supabase Auth JWT Route Protection

---

## 🚀 Local Installation & Setup

### 1. Prerequisites
* Node.js (v18+ recommended)
* Python 3.11

### 2. Backend Setup
Clone the repository and step into the backend workspace:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt

3. Frontend Setup
Step into the frontend directory:

Bash
cd ../frontend
npm install
npm run dev
