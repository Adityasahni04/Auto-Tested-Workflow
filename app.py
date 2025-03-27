from selenium import webdriver
from selenium.webdriver.common.by import By

# Set up WebDriver to connect to Selenium Grid
options = webdriver.ChromeOptions()
driver = webdriver.Remote(
    command_executor="http://localhost:4444/wd/hub",
    options=options
)

# Open a website
driver.get("https://www.google.com")

# Print page title
print("Page title is:", driver.title)

# Search for something
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Selenium WebDriver")
search_box.submit()

# Wait for results to load and print the new page title
driver.implicitly_wait(5)
print("New page title is:", driver.title)

# Close browser
driver.quit()
