from flask import Flask, render_template, request
import requests
import os
import datetime
import json

app = Flask(__name__, template_folder=os.getcwd() + "/templates", static_folder=os.getcwd() + "/static")


@app.route('/')
def main_page():
    out = list()
    for i in os.listdir("static/songs"):
        s = os.listdir(f"static/songs/{i}")
        if s[0][-4:] == ".txt":
            out.append([i, s[0][:-4]])
        else:
            out.append([i, s[1][:-4]])
    return render_template('main.html',
                           out=out,
                           )


@app.route('/<song>')
def song_find(song):
    if song in os.listdir("static/songs"):
        s = os.listdir(f"static/songs/{song}")
        if s[0][-4:] == ".txt":
            name = s[0][:-4]
            filename = f"static/songs/{song}/{s[1]}"
            with open(f"static/songs/{song}/{s[0]}", "r", encoding="utf8") as file:
                text = "<br>".join(file.readlines())
        else:
            name = s[1][:-4]
            filename = f"static/songs/{song}/{s[0]}"
            with open(f"static/songs/{song}/{s[1]}", "r", encoding="utf8") as file:
                text = "<br>".join(file.readlines())
        return render_template('song.html',
                               name=name,
                               filename=filename,
                               text=text,
                               )
    else:
        return "<h1>Ошибка 404</h1><h2>Страница не найдена</h2>", 404


@app.route('/load_my_song', methods=["GET", "POST"])
def load_my_song():
    if request.method == "GET":
        return render_template('load_song.html')
    else:
        client_secret = "28651c1d83744614ba3f4efc912b9bf8"

        token = request.args.get("access_token")
        headers = {
            'Authorization': f'OAuth {token}'
        }
        data = requests.get("https://login.yandex.ru/info", headers=headers,
                            params={"format": "json",
                                    "jwt_secret": client_secret}).json()
        filename = str(datetime.datetime.now()).replace(":", "-")
        os.mkdir(f"static/Заявки/{filename}")
        request.files["sound-file"].save(
            f"static/Заявки/{filename}/" +
            request.files["sound-file"].filename)
        with open(f"static/Заявки/{filename}/" + request.form["title"] + ".txt", "w", encoding="utf8") as file:
            file.write(request.form["text"])
        with open(f"static/Заявки/{filename}/data", "w") as file:
            json.dump(data, file)
        return "<a href='/'>Заявка принята скоро ответим</a>"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=False)
