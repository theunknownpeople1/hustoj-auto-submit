from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os

username=str(input("please input usename:"))
password=str(input("please input password:"))
cid=str(input("please input cid:"))
num=int(input("please input number of problems:"))

driver=webdriver.Edge()
driver.get("http://***/loginpage.php")
time.sleep(0.1)
input_elements = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/form/div[1]/div[1]/div/input")
input_elements.send_keys(username)
input_elements = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/form/div[1]/div[2]/div/input")
input_elements.send_keys(password)
driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/form/div[1]/button").click()
time.sleep(0.1)
#login

for i in range (num):
    position="http://***/problem.php?cid="+cid+"&pid="+str(i)
    driver.get(position)
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div[1]/div/div/a[2]").click()
    time.sleep(0.1)
    #locate problem 

    elements=driver.find_element(By.XPATH, "/html/body/div[2]/div/center/form/pre")
    ActionChains(driver).double_click(elements).perform()
    #activate cursors
    filename=str(i+1)+'.c'
    filedir = os.path.join(os.path.dirname(__file__), filename)
    with open(filedir, 'r') as file:
        text=file.read()    

 
    # 使用JavaScript设置input的值


    input_elements = driver.find_element(By.XPATH, "/html/body/div[2]/div/center/form/pre/textarea")
    driver.execute_script("""
        var editor = ace.edit("source");  // 替换为实际的 ACE 编辑器 ID 或容器的 class 名称
        editor.setOptions({
            enableAutoClosingBrackets: false,    // 禁用自动闭合括号
            enableAutoClosingQuotes: false,      // 禁用自动闭合引号
            enableBasicAutocompletion: false,    // 禁用基本补全
            enableLiveAutocompletion: false,     // 禁用实时补全
            enableSnippets: false,               // 禁用代码片段补全
            enableAutoIndent: false,             // 禁用回车时自动缩进
            autoClearEmptyLines: false,          // 禁用回车时自动清除空行
            wrap: false,                         // 禁用自动换行
            showPrintMargin: false,              // 禁用打印边距显示
            behavioursEnabled: false,            // 禁用所有行为（包括回车补全）
            useWorker: false                     // 禁用 Web Worker
        });

        // 禁用回车键的默认行为
        editor.on("keydown", function(e) {
            if (e.keyCode === 13) { // 回车键
                e.preventDefault();  // 禁止默认回车行为
            }
        });

        // 移除代码补全和插入命令
        editor.commands.removeCommand("insertSnippet");  // 禁用代码片段插入
        editor.commands.removeCommand("complete");       // 禁用代码补全
    """)
    input_elements.send_keys(text)
    driver.find_element(By.XPATH, "/html/body/div[2]/div/center/form/span[3]/button").click()
    time.sleep(10)