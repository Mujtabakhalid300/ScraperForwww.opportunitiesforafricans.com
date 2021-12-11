import json
from bs4 import BeautifulSoup
import lxml
import requests


def main_scrapper():  # scrap the main site for links
    # main site
    main_site = 'https://www.opportunitiesforafricans.com/category/call-for-applications/'
    r = requests.get(main_site).content
    # getting the source
    soup = BeautifulSoup(r, 'lxml')
    # getting all the links
    links = soup.find_all('a')
    # removing links that are not posts
    rqr = []
    rqr2 = []
    rqr3 = []
    rqr4 = []

    for i in links:
        if i['href'].count('/') == 4:
            rqr.append(i['href'])
        else:
            pass
    min = 63
    for i in rqr:
        if len(i) < min:
            pass
        else:
            rqr2.append(i)

    for i in rqr2:
        if '#respond' in i:
            pass
        else:
            rqr3.append(i)

    for i in rqr3:
        if i in rqr4:
            pass
        else:
            rqr4.append(i)
    rqr4.pop()
    # finally return the list of all posts on the main page
    return rqr4


def scraper(site):  # this will scrap individual posts
    response = requests.get(site)
    r = response.content
    # getting the source code of the page
    soup = BeautifulSoup(r, 'lxml')
    # getting the title
    title = soup.find('h1', class_='entry-title').string
    # getting the details para of the post
    allstr = soup.get_text()
    # removing unnecessary parts
    rqr = allstr.split("WhatsApp")
    rqr1 = rqr[1]
    rqr2 = rqr1.split('Facebook')
    rqr3 = rqr2[0].split('\n')
    nonempty = [x for x in rqr3 if x.strip() != ""]
    rqr4 = ''
    for line in nonempty:
        rqr4 += line + '\n'
    details = rqr4
    # store the detail in the details variable
    rqr5 = rqr4.splitlines()
    # getting the link
    linktext = rqr5[-1]
    # try clause to avoid errors if link is not found
    try:
        link = soup.find('a', string=linktext)['href']
    except TypeError:
        link = soup.find('a', rel="noreferrer noopener")['href']

    # creating a dict object named item with the data scrapped
    item = {}
    item['title'] = title
    item['detail'] = details
    item['link'] = link
    # returning the dict object
    return item


# storing all the links to links list by running the main_scrap() function we created
links = main_scrapper()

# if you want to print the links uncomment this code block
# for i in links:
#     print(str(links.index(i)) + "   " + i)

# list to store every dict object from every post in the links list
ls_dict = []

# final dict object that will be stored to a .json file
posts = {}

# appending the ls_dict with item dict from scraper()
for i in links:
    ls_dict.append(scraper(i))
    print(str(links.index(i)) + '# Done scrapping ' + i)

# adding list of items to the final posts dict
posts['names'] = ls_dict

# finally writing the dict into a data.json file
with open('data.json', 'w') as w:
    json.dump(posts, w, indent=4)
