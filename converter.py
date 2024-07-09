from moviepy.editor import VideoFileClip, AudioFileClip
import moviepy.config as config
import os

# Set a custom FFMPEG binary path if needed
# config.change_settings({"FFMPEG_BINARY": "/path/to/ffmpeg"})

def convert_video(input_path, output_format):
    try:
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = f"{os.path.dirname(input_path)}/{base_name}.{output_format}"
        
        if output_format in ["mp4", "avi", "mov"]:
            clip = VideoFileClip(input_path)
            
            # Handle potential FPS issues
            if clip.fps is None or clip.fps == 0:
                clip = clip.set_fps(30)  # Set a default FPS if it's not detected
            
            clip.write_videofile(output_path, codec="libx264" if output_format == "mp4" else None,
                                 audio_codec="aac" if output_format == "mp4" else "pcm_s16le",
                                 threads=4, ffmpeg_params=["-strict", "-2"])
        elif output_format in ["mp3", "wav"]:
            clip = AudioFileClip(input_path)
            clip.write_audiofile(output_path)
        else:
            raise ValueError(f"Unsupported format: {output_format}")
        
        clip.close()
        return output_path
    except Exception as e:
        raise Exception(f"Error converting video: {str(e)}")