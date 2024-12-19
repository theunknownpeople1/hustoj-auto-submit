from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import schedule
import pyperclip
#注意安装以上所有库selenium&schedule&pyperclip&datetime，time和os自带

username=str(input("please input usename:"))
password=str(input("please input password:"))
cid=str(input("please input cid:"))
num=int(input("please input number of problems:"))
#输入登录用户名密码比赛号和题目数量
driver=webdriver.Edge()
#默认使用edge打开，可以改chrome，后面记得跟着改

def auto_submit(username,password,cid,num):
    options = webdriver.EdgeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Edge(options=options)
    #禁用自动关闭浏览器
    driver.get("http://***/loginpage.php")
    time.sleep(0.1)
    #***处设置hustoj地址，后面所有地址都是

    input_elements = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/form/div[1]/div[1]/div/input")
    input_elements.send_keys(username)
    input_elements = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/form/div[1]/div[2]/div/input")
    input_elements.send_keys(password)
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div/form/div[1]/button").click()
    time.sleep(0.1)
    #登录
    
    filename='1.c'
    filedir = os.path.join(os.path.dirname(__file__), filename)
    with open(filedir, 'r') as file:
        text=file.read()   
    pyperclip.copy(text) 
    #预读第一题文件
    
    driver.get("http://***/contest.php")
    j=1
    while True:
        tab_element=driver.find_element(By.XPATH, "/html/body/div[2]/div/div/table/tbody/tr["+str(j)+"]/td[1]")
        if cid in tab_element.text:
            break
        else: j+=1
    while True:
        driver.get("http://***/contest.php")
        listen_locate=driver.find_element(By.XPATH, "/html/body/div[2]/div/div/table/tbody/tr["+str(j)+"]/td[3]/span[1]")
        if "运行中" in listen_locate.text:
            break
        else:
            time.sleep(0.5)       
    #监听页面变化

    for i in range (num):
        position="http://***/problem.php?cid="+cid+"&pid="+str(i)
        driver.get(position)
        driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div[1]/div/div/a[2]").click()
        #打开题目页

        elements=driver.find_element(By.XPATH, "/html/body/div[2]/div/center/form/pre")
        ActionChains(driver).double_click(elements).perform()
        #激活输入光标

        #所有文件以“数字.c”命名，并且存放在此文件同目录下
        if i!=0:
            filename=str(i+1)+'.c'
            filedir = os.path.join(os.path.dirname(__file__), filename)
            with open(filedir, 'r') as file:
                text=file.read()   
            pyperclip.copy(text)  
            #复制代码

        text_element=driver.find_element(By.XPATH, "/html/body/div[2]/div/center/form/pre/textarea")
        text_element.send_keys(Keys.CONTROL + 'v')
        #粘贴代码
        
        if i!=0:
            elapsed_time = time.time() - start_time
            remaining_time = 10 - elapsed_time
            if remaining_time > 0:
                time.sleep(remaining_time)
        #从上次点击提交开始等待10s交下一题，防止被ban

        driver.find_element(By.XPATH, "/html/body/div[2]/div/center/form/span[3]/button").click()
        #点击提交

        start_time = time.time()
        #计录上一次提交的时间

schedule.every().thursday.at("11:59:50").do(auto_submit,username,password,cid,num)
#设置计划启动浏览器的时间，提前10s左右，防止刷新次数过多暴毙

while True:
    schedule.run_pending()
    time.sleep(1)
    #从开始运行后轮询直至启动时间