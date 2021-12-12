from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from termcolor import colored, cprint
import time, os, ctypes
from bs4 import BeautifulSoup
#Настройки

#Поддержка разноцветного текста на Windwos
try:
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
except:
    pass

def clear(): #очистка терменила 
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except:
        print("clear fail")

#Закрывает первую страницу
def close_plagins_page(): 
    window_after = driver.window_handles[0]
    driver.close()
    driver.switch_to_window(window_after)

#By ZederBreys
#Settings browser
options = Options()
options.headless = False
#options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0") #FireFox
options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36') #Chrome

# Отключает логи, кроме первой строки инициализации:
# DevTools listening on ws://127.0.0.1:63103/devtools/browser/.....
options.add_argument('--log-level=3')

options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-infobars")
options.add_argument("--lang=en-US.")

clear()

# addons chrome 
EXTENSION_PATH = "Metamask.crx"
options.add_extension(EXTENSION_PATH)

url = "https://google.com"

driver = webdriver.Chrome(options=options)
driver.get(url)
close_plagins_page()
print(driver.title)

def create_wallet(name_wallet, count):
    webdriver.support.wait.WebDriverWait(driver, 60).until(lambda x: x.find_element_by_xpath("""//div[@class="identicon"]""")).click()
    webdriver.support.wait.WebDriverWait(driver, 60).until(lambda x: x.find_element_by_xpath("//div[contains(text(), 'Create Account')]")).click()
    write_name_account = webdriver.support.wait.WebDriverWait(driver, 60).until(lambda x: x.find_element_by_xpath("""//input[@class='new-account-create-form__input']""")) # Вводим название счёта
    write_name_account.send_keys(f"{name_wallet} - {str(count)}")
    webdriver.support.wait.WebDriverWait(driver, 60).until(lambda x: x.find_element_by_xpath("//button[contains(text(), 'Create')]")).click() #crate accunt
    print(f"Счёт {name_wallet} - {str(count)} создан!")


def save_wallet_address(password):
    webdriver.support.wait.WebDriverWait(driver, 60).until(lambda x: x.find_element_by_xpath("""//button[@title="Account Options"]""")).click()
    webdriver.support.wait.WebDriverWait(driver, 60).until(lambda x: x.find_element_by_xpath("//span[contains(text(), 'Account details')]")).click()
    soup = BeautifulSoup(driver.page_source, "lxml")
    addres_wallet = soup.find("div", {"class": "qr-code"}).find("div", {"class": "qr-code__address"}).find(text=True)

    webdriver.support.wait.WebDriverWait(driver, 60).until(lambda x: x.find_element_by_xpath("//button[contains(text(), 'Export Private Key')]")).click()
    
    password_write = webdriver.support.wait.WebDriverWait(driver, 60).until(lambda x: x.find_element_by_xpath("""//input[@type="password"]""")) #input password
    password_write.send_keys(str(password))

    #confirm
    test22 = webdriver.support.wait.WebDriverWait(driver, 60).until(lambda x: x.find_elements_by_xpath(""" //button[@role="button"]"""))[1]
    test22.click()

    #driver.execute_script("""aler_test2 = document.querySelector("textarea").value;
    #alert(aler_test2)""")
    #Сохранием скеретный ключ
    private_key_restore = webdriver.support.wait.WebDriverWait(driver, 60).until(lambda x: x.find_element_by_xpath("""//textarea"""))
    private_key_restore = str(private_key_restore.text)
    
    #private_key_restore = soup.find("textarea")
    #soup = BeautifulSoup(driver.page_source, "lxml")
    #print(private_key_restore)
    #private_key_restore = private_key_restore.find(text=True)
    #print(private_key_restore)

    #done
    webdriver.support.wait.WebDriverWait(driver, 60).until(lambda x: x.find_element_by_xpath(""" //button[@role="button"]""")).click()
    
    return f"{addres_wallet}:{private_key_restore}"

if (str(driver.title.lower()) == "metamask"):
    try:
        webdriver.support.wait.WebDriverWait(driver, 60).until(lambda x: x.find_element_by_xpath("//button[contains(text(), 'Get Started')]")).click() # ожилаем появления элемента
    except:
        clear()
        print(colored("Ошибка загрузки расширения\n Драйвер браузера иногда отказывается загружать расширения. Попробуйте повторно запустить скрипт", "red"))
    #"Get Started"
    clear()
    print(colored("Начнём!", "blue"))
    while True:
        print(("Импортировать(1) / Создать(2)?"))
        choice_of_actions = input("Ваш выбор: ")
        if str(choice_of_actions.lower()) == "1":
            print(colored("Импортировать", "blue"))
            print("Введите seed фразу MetaMask: ")
            seed_metamask = input("Seed фраза: ")

            clear()
            print(colored("Seed фраза получена", "blue"))

            print("Введите новый пароль от MetaMask: ")
            new_passwrod_metamask = input("Пароль: ")
            clear()
            print(colored("Новый пароль получен", "blue"))

            print("Продолжаем...")
            webdriver.support.wait.WebDriverWait(driver, 60).until(lambda x: x.find_element_by_xpath("//button[contains(text(), 'Import wallet')]")).click()
            webdriver.support.wait.WebDriverWait(driver, 60).until(lambda x: x.find_element_by_xpath("//button[contains(text(), 'No Thanks')]")).click()

            #Восстоновление аккаунта...

            #seed input
            seed_input_in  = webdriver.support.wait.WebDriverWait(driver, 60).until(lambda x: x.find_element_by_xpath("""//input[@placeholder='Paste Secret Recovery Phrase from clipboard']"""))
            seed_input_in.clear()
            seed_input_in.send_keys(str(seed_metamask))

            #password input
            password_input_in = driver.find_element_by_id("password")
            password_input_in.clear()
            password_input_in.send_keys(str(new_passwrod_metamask))

            password_confirm_input_in = driver.find_element_by_id("confirm-password") #confirm
            password_confirm_input_in.clear()
            password_confirm_input_in.send_keys(str(new_passwrod_metamask))

            #checkbox == true
            driver.execute_script("""document.querySelectorAll('div[role="checkbox"')[1].click()""")
            #sumbit
            driver.execute_script("""document.querySelector('button[type="submit"').click()""")
            #all done
            webdriver.support.wait.WebDriverWait(driver, 60).until(lambda x: x.find_element_by_xpath("//button[contains(text(), 'All Done')]")).click()
            #driver.execute_script("""document.querySelector('button[role="button"').click()""")
            break
        elif str(choice_of_actions.lower()) == "2":
            print(colored("Создать", "blue"))

            webdriver.support.wait.WebDriverWait(driver, 60).until(lambda x: x.find_element_by_xpath("//button[contains(text(), 'Create a Wallet')]")).click() # ожилаем появления элемента
            clear()
            print(colored("Эта опция будет добавлена в будущем!", "red"))
            break
        else:
            clear()
            print(colored("Выбор неверный", "red"))
    
    input(colored("Настройте нужную вам сеть в metamask после чего нажмите любую клавишу", "magenta"))
    name_acc = input(colored("Введите название счёта: ", "blue"))
    ammount = input(colored("Количество аккаунтов: ", "blue"))
    clear()
    print(colored("Название: " + str(name_acc), "magenta"))
    print(colored("Количество: " + str(ammount), "magenta"))
    print(colored("-" * 35 ,"magenta"))
    final_time_create = list()
    final_time_save = list()
    for i in range(int(ammount)):
        start_time_create = time.time()
        create_wallet(str(name_acc), int(i))
        final_time_create.append((time.time() - start_time_create)) #Формируем время на создание аккуанта

        start_time_save = time.time()
        ret = save_wallet_address(str(new_passwrod_metamask))
        final_time_save.append((time.time() - start_time_save)) #Формируем время на сохраение аккуанта
        print(str(ret))
        f = open(f"./metamask_wallet.txt" , "a")
        f.write(str(ret) + '\n')
        f.close
    print(colored(f"Среднее значение затраченное на создание аккаунта: {str((sum(final_time_create) / len(final_time_create)))}", "magenta"))
    print(colored(f"Среднее значение затраченное на сохранение ключа: {str((sum(final_time_save) / len(final_time_save)))}", "magenta"))
    driver.quit()