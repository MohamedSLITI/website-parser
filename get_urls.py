from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import random
import json
import time

dict_href_links = {}
chunk_size = 6000


def download_pdf(r, name):
    with open(f'output/{name}.pdf', 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)


def getdata(url):
    is_pdf = False
    r = requests.get(url)
    content_type = r.headers.get('content-type')
    if 'application/pdf' in content_type:
        name = url.split('/')[-1]
        download_pdf(r, name)
        is_pdf = True
    time.sleep(random.randint(1, 2))
    return r.text, is_pdf


def get_links(website_link):
    html_data, is_pdf = getdata(website_link)
    soup = BeautifulSoup(html_data, "html.parser")
    list_links = []
    for link in soup.find_all("a", href=True):

        # Append to list if new link contains original link
        if str(link["href"]).startswith((str(website_link))):
            list_links.append(link["href"])

        # Include all href that do not start with website link but with "/"
        if str(link["href"]).startswith("/") and '/eu/' in link["href"]:
            if link["href"] not in dict_href_links:
                print(link["href"])
                dict_href_links[link["href"]] = None
                link_with_www = 'https://www.goremedical.com/' + link["href"][1:]
                print("adjusted link =", link_with_www)
                list_links.append(link_with_www)

    # Convert list of links to dictionary and define keys as the links and the values as "Not-checked"
    dict_links = dict.fromkeys(list_links, "Not-checked")
    return dict_links, is_pdf


def get_subpage_links(l):
    for link in tqdm(l):
        # If not crawled through this page start crawling and get links
        if l[link] == "Not-checked":
            dict_links_subpages, is_pdf = get_links(link)
            # Change the dictionary value of the link to "Checked"
            l[link] = ["Checked", is_pdf]
        else:
            # Create an empty dictionary in case every link is checked
            dict_links_subpages = {}
        # Add new dictionary to old dictionary
        l = {**dict_links_subpages, **l}
    return l


def get_urls(website):
    # create dictionary of website
    dict_links = {website: "Not-checked"}

    counter, counter2 = None, 0
    while counter != 0:
        counter2 += 1
        dict_links2 = get_subpage_links(dict_links)
        counter = sum(value == "Not-checked" for value in dict_links2.values())
        # Print some statements
        print("")
        print("THIS IS LOOP ITERATION NUMBER", counter2)
        print("LENGTH OF DICTIONARY WITH LINKS =", len(dict_links2))
        print("NUMBER OF 'Not-checked' LINKS = ", counter)
        print("")
        dict_links = dict_links2
        # Save list in json file
        a_file = open("data.json", "w")
        json.dump(dict_links, a_file)
        a_file.close()
