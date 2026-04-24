from flask import session
app.secret_key = 'abc123'
# -*- coding: utf-8 -*-
from flask import Flask, request, render_template_string
import random

app = Flask(__name__)

SONG_DB = [
    {"lyrics": "确认过眼神 我遇上对的人", "title": "醉赤壁", "artist": "林俊杰"},
    {"lyrics": "雨下整夜 我的爱溢出就像雨水", "title": "七里香", "artist": "周杰伦"},
    {"lyrics": "你存在我深深的脑海里", "title": "小幸运", "artist": "田馥甄"},
    {"lyrics": "后来 我总算学会了如何去爱", "title": "后来", "artist": "刘若英"},
    {"lyrics": "我和你吻别在无人的街", "title": "吻别", "artist": "张学友"},
]

HTML = """
<h2>🎵 歌词竞猜</h2>
<p>{{lyrics}}</p>
<form method='post'>
歌名：<input name='title'><br>
歌手：<input name='artist'><br>
<button>提交</button>
</form>
<p>{{result}}</p>
"""

@app.route('/', methods=['GET','POST'])
def index():
    result = ""

    # 第一次访问时生成题目
    if 'song' not in session:
        session['song'] = random.choice(SONG_DB)

    if request.method == 'POST':
        t = request.form.get('title','')
        a = request.form.get('artist','')

        song = session['song']

        if t == song['title'] and a == song['artist']:
            result = "✅ 正确"
        else:
            result = f"❌ 正确答案：{song['title']} - {song['artist']}"

        # 下一题
        session['song'] = random.choice(SONG_DB)

    return render_template_string(
        HTML,
        lyrics=session['song']['lyrics'],
        result=result
    )

@app.route('/', methods=['GET','POST'])
def index():
    global current_song
    result = ""
    if request.method == 'POST':
        t = request.form.get('title','')
        a = request.form.get('artist','')
        if t == current_song['title'] and a == current_song['artist']:
            result = "✅ 正确！"
        else:
            result = f"❌ 错误：{current_song['title']} - {current_song['artist']}"
        current_song = random.choice(SONG_DB)

    return render_template_string(HTML, lyrics=current_song['lyrics'], result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
