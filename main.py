# coding:utf-8
from SinglePage.singlepage import *
from model.Base import db_session,init_db

from model.Cover import Cover
from model.Song import Song
from model.SongInfo import SongInfo
from model.Lyric import Lyric

apps = {
    Cover: '/covers/',
    Song: '/songs/',
    SongInfo: '/songinfos/',
    Lyric: '/lyrics/',
}

for obj in apps:
    register(obj, apps[obj])
# # # # # # # # # # register models# # # # # # # # # # # # # # # # # # # #

app.secret_key = 'super secret key'

# # # # # # # # # # # nodels # # # # # # # # # # # # # # # # # # #


@app.teardown_request
def auto_rollback(exception):
    if exception:
        db_session.rollback()
        db_session.remove()
    db_session.remove()
# # # # # # # # # # # exception handler# # # # # # # # # # # # # # # # # # #

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', debug=True, port=5050)
# # # # # # # # # # # start the engine# # # # # # # # # # # # # # # # # # #
