# CareerCraft 🚀

**An AI-powered career guidance platform that recommends the right career path, analyzes your resume, and connects you to the best-matching job openings with direct apply links.**

---

## ✨ Features

- **Personalized Career Recommendations**: Enter your education, skills, and interests, and get career paths that actually fit your profile.
- **Resume Analysis**: Upload your resume (PDF) and CareerCraft parses it to extract your skills, experience, and gaps.
- **Smart Job Matching**: Openings are ranked based on how well they match your resume.
- **Direct Apply Links**: Apply to the best-fit openings straight from the app, no extra searching.

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Backend | Python |
| AI / ML | Python (scikit-learn, NLP) |
| Database | SQL (schema + seed data) |
| Resume Parsing | PDF parser utility |

## 📁 Project Structure

```
CareerCraft/
├── ai/                  # Recommendation & matching logic
├── backend/
│   └── utils/           # PDF parser, helpers, security
├── database/
│   ├── schema/          # Table definitions
│   └── seed/            # Careers & skills data
├── frontend/            # UI code
├── streamlit_app.py     # App entry point
├── requirements.txt
└── README.md
```

## ⚙️ Getting Started

**1. Clone the repo**
```bash
git clone https://github.com/bhanuduhoon77/CareerCraft.git
cd CareerCraft
```

**2. Create a virtual environment (recommended)**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the app**
```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`.

## 🔄 How It Works

1. User enters their profile details.
2. CareerCraft suggests suitable career paths.
3. User uploads a resume, which is parsed and analyzed.
4. The app matches the resume against available openings.
5. Best-fit jobs are shown with direct apply links.

## 🔮 Future Improvements

- Live job listings via job board APIs
- Skill-gap suggestions with course recommendations
- Resume score and ATS-friendliness feedback
- User accounts to save progress

## 🤝 Contributing

Contributions are welcome! Fork the repo, create a branch, and open a pull request.

## 👤 Author

**Bhanu**
B.Tech CSIT, KIET Group of Institutions
GitHub: [@bhanuduhoon77](https://github.com/bhanuduhoon77)

---

⭐ If you found this useful, consider giving the repo a star!