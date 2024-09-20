import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

def scrape_website(website):
    print("Launching Chrome browser...")
    
    # Set the path to your Chrome driver executable
    chrome_driver_path = "./chromedriver.exe"
    
    # Configure Chrome options
    options = webdriver.ChromeOptions()
    
    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
    
    try:
        # Navigate to the website
        driver.get(website)
        print("Page Loaded...")
        
        # Retrieve the HTML content of the page
        html = driver.page_source
        time.sleep(10)
        
        return html
    finally:
        # Ensure proper cleanup by quitting the browser
        driver.quit()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body

    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    # Remove scipt and style tags from the body content
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    
    # Get the text and seperate using a new line
    cleaned_content = soup.get_text(separator="\n")

    # If there is no text between a \n char and the next text, remove spaces
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [
        # Step by max_length for the len of dom content and get the content
        dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)
    ]
