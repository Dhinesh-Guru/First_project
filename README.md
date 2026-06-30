# Weather App

A beautiful, modern Python-based desktop Weather App featuring a **glassmorphism design** that fetches real-time weather data and displays it in a stunning graphical interface built with **PyQt5**.

---

## 📌 Features
- **Modern Glassmorphism UI**: Semi-translucent container layout with clean borders, rounded corners, and soft drop shadows.
- **Dynamic Pastel Gradients**: App background automatically shifts to match the weather condition (e.g., sunny, rainy, snowy, cloudy).
- **Expanded Weather Details**: Displays temperature, condition description, **Feels Like** temperature, **Humidity**, and **Wind Speed**.
- **Smooth Fade-in Animation**: Results fade in smoothly over 400ms using transition animations.
- **Premium Custom Icon**: Includes a modern 3D glassmorphic app icon.
- **Robust Error Handling**: Displays clean error states for network issues, incorrect API keys, or invalid city names.

---

## 🛠️ Technologies Used
- **Python**
- **PyQt5** (GUI & Animations)
- **Requests** (API fetching)
- **python-dotenv** (Environment configuration)
- **OpenWeatherMap API** 

---

## 📂 Project Structure
```
Weather_App/
│
├── main.py             # Main application file
├── icon.png            # Premium app icon (PNG with transparency)
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
└── README.md           # Project documentation
```

---

## 🛠️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Dhinesh-Guru/First_project.git
cd First_project
```

### 2. Install Dependencies
Make sure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 3. Configure Your API Key
Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```
*(On Windows PowerShell, use: `Copy-Item .env.example .env`)*

Open `.env` in a text editor and replace `your_api_key_here` with your OpenWeatherMap API key:
```env
OPENWEATHER_API_KEY=your_api_key_here
```

### 4. Run the Application
```bash
python main.py
```

---

## 📦 Troubleshooting Dependencies
Before running the app, you can verify if the required modules are correctly installed by running:
```bash
python -m pip show PyQt5 requests python-dotenv
```
If any are missing, re-run the pip install command:
```bash
pip install -r requirements.txt
```