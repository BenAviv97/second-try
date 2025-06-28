from flask import Flask, request, render_template_string
import os
import datetime
from threading import Timer
from youtube_uploader import authenticate, upload_video

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

FORM_HTML = '''
<!doctype html>
<title>YouTube Auto Uploader</title>
<h1>Upload a video</h1>
<form method=post enctype=multipart/form-data>
  <label>Video File:<br><input type=file name=file required></label><br>
  <label>Title:<br><input type=text name=title></label><br>
  <label>Description:<br><textarea name=description></textarea></label><br>
  <label>Tags (comma separated):<br><input type=text name=tags></label><br>
  <label>Category ID:<br><input type=text name=category value="22"></label><br>
  <label>Privacy:<br>
    <select name=privacy>
      <option value="public">public</option>
      <option value="unlisted">unlisted</option>
      <option value="private">private</option>
    </select>
  </label><br>
  <label>Schedule Time:<br><input type=datetime-local name=schedule_time></label><br>
  <input type=submit value="Submit">
</form>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file:
            return 'No file provided', 400
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        title = request.form.get('title', 'Untitled')
        description = request.form.get('description', '')
        tags = request.form.get('tags', '')
        tags_list = [t.strip() for t in tags.split(',')] if tags else []
        category = request.form.get('category', '22')
        privacy = request.form.get('privacy', 'public')
        schedule_time = request.form.get('schedule_time')

        youtube = authenticate()

        def do_upload():
            upload_video(
                youtube=youtube,
                file_path=filepath,
                title=title,
                description=description,
                tags=tags_list,
                categoryId=category,
                privacyStatus=privacy,
            )

        if schedule_time:
            dt = datetime.datetime.fromisoformat(schedule_time)
            delay = (dt - datetime.datetime.now()).total_seconds()
            Timer(max(0, delay), do_upload).start()
            return f'Scheduled upload at {schedule_time}'
        else:
            do_upload()
            return 'Upload started'

    return render_template_string(FORM_HTML)

if __name__ == '__main__':
    app.run(debug=True)
