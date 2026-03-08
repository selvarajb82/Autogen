from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage, MultiModalMessage
from autogen_core import Image
from dotenv import load_dotenv
import os
import asyncio
import requests
from datetime import datetime
from openai import OpenAI
from PIL import Image as PILImage
from io import BytesIO
import time

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
weather_api_key = os.getenv('WEATHER_API_KEY')

model_client = OpenAIChatCompletionClient(model='gpt-4o-mini', api_key=api_key)
openai_client = OpenAI(api_key=api_key)


def generate_weather_image(city: str, weather_desc: str, weather_main: str) -> PILImage.Image:
    """
    Generate a weather image using DALL-E 3
    """
    try:
        print(f"   🎨 Generating DALL-E image for {city}...")
        start = time.time()
        
        prompt = f"Realistic weather scene showing {weather_main} {weather_desc} weather in {city}, professional photography, high quality, detailed"
        
        response = openai_client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        
        gen_time = time.time() - start
        print(f"   ✅ Image generated in {gen_time:.1f} seconds")
        
        # Download image
        img_response = requests.get(response.data[0].url, timeout=15)
        return PILImage.open(BytesIO(img_response.content))
        
    except Exception as e:
        print(f"   ❌ Error generating image: {e}")
        return None


async def get_weather_for_city(city: str, save_image: bool = False) -> MultiModalMessage:
    """
    Get weather for a single city and return multimodal message
    """
    try:
        print(f"\n{'='*50}")
        print(f"📍 Processing: {city}")
        print(f"{'='*50}")
        
        # Weather API call
        print("🌤️ Fetching weather data...")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
        
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if response.status_code != 200:
            return MultiModalMessage(
                content=[f"❌ Error for {city}: {data.get('message', 'Unknown error')}"], 
                source="weather_tool"
            )
        
        # Extract weather information
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        weather_desc = data['weather'][0]['description']
        weather_main = data['weather'][0]['main']
        country = data['sys']['country']
        
        print(f"✅ Weather data received: {weather_main}, {temperature}°C")
        
        # Create detailed text response
        text_response = (f"🌤️ **Weather in {city}, {country}**\n\n"
                       f"**Current Conditions:**\n"
                       f"• {weather_main} - {weather_desc}\n\n"
                       f"**Temperature:**\n"
                       f"• Current: {temperature}°C\n"
                       f"• Feels like: {feels_like}°C\n\n"
                       f"**Additional Details:**\n"
                       f"• Humidity: {humidity}%\n"
                       f"• Pressure: {pressure} hPa\n\n"
                       f"**Sun Times:**\n"
                       f"• Sunrise: {datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')}\n"
                       f"• Sunset: {datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')}")
        
        # Generate image
        image = generate_weather_image(city, weather_desc, weather_main)
        
        if image:
            print(f"✅ Image ready for {city}")
            
            # Save if requested
            if save_image:
                filename = f"weather_{city}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                image.save(filename)
                print(f"💾 Image saved as: {filename}")
            
            return MultiModalMessage(
                content=[text_response, Image.from_pil(image)], 
                source="weather_tool"
            )
        else:
            return MultiModalMessage(
                content=[text_response + "\n\n⚠️ Image generation failed"], 
                source="weather_tool"
            )
            
    except requests.exceptions.Timeout:
        return MultiModalMessage(content=[f"❌ Timeout fetching weather for {city}"], source="weather_tool")
    except Exception as e:
        return MultiModalMessage(content=[f"❌ Error for {city}: {str(e)}"], source="weather_tool")


def parse_city_input(user_input: str) -> list:
    """
    Parse user input to extract city names
    Examples:
    - "Chennai" -> ["Chennai"]
    - "Chennai, London, Tokyo" -> ["Chennai", "London", "Tokyo"]
    - "Chennai and London" -> ["Chennai", "London"]
    """
    # Remove common words and split
    user_input = user_input.replace(" and ", ",").replace("&", ",")
    
    # Split by commas and clean up
    cities = [city.strip() for city in user_input.split(",")]
    
    # Filter out empty strings
    cities = [city for city in cities if city]
    
    return cities


async def main():
    print("\n" + "=" * 70)
    print("🌤️  MULTIMODAL WEATHER ASSISTANT")
    print("=" * 70)
    print("\n📝 You can enter cities in various formats:")
    print("   • Single city: Chennai")
    print("   • Multiple cities: Chennai, London, Tokyo")
    print("   • With 'and': Chennai and London")
    print("\n💾 Images can be saved automatically")
    print("-" * 70)
    
    while True:
        print("\n" + "=" * 50)
        city_input = input("🌍 Enter city/cities (or 'exit' to quit): ").strip()
        
        if city_input.lower() in ['exit', 'quit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if not city_input:
            print("❌ Please enter at least one city")
            continue
        
        # Parse cities
        cities = parse_city_input(city_input)
        print(f"\n📋 Processing {len(cities)} city/cities: {', '.join(cities)}")
        
        # Ask about saving images
        save_choice = input("\n💾 Save images to disk? (y/n): ").strip().lower()
        save_images = save_choice == 'y'
        
        # Process each city
        for i, city in enumerate(cities, 1):
            print(f"\n📌 City {i}/{len(cities)}")
            
            # Get weather with image
            result = await get_weather_for_city(city, save_images)
            
            # Display results
            print("\n📤 RESULT:")
            for idx, item in enumerate(result.content):
                if isinstance(item, str):
                    print(f"\n{item}")
                else:
                    print(f"\n🖼️ [Image attached]")
            
            # Small delay between cities (but not after the last one)
            if i < len(cities):
                print(f"\n⏸️  Waiting 2 seconds before next city...")
                await asyncio.sleep(2)
        
        print("\n" + "=" * 50)
        print("✅ All requested cities processed!")
        print("=" * 50)


async def quick_test():
    """
    Quick test function for debugging
    """
    print("\n🔧 Quick Test Mode")
    print("Enter cities to test quickly (no save prompts)")
    
    city_input = input("Cities: ").strip()
    cities = parse_city_input(city_input)
    
    for city in cities:
        result = await get_weather_for_city(city, save_image=False)
        for item in result.content:
            if isinstance(item, str):
                print(f"\n{item[:200]}...")
            else:
                print(f"\n🖼️ [Image]")


if __name__ == "__main__":
    print("Select mode:")
    print("1. Interactive mode (with save options)")
    print("2. Quick test mode")
    
    choice = input("Choice (1/2): ").strip()
    
    if choice == "2":
        asyncio.run(quick_test())
    else:
        asyncio.run(main())