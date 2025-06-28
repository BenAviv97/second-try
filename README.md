# YouTube Uploader Web App

This repository contains a simple Flask web application that collects data needed
for uploading videos to YouTube. The application allows users to provide a
video file along with its title, description, and tags. The actual YouTube
upload logic is **not** implemented here.

## Running Locally

1. Install dependencies:

   ```bash
   pip install Flask
   ```

2. Start the server:

   ```bash
   python app/app.py
   ```

3. Open your browser at [http://localhost:5000](http://localhost:5000) and use
the form to upload a video and its metadata. Uploaded files are stored in
`app/uploads/`.

This app serves as a starting point for collecting upload data. A future task
can extend it to automatically upload the video to YouTube using the collected
information.
