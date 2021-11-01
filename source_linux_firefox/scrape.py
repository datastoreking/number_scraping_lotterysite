from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import csv

# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--ignore-ssl-errors')
# options.add_argument("--ignore-certificate-errors-spki-list")
# driver = webdriver.Chrome("./chromedriver",chrome_options=options)# get chromeDriver
driver = webdriver.Firefox(executable_path=r'geckodriver')
driver.set_window_size(960, 640)
total_numbers_group = []
left_numbers_group = []
driver.get("https://www.fdj.fr/jeux-de-tirage/amigo/resultats/")# set url
try:
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "swiper-wrapper")))
    print('waiting done')
    blocks = driver.find_elements(By.CLASS_NAME, 'result-amigo_page')
    for block_index in range(len(blocks)):
        row_contents = blocks[block_index].find_elements(By.CLASS_NAME,'result-amigo_content');
        for row_index in range(len(row_contents)):
            data_content = row_contents[row_index].find_elements(By.CLASS_NAME, 'result-amigo_item')
            left_content = data_content[1].find_elements(By.CLASS_NAME, 'numbers-item')
            line_left_number_list = []
            total_numbers_list = []
            for left_content_index in range(len(left_content)):
                left_numbers = left_content[left_content_index].find_element(By.CLASS_NAME, 'numbers-item_num').get_attribute('innerHTML');
                line_left_number_list.append(int(left_numbers))
                total_numbers_list.append(int(left_numbers))
            right_content = data_content[2].find_elements(By.CLASS_NAME, 'numbers-item')
            for right_content_index in range(len(right_content)):
                right_numbers = right_content[right_content_index].find_element(By.CLASS_NAME, 'numbers-item_num').get_attribute('innerHTML');
                total_numbers_list.append(int(right_numbers))
            total_numbers_list.sort()
            line_left_number_list.sort()
            print(total_numbers_list)
            left_numbers_group.insert(0, line_left_number_list)
            total_numbers_group.insert(0, total_numbers_list)
    with open('amigo.csv', 'w') as total:
        write = csv.writer(total)
        write.writerows(total_numbers_group)
    with open('amigo_BLUE.csv', 'w') as blue:
        write = csv.writer(blue)
        write.writerows(left_numbers_group)

except TimeoutException:
    print('network error')
driver.close()
