from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome import service as fs
import pyperclip
import subprocess

driver_path = 'chromedriver.exe'

options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_service = fs.Service(executable_path=driver_path)
driver = webdriver.Chrome(service=chrome_service, options=options)


f = open('score.txt', 'w')
f.close()

for k in range(0,1):
    driver.switch_to.new_window('tab')

    # 2.操作するページを開く
    driver.get('https://img.atcoder.jp/ahc018/6bada50282.html?lang=ja')

    # フォームへの削除と入力
    in_texts = driver.find_element(By.ID, "input")
    out_texts = driver.find_element(By.ID, "output")

    # フォームに入っている情報を削除
    in_texts.clear()
    out_texts.clear()

    print("now")
    cmd = "cargo run --release --bin tester python3 main.py < in/" + str(k).zfill(4) + ".txt"  + " > out.txt"
    runcmd = subprocess.call(cmd.split(),shell = True)

    f = open("in/" + str(k).zfill(4) + '.txt', 'r')
    in_ = f.read()

    pyperclip.copy(in_)

    in_texts.send_keys(Keys.CONTROL, "v")

    f.close()

    f = open('out.txt', 'r')
    out_ = f.read()

    pyperclip.copy(out_)

    out_texts.send_keys(Keys.CONTROL, "v")
    f.close()

# #!----------------------------------------------------------
    driver.switch_to.new_window('tab')

    driver.get('https://img.atcoder.jp/ahc018/6bada50282.html?lang=ja')

# フォームへの削除と入力
    in_texts = driver.find_element(By.ID, "input")
    out_texts = driver.find_element(By.ID, "output")

# フォームに入っている情報を削除
    in_texts.clear()
    out_texts.clear()
    
    print("past")
    cmd = "cargo run --release --bin tester python3 past.py < in/" + str(k).zfill(4) + ".txt"  + " > out.txt"
    runcmd = subprocess.call(cmd.split(),shell = True)

    f = open("in/" + str(k).zfill(4) + '.txt', 'r')
    in_ = f.read()

    pyperclip.copy(in_)

    in_texts.send_keys(Keys.CONTROL, "v")

    f.close()

    f = open('out.txt', 'r')
    out_ = f.read()

    pyperclip.copy(out_)

    out_texts.send_keys(Keys.CONTROL, "v")
    f.close()


f = open("score.txt","r")
r = list(map(int,f.read().split("\n")[:-1]))
f.close()
f = open("score.txt","a")
if sum(r) > 0:
    f.write("diff : +" + str(sum(r)))
else:
    f.write("diff : " + str(sum(r)))
f.close()