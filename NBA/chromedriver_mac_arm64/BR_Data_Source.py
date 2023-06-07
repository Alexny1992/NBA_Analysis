""" Grabs individual player stats from Basketball-Reference.com """
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from io import StringIO
from selenium.webdriver.common.by import By
import csv


driver = webdriver.Chrome()
action = ActionChains(driver)

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--incognito')
# chrome_options.add_argument('--headless')

def playerTotalsScrape():
    """
    Gets individual player stats from years 2013 to 2023 

    Output: {string} of comma-separated values
    """ 
    data = ''
    years = [year for year in range(2013, 2024) if year != 2020]
    for i, year in enumerate(years):

        url = 'https://www.basketball-reference.com/leagues/NBA_{}_totals.html'.format(year)
        driver.get(url)

        # WebDriverWait(driver, 5)
        # share_button_xpath = '//*[@id="inner_nav"]/ul/li[6]/div/ul/li[2]/a'
        # # total_button_xpath = '//div[@class="current"]' # header hides view if I don't do this
        # share_button = driver.find_element(by=By.XPATH, value=share_button_xpath)
        # # total_button = driver.find_element(by=By.XPATH, value=total_button)
        # driver.execute_script("arguments[0].scrollIntoView();", share_button)
        # action.move_to_element(share_button)

        WebDriverWait(driver, 5)
        export_button_xpath = '//*[@id="totals_stats_sh"]/div/ul/li[1]/div/ul/li[3]/button'
        export_button = driver.find_element(by=By.XPATH, value=export_button_xpath)
        action.move_to_element(export_button)
        driver.execute_script("arguments[0].click();", export_button)

        data += driver.find_element(By.ID, 'csv_totals_stats').text + "\n"
    return data


# def teamScrape():
#     """
#     Gets team total stats from years 2013 to 2023 
#     Output: {string} of comma-separated values
#     """
#     data = ''
    
#     for year in range(2013, 2024):

#         url = 'https://www.basketball-reference.com/leagues/NBA_{}.html#all_misc_stats'.format(year)

#         driver.get(url)

#         WebDriverWait(driver, 5)

#         header_elem_xpath = '//*[@id="inner_nav"]/ul/li[1]/a/u'
#         header_elem = driver.find_element(by=By.XPATH, value=header_elem_xpath)
#         driver.execute_script("arguments[0].scrollIntoView();", header_elem)

#         share_button_xpath = '//*[@id="advanced-team_sh"]/div/ul/li[2]/span'
#         share_button = driver.find_element(by=By.XPATH, value=share_button_xpath)
#         driver.execute_script("arguments[0].scrollIntoView();", share_button)
#         action.move_to_element(share_button)

#         WebDriverWait(driver, 5)

#         export_button_xpath = '//*[@id="advanced-team_sh"]/div/ul/li[2]/div/ul/li[3]/button'
#         export_button = driver.find_element(by=By.XPATH, value=export_button_xpath)
#         action.move_to_element(export_button)
#         driver.execute_script("arguments[0].click();", export_button)

#         data += driver.find_element(By.ID,'csv_advanced-team').text + "\n"

#     return data

def writeData():
#     """ Takes string from ScrapeDate() function and adds it to a csv file 
#     Input: {string} from ScrapeData() 
#     Output: CSV file 
#     """
    f = StringIO(playerTotalsScrape())
    reader = csv.reader(f, delimiter=',')
    
    with open('fixed.csv', 'w') as file:
        for row in reader:
            writer = csv.writer(file)
            writer.writerow(row)

    # f = StringIO(teamScrape())
    # reader = csv.reader(f, delimiter=',')

    # with open('2013-2023-Regular-TeamTotals-raw.csv', 'w') as file:
    #     for row in reader:
    #         writer = csv.writer(file)
    #         writer.writerow(row)

writeData()