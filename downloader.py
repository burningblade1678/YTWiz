from pytube import YouTube

def download_video(url, output_path):
    try:
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
        
        print(f"Downloading: {yt.title}")
        video_path = video.download(output_path)
        return video_path
    except Exception as e:
        raise Exception(f"Error downloading video: {str(e)}")