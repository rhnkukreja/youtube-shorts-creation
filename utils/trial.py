from moviepy.editor import TextClip, VideoFileClip, CompositeVideoClip
from moviepy.config import change_settings
# Example parameters for the text clip
overlay_text = "Hello, World!"
text_piece_duration = 5  # Duration of the text display in seconds
text_piece_start_time = 2  # Start time of the text display in seconds
text_coordinates = ('center', 'center')  # Position of the text
import os 


# Create the text clip
text_clip = (
    TextClip(
        txt=overlay_text,  # Ensure to use txt= for the text argument
        fontsize=70,
        font="Arial",  # Use a more commonly available font
        color="white",
        stroke_color="black",
        stroke_width=3,
        bg_color="brown"
    )
    .set_duration(text_piece_duration)
    .set_start(text_piece_start_time)
    .set_position(text_coordinates)  # Example position, adjust as needed
)

# # Load a video file (example)
# video = VideoFileClip("path_to_your_video.mp4")

# # Create a composite video with the text overlay
# composite = CompositeVideoClip([video, text_clip])

# # Write the result to a file
# composite.write_videofile("output_video.mp4", fps=24)
