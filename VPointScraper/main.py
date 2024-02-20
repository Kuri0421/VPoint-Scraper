import sys
import re
import csv
import argparse
from pprint import pprint
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


def main():
    print("========================================")
    print("============ VPoint Scraper ============")
    print("========================================")
    # コマンドライン引数のパーサーを作成
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start-date', help='(必須)YYYYMM形式の開始日付')
    parser.add_argument('-e', '--end-date', help='(必須)YYYYMM形式の終了日付')

    # コマンドライン引数を解析
    args = parser.parse_args()

    # 引数の値を取得
    start_date = args.start_date
    end_date = args.end_date

    # 引数の値をチェック
    if start_date is None or end_date is None:
        print("開始日付と終了日付を指定してください。")
        print("(ex) -s 202301 -e 202312")
        sys.exit(1)
    elif not start_date.isdigit() or not end_date.isdigit():
        print("日付は数字で入力してください。")
        print("(ex) 202301")
        sys.exit(1)
    elif len(start_date) != 6 or len(end_date) != 6:
        print("無効な日付形式です。YYYYDD形式を使用してください。")
        print("(ex) 202301")
        sys.exit(1)
    
    # 年月を取得
    start_year = start_date[:4]
    start_month = start_date[4:]
    end_year = end_date[:4]
    end_month = end_date[4:]

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")

    # CSVファイルの作成
    output_file = f"./{timestamp}.csv"
    header = ["日付", "ポイント", "概要", "獲得サイト", "詳細"]
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
    
    # WebDriverの設定
    options = webdriver.ChromeOptions()
    options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument('--disable-features=Translate')
    options.add_argument('--disable-gpu')
    options.add_argument('--incognito')
    options.add_argument('--test-type=gpu')
    options.add_argument('--disable-background-networking') 

    # WebDriverの起動
    driver = webdriver.Chrome(options=options)
    
    driver.get("https://www.smbcgroup-point.jp/redirect/top_page.html")
    driver.implicitly_wait(60)
    
    # ログインページへ遷移
    transition_vpass_login_page = driver.find_element(By.XPATH,"/html/body/main/div/div[2]/div[1]/a/span")
    transition_vpass_login_page.click()
    
    #ポイント履歴ページへ遷移
    try:
        click_vpass_login = driver.find_element(By.XPATH,"//*[@id=\"HistoryInquiry\"]/span")
        click_vpass_login.click()
    except:
        print("========================================")
        print("")
        print("規定時間内にログインがされませんでした")
        driver.quit()
        sys.exit(1)
        
    print("=========  ポイント履歴取得中  =========")
    #検索条件のウィンドウを開く
    click_vpoint_pointhistory_Rrefine_search = driver.find_element(By.XPATH,"//*[@id=\"tri_FNGP06Form\"]/fieldset/dl[1]/dt/a/span")
    click_vpoint_pointhistory_Rrefine_search.click()
    
    driver.implicitly_wait(5)
    #検索範囲を指定
    #YYYY
    try:
        select_vpoint_pointhistory_start_year = driver.find_element(By.XPATH,"//*[@id=\"scKknKshYmYear\"]")
        Select(select_vpoint_pointhistory_start_year).select_by_value(start_year)
        #MM
        select_vpoint_pointhistory_start_month = driver.find_element(By.XPATH,"//*[@id=\"scKknKshYmMoth\"]")
        Select(select_vpoint_pointhistory_start_month).select_by_value(start_month)
    
        #YYYY
        select_vpoint_pointhistory_end_year = driver.find_element(By.XPATH,"//*[@id=\"scKknShryYmYear\"]")
        Select(select_vpoint_pointhistory_end_year).select_by_value(end_year)
    
        #MM
        select_vpoint_pointhistory_end_month = driver.find_element(By.XPATH,"//*[@id=\"scKknShryYmMoth\"]")
        Select(select_vpoint_pointhistory_end_month).select_by_value(end_month)
    except:
        print("========================================")
        print("")
        print("指定した日付が存在しないか、無効な日付形式です。")
        print("開始年月：", start_year + start_month)
        print("終了年月：", end_year + end_month)
        
        driver.quit()
        sys.exit(1)

    #検索ボタンを押す
    click_vpoint_pointhistory_search = driver.find_element(By.XPATH,"//*[@id=\"tri_FNGP06Form\"]/fieldset/dl[1]/dd/button")
    click_vpoint_pointhistory_search.click()
    
    # ポイント履歴を取得
    extraction_page_number = driver.find_element(By.XPATH,"//*[@id=\"tri_FNGP06Form\"]/fieldset/div[2]/div[1]")
    
    # 現在のページ数と最大ページ数を取得
    match = re.match(r"(\d+)/(\d+)ページ", extraction_page_number.text)
    if match:
        current_page = int(match.group(1))
        max_page = int(match.group(2))
        
    extraction = []
    # ページ数分繰り返す
    while current_page <= max_page:
        extraction_vpoint_date = driver.find_elements(By.CLASS_NAME,"fSize13")
        extraction_vpoint_point = driver.find_elements(By.CLASS_NAME,"pointBoxItemInner")
        extraction_vpoint_oveveiw = driver.find_elements(By.CLASS_NAME,"pointBoxRight")
        
        for i in range(len(extraction_vpoint_date)):
            
            extraction_vpoint_oveveiw_re = re.split(r'\n', extraction_vpoint_oveveiw[i].text)

            extraction.append([extraction_vpoint_date[i].text,extraction_vpoint_point[i].text])
            extraction[-1] += extraction_vpoint_oveveiw_re
            
        click_vpoint_pointhistory_next_page = driver.find_element(By.XPATH,"//*[@id=\"tri_FNGP06Form\"]/fieldset/div[2]/div[2]/ul/li[3]/a")
        click_vpoint_pointhistory_next_page.click()
        current_page += 1
        
    # CSVファイルに書き込む
    print("============  ファイル出力中  ===========")
    with open(output_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        for data in extraction:
            writer.writerow(data)
    driver.quit()
    print("===============  完了  ===============")

if __name__ == "__main__":
    main()