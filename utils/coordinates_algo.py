from PIL import ImageFont, ImageDraw, Image
from config import *

PROJECT_PATH=r"C:\Users\rhnku\my_projects\shorts_videos\backend\utils"


def get_text_placement(text, number_i,image_width=1080, image_height=1920, font_path = PROJECT_PATH+"\Bookman Old Style Bold Italic.ttf" , font_size=FONT_SIZE):
    font = ImageFont.truetype(font_path, font_size)
    image = Image.new('RGB', (image_width, image_height))
    draw = ImageDraw.Draw(image)
    
    # Calculate text width and height with the given font
    bbox = draw.textbbox((0, 0), text, font=font)
    text_height = bbox[3] - bbox[1]
    
    lines = []
    line_widths = []
    words = text.split()
    line = []
    
    for word in words:
        # Check width of the line with the new word added
        line_test = ' '.join(line + [word])
        line_bbox = draw.textbbox((0, 0), line_test, font=font)
        line_width = 1.2*(line_bbox[2] - line_bbox[0])
        
        if line_width <= image_width:
            line.append(word)
        else:
            lines.append(' '.join(line))
            line_widths.append(line_bbox[2] - line_bbox[0])
            line = [word]
    # Add the last line
    lines.append(' '.join(line))
    line_widths.append(draw.textbbox((0, 0), line[-1], font=font)[2])
    
    # Calculate total height of text blocks to center vertically
    total_text_height = len(lines) * text_height
    if number_i==0:
        start_y= 200
    else:
        start_y = (image_height - total_text_height) // 2 if total_text_height < image_height else 0
    
    # Calculate the coordinates for each line of text
    text_coordinates = []
    for i, line in enumerate(lines):
        line_width = line_widths[i]
        start_x = (image_width - line_width) // 2
        start_x=abs(start_x)
        coordinate = (start_x, start_y + i * (1.32*text_height))
        text_coordinates.append((line, coordinate))
    
    return text_coordinates


def create_funnel_text_placement(text, number_i,image_width=1080, image_height=1920, font_path = PROJECT_PATH+ "\Bookman Old Style Bold Italic.ttf" , font_size=FONT_SIZE):
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(Image.new('RGB', (image_width, image_height)))

    words = text.split()
    lines = []
    # Start with the longest line in the middle and decrease the length of each subsequent line
    max_line_length = min(image_width, draw.textlength(text, font=font))
    while words:
        line = []
        while words and draw.textlength(' '.join(line + [words[0]]), font=font) <= max_line_length:
            line.append(words.pop(0))
        lines.append(' '.join(line))
        # Reduce the max line length for the next line
        max_line_length *= 0.9  # Reduce line length by 10%

    # Center the lines vertically
    bbox = draw.textbbox((0, 0), text, font=font)
    text_height = bbox[3] - bbox[1]
    total_text_height = len(lines) * text_height
    if number_i==0:
        start_y= 200
    else:
        start_y = (image_height - total_text_height) // 2 if total_text_height < image_height else 0

    # Create text placements
    text_placements = []
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), text, font=font)
        text_height = bbox[3] - bbox[1]
        text_width = draw.textlength(line, font=font)
        start_x = (image_width - text_width) // 2
        text_placements.append((line, (start_x, start_y)))
        start_y += (1.32*text_height)

    return text_placements



def get_json_for_moviepy_with_text_coordinates(json_for_moviepy):
    for i,text_object in enumerate(json_for_moviepy['overlay_texts']):
        text_sentence=text_object["text"]
        text_and_coordinates_list=create_funnel_text_placement(text_sentence,number_i=i)
        text_piece_json_list=[]
        for each_text_object in text_and_coordinates_list:
            text_piece_json={
                "text_piece":each_text_object[0],
                "coordinates":each_text_object[1]
            }
            text_piece_json_list.append(text_piece_json)
        text_object["text"]=text_piece_json_list

    return json_for_moviepy
    













# json_for_moviepy={
# 'audio_file_path': 'C:\\Users\\Rohan\\Desktop\\march\\youtube_shorts\\backend\\audio_files\\Money_psychology.mp3', 
# 'image_path': 'C:\\Users\\Rohan\\Desktop\\march\\youtube_shorts\\backend\\images\\Money_psychology.png', 
# 'overlay_texts': [
#     {
#         'text': 'Ever wondered why you feel richer when holding cold hard cash?', 
#         'start_time': 0, 
#         'duration': 3.93
#     }, 
#     {
#         'text': 'Your brain perceives physical money as more valuable than digital currency.', 
#         'start_time': 3.93, 
#         'duration': 4.58
#     }
#                 ]
# }


# print(get_json_for_moviepy_with_text_coordinates(json_for_moviepy))



# {
#     'audio_file_path': 'C:\\Users\\Rohan\\Desktop\\march\\youtube_shorts\\backend\\audio_files\\Money_psychology.mp3', 
#     'image_path': 'C:\\Users\\Rohan\\Desktop\\march\\youtube_shorts\\backend\\images\\Money_psychology.png', 
#     'overlay_texts': [
#         {
#         'text': [
#             {
#                 'text': 'Ever wondered why you', 
#                 'coordinates': (-52, 849)
#             }, 
#             {
#                 'text': 'feel richer when holding', 
#                 'coordinates': (-88, 923)
#             }, 
#             {
#                 'text': 'cold hard cash?', 
#                 'coordinates': (413, 997)
#             }
#             ], 
#             'start_time': 0, 
#             'duration': 3.93
#         }, 
#         {
#         'text': [
#             {
#                 'text': 'Your brain perceives', 
#                 'coordinates': (-87, 812)
#             }, 
#             {
#                 'text': 'physical money as more', 
#                 'coordinates': (-166, 886)
#             }, 
#             {
#                 'text': 'valuable than digital', 
#                 'coordinates': (-120, 960)
#             }, 
#             {
#                 'text': 'currency.', 
#                 'coordinates': (341, 1034)
#             }
#             ], 
#             'start_time': 3.93, 
#             'duration': 4.58
#         }
#     ]
# }