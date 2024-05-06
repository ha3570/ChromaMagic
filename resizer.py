import PySimpleGUI as sg
import cv2
import os

def resize_image(image_path, target_resolution, save_path):
    resolutions = {
        "360p": (480, 360),
        "480p": (640, 480),
        "720p": (1280, 720)
    }

    if target_resolution not in resolutions:
        sg.popup_error("Invalid resolution selected.")
        return

    try:
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            sg.popup_error("Failed to read the image file.")
            return

        # Resize the image
        resized_image = cv2.resize(image, resolutions[target_resolution])

        # Get the directory and filename without extension
        directory, filename = os.path.split(image_path)
        filename_no_extension, extension = os.path.splitext(filename)

        # Construct the new filename with resolution suffix
        new_filename = f"{filename_no_extension}_{target_resolution}{extension}"

        # Construct the save path
        save_filepath = os.path.join(save_path, new_filename)

        # Save the resized image
        cv2.imwrite(save_filepath, resized_image)

        sg.popup(f"Image resized and saved as: {new_filename}")

    except Exception as e:
        sg.popup_error(f"An error occurred: {str(e)}")

def get_save_location():
    folder_path = sg.popup_get_folder("Select save location")
    if folder_path:
        return folder_path
    else:
        return None

def convert_to_grayscale(image_path):
    try:
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            sg.popup_error("Failed to read the image file.")
            return

        # Convert the image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        return gray_image

    except Exception as e:
        sg.popup_error(f"An error occurred: {str(e)}")
        return None

# GUI layout
layout = [
    [sg.Text("Select an image file:")],
    [sg.InputText(key='-IN FILE-', enable_events=True), sg.FileBrowse()],
    [sg.Text("Select target resolution:")],
    [sg.Combo(['360p', '480p', '720p'], default_value='360p', key='-RESOLUTION-')],
    [sg.Text("Save location:")],
    [sg.InputText(key='-SAVE LOCATION-'), sg.FolderBrowse()],
    [sg.Checkbox("Convert to grayscale", key='-GRAYSCALE-')],
    [sg.Button("Resize and Save")]
]

window = sg.Window("Image Resizer", layout)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == "Resize and Save":
        image_path = values['-IN FILE-']
        target_resolution = values['-RESOLUTION-']
        save_path = values['-SAVE LOCATION-']
        grayscale = values['-GRAYSCALE-']

        if image_path:
            if save_path:
                if grayscale:
                    gray_image = convert_to_grayscale(image_path)
                    if gray_image is not None:
                        image_path = os.path.join(save_path, "grayscale_" + os.path.basename(image_path))
                        cv2.imwrite(image_path, gray_image)
                resize_image(image_path, target_resolution, save_path)
            else:
                sg.popup_error("Please select a save location.")
                save_path = get_save_location()
                if save_path:
                    if grayscale:
                        gray_image = convert_to_grayscale(image_path)
                        if gray_image is not None:
                            image_path = os.path.join(save_path, "grayscale_" + os.path.basename(image_path))
                            cv2.imwrite(image_path, gray_image)
                    resize_image(image_path, target_resolution, save_path)

window.close()
