from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request
from bottle import get
from bottle import post

import datetime

import albums_s # подгружаем фаил с кодом работы с БД

def make_russian(number):
    """
    Изменяет окончание слов
    """
    if str(number).endswith("1"): # если строка заканчивается на 1
        return "{} альбом".format(str(number))
    elif str(number).endswith(("0", "5", "6", "7", "8", "9", "11", "12", "13", "14", "15", "16", "17", "18", "19")):
        return "{} альбомов".format(str(number))
    elif str(number).endswith(("2", "3", "4")):
        return "{} альбома".format(str(number))

@route("/albums", method = "GET")
def menu():
    """
    отображает меню для ввода данных
    """
    # action="/albums/" method="get" -  указывает URL-адрес и метод, которые будут получать данные формы
    return"""
        <h1>Данный скрипт позволяет найти альбомы по имени исполнителя, либо добавить новые данные об исполнителе.</h1>
        <h2>В этом поле можно ввести имя испольнителя для поиска его альбомов в БД.</h2>
        <form action="/albums/" method="get">
            Исполнитель: <input name="artist" type="text" />
            <input value="Найти" type="submit" />
        </form>
        <br>
        <h2>В этом поле можно ввести новые данные об исполнителе.</h2>
        <p> *Необходимо заполнить все формы.</p>
        <form action="/albums/" method="post">
            Исполнитель: <input name="artist" type="text" />
            Альбом: <input name="album" type="text" />
            Жанр: <input name="genre" type="text" />
            Год выпуска альбома: <input name="year" type="text" />
            <input value="Добавить запись" type="submit" />
        </form>
        """

@get("/albums/")
def albums():
    """
    получаем значения GET-параметрa artist
    """
    artist = request.query.artist.capitalize() # приводим к единообразию
    albums_list = albums_s.find(artist) # вызываем функцию из подгруженного фаила с кодом для работы с БД
    if not albums_list:
        message = "Альбомов исполнителя {} не найдено!".format(artist)
        result = HTTPError(404, message)
    else:
        albums_names = [album.album for album in albums_list]
        albums_cnt = len(albums_names)
        result = "Найдено {} исполнителя {}.<br>".format(make_russian(albums_cnt), artist)
        result = result + "<br>".join(albums_names) # добавляет итерируемое что-то, "список" в данном случае, а <br> в браузере каждое значение этого списка переносит на новую строку
    return result

@post("/albums/")
def albums():
    """
    получаем значения POST-параметров artist, album, genre, year и приводим их к единообразию
    """
    album = {"artist": (request.forms.artist).capitalize(),
    "year": request.forms.year,
    "genre": (request.forms.genre).capitalize(),
    "album": (request.forms.album).capitalize()
    }
     # провераем, что год введен числом и он не из будущего, что введены значения всех параметров
    if (album["year"]).isdigit() and\
        (len(album["year"])<=4 and datetime.datetime(year = int(album["year"]), month = 1, day = 1)<=datetime.datetime.today()) and\
        album["genre"] and\
        album["album"]:
        message, albums_cnt = albums_s.add_album(album) # вызываем функцию из подгруженного фаила с кодом для работы с БД
        if albums_cnt!=0:
            result = HTTPError(409, message)
        else: result = message
    else:
        message = f"""Для записи альбома необходимо ввести данные для следующих параметров:
                artist, album, genre, year. При этом год должен быть не из будущего!"""
        result = HTTPError(400, message)
    return result # выводим сообщение о ходе операции

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)

