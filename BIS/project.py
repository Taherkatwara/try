import cv2

def text_to_binary(text):
    binary_data = ' '.join(format(ord(char), '08b') for char in text)
    return binary_data

def hide_text_in_video(video_path, text, output_path):
    binary_text = text_to_binary(text)
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    text_index = 0

    for _ in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            break

        if text_index < len(binary_text):
            for row in frame:
                for pixel in row:
                    for i in range(3):  # For RGB, use range(3); for grayscale, use range(1)
                        pixel[i] = pixel[i] & ~1 | int(binary_text[text_index])
                        text_index += 1
                        if text_index >= len(binary_text):
                            break
                    if text_index >= len(binary_text):
                        break
                if text_index >= len(binary_text):
                    break

        out.write(frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

def extract_text_from_video(video_path):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    binary_text = ''
    text_index = 0

    for _ in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            break

        for row in frame:
            for pixel in row:
                for i in range(3):  # For RGB, use range(3); for grayscale, use range(1)
                    binary_text += str(pixel[i] & 1)
                    text_index += 1
                    if text_index >= 8:
                        text = ''.join(chr(int(binary_text[i:i+8], 2)) for i in range(0, len(binary_text), 8))
                        return text.strip()

    cap.release()
    cv2.destroyAllWindows()

# Example usage:
input_video_path = "input_video.mp4"
text_to_hide = "Hello, this is a secret message!"
output_video_path = "output_video_encoded.mp4"

# Hide text in the video
hide_text_in_video(input_video_path, text_to_hide, output_video_path)

# Extract hidden text from the video
extracted_text = extract_text_from_video(output_video_path)
print("Extracted text:", extracted_text)
