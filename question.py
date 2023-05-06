from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import shutil
from math import ceil
from unicodedata import east_asian_width
import argparse


width_dict = {
  'F': 2,   # Fullwidth
  'H': 1,   # Halfwidth
  'W': 2,   # Wide
  'Na': 1,  # Narrow
  'A': 2,   # Ambiguous
  'N': 1    # Neutral
}


def count_chat_elms(driver):
    query = "//main//div[contains(text(), 'Model:')]/.."
    chat_elms = driver.find_element(By.XPATH, query)
    return len(chat_elms.find_elements(By.XPATH, "*"))


def send_question(driver, question):
    query = '//textarea[@tabindex="0"]'
    textarea = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, query)))
    # print(textarea)
    textarea.send_keys(question)
    send = textarea.find_element(By.XPATH, "../button")
    # print(send)
    send.click()


def clear_line(n=1):
    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'
    for i in range(n):
        print(LINE_UP, end=LINE_CLEAR)


def count_lines(s):
    terminal_size = shutil.get_terminal_size()
    n = terminal_size[0]
    counts = [ceil(sum([width_dict[east_asian_width(y)] for y in x], 1) / n)
              for x in s.split("\n")]
    return sum(counts)


def main(question):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=options)

    original_window = driver.current_window_handle
    # print(driver.window_handles[0])

    for w in driver.window_handles:
        driver.switch_to.window(w)
        if driver.current_url.startswith('https://chat.openai.com/'):
            print(driver.title)
            print(driver.current_url)
            break

    start_n = count_chat_elms(driver)

    send_question(driver, question)

    end_n = start_n
    while True:
        end_n = count_chat_elms(driver)
        if end_n > start_n:
            break

    # time.sleep(10)

    n_skip = 0
    answer_prev = None
    while True:
        query = "//main//div[contains(text(), 'Model:')]/../*[last()-1]"
        answer = driver.find_element(By.XPATH, query)
        answer_text = answer.text
        if answer_text == answer_prev:
            if n_skip > 4: break
            n_skip += 1
            continue
        if answer_prev:
            n = count_lines(answer_prev)
            clear_line(n)
        print(answer_text)
        answer_prev = answer_text
        sys.stdout.flush()
        time.sleep(1)

    # print(answer_prev)

    driver.switch_to.window(original_window)


if __name__ == '__main__':
    question = ""
    for line in sys.stdin:
        question += line.rstrip()

    main(question)
