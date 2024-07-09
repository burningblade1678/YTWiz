import os
import shutil

def save_file(input_path, output_name, output_location):
    try:
        _, ext = os.path.splitext(input_path)
        output_path = os.path.join(output_location, f"{output_name}{ext}")
        
        counter = 1
        while os.path.exists(output_path):
            output_path = os.path.join(output_location, f"{output_name}_{counter}{ext}")
            counter += 1
        
        shutil.move(input_path, output_path)
        return output_path
    except Exception as e:
        raise Exception(f"Error saving file: {str(e)}")

def clean_up():
    # Add any necessary cleanup operations here
    pass