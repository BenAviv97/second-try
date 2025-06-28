# second-try

This repository contains a simple script to upload videos to YouTube using the YouTube Data API. It now also includes a minimal web interface for submitting uploads or scheduling them for the future.

## Requirements

- Python 3
- `google-api-python-client`
- `google-auth-oauthlib`
- `google-auth-httplib2`
- `Flask`

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

1. Obtain OAuth2 credentials from Google Cloud and save them as `client_secrets.json` in the repository root.
2. Run the uploader with the video file and any optional metadata. Use `--schedule` to provide an ISO timestamp if you want to delay the upload:

```bash
python youtube_uploader.py path/to/video.mp4 \
  --title "My Video" \
  --description "Description" \
  --tags tag1 tag2 \
  --category 22 \
  --privacy unlisted \
 --schedule 2030-01-01T12:00  # optional
```

The first run will prompt you to authorize the application in the browser. A `token.pickle` file will be generated to store your credentials for future uploads. The `--schedule` flag expects a date in `YYYY-MM-DDTHH:MM` format.

### Web interface

Instead of using the command line you can run a small Flask server which presents a single page form. The form lets you upload a video file, set its metadata and optionally specify a future date/time for the upload.

```bash
python web_app.py
```

Visit `http://localhost:5000` in your browser and fill out the form. If a schedule time is provided the server will wait until that time before uploading.

