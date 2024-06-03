from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, AudioFileClip, CompositeAudioClip
from project.config import *
from moviepy.config import change_settings
import os 


def create_the_video(json_for_moviepy, output_video_path):
    audio_path = json_for_moviepy["audio_file_path"]
    image_path = json_for_moviepy["image_path"]
    duration = AudioFileClip(audio_path).duration
    image_clip = (
        ImageClip(image_path)
        .set_duration(duration)
        .resize(newsize=VIDEO_ASPECT_RATIO)
        .set_position("center")
    )
    os.environ["IMAGEMAGICK_BINARY"] =IMAGEMAGICK_BINARY_PATH
    change_settings({"IMAGEMAGICK_BINARY": IMAGEMAGICK_BINARY_PATH})

    text_clips = []
    for overlay_text_object in json_for_moviepy["overlay_texts"]:
        overlay_text_pieces_list = overlay_text_object["text"]
        text_piece_duration = float(overlay_text_object["duration"])
        text_piece_start_time = float(overlay_text_object["start_time"])
        for overlay_text_piece in overlay_text_pieces_list:
            overlay_text=overlay_text_piece["text_piece"]
            text_coordinates=overlay_text_piece["coordinates"]
            print(overlay_text)
            text_clip = (
                TextClip(
                    txt=overlay_text,  # Ensure to use txt= for the text argument
                    fontsize=FONT_SIZE,
                    # font="Arial-Bold",  # Changed to a more commonly available font
                    font="Bookman-Old-Style-Bold-Italic",
                    color="white",
                    stroke_color="black",
                    stroke_width=3,
                    bg_color="brown"
                )
                .set_duration(text_piece_duration)
                .set_start(text_piece_start_time)
                .set_position(text_coordinates)  # Example position, adjust as needed
            )
            text_clips.append(text_clip)

    # Include both image_clip and text_clips in a single list for CompositeVideoClip
    video_clip = CompositeVideoClip([image_clip] + text_clips, size=VIDEO_ASPECT_RATIO)

    audio_clip = AudioFileClip(audio_path)
    bg_clip= AudioFileClip(PROJECT_PATH+"\m_bg_music_1_full.mp3").volumex(0.1).set_duration(duration).set_start(0)

    bg_clip=bg_clip.subclip(0,duration)
    combined_audio = CompositeAudioClip([audio_clip, bg_clip])

    final_clip = video_clip.set_audio(combined_audio)
    final_clip.write_videofile(output_video_path, fps=24)
