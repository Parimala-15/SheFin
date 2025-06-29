# 💸 SheFin: AI-Powered Financial Assistant for Women

**SheFin** is a smart, AI-powered, multilingual financial assistant built with **Streamlit**, designed especially for Indian women. It provides personalized financial guidance, budgeting tools, goal tracking, and Indian government scheme recommendations using modern AI technologies like  **Google Gemini**,

---

## 📌 Features

- 🤖 **AI-based financial chatbot** using OpenAI, Gemini & Claude
- 📊 **Goal planning**, savings tracking, and SIP/EMI calculators
- 🌐 **Multilingual UI** – English, Hindi, and Tamil
- 🏛️ **Government scheme matcher** (SSY, PMJDY, APY, Mudra, MSK)
- 🔐 Secure with `.env`, password hashing, and session protection
- 📈 Beautiful, interactive visualizations using **Plotly**
- ⚙️ Modular, maintainable architecture using **Python 3.11+**

---

## 🛠️ Tech Stack

| Layer       | Technology                          |
|------------|--------------------------------------|
| Frontend    | Streamlit (Custom UI, Gradient Themes) |
| Backend     | Python 3.11+                        |
| AI Services | Google Gemini |
| Database    | SQLite  |
| Visualization | Plotly, Pandas                     |
| Packaging   | `pyproject.toml` + `setuptools`     |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
1. git clone https://github.com/your-username/SheFin.git
cd SheFin

2. Set Up Virtual Environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install Using pyproject.toml
pip install .

For development use:
pip install -e .
No need for requirements.txt — dependencies are managed inside pyproject.toml.

4. Configure Environment Variables
Create a .env file:
GOOGLE_API_KEY=your-gemini-key

5. Run the App
python -m streamlit run app.py



