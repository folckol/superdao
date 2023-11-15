import json
import time
import zipfile

from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.expected_conditions import visibility_of_element_located, element_to_be_clickable
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

api = ''
with open('data.txt', 'r') as file:
    for i in file:
        if i.strip('\n') == '':
            pass
        else:
            api = i.strip('\n')
            break




anticaptcha_plugin_path = r'anticaptcha-plugin_v0.62.zip'

def using_proxy():
    def get_proxy():
        proxy = {}

        with open("proxy.txt", "r") as file:
            proxy = file.readline()
            file.close()

        return proxy

    proxy = str(get_proxy())
    proxy_list = proxy.split(':')
    pass1 = str(proxy_list[3])

    PROXY_HOST = str(proxy_list[0])  # rotating proxy or host
    PROXY_PORT = str(proxy_list[1])
    PROXY_USER = str(proxy_list[2])
    PROXY_PASS = str(pass1.strip())

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "browsingData",
            "proxy",
            "storage",
            "tabs",
            "webRequest",
            "webRequestBlocking",
            "downloads",
            "notifications",
            "<all_urls>"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

    return manifest_json, background_js, proxy

def acp_api_send_request(driver, message_type, data={}):
    message = {
        'receiver': 'antiCaptchaPlugin',
        'type': message_type,
        **data
    }

    return driver.execute_script("""
    return window.postMessage({});
    """.format(json.dumps(message)))

def Func(pp):
    emails = ''
    with open('emails.txt', 'r') as file:
        for i in file:
            if i.strip('\n') == '':
                pass
            else:
                emails = i.strip('\n')
                break

    wallets = ''
    with open('wallets.txt', 'r') as file:
        for i in file:
            if i.strip('\n') == '':
                pass
            else:
                wallets = i.strip('\n')
                break

    chrome_options = Options()

    manifest_json, background_js, proxy = using_proxy()
    pluginfile = 'Proxy_ext.zip'

    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    chrome_options.add_extension(pluginfile)

    chrome_options.add_argument('--user-agent=%s' % UserAgent)
    chrome_options.add_extension(anticaptcha_plugin_path)
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

    # Активируем антикапчу
    driver.get('https://antcpt.com/blank.html')
    acp_api_send_request(
        driver,
        'setOptions',
        {'options': {'antiCaptchaApiKey': api}}
    )

    driver.get('https://play.superdao.co/survive?source=twitter&campaign=share')
    WebDriverWait(driver, 10).until(lambda d: d.find_element(By.CSS_SELECTOR, '[type="email"]')).send_keys(emails)
    WebDriverWait(driver, 10).until(lambda d: d.find_element(By.XPATH, '//span[text()="Let\'s play"]')).click()
    l = [6, 9, 10, 15, 12, 15, 15, 15, 13, 14]  # C, C, A, C, A, C, C, C, A, B;
    for i in l:
        WebDriverWait(driver, 10).until(lambda d: d.find_element(By.CSS_SELECTOR, f'div:nth-child({i}) > div > div')).click()
        WebDriverWait(driver, 10).until(lambda d: d.find_element(By.XPATH, '//span[text()="Next"]')).click()
        WebDriverWait(driver, 10).until(lambda d: d.find_element(By.XPATH, '//span[text()="Next"]')).click()
    WebDriverWait(driver, 10).until(lambda d: d.find_element(By.CSS_SELECTOR, 'div input:nth-child(1)')).send_keys(wallets)
    WebDriverWait(driver, 180).until(visibility_of_element_located((By.CSS_SELECTOR, '.antigate_solver.solved')))
    WebDriverWait(driver, 10).until(lambda d: d.find_element(By.XPATH, '//span[text()="Submit"]')).click()

    WebDriverWait(driver, 30).until(lambda d: d.find_element(By.CSS_SELECTOR, 'a[href="https://twitter.com/superdao_co"]'))

    driver.quit()

    print(f'Done - {pp}')
    pp+=1
    return pp



if __name__ == '__main__':


    pp = 0
    errors = 0
    while True:
        try:
            pp = Func(pp)

            with open('proxy.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()

            with open('proxy.txt', 'w', encoding='utf-8') as file:
                lines = file.writelines(lines[1:])

            with open('emails.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()

            with open('emails.txt', 'w', encoding='utf-8') as file:
                lines = file.writelines(lines[1:])

            with open('wallets.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()

            with open('wallets.txt', 'w', encoding='utf-8') as file:
                lines = file.writelines(lines[1:])

        except IndexError:

            errors+=1
            if errors == 5:
                break

        except Exception as e:
            # print(e)
            print(f'Error - {pp}')
            pass

    input()



