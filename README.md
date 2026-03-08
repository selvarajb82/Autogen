# 🌤️ Multimodal Weather Assistant

An AI-powered weather assistant that fetches real-time weather data and generates stunning weather scene images using **DALL-E 3**, orchestrated through **Microsoft AutoGen's** multi-agent framework.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![AutoGen](https://img.shields.io/badge/AutoGen-Multi--Agent-green)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-purple?logo=openai)
![DALL-E 3](https://img.shields.io/badge/DALL--E%203-Image%20Gen-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🎯 What It Does

Type in any city name and the assistant will:

1. **Fetch real-time weather data** from OpenWeatherMap API
2. **Generate a photorealistic weather scene** of that city using DALL-E 3
3. **Return a multimodal response** combining text weather report + AI-generated image

> If it's raining in London, you don't just read about it — you *see* it.

---

## 🚀 Demo

https://github.com/user-attachments/assets/your-demo-video-id

*Replace the link above with your actual demo video after uploading it to GitHub.*

---

## ✨ Features

- **Multi-City Support** — Process multiple cities in a single request (`Chennai, London, Tokyo`)
- **Real-Time Weather Data** — Temperature, humidity, pressure, sunrise/sunset times
- **AI-Generated Weather Images** — DALL-E 3 creates realistic weather scenes for each city
- **Multimodal Responses** — Text + image combined using AutoGen's `MultiModalMessage`
- **Flexible Input Parsing** — Supports commas, "and", or single city inputs
- **Image Saving** — Optionally save generated images to disk
- **Async Architecture** — Handles multiple cities efficiently with Python's `asyncio`
- **Two Modes** — Interactive mode with save options or quick test mode for debugging

---

## 🏗️ Architecture

```
User Input (City Names)
        │
        ▼
┌───────────────────┐
│   Input Parser    │  ← Handles "Chennai, London and Tokyo"
└───────┬───────────┘
        │
        ▼
┌───────────────────┐     ┌─────────────────────┐
│  OpenWeatherMap   │────▶│  Weather Data        │
│  API              │     │  (Temp, Humidity,    │
└───────────────────┘     │   Pressure, etc.)    │
                          └──────────┬────────────┘
                                     │
                                     ▼
                          ┌─────────────────────┐
                          │  DALL-E 3 (OpenAI)  │
                          │  Image Generation    │
                          └──────────┬────────────┘
                                     │
                                     ▼
                          ┌─────────────────────┐
                          │  AutoGen Framework   │
                          │  MultiModalMessage   │
                          │  (Text + Image)      │
                          └─────────────────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Agent Framework | Microsoft AutoGen |
| Language Model | GPT-4o-mini |
| Image Generation | DALL-E 3 |
| Weather Data | OpenWeatherMap API |
| Language | Python 3.10+ |
| Async Runtime | asyncio |
| Image Processing | Pillow (PIL) |

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/multimodal-weather-assistant.git
cd multimodal-weather-assistant
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
WEATHER_API_KEY=your_openweathermap_api_key_here
```

---

## 🔑 Getting API Keys

### OpenAI API Key
1. Go to [platform.openai.com](https://platform.openai.com/)
2. Navigate to API Keys
3. Create a new secret key
4. Ensure you have access to GPT-4o-mini and DALL-E 3

### OpenWeatherMap API Key
1. Go to [openweathermap.org](https://openweathermap.org/api)
2. Sign up for a free account
3. Navigate to API Keys section
4. Copy your default key (or generate a new one)

---

## 📋 Requirements

```txt
autogen-agentchat
autogen-ext[openai]
autogen-core
openai
python-dotenv
requests
Pillow
```

Save the above as `requirements.txt`.

---

## 🚀 Usage

### Run the assistant

```bash
python weather_assistant.py
```

### Interactive Mode (Option 1)

```
🌍 Enter city/cities (or 'exit' to quit): Chennai, London, Tokyo

📋 Processing 3 city/cities: Chennai, London, Tokyo

💾 Save images to disk? (y/n): y

==================================================
📍 Processing: Chennai
==================================================
🌤️ Fetching weather data...
✅ Weather data received: Clear, 32°C
🎨 Generating DALL-E image for Chennai...
✅ Image generated in 8.2 seconds
💾 Image saved as: weather_Chennai_20250308_143022.png
```

### Quick Test Mode (Option 2)

Runs without save prompts — useful for debugging and quick lookups.

### Input Formats

```
Single city:     Chennai
Multiple cities: Chennai, London, Tokyo
Using 'and':     Chennai and London
Mixed:           Paris, Berlin and Rome
```

---

## 📁 Project Structure

```
multimodal-weather-assistant/
├── weather_assistant.py    # Main application
├── .env                    # API keys (not tracked)
├── .gitignore
├── requirements.txt
├── README.md
└── images/                 # Saved weather images (auto-created)
```

---

## 🖼️ Sample Output

| City | Weather | Generated Image |
|------|---------|----------------|
| Chennai | Clear, 32°C | *AI-generated clear sky scene* |
| London | Rainy, 12°C | *AI-generated rainy London scene* |
| Tokyo | Cloudy, 18°C | *AI-generated cloudy Tokyo scene* |

*Add your actual screenshots/images here after running the app.*

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Microsoft AutoGen](https://github.com/microsoft/autogen) — Multi-agent orchestration framework
- [OpenAI](https://openai.com/) — GPT-4o-mini and DALL-E 3
- [OpenWeatherMap](https://openweathermap.org/) — Real-time weather data API

---

## 📬 Connect

If you found this project interesting, let's connect! Feel free to reach out on [LinkedIn](https://linkedin.com/in/your-profile).

⭐ **Star this repo if you found it useful!**
