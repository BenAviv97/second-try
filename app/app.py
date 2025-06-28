from flask import Flask, render_template, request, redirect, url_for, flash
import os

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'change-me'


@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        tags = request.form.get('tags')
        file = request.files.get('file')
        if not file:
            flash('Video file is required.')
            return redirect(request.url)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        flash('Data received. Video saved to {}'.format(filepath))
        # Here would be logic to queue the video for upload
        return redirect(url_for('upload'))
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
