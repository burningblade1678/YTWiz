from moviepy.editor import VideoFileClip, AudioFileClip

def convert_video(input_path, output_format):
    try:
        if output_format in ["mp4", "avi", "mov"]:
            clip = VideoFileClip(input_path)
            output_path = input_path.rsplit(".", 1)[0] + f".{output_format}"
            clip.write_videofile(output_path, codec="libx264" if output_format == "mp4" else None)
        elif output_format in ["mp3", "wav"]:
            clip = AudioFileClip(input_path)
            output_path = input_path.rsplit(".", 1)[0] + f".{output_format}"
            clip.write_audiofile(output_path)
        else:
            raise ValueError(f"Unsupported format: {output_format}")
        
        clip.close()
        return output_path
    except Exception as e:
        raise Exception(f"Error converting video: {str(e)}")