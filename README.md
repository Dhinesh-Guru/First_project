# Weather App

A simple Python-based Weather App that fetches real-time weather data using an API and displays it in a user-friendly GUI built with **PyQt5**.

## 📌 Features
- Fetch real-time weather information for any city.
- User-friendly PyQt5 interface.
- Displays temperature, humidity, and weather conditions.
- Error handling for invalid city names or network issues.

## 🛠️ Technologies Used
- **Python**
- **PyQt5** (GUI)
- **Requests** (API calls)
- **OpenWeatherMap API** 

## 📂 Project Structure
```
Weather_App/
│
├── main.py # Main application file
├── icon.jpg # App icon
├── requirements.txt # Python dependencies
└── README.md # Project documentation
```

## 🛠️ Setup & Installation

1. Clone the repository

```bash
git clone https://github.com/your-username/Weather_App.git
cd Weather_App
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Set up your API key

*Copy .env.example to .env:*

```bash
cp .env.example .env
```

Open .env and replace your_api_key_here with your OpenWeatherMap API key.

4. Run the application

```bash
python main.py
```

📄 .env.example content:

```env
API_KEY=your_api_key_here
```

## 📦 Checking if Required Modules Are Installed

Before running the app, you can check whether all required modules are installed:

```bash
python -m pip show PyQt5 requests python-dotenv
```

If any are missing, install them using:

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install PyQt5 requests python-dotenv
```