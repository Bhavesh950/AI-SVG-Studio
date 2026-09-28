<p align="center">
  <img src="AI SVG Studio banner.png" alt="AI SVG Studio banner" width="100%">
</p>


# 🎨 AI SVG Studio

> An AI-powered design studio that transforms natural-language prompts into professional, scalable SVG banners and infographics.

**AI SVG Studio** combines **Google Gemini**, **Python**, **Streamlit**, and a reusable SVG template engine to generate visually structured SVG designs from simple design briefs.

🌐 **Live Demo:**  
https://ai-svg-studio-mq2tbhebhug3z7aaqfj5b4.streamlit.app/

💻 **GitHub Repository:**  
https://github.com/Bhavesh950/AI-SVG-Studio

---

## 🚀 Overview

AI SVG Studio allows users to describe a banner or infographic using natural language.

For example:

> Create a modern professional infographic about the future of Generative AI with 5 key applications.

The application uses **Google Gemini** to understand the design brief and generate a structured design specification containing elements such as:

- Content
- Headings
- Supporting text
- Layout requirements
- Visual style
- Color direction
- Design structure

The generated specification is then processed by a **Python-based reusable SVG template engine** to produce the final scalable SVG design.

---

## 🧠 How It Works

```text
Natural Language Design Prompt
            ↓
      Google Gemini
            ↓
Structured Design Specification
            ↓
Python SVG Template Engine
            ↓
Reusable SVG Template
            ↓
      Final SVG Design
            ↓
Live Preview + Download
```

### AI + Programmatic Rendering

Gemini is used for the **AI/design specification layer**.

The final SVG rendering is handled by the application's **Python-based reusable SVG templates**.

This approach keeps the design generation structured, reusable, and controllable.

---

## ✨ Key Features

### 🤖 AI Design Generation

- Natural-language design prompts
- Google Gemini integration
- AI-generated content and design specifications
- Structured design generation workflow

### 🎨 SVG Design Generation

- Multiple reusable SVG templates
- Multiple layouts
- Multiple visual styles
- Multiple color themes
- Scalable vector-based output
- Clean SVG structure

### ⚡ Generation Modes

#### Single SVG

Generate one customized SVG design from a natural-language prompt.

#### Batch SVG

Generate multiple SVG designs using reusable templates and different design configurations.

### 🖥️ Interactive UI

- Chat-based design workflow
- Design settings panel
- Category selection
- Design type selection
- Visual style selection
- Template selection
- Color theme selection
- Live SVG preview
- Full-screen SVG preview
- SVG download
- Batch download
- JSON design specification
- SVG source code viewer

### 💬 Chat Workflow

The application supports multiple chats so users can work on different design ideas separately.

Each chat maintains its own generated designs and conversation history during the session.

---

## 🎯 Design Options

### Categories

- Technology
- Business
- Education
- Healthcare
- Finance
- Marketing
- Cybersecurity
- E-Commerce
- Sustainability
- Productivity

### Design Types

- Feature Highlights
- Step-by-Step
- Statistics
- Comparison
- Quote / Highlight
- Infographic

### Visual Styles

- Modern
- Professional
- Minimal
- Futuristic

### Templates

The application uses reusable SVG templates to create different visual structures and layouts.

### Color Themes

Multiple predefined color themes can be selected to create visually different designs.

---

## 📦 Example Workflow

### Step 1 — Enter a Prompt

```text
Create a modern professional infographic about
Generative AI with 5 key applications.
```

### Step 2 — Configure Design

Select:

```text
Category      → Technology
Design Type   → Feature Highlights
Visual Style  → Modern
Template      → Feature
Color Theme   → Ocean Blue
```

### Step 3 — Generate

Google Gemini generates the structured design specification.

### Step 4 — Render

The Python SVG engine converts the specification into a reusable SVG layout.

### Step 5 — Preview & Download

The generated SVG can be previewed and downloaded directly from the application.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application and SVG generation logic |
| Streamlit | Interactive web interface |
| Google Gemini | AI-powered design specification generation |
| LangChain | Gemini integration |
| SVG | Scalable vector output |
| GitHub | Version control and source hosting |

---

## 📁 Project Structure

```text
AI-SVG-Studio/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── .streamlit/
    └── secrets.toml
```

### Main Files

**`app.py`**

Contains the Streamlit application, Gemini integration, SVG generation logic, templates, chat workflow, preview, and download functionality.

**`requirements.txt`**

Contains the Python dependencies required to run the application.

**`README.md`**

Project documentation and setup instructions.

**`.gitignore`**

Prevents sensitive files and local development files from being committed.

**`.streamlit/secrets.toml`**

Stores the Gemini API key locally.

> `secrets.toml` should never be committed to GitHub.

---

# 🖥️ Manual Desktop Setup

If you want to run AI SVG Studio locally on your computer instead of using the live demo, follow these steps.

## 1. Download the Project

Open the GitHub repository:

https://github.com/Bhavesh950/AI-SVG-Studio

Click:

```text
Code → Download ZIP
```

Extract the downloaded ZIP file.

---

## 2. Open the Project in VS Code

Open the extracted:

```text
AI-SVG-Studio
```

folder in VS Code.

The project should contain:

```text
AI-SVG-Studio/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 3. Open the Terminal

In VS Code:

```text
Terminal → New Terminal
```

Make sure the terminal is opened inside the project folder.

---

## 4. Create a Virtual Environment

Run:

```bash
python -m venv venv
```

---

## 5. Activate the Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

If PowerShell blocks virtual-environment activation, you can still install and run using the virtual environment's Python directly:

```bash
venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

## 6. Install Dependencies

Run:

```bash
pip install -r requirements.txt
```

---

## 7. Configure Google Gemini API Key

Create the following folder inside the project:

```text
.streamlit
```

Inside that folder create:

```text
secrets.toml
```

The structure should look like:

```text
AI-SVG-Studio/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── .streamlit/
    └── secrets.toml
```

Add your Gemini API key:

```toml
GOOGLE_API_KEY = "YOUR_API_KEY"
```

Replace:

```text
YOUR_API_KEY
```

with your own Google Gemini API key.

### 🔐 Important

Never share your API key publicly.

Never commit:

```text
.streamlit/secrets.toml
```

to GitHub.

---

## 8. Run the Application

Run:

```bash
streamlit run app.py
```

The application should open automatically in your browser.

If it does not open automatically, visit:

```text
http://localhost:8501
```

---

# 🌐 Live Deployment

The application is deployed using Streamlit.

### Live Application

https://ai-svg-studio-mq2tbhebhug3z7aaqfj5b4.streamlit.app/

The deployed application uses Streamlit Secrets for the Gemini API key.

The API key is not stored in the public GitHub repository.

---

# 🔐 Security

Sensitive credentials are excluded from the repository using `.gitignore`.

The project ignores:

```text
__pycache__/
*.pyc
.env
.streamlit/secrets.toml
.venv/
venv/
```

The Gemini API key should always be stored through local or deployment secrets.

---

# 💡 Use Cases

AI SVG Studio can be used to generate visual content such as:

- LinkedIn graphics
- Technology infographics
- Educational content
- Business announcements
- Marketing banners
- Product feature highlights
- Statistics graphics
- Step-by-step explainers
- Comparison graphics
- Social media visual content
- Professional presentation graphics

---

# 🎥 Demo

The project includes a demonstration of the complete workflow:

```text
Prompt
  ↓
AI Design Specification
  ↓
SVG Generation
  ↓
Live Preview
  ↓
Download
```

---

# 📌 Project Highlights

This project demonstrates practical integration of:

- Generative AI
- Prompt-based design generation
- Structured AI outputs
- Google Gemini
- Python programming
- Programmatic SVG generation
- Reusable template architecture
- Streamlit application development
- Batch design generation
- Interactive UI development
- GitHub version control
- Cloud deployment

---

# 🔄 Future Improvements

Possible future enhancements include:

- Additional SVG templates
- More advanced layout generation
- Custom font selection
- User-uploaded brand assets
- Persistent user accounts
- Saved design history
- Advanced SVG validation
- More customization controls
- Additional AI model support

---

# 👨‍💻 Author

## Bhavesh Mulchandani

GitHub:  
https://github.com/Bhavesh950

---

## 🔗 Project Links

🌐 **Live Demo:**  
https://ai-svg-studio-mq2tbhebhug3z7aaqfj5b4.streamlit.app/

💻 **GitHub:**  
https://github.com/Bhavesh950/AI-SVG-Studio

---

⭐ If you find this project interesting, feel free to explore the repository and try the live demo.
