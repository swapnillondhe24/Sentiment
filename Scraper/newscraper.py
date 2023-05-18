from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import csv

def scrape_amazon():
    # Set up Selenium webdriver
    service = Service("./chromedriver_mac64/chromedriver")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode
    driver = webdriver.Chrome(service=service, options=options)
    
    url = "https://www.amazon.com/"  # Update the URL according to your requirement
    driver.get(url)

    items = driver.find_elements(By.CSS_SELECTOR, "div.a-section div.review div.aok-relative")
    print("Number of items found:", len(items))

    with open("data.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Content", "Date", "Variant", "Images", "Verified", "Author", "Rating", "Product", "URL"])
        for item in items:
            title = item.find_element(By.CSS_SELECTOR, "h2").text.strip()
            content = item.find_element(By.CSS_SELECTOR, "p").text.strip()
            date = item.find_element(By.CSS_SELECTOR, "span.date").text.strip()
            variant = item.find_element(By.CSS_SELECTOR, "span.variant").text.strip()
            images = item.find_elements(By.CSS_SELECTOR, "img")
            image_urls = [image.get_attribute("src") for image in images]
            verified = item.find_element(By.CSS_SELECTOR, "span.verified").text.strip()
            author = item.find_element(By.CSS_SELECTOR, "span.author").text.strip()
            rating = item.find_element(By.CSS_SELECTOR, "span.rating").text.strip()
            product = item.find_element(By.CSS_SELECTOR, "span.product").text.strip()
            url = item.find_element(By.TAG_NAME, "a").get_attribute("href")

            writer.writerow([title, content, date, variant, image_urls, verified, author, rating, product, url])

    print("Scraping from Amazon completed.")

    driver.quit()

scrape_amazon()
