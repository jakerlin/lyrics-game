# -*- coding: utf-8 -*-
from flask import Flask, request, render_template_string, session
import random, time

app = Flask(__name__)
app.secret_key = 'abc123'

# ===== 曲库 =====
SONG_DB = [
    {"lyrics": "确认过眼神 我遇上对的人", "title": "醉赤壁", "artist": "林俊杰"},
    {"lyrics": "雨下整夜 我的爱溢出就像雨水", "title": "七里香", "artist": "周杰伦"},
    {"lyrics": "后来 我总算学会了如何去爱", "title": "后来", "artist": "刘若英"},
    {"lyrics": "你存在我深深的脑海里", "title": "小幸运", "artist": "田馥甄"},
]

# ===== 排行榜 =====
SCORES = {}

HTML = """
<!doctype html>
<html>
<head>
<meta charset='utf-8'>
<title>歌词竞猜</title>
<style>
body{background:#f0f2f5;font-family:Arial;text-align:center}
.card{background:white;width:400px;margin:40px auto;padding:20px;border-radius:12px}
input{margin:5px;padding:6px}
button{padding:8px 16px;background:#1677ff;color:white;border:none;border-radius:6px}
</style>
<script>
let time = 30;
function countdown(){
    let t = document.getElementById('timer');
    if(time<=0){ document.forms[0].submit(); }
    else{ t.innerText = time; time--; setTimeout(countdown,1000); }
}
</script>
</head>
<body onload="countdown()">

<div class="card">
<h2>🎵 歌词竞猜</h2>
<p>⏱ 剩余 <span id="timer">30</span> 秒</p>
<p><b>{{lyrics}}</b></p>

<form method="post">
<input name="username" placeholder="你的名字" required><br>
<input name="title" placeholder="歌名"><br>
<input name="artist" placeholder="歌手"><br>
<button>提交</button>
</form>

<p>{{result}}</p>
</div>

<div class="card">
<h3>🏆 排行榜</h3>
<ol>
{% for u,s in scores %}
<li>{{u}} - {{s}}</li>
{% endfor %}
</ol>
</div>

</body>
</html>
"""

@app.route('/', methods=['GET','POST'])
def index():
    result = ""

    if 'song' not in session:
        session['song'] = random.choice(SONG_DB)

    if request.method == 'POST':
        user = request.form.get('username')
        t = request.form.get('title','')
        a = request.form.get('artist','')

        song = session['song']

        if t == song['title'] and a == song['artist']:
            SCORES[user] = SCORES.get(user,0) + 1
            result = "✅ 正确 +1分"
        else:
            result = f"❌ 正确答案：{song['title']} - {song['artist']}"

        session['song'] = random.choice(SONG_DB)

    scores = sorted(SCORES.items(), key=lambda x:-x[1])[:10]

    return render_template_string(
        HTML,
        lyrics=session['song']['lyrics'],
        result=result,
        scores=scores
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
