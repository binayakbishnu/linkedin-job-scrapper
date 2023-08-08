import requests
from bs4 import BeautifulSoup

from flask import Flask, render_template
import time

app = Flask(__name__)

# def get_timestamp():
#     return int(time.time())
# app.jinja_env.globals.update(get_timestamp=get_timestamp)

app.debug = True
# app.use_reloader = True


def pull_data(search_query):
    # url = "https://www.linkedin.com/jobs"
    url = f"https://www.linkedin.com/jobs/search/?keywords={search_query.replace(' ', '%20')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }

    #? Send a GET request to the LinkedIn job listings page
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    #? Find all job listing cards on the page
    job_cards = soup.find_all("li", class_="result-card")
    job_cards = soup.find_all("li", class_="discovery-templates-entity-item list-style-none")
    job_cards = soup.find_all("li", class_="ember-view   jobs-search-results__list-item occludable-update p0 relative scaffold-layout__list-item")
    job_cards = soup.find_all("li", class_="")
    for job in job_cards:
        with open('sample.html', 'w', encoding="utf-8") as f:
            f.write(str(job_cards) + '\n')
        
    return job_cards

def process_imported_data(job_cards):
    data = {}
    data["search_query"] = search_query
    data["content"] = []

    #? Iterate over the job cards and extract relevant information
    for card in job_cards:
        temp = card.find("img")
        company_logo = temp["data-delayed-url"] if temp!=None else None

        temp = card.find("a", class_="base-card__full-link")
        link = temp["href"] if temp!=None else None

        position = card.find("h3").get_text().strip()

        company_name = card.find("h4").get_text().strip()

        temp = card.find("a", class_="hidden-nested-link")
        company_url = temp["href"] if temp!=None else None

        location = card.find("span", class_="job-search-card__location").get_text().strip()

        # post_date = card.find("time").get_text().strip()

        post_date = card.find("time")["datetime"] + " (" + card.find("time").get_text().strip() + ")"

        benefits = card.find("span", class_="result-benefits__text").get_text().strip() if card.find("span", class_="result-benefits__text") != None else None

        # description = card.find("p", class_="job-search-card__snippet").get_text().strip()
        
        company_logo.replace("&amp;", "&")
        
        i = link.index("?") if link!=None else None
        link = link[0:i] if link!=None else None
        
        # Print or store the extracted information as desired
        # print("Link:", link)
        # print("Title:", position)
        # print("Company:", company_name)
        # print("Logo:", company_logo)
        # print("Company link:", company_link)
        # print("Location:", location)
        # print("Date posted:", post_date)
        # if(benefits != None):
        #     print("Benefits:", benefits)
        # # print("Description:", description)
        # print("-----------------------")
        
        item = {}
        item["link"] = link
        item["position"] = position
        item["company_name"] = company_name
        item["company_logo"] = company_logo
        item["company_url"] = company_url
        item["location"] = location
        item["post_date"] = post_date
        # if(benefits != None):
        item["benefits"] = benefits
            
        data["content"].append(item)
        
    return data

@app.route('/')
def display_output():
    # Pass the data to the HTML template
    processed_data = process_imported_data(job_cards)
    return render_template('index.html', data=processed_data)

if __name__ == '__main__':
    # search_query = "data consultant"
    search_query = "web developer"
    # search_query = "business intelligence"

    job_cards = pull_data(search_query)
    
    app.run()