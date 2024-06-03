import utils.cg_response as cg_response
from utils.image_utils import GetImages
from utils.audio_utils import GetAudio
import utils.moviepy_video_compiler as moviepy_video_compiler
from moviepy.editor import AudioFileClip, concatenate_audioclips, VideoFileClip, concatenate_videoclips
import json
import utils.coordinates_algo as coordinates_algo
from multiprocessing import Pool
import os
from config import *

def create_directory(path, folder_name):
    folder_path = os.path.join(path, folder_name)
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Directory '{folder_path}' created successfully.")
    else:
        print(f"Directory '{folder_path}' already exists.")



def text_to_video(topic, output_video_path):

    llm_response=cg_response.get_response_from_cg(topic)

    llm_response = json.loads(llm_response)
    try:
        # Try to access the first format
        image_description = llm_response["image_description"]
    except KeyError:
        # If the first format isn't present, fall back to the second
        try:
            image_description = llm_response["Output"]["image_description"]
        except KeyError:
            # Handle the case where neither format is present
            image_description = "Default description or an error message"
    topic_modified=topic.replace(" ","_")
    create_directory(PROJECT_PATH, "images")
    image_file_path=PROJECT_PATH+f"\images\{topic_modified}.png"
    GetImages().get_image_path(image_file_path, image_description)

    audio_clips_list = []
    overlay_texts_list = []

    for part_num, part_text in llm_response["Output"].items():
        if part_num =="image_description":
            break 
        part_number = int(part_num.split("_")[1])
        # Generate file path for audio
        create_directory(PROJECT_PATH, "clips_audio")
        audio_file_path = PROJECT_PATH+f"\clips_audio\{topic_modified}_{part_number}.mp3"
        print(audio_file_path)
        print("73 - driver_script")
        print(part_text)

        GetAudio().generateAudio(audio_file_path, part_text)
        print("76 - driver_script")
        # Load the generated audio clip
        audio_clip = AudioFileClip(audio_file_path)
        audio_clips_list.append(audio_clip)
        
        # Get the duration of the audio clip
        duration = audio_clip.duration
        
        start_time = sum(clip.duration for clip in audio_clips_list[:-1]) if audio_clips_list else 0
        
        # Create overlay text JSON for each part
        overlay_text_json = {
            "text": part_text,
            "start_time": start_time,
            "duration": duration
        }
        overlay_texts_list.append(overlay_text_json)


    final_audio = concatenate_audioclips(audio_clips_list)
    audio_file_path=PROJECT_PATH+f"\clips_audio\{topic_modified}.mp3"
    final_audio.write_audiofile(audio_file_path)
    video_duration=AudioFileClip(audio_file_path).duration

    title_json= {
            "text": topic,
            "start_time": 0,
            "duration": video_duration
    }

    overlay_texts_list.insert(0, title_json)

    json_for_moviepy={
        "audio_file_path":audio_file_path,
        "image_path":image_file_path,
        "overlay_texts":overlay_texts_list
    }

    print(json_for_moviepy)

    json_for_moviepy_with_text_coordinates=coordinates_algo.get_json_for_moviepy_with_text_coordinates(json_for_moviepy)
    moviepy_video_compiler.create_the_video(json_for_moviepy_with_text_coordinates,output_video_path)
    return output_video_path


def generate_video(topic):
    create_directory(PROJECT_PATH, "output_videos")
    output_video_path = PROJECT_PATH+ f"\output_videos\{topic}.mp4"
    text_to_video(topic, output_video_path)
    return output_video_path



topic="" # enter the topic of your choice

generate_video(topic)




