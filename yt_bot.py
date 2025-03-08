from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import yt_dlp
import os
import pickle
import time

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
CLIENT_SECRETS_FILE = "client_secrets.json"
TOKEN_PICKLE_FILE = 'token.pickle'

def get_authenticated_service():
    credentials = None
    if os.path.exists(TOKEN_PICKLE_FILE):
        with open(TOKEN_PICKLE_FILE, 'rb') as token:
            credentials = pickle.load(token)
    
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)
        
        with open(TOKEN_PICKLE_FILE, 'wb') as token:
            pickle.dump(credentials, token)
    
    return build('youtube', 'v3', credentials=credentials)

def get_trending_shorts():
    ydl_opts = {
        'format': 'best',
        'quiet': True,
    }
    
    with yt_dlp.YtDlp() as ydl:
        # Search for trending shorts
        results = ydl.extract_info(
            "https://www.youtube.com/hashtag/shorts",
            download=False
        )
        
        # Get top 2 shorts
        return results['entries'][:2]

def download_short(url, output_path):
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
    }
    
    with yt_dlp.YtDlp(ydl_opts) as ydl:
        ydl.download([url])

def upload_video(youtube, file_path, title, description):
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': ['shorts', 'viral'],
            'categoryId': '22'
        },
        'status': {
            'privacyStatus': 'private',  # Start as private to review before making public
            'selfDeclaredMadeForKids': False
        }
    }

    insert_request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True)
    )
    
    response = insert_request.execute()
    return response

def main():
    youtube = get_authenticated_service()
    
    while True:
        try:
            # Get trending shorts
            trending_shorts = get_trending_shorts()
            
            for short in trending_shorts:
                # Download the short
                output_file = f"downloaded_short_{short['id']}.mp4"
                download_short(short['webpage_url'], output_file)
                
                # Upload to YouTube
                title = f"🔥 {short['title']}"
                description = "Trending short #shorts"
                
                upload_video(youtube, output_file, title, description)
                
                # Clean up downloaded file
                os.remove(output_file)
                
                print(f"Successfully processed: {title}")
                
            # Wait for 24 hours before next batch
            time.sleep(24 * 60 * 60)
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            time.sleep(300)  # Wait 5 minutes before retrying

if __name__ == "__main__":
    main()
