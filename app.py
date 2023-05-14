from flask import Flask,request,Response,render_template
import os,re,json,glob


app = Flask(__name__, static_folder='static')


@app.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response


def get_chunk(full_path, byte1=None, byte2=None):
    file_size = os.stat(full_path).st_size
    start = 0

    if byte1 < file_size:
        start = byte1
    if byte2:
        length = byte2 + 1 - byte1
    else:
        length = file_size - start

    with open(full_path, 'rb') as f:
        f.seek(start)
        chunk = f.read(length)
    return chunk, start, length, file_size


def prepare_videos():
    print('Making thumbnails...')
    for x in glob.glob('static/videos/*.mp4'):
        thumbnail = 'static/videos/{}.gif'.format(os.path.basename(x))
        command = 'ffmpeg -hide_banner -loglevel error -y -ss 00:01:00 -t 5 -i {} -s 200x100 -r 5 {}'.format(x, thumbnail)
        os.path.exists(thumbnail) or os.system(command)
        print('   ', thumbnail)

    with open('static/videos.js', 'w') as s:
        videos_list = json.dumps([os.path.basename(x) for x in glob.glob('static/videos/*.mp4')])
        s.write('let videos = {};'.format(videos_list))


@app.route('/')
def main_page():
    return render_template('video.html')


@app.route('/video')
def get_file():
    range_header = request.headers.get('Range', None)
    byte1, byte2 = 0, None
    if range_header:
        match = re.search(r'(\d+)-(\d*)', range_header)
        groups = match.groups()

        if groups[0]:
            byte1 = int(groups[0])
        if groups[1]:
            byte2 = int(groups[1])


    video_file = request.args.get('name')
    if re.search('^[a-zA-Z0-9_]+.mp4$', video_file) is None:
        raise Exception('Fuck that, i quit 🤲')
    video_file = 'static/videos/{}'.format(video_file)
    chunk, start, length, file_size = get_chunk(video_file, byte1, byte2)
    resp = Response(chunk, 206, mimetype='video/mp4',
                    content_type='video/mp4', direct_passthrough=True)
    resp.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(start, start + length - 1, file_size))
    return resp


if __name__ == '__main__':
    prepare_videos()
    app.run(host='0.0.0.0', port=5555)
