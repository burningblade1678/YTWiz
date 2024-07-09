from moviepy.editor import AudioFileClip
import os

def convert_video(input_path, output_format):
    try:
        base_name = os.path.splitext(input_path)[0]
        output_path = f"{base_name}.{output_format}"
        
        audio = AudioFileClip(input_path)
        audio.write_audiofile(output_path)
        audio.close()
        
        return output_path
    except Exception as e:
        raise Exception(f"Error converting audio: {str(e)}")