# second-try

This repository contains a simple script to upload videos to YouTube using the YouTube Data API.

## Requirements

- Python 3
- `google-api-python-client`
- `google-auth-oauthlib`
- `google-auth-httplib2`

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

1. Obtain OAuth2 credentials from Google Cloud and save them as `client_secrets.json` in the repository root.
2. Run the uploader with the video file and any optional metadata:

```bash
python youtube_uploader.py path/to/video.mp4 --title "My Video" --description "Description" --tags tag1 tag2 --category 22 --privacy unlisted
```

The first run will prompt you to authorize the application in the browser. A `token.pickle` file will be generated to store your credentials for future uploads.
