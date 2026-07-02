# 🎙️ Voice-Based Concept Understanding Analyser

An AI-powered application that evaluates a student's conceptual understanding from voice explanations. The system converts speech to text, compares it with a reference concept using Sentence-BERT, analyzes speech quality, and generates a detailed PDF performance report.

---

## 📌 Features

- 🎤 Speech-to-Text using OpenAI Whisper
- 🧠 Semantic Similarity Analysis using Sentence-BERT
- 📊 Interactive Performance Dashboard
- 📈 Similarity History Visualization
- 🔊 Audio Feature Analysis
- 💬 Filler Word Detection
- 📄 Automatic PDF Report Generation
- 🗄️ SQLite Database for Report Storage
- 🏆 Top Performing Students
- 📚 Topic-wise Performance Analysis

---

## 🛠️ Technologies Used

- Python
- Streamlit
- OpenAI Whisper
- Sentence-BERT
- SQLite
- Plotly
- ReportLab
- Librosa
- Pandas

---

## 📂 Project Structure

```
Voice-Based Concept Understanding Analyser/
│
├── app.py
├── requirements.txt
├── README.md
│
├── audio/
│   ├── audio_features.py
│   ├── filler_detection.py
│   └── waveform.py
│
├── data/
│   └── topics.py
│
├── database/
│   ├── database.py
│   └── vbcua.db
│
├── models/
│   ├── whisper_model.py
│   ├── semantic_model.py
│   └── scoring.py
│
├── reports/
│   └── pdf_report.py
│
├── reports_output/
│
└── uploads/
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone <repository-url>
cd Voice-Based-Concept-Understanding-Analyser
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The application will be available at:

```
http://localhost:8501
```

---

## 📖 Workflow

1. Enter student details.
2. Select a topic.
3. Upload a voice explanation.
4. Convert speech to text.
5. Compare explanation using Sentence-BERT.
6. Analyze audio quality.
7. Generate similarity score.
8. Save results to the database.
9. Generate and download a PDF report.

---

## 📊 Dashboard

The dashboard provides:

- Total Reports
- Average Similarity
- Best Similarity
- Average Duration
- Similarity History
- Topic-wise Performance
- Top Performing Students
- Previous Reports

---

## 📄 Generated Report

Each PDF report includes:

- Student Information
- Selected Topic
- Speech Transcript
- Similarity Score
- Understanding Level
- Audio Statistics
- AI Feedback
- Report Generation Details

---

## 🚀 Future Enhancements

- User Authentication
- Cloud Database Integration
- Multi-language Support
- Real-time Voice Recording
- AI Performance Recommendations
- Online Deployment

---


## 👥 Project

Developed as part of an AI Internship Project.

---

## 📜 License

This project is intended for educational and academic purposes only.