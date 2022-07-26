"""SUNFLOWER FARMERS BOT."""
import os
import time

from selenium import webdriver, common

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from logger import log
from settings import settings, plants_type


log('[STARTING SUNFLOWER FARMERS AUTOMATED BOT...] \n')
OPTIONS = webdriver.ChromeOptions()
OPTIONS.add_argument("--disable-blink-features=AutomationControlled")
# OPTIONS.add_extension("MetaMask.crx")
OPTIONS.add_extension("extension_10_17_0_0.crx")
OPTIONS.add_argument("--disable-gpu")
OPTIONS.add_argument("--disable-software-rasterizer")

S = Service(ChromeDriverManager().install())
DRIVER = None
GLOBAL_SLEEP = settings['time_monitor']
SELECTED_PLANT = settings['selected_plant']
MAX_WAIT_TIME = settings['max_wait_time']

# ACC VARIABLES
PHRASE = ''
PASSWD = ''

# CHECK multi_acc_list option in config.yaml
MULTI_ACC_TOTAL = 0
MULTI_ACC_CURRENT = 0


def start_game():
    """Starting the game process."""
    log('\nCleaning unused tabs...')
    close_unused_tabs()
    log('Log in to MetaMask...')
    login_metamask()
    log('Installing Polygon Network...')
    install_polygon_network()
    add_personal_sfl_wallet()
    time.sleep(3)
    log('Starting the game...')
    tries = 0
    DRIVER.get('https://sunflower-farmers.com/play/')
    time.sleep(5)
    auth_metamask()
    from_welcome_to_ready()

    time.sleep(3)
    while True:
        try:
            in_game_process()
            time.sleep(GLOBAL_SLEEP * 60)
        except Exception as e:
            print(e)
            DRIVER.refresh()
            time.sleep(10)
            from_welcome_to_ready()


def auth_metamask():
    DRIVER.switch_to.window(DRIVER.window_handles[1])
    xpath('//button[@class="button btn--rounded btn-primary"]').click()
    xpath('//button[@class="button btn--rounded btn-primary page-container__footer-button"]').click()
    time.sleep(3)
    DRIVER.switch_to.window(DRIVER.window_handles[1])
    xpath('//button[@class="button btn--rounded btn-primary btn--large request-signature__footer__sign-button"]').click()
    DRIVER.switch_to.window(DRIVER.window_handles[0])

def in_game_process():
    """Main loop process."""
    # progress_plants = count_progress_plants()
    # log('Harvest in progress ---------- Total: [%s]' % progress_plants)
    # log('Checking empty places...')
    # if progress_plants == total_harvest_able():
    #     log('Maximum capacity reached. No places to plant.', 'red')
    #     log('So ok...')
    #     if not settings['use_multi_acc']:
    #         log('Checking again in %s minutes...' % GLOBAL_SLEEP)
    #         log('No Worries. You can change it on config.yaml!')
    #     else:
    #         log('Switching to next account...', 'yellow')
    #     log('☕ Take some coffee and fresh air...')
    #     return None

    # log('Checking collectables items...', 'white')
    log('select seed...', 'white')
    select_seed()
    time.sleep(1)
    log('harvest and plant...', 'white')
    harvest_and_plant()
    time.sleep(1)
    # log('Saving...', 'white')
    # save()
    # while is_saving():
    #     time.sleep(3)
    # log('Saved!')


def count_free_slots():
    """Count Free slots to plant."""
    log('Counting free slots...', 'yellow')
    return len(css('.plant-hint'))

def total_harvest_able():
    """Total harvest capacity."""
    return len(css('.harvest'))

def from_welcome_to_ready():
    while True:
        try:
            DRIVER.find_element(By.XPATH, "//button[@class='bg-brown-200 w-full p-1 shadow-sm text-white text-shadow object-contain justify-center items-center hover:bg-brown-300 cursor-pointer flex disabled:opacity-50  overflow-hidden mb-2']").click()
            break
        except Exception as exception:
            print(exception)
            time.sleep(3)
    time.sleep(15)
    # clear notifications
    try:
        DRIVER.find_element(By.XPATH, "//img[@class='h-6 cursor-pointer']").click()
    except common.exceptions.NoSuchElementException as exception:
        pass
    time.sleep(0.5)
    get_back_shovel()
    time.sleep(0.5)

def harvest_and_plant():
    """Check collectible plant."""
    slots = DRIVER.find_elements(By.XPATH, "//div[@class='relative group']")
    for e in slots:
        # img_cnt_before = len(e.find_element(By.XPATH, './/img'))
        e.click()
        time.sleep(0.2)
        # img_cnt_after = len(e.find_element(By.XPATH, './/img'))
        get_back_shovel()
        time.sleep(0.5)
        # if img_cnt_before == img_cnt_after:
        e.click()
        time.sleep(0.2)
        open_chest()
        time.sleep(0.5)

        e.click()
        time.sleep(0.5)

def get_back_shovel():
    try:
        DRIVER.find_element(By.XPATH, "//img[@class='bg-brown-200 w-full p-1 shadow-sm text-white text-shadow object-contain justify-center items-center hover:bg-brown-300 cursor-pointer flex disabled:opacity-50  text-sm']").click()
        xpath("//img[@class='absolute z-10 hover:img-highlight cursor-pointer']").click()
        xpath("//button[@class='bg-brown-200 w-full p-1 shadow-sm text-white text-shadow object-contain justify-center items-center hover:bg-brown-300 cursor-pointer flex disabled:opacity-50  text-sm']").click()
        log('get back shovel', 'green')
    except common.exceptions.NoSuchElementException as exception:
        pass


def open_chest():
    try:
        e = DRIVER.find_element(By.XPATH, "//img[@class='w-16 hover:img-highlight cursor-pointer']")
        e.click()
        xpath(
            "//button[@class='bg-brown-200 w-full p-1 shadow-sm text-white text-shadow object-contain justify-center items-center hover:bg-brown-300 cursor-pointer flex disabled:opacity-50  mt-4 w-full']").click()
        log('open chest...', 'green')
    except common.exceptions.NoSuchElementException as exception:
        pass

def save():
    """Save harvest."""
    save_btn = xpath('//*[@id="timer"]/img')
    js_click(save_btn)
    js_click(xpath('//*[@id="save-error-buttons"]/div'))
    main_window_handle = None
    while not main_window_handle:
        main_window_handle = DRIVER.current_window_handle
    signin_window_handle = None
    while not signin_window_handle:
        for handle in DRIVER.window_handles:
            if handle != main_window_handle:
                signin_window_handle = handle
                break
    DRIVER.switch_to.window(signin_window_handle)
    metamask_btn = xpath('//*[@id="app-content"]/div/div[2]/div/div[4]/div[3]/footer/button[2]')
    metamask_btn.click()
    DRIVER.switch_to.window(main_window_handle)


def select_seed():
    """Select seed on basket."""
    # open items tab
    try:
        xpath("//div[@class='w-16 h-16 sm:mx-8 mt-2 relative flex justify-center items-center shadow rounded-full cursor-pointer']").click()
    except common.exceptions.NoSuchElementException as exception:
        xpath("//div[@class='flex flex-col items-end mr-2 sm:block fixed top-16 right-0 z-50']").click()
    # select first seed
    DRIVER.find_elements(By.XPATH, "//div[@class='flex mb-2 flex-wrap -ml-1.5']")[0].find_element(By.XPATH, './/div/div').click()
    # close tab
    xpath("//img[@class='h-6 cursor-pointer mr-2 mb-1']").click()


def count_progress_plants():
    """Count all plants in progress."""
    progress_plants = css('div.flex.flex-col.text-xxs.text-white.text-shadow.ml-2.mr-2')
    for idx, plant in enumerate(progress_plants):
        log('Plants slot %s: %s left.' % (idx + 1, plant.text), 'white')
    return len(progress_plants)


def close_unused_tabs():
    """Close initial metamask plugin tab."""
    main_window_handle = None
    while not main_window_handle:
        main_window_handle = DRIVER.current_window_handle

    for handle in DRIVER.window_handles:
        if handle != main_window_handle:
            DRIVER.switch_to.window(handle)
            DRIVER.close()
            break
    DRIVER.switch_to.window(main_window_handle)


def is_loading():
    """Show Sunflower farmers loading modal."""
    try:
        return 'loading' in xpath('//*[@id="welcome"]/h1', False).text.lower()
    except:
        return None


def is_saving():
    """Check if is saving your farm."""
    try:
        return 'saving' in xpath('//*[@id="saving"]/h4').text.lower()
    except:
        return None


def js_click(element):
    """Execute a JS click on browser."""
    DRIVER.execute_script("arguments[0].click();", element)


def xpath(path, raise_error=True):
    """Find by xpath."""
    found_element = False
    tries = 5
    while not found_element and tries > 0:
        try:
            found_element = DRIVER.find_element(By.XPATH, path)
            return found_element
        except common.exceptions.NoSuchElementException:
            tries -= 1
            time.sleep(1)
    if not raise_error:
        return None
    raise ValueError('Element Not found, Max tries reached.')


def css(css_selector, raise_error=True):
    """Find elements by css."""
    found_elements = False
    tries = 5
    while not found_elements and tries > 0:
        try:
            found_elements = DRIVER.find_elements(By.CSS_SELECTOR, css_selector)
            return found_elements
        except common.exceptions.NoSuchElementException:
            tries -= 1
            time.sleep(1)
    if not raise_error:
        return None
    raise ValueError('Element Not found, Max tries reached.')


def login_metamask():
    """Start login into metamask, see config.yaml for more infor."""
    time.sleep(3)
    DRIVER.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#initialize/create-password/import-with-seed-phrase')
    time.sleep(3)
    inputs = DRIVER.find_elements(By.XPATH, "//input[@class='MuiInputBase-input MuiInput-input']")
    splitted_phase = PHRASE.split()
    i = 0
    for e in inputs:
        if i >= 12:
            e.send_keys(PASSWD)
            print(PASSWD)
        else:
            e.send_keys(splitted_phase[i])
            print(splitted_phase[i])
        i = i + 1

    xpath('//input[@id="create-new-vault__terms-checkbox"]').click()
    DRIVER.find_element(By.XPATH, '//button[@class="button btn--rounded btn-primary create-new-vault__submit-button"]').click()
    xpath('//button[@class="button btn--rounded btn-primary first-time-flow__button"]', False).click()


def install_polygon_network():
    """Instaling Polygon network on Metamask."""
    xpath('/html/body').send_keys(Keys.CONTROL + Keys.HOME)
    xpath('//*[@id="app-content"]/div/div[1]/div/div[2]/div[1]/div/span').click()
    xpath('//button[@class="button btn--rounded btn-secondary"]').click()
    name = 'Polygon'
    rpc_url = 'https://polygon-rpc.com'
    chain_id = '137'
    symbol = 'MATIC'
    block_explorer_url = 'https://polygonscan.com/'
    inputs = DRIVER.find_elements(By.XPATH, '//input[@class="form-field__input"]')
    inputs[0].send_keys(name)
    inputs[1].send_keys(rpc_url)
    inputs[2].send_keys(chain_id)
    inputs[3].send_keys(symbol)
    inputs[4].send_keys(block_explorer_url)
    xpath('//button[@class="button btn--rounded btn-primary"]').click()

def add_personal_sfl_wallet():
    xpath("//div[@class='identicon'][1]").click()
    DRIVER.find_elements(By.XPATH, "//div[@class='account-menu__item__text']")[1].click()
    xpath("//input[@id='private-key-box']").send_keys(SECRET_KEY)
    xpath("//button[@class='button btn--rounded btn-primary btn--large new-account-create-form__button']").click()

def setup_linux_env():
    """Setup based in os.env variables.

    Please check config.yaml file if this option is activated.
    Usage (config.yaml):
        set_linux_env: true
    """
    if os.name == 'posix':
        global PHRASE
        global PASSWD
        PHRASE = os.environ['SUNFLOWER']
        PASSWD = os.environ['PASSWD']


def setup_single_acc():
    """Setup single Account."""
    global PHRASE
    global PASSWD
    global SECRET_KEY
    PHRASE = settings['private']['secret_phrase']
    PASSWD = settings['private']['passwd']
    SECRET_KEY = settings['private']['secret_key']


def multi_acc_change():
    """Change accounts."""
    login_list = settings['multi_acc_list']
    global MULTI_ACC_TOTAL
    global PHRASE
    global PASSWD
    global MULTI_ACC_CURRENT
    global SELECTED_PLANT
    MULTI_ACC_TOTAL = len(login_list)
    selected_acc = login_list[MULTI_ACC_CURRENT]
    PHRASE = selected_acc[0]
    PASSWD = selected_acc[1]
    SELECTED_PLANT = selected_acc[2]
    MULTI_ACC_CURRENT += 1
    if MULTI_ACC_CURRENT >= MULTI_ACC_TOTAL:
        MULTI_ACC_CURRENT = 0


def setup_driver():
    """Setup start driver."""
    tries = 0
    max_tries = 5
    global DRIVER
    while not DRIVER:
        try:
            DRIVER = webdriver.Chrome(service=S, options=OPTIONS)
            # DRIVER = webdriver.Chrome(executable_path='/Users/mengkaili/Desktop/chromedriver', options=OPTIONS)
        except:
            if tries <= max_tries:
                raise ValueError('Was not possible to mount driver.')
            tries += 1
            log('Failed to mount driver instance. Trying again...', 'red')
            time.sleep(3)


def get_new_driver():
    """Close and open a new driver."""
    log('Closing browser.')
    global DRIVER
    DRIVER.close()
    DRIVER = None
    log('Setup new Driver.')
    setup_driver()


def main():
    """Main Process."""
    setup_driver()
    if not settings['use_multi_acc']:
        log(['SINGLE ACCOUNT MODE SELECTED...'])
        if settings['set_linux_env']:
            setup_linux_env()
        else:
            setup_single_acc()
        start_game()
    else:
        log(['MULTI ACCOUNT MODE SELECTED...'])
        while True:
            multi_acc_change()
            start_game()
            get_new_driver()
            time.sleep(5)




if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print(e)
            time.sleep(3)
            if DRIVER is not None:
                DRIVER.quit()
