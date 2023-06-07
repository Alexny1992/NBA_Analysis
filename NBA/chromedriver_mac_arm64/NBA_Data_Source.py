from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('http://seleniumhq.org/')
# action = ActionChains(driver)

# web = webdriver.Chrome(executable_path="chromedriver")
# web.get("https://www.basketball-reference.com/leagues/NBA_2000_totals.html")