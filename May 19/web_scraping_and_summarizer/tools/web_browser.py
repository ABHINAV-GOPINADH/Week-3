from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def fetch_content(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Use the locally installed ChromeDriver
    service = Service()  # No need to specify path since it's in PATH

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    content = driver.page_source
    driver.quit()

    return content
