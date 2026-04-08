# 🎓 SREC AI Chatbot for College Enquires

An intelligent, AI-powered campus assistant designed for **Santhiram Engineering College (SREC), Nandyal**. This project automates college enquiries using a custom NLP pipeline, providing instant answers about admissions, fees, placements, and more.

---

## 🚀 Key Features
- **AI-Driven Responses**: Uses a TF-IDF coupled with a Naive Bayes classifier for intent recognition.
- **Real-Time Interaction**: Smooth, modern chat interface with typing indicators and quick-action chips.
- **Comprehensive Knowledge**: Pre-trained on college-specific data (Admissions, Fees, Courses, Hostels, etc.).
- **Responsive Design**: Premium "glassmorphism" UI that works beautifully across mobile and desktop.
- **Offline Capability**: Backend runs on Flask with a local SQLite database for training data.

---

## 🛠️ Technology Stack
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript (ES6+)
- **Backend**: Python 3.x, Flask
- **NLP Engine**: Scikit-Learn (TF-IDF Vectorizer + Multinomial Naive Bayes)
- **Database**: SQLite3
- **Tools**: Joblib (for model persistence)

---

## 📂 Project Structure
```text
.
├── app.py                # Main Flask backend & API routes
├── database.py           # DB initialization & enquiry logic
├── nlp_engine.py         # NLP training & prediction pipeline
├── CLOADcollege_chatbot.html # Main landing page & chat UI
├── CLOADcollege_chatbot.css  # Premium styling & animations
├── CLOADcollege_chatbot.js   # Frontend logic & API integration
├── requirements.txt      # Project dependencies
├── chatbot_model.pkl     # Pre-trained ML model
└── college.db            # Training data & response database
```

---

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/praveenyallala2-ops/ai-chatbot-for-college-enquires.git
   cd ai-chatbot-for-college-enquires
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Train the model (Optional):**
   The project comes with a pre-trained model, but you can re-train it by running the backend.
   ```python
   python nlp_engine.py
   ```

4. **Run the Application:**
   ```bash
   python app.py
   ```
   *The server will start at `http://127.0.0.1:5000`.*

---

## 🧪 Usage
- Open `CLOADcollege_chatbot.html` in your browser or visit `http://127.0.0.1:5000`.
- Click the **"Chat with Assistant"** button.
- Ask questions like:
  - *"What is the fee for B.Tech?"*
  - *"Tell me about placements."*
  - *"How can I get admission?"*

---

## 📄 License
This project is developed as part of the B.Tech Minor Project at SREC Nandyal.
