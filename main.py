import services.startDriver
import os
import traceback
import re


def get_links(driver):
    location_list = driver.find_elements_by_css_selector(
        '#mw-content-text li a:first-child')
    reflist = driver.find_elements_by_css_selector(
        '#mw-content-text .reflist li a')
    navbox = driver.find_elements_by_css_selector(
        '#mw-content-text .navbox li a')
    location_list = [x for x in location_list if x not in reflist]
    location_list = [x for x in location_list if x not in navbox]

    # location_list = location_list[:100]

    list_length = len(location_list)

    location_links = []
    for ind_name, x in enumerate(location_list):
        if (ind_name + 1) % 100 == 0 or (ind_name + 1) >= list_length:
            try:
                print("Got link:", (ind_name + 1), "/", list_length,
                      "of", ind_loc, "/", loc_length, "locations")
            except:
                pass
        try:
            location_links.append(
                [x.get_attribute('href'), x.get_attribute('title')])
        except:
            pass

    print()
    print()

    return location_links


def dict_entry(name, reading):
    s = '''<entry>
<k_ele>
<keb>'''
    s += name
    s += '''</keb>
</k_ele>
<r_ele>
<reb>'''
    s += reading
    s += '''</reb>
</r_ele>
</entry>\n'''
    return s


def scrap_names(driver):
    location_links = get_links(driver)

    # reading_list = []
    global ind_loc
    global loc_length
    loc_length = len(location_links)

    for ind_location, location in enumerate(location_links):
        # if ind_location < 42:
        #     continue
        ind_loc = ind_location + 1
        driver.get(location[0])
        
        print(location[1])

        name_links = get_links(driver)

        reading_list_length = len(name_links)

        for ind_name_reading, name in enumerate(name_links):
            try:
                driver.get(name[0])
                first_p = driver.find_element_by_css_selector(
                    "#mw-content-text p:first-of-type")
                reading = re.search(r'（([ぁ-ゞ\s]+)、', first_p.text).group(1)

                f.write(dict_entry(name[1], reading))
                # reading_list.append([name[1],reading])
            except:
                pass
            finally:
                if (ind_name_reading + 1) % 20 == 0 or (ind_name_reading + 1) >= reading_list_length:
                    try:
                        print("Processed:", (ind_name_reading + 1), "/",
                              reading_list_length, "of", ind_loc, "/", loc_length, "locations")
                    except:
                        pass

        print()
        print()


def run():
    os.system('clear')

    global f
    f = open("output/JMdict.xml", "w")
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<JMdict>\n')

    driver = services.startDriver.start()

    wiki_url = 'https://ja.wikipedia.org/wiki/日本人の一覧'

    driver.get(wiki_url)

    try:
        scrap_names(driver)
    except:
        print(traceback.format_exc())
    finally:
        driver.close()
        f.write('</JMdict>')
        f.close()


if __name__ == "__main__":
    run()
