import os
import pickle
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from threading import Timer
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def authenticate():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
            creds = flow.run_console()
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('youtube', 'v3', credentials=creds)

def upload_video(youtube, file_path, title, description, tags=None, categoryId='22', privacyStatus='public'):
    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or [],
            "categoryId": categoryId
        },
        "status": {"privacyStatus": privacyStatus}
    }
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=request_body, media_body=media)
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")
    print(f"Upload complete: {response['id']}")
    return response

def schedule_upload(youtube, when, *args, **kwargs):
    """Schedule an upload at the specified datetime."""
    if isinstance(when, str):
        when = datetime.datetime.fromisoformat(when)
    delay = (when - datetime.datetime.now()).total_seconds()
    Timer(max(0, delay), upload_video, args=(youtube,)+args, kwargs=kwargs).start()

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Upload a video to YouTube")
    parser.add_argument('file', help='Video file path')
    parser.add_argument('--title', default='Untitled', help='Video title')
    parser.add_argument('--description', default='', help='Video description')
    parser.add_argument('--tags', nargs='*', help='Video tags separated by space')
    parser.add_argument('--category', default='22', help='YouTube category ID')
    parser.add_argument('--privacy', default='public', help='Video privacy status')
    parser.add_argument('--schedule', help='Schedule upload at ISO datetime (YYYY-MM-DDTHH:MM)')
    args = parser.parse_args()

    youtube = authenticate()
    if args.schedule:
        schedule_upload(
            youtube,
            args.schedule,
            args.file,
            args.title,
            args.description,
            args.tags,
            args.category,
            args.privacy,
        )
    else:
        upload_video(
            youtube=youtube,
            file_path=args.file,
            title=args.title,
            description=args.description,
            tags=args.tags,
            categoryId=args.category,
            privacyStatus=args.privacy,
        )

if __name__ == "__main__":
    main()
