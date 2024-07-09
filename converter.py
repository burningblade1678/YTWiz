import os
import subprocess
from moviepy.editor import VideoFileClip, AudioFileClip

def convert_video(input_path, output_format):
    try:
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = f"{os.path.dirname(input_path)}/{base_name}.{output_format}"
        
        if output_format in ["mp4", "avi", "mov"]:
            # Use ffmpeg directly for video conversion
            cmd = [
                "ffmpeg", "-i", input_path,
                "-c:v", "libx264", "-preset", "medium", "-crf", "23",
                "-c:a", "aac", "-b:a", "128k",
                "-movflags", "+faststart",
                "-y",  # Overwrite output file if it exists
                output_path
            ]
            subprocess.run(cmd, check=True, stderr=subprocess.PIPE)
        elif output_format in ["mp3", "wav"]:
            clip = AudioFileClip(input_path)
            clip.write_audiofile(output_path)
            clip.close()
        else:
            raise ValueError(f"Unsupported format: {output_format}")
        
        return output_path
    except subprocess.CalledProcessError as e:
        raise Exception(f"FFmpeg error: {e.stderr.decode()}")
    except Exception as e:
        raise Exception(f"Error converting video: {str(e)}")