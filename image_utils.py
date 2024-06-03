import os
import requests
from moviepy.editor import ImageClip
from PIL import Image
from config import *

class GetImages:
    def __init__(self):
        pass

    def getImages(self, search_term):
        headers = {"Ocp-Apim-Subscription-Key": BING_IMAGE_SEARCH_KEY}
        search_term = search_term if search_term else "Black image"

        params = {
            "q": search_term,
            "license": "Public",
            "count": 35,
            "aspect": "Wide",
            "minWidth": 480,
            "minHeight": 270,
        }  # the ratio for the image is 16:9
        response = requests.get(
            BING_IMAGE_SEARCH_URL, headers=headers, params=params
        )
        response.raise_for_status()
        search_results = response.json()
        urls = []

        for ele in search_results["value"]:
            try:
                if ele["encodingFormat"] in ("jpeg", "png"):
                    urls.append(ele["contentUrl"])
                else:
                    pass
            except KeyError:
                print("Key Error")
        return urls

    def downloadImage_0(self, url, filename):
        try:
            response = requests.get(url)
        except Exception:
            return "error"

        if response.status_code:
            fp = open(filename, "wb")
            fp.write(response.content)
            fp.close()
        return filename

    def downloadImage(self,urls, filename):
        target_size = (1080, 1920)  # Target dimensions for resizing

        for url in urls:
            try:
                response = requests.get(url)
                response.raise_for_status()  # This will raise an HTTPError if the download failed

                # Save the image temporarily
                # temp_filename = filename + ".temp"
                file_path=filename
                file_dir, file_name = os.path.split(file_path)
                file_base_name, file_extension = os.path.splitext(file_name)
                new_file_base_name = file_base_name + "_temp"
                new_file_path = os.path.join(file_dir, new_file_base_name + file_extension)
                temp_filename=new_file_path


                with open(temp_filename, "wb") as fp:
                    fp.write(response.content)

                # Try to open the image to verify it's not corrupted and resize it
                try:
                    with Image.open(temp_filename) as img:
                        img.verify()  # Verify the image integrity

                        # Re-open the image for editing since img.verify() leaves the file in an unusable state
                        img = Image.open(temp_filename)

                        # Check if the image has an alpha channel or is not in desired format
                        # Including 'P' mode to exclude paletted images
                        if img.mode in ["RGBA", "LA", "P"]:
                            raise ValueError(
                                "Image is 3-dimensional or not in desired format."
                            )
                        
                        # Resizing the image with Pillow
                        resized_img = img.resize(target_size, Image.Resampling.LANCZOS)
                        
                        # Saving the resized image
                        resized_img.save(filename)
                        os.remove(temp_filename)  # Remove the temporary file
                        print("Image Downloaded and Resized")
                        return filename
                except (OSError, SyntaxError, ValueError, AttributeError) as e:
                    print(f"Image failed verification or resizing: {e}")
                    os.remove(temp_filename)  # Remove the corrupted or temporary file

            except Exception as e:
                print(f"Error downloading image from {url}: {e}")

            # If no valid image was downloaded
        return None


    def get_image_path(self, file_path, image_description):
        urls = self.getImages(image_description)
        print(urls)
        file_path = self.downloadImage(urls, file_path)
        return file_path


