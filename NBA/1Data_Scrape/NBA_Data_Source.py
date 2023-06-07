""" Grabs individual player stats from Basketball-Reference.com """
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from io import StringIO
import csv


driver = webdriver.Chrome()



def Player_totals_Scrape():
    """
    Gets individual player stats from years 2013 to 2022 
    Output: {string} of comma-separated values
    """
    data = ''

    for year in range(2013, 2022):

        url = 'https://www.basketball-reference.com/leagues/NBA_{}_per_game.html'.format(year)

        driver.get(url)
        action = ActionChains(driver)

        WebDriverWait(driver, 5)
        share_button_xpath = '//*[@id="per_game_stats_sh"]/div/ul/li[1]/div/ul/li[3]/button'
        total_button_xpath = '//*[@id="subnav"]/li[4]' # header hides view if I don't do this
        share_button = driver.find_element("xpath", share_button_xpath)
        print(share_button)


        total_button = driver.find_element(By.XPATH,total_button_xpath)
        driver.execute_script("arguments[0].scrollIntoView();", total_button)
        action.move_to_element(share_button)

        WebDriverWait(driver, 5)
        export_button_xpath = '//button[text()[contains(., "Get table as CSV (for Excel)")]]'
        export_button = driver.find_element(By.XPATH,export_button_xpath)
        action.move_to_element(export_button)
        driver.execute_script("arguments[0].click();", export_button)

        data += driver.find_element(By.ID, "csv_per_game_stats").text + "\n"
    return data





def Team_Scrape():
    """
    Gets team total stats from years 2013 to 2022 
    Output: {string} of comma-separated values
    """
    data = ''
    
    for year in range(2013,2023):

        url = 'https://www.basketball-reference.com/leagues/NBA_{}.html#all_misc_stats'.format(year)
        driver.get(url)

        action = ActionChains(driver)

        # header_elem_xpath = '//*[@id="inner_nav"]/ul/li[8]/div/ul[6]/li[3]/a]]'
        # header_elem = driver.find_element(By.XPATH, header_elem_xpath)
        # driver.execute_script("arguments[0].scrollIntoView();", header_elem)

        # # share_button_xpath = '//*[@id="totals-team_sh"]/div/ul/li[2]/div/ul/li[3]/button'
        # # share_button = driver.find_element(By.XPATH, share_button_xpath)
        # # driver.execute_script("arguments[0].scrollIntoView();", share_button)
        # # action.move_to_element(share_button)

        export_button_xpath = '//*[@id="per_game-team_sh"]/div/ul/li[2]/div/ul/li[3]/button'
        export_button = driver.find_element(By.XPATH,export_button_xpath)
        action.move_to_element(export_button)
        driver.execute_script("arguments[0].click();", export_button)

        data += driver.find_element(By.ID, "csv_per_game-team").text + "\n"
    return data

def writeData():
    """ Takes string from ScrapeDate() function and adds it to a csv file 
    Input: {string} from ScrapeData() 
    Output: CSV file 
    """
    f = StringIO(Player_totals_Scrape())
    reader = csv.reader(f, delimiter=',')
    
    with open('2013-2023-NBA_API-TeamStat-raw', 'w') as file:
        for row in reader:
            writer = csv.writer(file)
            writer.writerow(row)

    f = StringIO(Team_Scrape())
    reader = csv.reader(f, delimiter=',')

    with open('2013-2023-Regular-TeamTotals-raw.csv', 'w') as file:
        for row in reader:
            writer = csv.writer(file)
            writer.writerow(row)

writeData()

