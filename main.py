import time
import json
from selenium.webdriver import Chrome

driver = Chrome("C:\\chromedriver.exe")
driver.get("https://csgolist.com/")

qualitys_dict = {'Consumer Grade': 'White', 'Industrial Grade': 'Light Blue', 'Mil-Spec': 'Blue', 'Restricted': 'Purple', 'Classified': 'Pink', 'Covert': 'Red', 'Covert Knife': 'Yellow', 'Contraband': 'Yellow'}
links = []

skin_data = {}

hrefs = driver.find_elements_by_css_selector("ul li a")
for href in hrefs:
    links.append(href.get_attribute('href'))

with open("skins.text", "r+", encoding='utf-8') as file:
    for link in links:
        if link is not None:
            driver.get(link)
            title = driver.find_element_by_css_selector(".headline .center").text
            if title.find("CASE") != -1:
                break
            else:
                weapon_name = title[:title.find("PRICE")]
                skin_data[weapon_name] = {}
                file.write(f"[{weapon_name}]\n")
                file.write("{\n")
                time.sleep(.5)
                print("\n"+weapon_name)

                weapon_skins = driver.find_elements_by_css_selector(".item-name .name")
                qualitys = driver.find_elements_by_css_selector(".center.item-rare p")

                for skins, quality, in zip(weapon_skins, qualitys):
                    print(f'{skins.text[skins.text.lower().find("|")+2:]}, {qualitys_dict[quality.text]}')
                    skin_data[weapon_name][skins.text[skins.text.lower().find("|")+2:]] = qualitys_dict[quality.text]
                    file.write(f"{skins.text[skins.text.lower().find('|')+2:]}:{qualitys_dict[quality.text]}\n")
                file.write("}\n")

driver.close()
driver.quit()

with open('skins.json', 'w', encoding='utf-8') as f:
    json.dump(skin_data, f, ensure_ascii=False, indent=4)