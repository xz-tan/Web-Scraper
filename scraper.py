from bs4 import BeautifulSoup
import os
import requests
import string


num_pages = int(input())
type_of_article = input()


counter = 1

while counter <= num_pages:
    URL = "https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page=" + str(counter)
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')
    directory_name = f'Page_{counter}'
    os.mkdir(directory_name)
    os.chdir(directory_name)
    all_links = []

    for tag in soup.find_all("article"):
        for anchor in tag.find_all("a"):
            all_links.append(anchor.get('href'))
    article_type = soup.find_all("span", {"class":"c-meta__type"})
    article_type_list = [i.text for i in article_type]
    index_of_article = [i for i, x in enumerate(article_type_list) if x == type_of_article]
    saved_articles = []

    for index in index_of_article:
        link_of_article = "https://www.nature.com" + all_links[index]
        r = requests.get(link_of_article)
        soup1 = BeautifulSoup(r.content, 'html.parser')
        title = soup1.find("title").text
        title = title.translate(str.maketrans('', '', string.punctuation))
        title = title.replace(" ", "_")
        final_title = title.replace("__Research_Highlights", "")
        file_name = final_title + ".txt"
        if type_of_article == "Research Highlight":
            file_content = soup1.find('div', {'class': 'article-item__body'})
        else:
            file_content = soup1.find('div', {'class': 'c-article-body'})
        file_content = file_content.text.strip()
        binary_content = file_content.encode()
        article_file = open(file_name, "wb")
        article_file.write(binary_content)
        article_file.close()

    os.chdir("..")
    counter += 1

"""A more efficient method
articles = soup.find_all('article')
    for article in articles:
        article_type = article.find('span', {'class': 'c-meta__type'}).text
        if article_type == article_type_choice:
            article_url = article.find('a').get('href')
            articles_urls.append('https://www.nature.com' + article_url)
    return articles_urls
"""









