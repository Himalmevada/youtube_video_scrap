from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import logging
import pymongo

logging.basicConfig(filename="scrapper.log", level=logging.INFO)

app = Flask(__name__)


@app.route("/", methods=['GET'])
def homepage():
    return render_template("index.html")


@app.route("/youtube_scrap", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:

            url = request.form["content"]
            # url = "https://www.youtube.com/@CarryisLive/videos"

            driver = webdriver.Chrome()
            driver.get(url)

            videos = driver.find_elements(
                By.CLASS_NAME, 'style-scope ytd-rich-grid-media')

            yt_channel_name = driver.find_element(
                By.XPATH, './/*[@id="text-container"]').text
            yt_channel_name = yt_channel_name.replace(" ", "_")


# //*[@id = "thumbnail"]
            csv_data = []

            for video in videos[0:5]:
                link = video.find_element(
                    By.XPATH, './/*[@id="thumbnail"]').get_attribute('href')
                thumbnail = video.find_element(
                    By.XPATH, './/*[@id="thumbnail"]/yt-image/img').get_attribute('src')
                title = video.find_element(
                    By.XPATH, './/*[@id="video-title"]').text
                views_count = video.find_element(
                    By.XPATH, './/*[@id="metadata-line"]/span[1]').text
                uploaded_time = video.find_element(
                    By.XPATH, './/*[@id="metadata-line"]/span[2]').text

                yt_dict = {"Channel_Name": yt_channel_name, "Url": link, "Thumbnail": thumbnail, "Title": title,
                           "Views": views_count, "Posted": uploaded_time}
                csv_data.append(yt_dict)
            print(csv_data)

            yt_csv_df = pd.DataFrame(csv_data)
            yt_csv_df.to_csv(f"csv/{yt_channel_name}.csv", index=False)

            client = pymongo.MongoClient(
                "mongodb+srv://admin:admin@cluster0.ge05dtm.mongodb.net/?retryWrites=true&w=majority")
            db = client["scraper_db"]
            coll = db["youtube_coll"]
            coll.insert_many(csv_data)
            logging.info("log my final result {}".format(csv_data))

            return render_template('results.html', csv_data=csv_data)

        except Exception as e:
            logging.info(e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')


# Postman API :

@app.route("/youtube_scrap", methods=['POST', 'GET'])
def index_api():
    if request.method == 'POST':
        try:

            url = request.json["content"]
            # url = "https://www.youtube.com/@CarryisLive/videos"

            driver = webdriver.Chrome()
            driver.get(url)

            videos = driver.find_elements(
                By.CLASS_NAME, 'style-scope ytd-rich-grid-media')

            yt_channel_name = driver.find_element(
                By.XPATH, './/*[@id="text-container"]').text
            yt_channel_name = yt_channel_name.replace(" ", "_")

            csv_data = []

            for video in videos[0:5]:
                link = video.find_element(
                    By.XPATH, './/*[@id="thumbnail"]').get_attribute('href')
                thumbnail = video.find_element(
                    By.XPATH, './/*[@id="thumbnail"]/yt-image/img').get_attribute('src')
                title = video.find_element(
                    By.XPATH, './/*[@id="video-title"]').text
                views_count = video.find_element(
                    By.XPATH, './/*[@id="metadata-line"]/span[1]').text
                uploaded_time = video.find_element(
                    By.XPATH, './/*[@id="metadata-line"]/span[2]').text

                yt_dict = {"Channel_Name": yt_channel_name, "Url": link, "Thumbnail": thumbnail, "Title": title,
                           "Views": views_count, "Posted": uploaded_time}
                csv_data.append(yt_dict)
            # print(csv_data)

            yt_csv_df = pd.DataFrame(csv_data)
            yt_csv_df.to_csv(f"csv/{yt_channel_name}.csv", index=False)

            client = pymongo.MongoClient(
                "mongodb+srv://admin:admin@cluster0.ge05dtm.mongodb.net/?retryWrites=true&w=majority")
            db = client["scraper_db"]
            coll = db["youtube_coll"]
            coll.insert_many(csv_data)

            logging.info("log my final result {}".format(csv_data))

            return jsonify(csv_data)
            # return render_template('results.html', csv_data=csv_data)

        except Exception as e:
            # logging.info(e)
            return e
            # return 'something is wrong'
    # return render_template('results.html')

    else:
        return jsonify(csv_data)
        # return render_template('index.html')


# ----------------------------


if __name__ == "__main__":
    app.run(host="0.0.0.0")
