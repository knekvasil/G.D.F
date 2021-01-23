# main.py
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

if __name__ == '__main__':

    url = "https://brokercheck.finra.org/"
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    driver.get(url)

    time.sleep(2)

    driver.find_element_by_id("firm-input").send_keys("602")
    driver.find_element_by_class_name("md-ink-ripple").click()

    time.sleep(2)

    broker_dictionary = dict()
    broker_name = str()
    max_page = int(driver.find_element_by_partial_link_text("page").text[5])
    current_page = 1

    while current_page <= max_page:
        broker_store = driver.find_elements_by_class_name("tile-item")
        main_window = driver.window_handles[0]

        time.sleep(2)
        for broker in broker_store:
            broker_name = broker.find_element_by_xpath(".//span[@ng-bind-html='vm.item.getFullName()']").text
            broker_crd = broker.find_element_by_xpath(".//span[@ng-bind-html='vm.item.id'][@class='ng-binding']").text

            time.sleep(2)
            try:
                disclosure = broker.find_element_by_xpath(".//div[@ng-if='vm.item.hasDisclosures()']"
                                                          "[@class='ng-scope']")
                driver.execute_script(f"window.open('https://brokercheck.finra.org/individual/summary/{broker_crd}',"
                                      f" 'new window')")

                time.sleep(2)
                broker_window = driver.window_handles[1]
                driver.switch_to.window(broker_window)

                time.sleep(2)
                try:
                    date_eval = int(driver.find_element_by_xpath("//div[@class='ng-binding flex-xs-30 flex-gt-xs-25']"
                                                                 "[@ng-bind='item.eventDate']").text[-4:])
                    if date_eval >= 2015:
                        broker_dictionary[broker_crd] = broker_name
                        print(f"{broker_name} has a post-2015 disclosure!")
                    else:

                        print(f"{broker_name} only has pre-2015 disclosures.")
                except NoSuchElementException:
                    print(f"Limited information about {broker_name}.")

                time.sleep(2)
                driver.close()
                driver.switch_to.window(main_window)

                time.sleep(1)
            except NoSuchElementException:
                print(f"{broker_name} does not have any disclosures.")

        time.sleep(1)
        driver.find_element_by_partial_link_text("›").click()
        current_page += 1

        time.sleep(2)
    print("\nBrokers with a post-2014 disclosure include:")
    for key in broker_dictionary.keys():
        print(f"{broker_dictionary[key]}: CRD#{key}")

    time.sleep(1)
    driver.quit()
