from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
from utils.write_to_gspread import *
import threading
from pathlib import Path

options = Options()
# options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument('use-fake-ui-for-media-stream')
driver = webdriver.Chrome(executable_path=Path(__file__).parent / "browser/chromedriver1.exe", options=options)
# driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.maximize_window()
driver.set_page_load_timeout(3000)


def switch_to_window_by_handle_number(handle_number):
    return driver.switch_to.window(driver.window_handles[handle_number])


def open_url_new_tab(url):
    driver.execute_script(f"window.open('{url}','_blank')")
    switch_to_window_by_handle_number(-1)


def join_room():
    url = f'https://vchat.scholars-home.org/test_link_0'
    try:
        open_url_new_tab(url)
    except Exception as e:
        print(e)


def join_custom_room(url):
    try:
        open_url_new_tab(url)
    except:
        return


# gsheet_name = create_gsheet()


def one_room_one_join(room_num):
    url = f'https://vchat.scholars-home.org/test_link_{room_num}'
    room_number = int(url.split('/test_link_')[-1])
    gsheet_name = "MCR_Room_data"
    # try:
    room_number = room_number
    sheet_name = f'Room_{room_number}'
    create_worksheet(json_file, gsheet_name, sheet_name, 100, 10)
    # sleep(3)
    write_result_on_gspread(gsheet_name, sheet_name, 1, 1, 'Room_number', 1, 2, 'Number_of_participant', 1, 3, 'Timestamp')
    new_url = f"https://vchat.scholars-home.org//test_link_{room_number}"
    open_url_new_tab(new_url)
    for j in range(1, 50):
        join_custom_room(new_url)
        # sleep(1)
        write_result_on_gspread(gsheet_name, sheet_name, j + 1, 1, room_number, j + 1, 2, j, j + 1, 3, read_date_time_underscore_format1())
    # except Exception as e:
    #     print(e)
    # sleep(5)


threads = []
for i in range(5):
    t = threading.Thread(target=one_room_one_join, args=(i,))
    # t = threading.Thread(target=join_room)
    threads.append(t)
    sleep(3)
    t.start()
print("Done!")