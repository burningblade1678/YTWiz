import os
from moviepy.editor import AudioFileClip

def convert_video(input_path, output_format):
    try:
        base_name = os.path.splitext(input_path)[0]
        output_path = f"{base_name}.{output_format}"
        
        if output_format in ['mp3', 'wav', 'ogg']:
            audio = AudioFileClip(input_path)
            audio.write_audiofile(output_path)
            audio.close()
        else:
            raise ValueError(f"Unsupported format: {output_format}")
        
        return output_path
    except Exception as e:
        raise Exception(f"Error converting audio: {str(e)}")