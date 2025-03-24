import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def login_to_tuta(email, password, account_label=""):
    """
    登录Tuta邮箱
    
    参数:
        email: 邮箱地址
        password: 密码
        account_label: 账号标识，用于日志和截图
    
    返回:
        bool: 登录是否成功
    """
    driver = None
    try:
        # Chrome浏览器配置
        print(f"配置Chrome浏览器... [{account_label}]")
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 无界面模式
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        # 添加反检测参数
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # 启动浏览器
        print(f"启动Chrome浏览器... [{account_label}]")
        driver = webdriver.Chrome(options=chrome_options)
        
        # 执行JavaScript来绕过自动化检测
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
        
        # 访问Tuta登录页面
        print(f"访问Tuta登录页面... [{account_label}]")
        driver.get('https://app.tuta.com/login')
        time.sleep(5)  # 等待页面加载
        
        # 保存页面状态
        screenshot_name = f'login_page_{account_label}.png' if account_label else 'login_page.png'
        driver.save_screenshot(screenshot_name)
        
        # 查找邮箱输入框
        print(f"查找邮箱输入框... [{account_label}]")
        email_selectors = [
            'input[type="email"]',
            'input[name="email"]',
            'input[placeholder*="email" i]',
            'input[placeholder*="邮箱" i]',
            '//input[@type="email"]',
            '//input[contains(@placeholder, "mail") or contains(@placeholder, "邮箱")]'
        ]
        
        email_input = None
        for selector in email_selectors:
            try:
                if selector.startswith('//'):
                    email_input = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                else:
                    email_input = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                if email_input:
                    print(f"找到邮箱输入框: {selector} [{account_label}]")
                    break
            except:
                continue
        
        if not email_input:
            # 尝试查找任何输入框
            print(f"无法通过选择器找到邮箱输入框，尝试查找所有输入框... [{account_label}]")
            inputs = driver.find_elements(By.TAG_NAME, "input")
            if inputs:
                print(f"找到 {len(inputs)} 个输入框，尝试使用第一个 [{account_label}]")
                email_input = inputs[0]
            else:
                driver.save_screenshot(f'no_email_field_{account_label}.png')
                raise Exception(f"无法找到邮箱输入框 [{account_label}]")
            
        print(f"输入邮箱地址... [{account_label}]")
        email_input.clear()
        email_input.send_keys(email)
        time.sleep(1)
        
        # 查找密码输入框
        print(f"查找密码输入框... [{account_label}]")
        password_selectors = [
            'input[type="password"]',
            'input[name="password"]',
            'input[placeholder*="password" i]',
            'input[placeholder*="密码" i]',
            '//input[@type="password"]'
        ]
        
        password_input = None
        for selector in password_selectors:
            try:
                if selector.startswith('//'):
                    password_input = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                else:
                    password_input = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                if password_input:
                    print(f"找到密码输入框: {selector} [{account_label}]")
                    break
            except:
                continue
        
        if not password_input:
            # 尝试找到第二个输入框
            inputs = driver.find_elements(By.TAG_NAME, "input")
            if len(inputs) > 1:
                print(f"未找到密码输入框，尝试使用第二个输入框 [{account_label}]")
                password_input = inputs[1]
            else:
                driver.save_screenshot(f'no_password_field_{account_label}.png')
                raise Exception(f"无法找到密码输入框 [{account_label}]")
            
        print(f"输入密码... [{account_label}]")
        password_input.send_keys(password)
        time.sleep(1)
        
        # 查找登录按钮
        print(f"查找登录按钮... [{account_label}]")
        login_selectors = [
            'button[type="submit"]',
            '//button[contains(text(), "Login") or contains(text(), "登录") or contains(text(), "Log in")]',
            '//button[@type="submit"]',
            '//input[@type="submit"]'
        ]
        
        login_button = None
        for selector in login_selectors:
            try:
                if selector.startswith('//'):
                    login_button = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                else:
                    login_button = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                if login_button:
                    print(f"找到登录按钮: {selector} [{account_label}]")
                    break
            except:
                continue
        
        if not login_button:
            # 尝试查找所有按钮
            print(f"无法通过选择器找到登录按钮，尝试查找所有按钮... [{account_label}]")
            buttons = driver.find_elements(By.TAG_NAME, "button")
            if buttons:
                print(f"找到 {len(buttons)} 个按钮，尝试找到类型为submit的按钮 [{account_label}]")
                for button in buttons:
                    if button.get_attribute('type') == 'submit' or 'login' in button.text.lower() or '登录' in button.text:
                        login_button = button
                        print(f"找到可能的登录按钮: {button.text} [{account_label}]")
                        break
                
                if not login_button and buttons:
                    print(f"未找到明确的登录按钮，使用第一个按钮 [{account_label}]")
                    login_button = buttons[0]
            else:
                driver.save_screenshot(f'no_login_button_{account_label}.png')
                raise Exception(f"无法找到登录按钮 [{account_label}]")
            
        print(f"点击登录按钮... [{account_label}]")
        login_button.click()
        print(f"已点击登录按钮 [{account_label}]")
        
        # 等待登录完成
        print(f"等待登录完成并验证... [{account_label}]")
        time.sleep(10)  # 给登录过程足够的时间
        driver.save_screenshot(f'after_login_{account_label}.png')
        
        # 检查URL变化来验证登录
        current_url = driver.current_url
        if 'login' not in current_url.lower():
            print(f"登录成功! URL已改变: {current_url} [{account_label}]")
            driver.save_screenshot(f'login_success_{account_label}.png')
            
            # 停留一会儿，确保登录状态被记录
            time.sleep(10)
            return True
        else:
            print(f"登录可能不成功，URL仍包含login [{account_label}]")
            driver.save_screenshot(f'login_verification_failed_{account_label}.png')
            return False
            
    except Exception as e:
        print(f"发生错误: {str(e)} [{account_label}]")
        if driver:
            driver.save_screenshot(f'error_{account_label}.png')
        return False
        
    finally:
        # 确保浏览器关闭
        if driver:
            print(f"关闭浏览器... [{account_label}]")
            driver.quit()

def main():
    results = []
    log_message = "登录执行时间: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n"
    
    # 自动查找所有账号
    account_num = 1
    while True:
        # 检查是否有这个编号的账号
        email_key = f'TUTA_EMAIL_{account_num}' if account_num > 1 else 'TUTA_EMAIL'
        password_key = f'TUTA_PASSWORD_{account_num}' if account_num > 1 else 'TUTA_PASSWORD'
        
        email = os.environ.get(email_key)
        password = os.environ.get(password_key)
        
        # 如果没有找到环境变量，尝试寻找下一个账号
        if not email or not password:
            if account_num == 1:
                # 如果是第一个账号且未找到，继续检查第二个账号
                account_num += 1
                continue
            else:
                # 如果不是第一个账号且未找到，说明已经没有更多账号了
                break
        
        print(f"\n=== 开始登录第{account_num}个账号 ===")
        success = login_to_tuta(email, password, f"account{account_num}")
        result = f"账号{account_num}登录{'成功' if success else '失败'}"
        results.append(result)
        log_message += result + "\n"
        print(f"账号{account_num}登录结果: {result}")
        
        # 检查下一个账号
        account_num += 1
    
    # 写入日志文件
    with open('login_history.log', 'a') as f:
        f.write(log_message)
    
    # 如果所有账号都登录失败，退出代码返回非零值
    if results and all("失败" in result for result in results):
        print("所有账号登录均失败")
        exit(1)
    
    print("登录过程完成")

if __name__ == "__main__":
    main()
