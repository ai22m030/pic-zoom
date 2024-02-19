import cv2

def create_zoom_effect(input_image_path, output_video_path, duration_sec=5, fps=30, zoom_factor=1.05):
    # Load the image
    image = cv2.imread(input_image_path)
    if image is None:
        raise ValueError(f"Failed to load the image from {input_image_path}. Please check the file path.")

    height, width = image.shape[:2]

    # Calculate the number of frames required
    num_frames = int(duration_sec * fps)

    # Prepare the video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # For an mp4 output
    video = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    if not video.isOpened():
        raise IOError(f"Failed to open the video file for writing at {output_video_path}. Please check the file path and permissions.")

    for i in range(num_frames):
        # Calculate the zoom for this frame
        scale = 1 + (zoom_factor - 1) * (i / float(num_frames - 1))  # Ensure gradual zoom

        # Apply the zoom and keep the image centered
        new_width = int(width / scale)
        new_height = int(height / scale)
        resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

        # Create a border around the resized image to maintain the original dimensions
        x_border = (width - new_width) // 2
        y_border = (height - new_height) // 2
        bordered = cv2.copyMakeBorder(resized, y_border, y_border, x_border, x_border, cv2.BORDER_CONSTANT, value=[0, 0, 0])

        # Ensure the bordered image matches the original dimensions, adjusting if necessary
        bordered = cv2.resize(bordered, (width, height), interpolation=cv2.INTER_LINEAR)

        # Write the frame to the video
        video.write(bordered)

    # Release the video writer
    video.release()
    print(f"Video successfully saved to {output_video_path}")

# Usage
create_zoom_effect('image.jpg', 'output_video.mp4')
