import yt_dlp

def download_video(url, output_path):
    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'format': 'bestaudio/best',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return f"{output_path}/{info['title']}.{info['ext']}"
    except Exception as e:
        raise Exception(f"Error downloading video: {str(e)}")