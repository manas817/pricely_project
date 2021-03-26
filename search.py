from selenium import webdriver
import pandas as pd

text = input("Search: ") 
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

 
driver.get("https://www.google.com");
search = driver.find_element_by_name("q")
search.send_keys(f"{text}")
search.submit()


counter = 1
page = 1

# initalizing the required data
pages = []
total_searchs = []
titles = []
urls = []
descriptions = []


# this function gets the neccessary data at that particular page and returns the total count of search results
def searchResults(count, page):
    results = driver.find_elements_by_xpath('//div[@class="tF2Cxc"]')
    for result in results:
        if count <= 10:
            page_no = page
            search_no = count
            title = result.find_element_by_xpath('.//h3')
            title = title.text
            link = result.find_element_by_xpath('.//div[@class="yuRUbf"]/a').get_attribute("href")
            description = result.find_element_by_xpath('.//span[@class="aCOpRe"]')
            description = description.text

            # not to include the unnecessary links (videos, "people also searched" etc)
            if not title or not link or not description:
                continue

            count += 1
            pages.append(page_no)
            total_searchs.append(search_no)
            titles.append(title)
            urls.append(link)
            descriptions.append(description)

    return count


counter = searchResults(counter, page)
if counter <= 10:
    next = driver.find_element_by_id("pnnext").click()   #go to the next page
    page += 1
    searchResults(counter, page)


data = {
    'Page_Number': pages,
    'Search_Result_Number': total_searchs,
    'Search_Result_Title': titles,
    'Search_Result_URL': urls,
    'Search_Result_Description': descriptions,
}

df = pd.DataFrame(data)
df.to_csv('file.csv')