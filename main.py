from flask import Flask, jsonify
from gevent.pywsgi import WSGIServer
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import os


app = Flask(__name__)


@app.route("/get-deals")
def getDeals():
    k_url = 'https://www.konga.com/deals/daily'

    # opening up connection with konga, grabbing page
    k_client = uReq(k_url)
    k_html = k_client.read()
    k_client.close()

    page_soup = soup(k_html, "html.parser")
    # grabs each deal on products on the deals page
    containers = page_soup.findAll("li", {"class": "bbe45_3oExY _3b9ce_2Ge9A"})
    items = []
    for container in containers:
        item_image = container.img["alt"]
        title_container = container.findAll("h3", {"class": "ec84d_3T7LJ"})
        product_name = title_container[0].text
        pricing_container = container.findAll("div", {"class": "dcb26_2NJyv"})
        price = pricing_container[0].text.replace("+", " ")
        timing_class = container.findAll("span", {"class": "_01228_3ZMGW"})
        time_left = timing_class[0].text
        inventory_class = container.findAll("div", {"class": "_05703_3Dc2e"})
        item_percentage_sold = inventory_class[0].text
        discount_container = container.findAll(
            "span", {"class": "_4472a_zYlL- _6c244_q2qap"})
        discount = "None"
        if discount_container:
            discount = discount_container[0].text
        item = {"name": product_name, "image": item_image, "price": price,
                "time_left": time_left, "percentage_sold": item_percentage_sold, "discount": discount}
        items.append(item)

    return jsonify(items)


if __name__ == '__main__':
    http_server = WSGIServer(('', 8000), app)
    http_server.serve_forever()
