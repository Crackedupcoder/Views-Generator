from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from asgiref.sync import sync_to_async, async_to_sync
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import asyncio
import random
import os

def generate_views(search_url, number):
    print('Started generating views')

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless Chrome
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Generate a random user agent
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value, OperatingSystem.MAC.value]
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

    for i in range(number):
        user_agent = user_agent_rotator.get_random_user_agent()
        chrome_options.add_argument(f"user-agent={user_agent}")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        try:
            print(f'Navigating to {search_url} for view {i + 1}')
            driver.get(search_url)
            asyncio.sleep(random.uniform(0.5, 2))  # Simulate reading time
            
            print(f'Scrolling page for view {i + 1}')
            body = driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.PAGE_DOWN)
            asyncio.sleep(1)  # Simulate more reading time

            print(f'View {i + 1} generated successfully')
        except Exception as e:
            print(f'Error generating view {i + 1}: {e}')
        finally:
            driver.quit()

    print('Done generating views')

@sync_to_async
def run_generate_views(search_url, number):
    generate_views(search_url, number)

@csrf_exempt
def handle_generate_views(request):
    if request.method == 'POST':
        try:
            data = request.POST
            url = data.get('url')
            number = int(data.get('number'))

            # Run the sync function in a sync context
            async_to_sync(run_generate_views)(url, number)

            return JsonResponse({'message': 'Views generated successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'message': f'Error generating views: {e}'}, status=500)
    return JsonResponse({'message': 'Invalid request method'}, status=405)

def index(request):
    try:
        return render(request, 'index.html')
    except Exception as e:
        return HttpResponse(f'<h1>Internal Server Error</h1><p>{e}</p>', status=500)
