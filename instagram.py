from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import requests, time, random, string, re, os, threading, math, pyautogui
from datetime import datetime

DOMAINS = [
    "hunght1890.com","hunght1890.site","simpace.edu.vn","mail.hunght1890.site",
    "mail.hunght1890.com","hoanganh.mx","lienvietlaw.com","toanthinhphatmedical.com",
    "inpos.com.vn","itemjunction.net","oggymail.net","bapnumail.com","duahaumail.com",
    "duahaumail.net","lakebamail.com","bapoggymail.com","bapoggymail.net",
    "denmarumail.com","kataranmail.com","kenturemail.com","sanpekomail.com",
    "santaramail.com","lamtruonglab.com","lamtruonglab.net","lamtruongstudio.com",
    "dongagroup.vn","donglucsport.com","quanlytinhgon.vn","satato.com.vn",
    "batdongsanvgp.com","chiasekhoahoc.vn","harborheights.education","ait-tesol.edu.vn"
]

def load_proxies():
    proxies = []
    if os.path.exists("proxies.txt"):
        with open("proxies.txt","r",encoding="utf-8") as f:
            for line in f:
                line=line.strip()
                if line and not line.startswith("#"):
                    proxies.append(line)
    return proxies

PROXIES = load_proxies()

def random_proxy():
    return random.choice(PROXIES) if PROXIES else None

def random_email(length=8):
    letters=string.ascii_lowercase+string.digits
    username=''.join(random.choice(letters) for _ in range(length))
    domain=random.choice(DOMAINS)
    return username,f"{username}@{domain}"

def get_email_code(email):
    api_url=f"https://hunght1890.com/{email}"
    for _ in range(30):
        try:
            res=requests.get(api_url,timeout=5)
            if res.status_code==200:
                mails=res.json()
                if mails:
                    subject=mails[0].get("subject","")
                    body=mails[0].get("body","")
                    match=re.search(r"\b\d{6}\b",body)
                    if match: return match.group(0)
                    match=re.search(r"\b\d{6}\b",subject)
                    if match: return match.group(0)
            time.sleep(2)
        except: time.sleep(2)
    return None

def random_password(length=12):
    chars=string.ascii_letters+string.digits+"!@#$%^&*()_+-="
    return ''.join(random.choice(chars) for _ in range(length))

def random_fullname_from_files():
    with open("ho.txt","r",encoding="utf-8") as f:
        ho_list=[line.strip() for line in f if line.strip()]
    with open("ten.txt","r",encoding="utf-8") as f:
        ten_list=[line.strip() for line in f if line.strip()]
    return f"{random.choice(ho_list)} {random.choice(ten_list)}"

def random_username(length=8):
    chars=string.ascii_lowercase+string.digits+"_"
    return ''.join(random.choice(chars) for _ in range(length))

def save_account(username,password,birthday,email):
    now=datetime.now().strftime("%H:%M:%S %d-%m-%Y")
    line=f"{username}|{password}|{birthday}|{email}|{now}\n"
    with open("acc.txt","a",encoding="utf-8") as f: f.write(line)
    print("Lưu:",username,email)

def create_account(index,cols,window_w,window_h):
    proxy = random_proxy()
    chrome_options=Options()
    chrome_options.add_argument("--lang=vi")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument("--log-level=3")

    if proxy:
        parts = proxy.replace(" ",":").split(":")
        if len(parts)==2:
            ip,port = parts
            chrome_options.add_argument(f"--proxy-server=http://{ip}:{port}")
        elif len(parts)==4:
            ip,port,user,pwd = parts
            manifest_json = """
            {
                "version": "1.0.0",
                "manifest_version": 2,
                "name": "Proxy",
                "permissions": ["proxy","tabs","unlimitedStorage","storage","<all_urls>","webRequest","webRequestBlocking"],
                "background": {"scripts": ["background.js"]}
            }
            """
            background_js = f"""
            chrome.proxy.settings.set({{value: {{mode: "fixed_servers", rules: {{singleProxy: {{scheme: "http", host: "{ip}", port: parseInt({port})}}}}}}, scope: "regular"}}, function() {{}});
            chrome.webRequest.onAuthRequired.addListener(
                function(details, callbackFn) {{
                    callbackFn({{authCredentials: {{username: "{user}", password: "{pwd}"}}}});
                }},
                {{urls: ["<all_urls>"]}},
                ['blocking']
            );
            """
            pluginfile = f"proxy_auth_plugin_{index}.zip"
            import zipfile
            with zipfile.ZipFile(pluginfile,'w') as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", background_js)
            chrome_options.add_extension(pluginfile)

    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)

    row=index//cols
    col=index%cols
    x=col*window_w
    y=row*window_h
    driver.set_window_rect(x,y,window_w,window_h)

    try:
        driver.get("https://www.instagram.com/accounts/emailsignup/")
        time.sleep(15)

        username_mail,email=random_email()
        password=random_password()
        fullname=random_fullname_from_files()
        username=random_username()

        driver.find_element(By.NAME,"emailOrPhone").send_keys(email)
        driver.find_element(By.NAME,"password").send_keys(password)
        driver.find_element(By.NAME,"fullName").send_keys(fullname)
        driver.find_element(By.NAME,"username").send_keys(username)
        driver.find_element(By.XPATH,"//button[@type='submit']").click()
        time.sleep(15)

        month=random.randint(1,12)
        day=random.randint(1,28)
        year=random.randint(1950,2007)
        Select(driver.find_element(By.XPATH,"//select[@title='Tháng:']")).select_by_value(str(month))
        Select(driver.find_element(By.XPATH,"//select[@title='Ngày:']")).select_by_value(str(day))
        Select(driver.find_element(By.XPATH,"//select[@title='Năm:']")).select_by_value(str(year))
        birthday=f"{day:02d}/{month:02d}/{year}"
        time.sleep(15)
        driver.find_element(By.XPATH,"//button[text()='Tiếp']").click()

        code=get_email_code(email)
        if code:
            driver.find_element(By.NAME,"email_confirmation_code").send_keys(code)
            driver.find_element(By.XPATH,"//div[@role='button' and text()='Tiếp']").click()
            print("Thành công:",username,email,"Proxy:",proxy)
            save_account(username,password,birthday,email)
            time.sleep(60)
        else:
            print("Không lấy được mã:",email,"Proxy:",proxy)
            driver.quit()
            create_account(index,cols,window_w,window_h)  # tạo lại nick khác
            return
    finally:
        driver.quit()

def main():
    total=int(input("Tạo bao nhiêu nick: "))
    threads_num=int(input("Chạy bao nhiêu luồng: "))

    screen_w,screen_h=pyautogui.size()
    cols=threads_num
    rows=math.ceil(total/threads_num)
    window_w=screen_w//cols
    window_h=screen_h//rows

    threads=[]
    for i in range(total):
        t=threading.Thread(target=create_account,args=(i,cols,window_w,window_h))
        threads.append(t)
        t.start()
        if (i+1)%threads_num==0:
            for t in threads: t.join()
            threads=[]
    for t in threads: t.join()

if __name__=="__main__":
    main()
