import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np
import wave

# Predefined list of emojis
EMOJI_LIST = ['😀', '😂', '😍', '😢', '😎', '🤔', '😡', '🥳', '😱', '👍']

class EmojiSteganographyGUI:
    def __init__(self, master):
        self.master = master

        # Create input fields for message and emojis
        self.message_label = tk.Label(master, text="Message to Encode:")
        self.message_label.pack()
        self.message_entry = tk.Text(master, height=5, width=40)
        self.message_entry.pack()

        self.emojis_label = tk.Label(master, text="Input Emojis (one per line):")
        self.emojis_label.pack()
        self.emojis_entry = tk.Text(master, height=5, width=40)
        self.emojis_entry.pack()

        # Create buttons for encoding and decoding
        self.encode_button = tk.Button(master, text="Encode Message into Emojis", command=self.encode_message)
        self.encode_button.pack(pady=10)
        self.decode_button = tk.Button(master, text="Decode Message from Emojis", command=self.decode_message)
        self.decode_button.pack(pady=10)

        # Create output field for modified emojis
        self.output_label = tk.Label(master, text="Modified Emojis (Encoded):")
        self.output_label.pack(pady=10)
        self.output_text = tk.Text(master, height=5, width=40)
        self.output_text.pack()

    def hide_message_in_emojis(self, message, emojis):
        # Convert the message to binary
        binary_message = ''.join(format(ord(c), '08b') for c in message)

        # Initialize the modified emojis list
        modified_emojis = []

        # Hide the message in the least significant bits of each pixel
        for i in range(len(binary_message)):
            emoji = emojis[i % len(emojis)]
            emoji_array = np.array([ord(c) for c in emoji])
            pixel = emoji_array[0]
            binary_pixel = format(pixel, '08b')
            binary_pixel = binary_pixel[:-1] + binary_message[i]
            emoji_array[0] = int(binary_pixel, 2)
            modified_emoji = ''.join(chr(c) for c in emoji_array)
            modified_emojis.append(modified_emoji)

        return modified_emojis

    def extract_message_from_emojis(self, modified_emojis):
        # Initialize the binary message
        binary_message = ''

        # Extract the message from the least significant bits of each pixel
        for modified_emoji in modified_emojis:
            modified_emoji_array = np.array([ord(c) for c in modified_emoji])
            pixel = modified_emoji_array[0]
            binary_pixel = format(pixel, '08b')
            binary_message += binary_pixel[-1]

        # Convert the binary message to text
        message = ''
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i+8]
            if byte == '00000000':
                break
            message += chr(int(byte, 2))

        return message

    def encode_message(self):
        message = self.message_entry.get("1.0", "end-1c")
        emojis = self.emojis_entry.get("1.0", "end-1c").splitlines()
        modified_emojis = self.hide_message_in_emojis(message, emojis)
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", '\n'.join(modified_emojis))

    def decode_message(self):
        modified_emojis = self.output_text.get("1.0", "end-1c").splitlines()
        message = self.extract_message_from_emojis(modified_emojis)
        messagebox.showinfo("Decoded Message", message)

# Helper functions for audio and image steganography (unchanged)
def generate_random_audio(duration_seconds, output_filename):
    sample_rate = 44100  # Sample rate in Hz
    num_samples = duration_seconds * sample_rate
    noise = np.random.randint(-32768, 32767, num_samples, dtype=np.int16)  # Generate white noise
    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 2 bytes for int16
        wf.setframerate(sample_rate)
        wf.writeframes(noise.tobytes())

def hide_text_in_audio(audio_path, text, output_path):
    audio = wave.open(audio_path, 'rb')
    params = audio.getparams()
    n_samples = params.nframes
    audio_samples = np.frombuffer(audio.readframes(n_samples), dtype=np.int16)

    # Convert text to binary and add terminator
    binary_message = ''.join(format(ord(c), '08b') for c in text) + '11111111'
    binary_message = np.array(list(map(int, binary_message)), dtype=np.int16)

    # Ensure audio_samples is writable
    audio_samples = audio_samples.copy()
    for i in range(len(binary_message)):
        if i >= len(audio_samples): break
        audio_samples[i] = (audio_samples[i] & ~1) | binary_message[i]

    with wave.open(output_path, 'wb') as wf:
        wf.setparams(params)
        wf.writeframes(audio_samples.tobytes())

def reveal_text_from_audio(audio_path):
    audio = wave.open(audio_path, 'rb')
    n_samples = audio.getnframes()
    audio_samples = np.frombuffer(audio.readframes(n_samples), dtype=np.int16)

    extracted_bits = []
    for sample in audio_samples:
        extracted_bits.append(sample & 1)

    message = ""
    for i in range(0, len(extracted_bits), 8):
        byte = extracted_bits[i:i + 8]
        if byte == [1, 1, 1, 1, 1, 1, 1, 1]:  # Terminator
            break
        message += chr(int(''.join(map(str, byte)), 2))

    return message

def encode_message(image_path, message, output_path):
    img = Image.open(image_path).convert('RGB')
    img_array = np.array(img)

    binary_message = ''.join(format(ord(c), '08b') for c in message) + '11111111'

    flat_array = img_array.flatten()

    for i in range(len(binary_message)):
        flat_array[i] = (flat_array[i] & ~1) | int(binary_message[i])

    modified_array = flat_array.reshape(img_array.shape)

    modified_img = Image.fromarray(modified_array.astype('uint8'), 'RGB')
    modified_img.save(output_path)

def decode_message(image_path):
    img = Image.open(image_path).convert('RGB')
    img_array = np.array(img)

    flat_array = img_array.flatten()

    extracted_binary = ''.join([str(pixel & 1) for pixel in flat_array])

    message = ""

    for i in range(0, len(extracted_binary), 8):
        byte = extracted_binary[i:i + 8]
        if byte == '11111111':
            break
        message += chr(int(byte, 2))

    return message

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    image_entry.delete(0, tk.END)
    image_entry.insert(0, file_path)

    img = Image.open(file_path)
    img.thumbnail((200, 200), Image.ANTIALIAS)

    photo = ImageTk.PhotoImage(img)
    image_label.configure(image=photo)
    image_label.image = photo

def select_audio():
    file_path = filedialog.askopenfilename(filetypes=[("WAV Files", "*.wav")])
    audio_entry.delete(0, tk.END)
    audio_entry.insert(0, file_path)

def encode_image():
    image_path = image_entry.get()
    message = message_entry.get()

    output_path = "output_image.png"

    try:
        encode_message(image_path, message, output_path)
        messagebox.showinfo("Success", f"Message encoded successfully!\nEncoded image saved as: {output_path}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def decode_image():
    image_path = image_entry.get()

    try:
        message = decode_message(image_path)
        messagebox.showinfo("Decoded Message", message)

    except Exception as e:
        messagebox.showerror("Error", str(e))

def encode_audio():
    audio_path = audio_entry.get()
    message = audio_message_entry.get()

    output_path = "output_audio.wav"

    try:
        hide_text_in_audio(audio_path, message, output_path)
        messagebox.showinfo("Success", f"Message encoded successfully!\nEncoded audio saved as: {output_path}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def decode_audio():
    audio_path = audio_entry.get()

    try:
        message = reveal_text_from_audio(audio_path)
        messagebox.showinfo("Decoded Message", message)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("Steganography Tool")
root.geometry("600x600")

# Style configuration
style = ttk.Style()
style.configure("TLabel", font=("Arial", 12))
style.configure("TButton", font=("Arial", 10))

# Notebook widget for tabs
notebook = ttk.Notebook(root)

# Image Steganography Tab
image_frame = ttk.Frame(notebook)
notebook.add(image_frame, text="Image Steganography")

image_label = ttk.Label(image_frame, text="Select an Image:")
image_label.pack()

image_entry = ttk.Entry(image_frame, width=40)
image_entry.pack()

image_browse_button = ttk.Button(image_frame, text="Browse", command=select_image)
image_browse_button.pack()

message_label = ttk.Label(image_frame, text="Enter Message:")
message_label.pack()

message_entry = ttk.Entry(image_frame, width=40)
message_entry.pack()

encode_button = ttk.Button(image_frame, text="Encode Image", command=encode_image)
encode_button.pack(pady=10)

decode_button = ttk.Button(image_frame, text="Decode Image", command=decode_image)
decode_button.pack(pady=10)

image_label = ttk.Label(image_frame)
image_label.pack()

# Audio Steganography Tab
audio_frame = ttk.Frame(notebook)
notebook.add(audio_frame, text="Audio Steganography")

audio_label = ttk.Label(audio_frame, text="Select an Audio File:")
audio_label.pack()

audio_entry = ttk.Entry(audio_frame, width=40)
audio_entry.pack()

audio_browse_button = ttk.Button(audio_frame, text="Browse", command=select_audio)
audio_browse_button.pack()

audio_message_label = ttk.Label(audio_frame, text="Enter Message:")
audio_message_label.pack()

audio_message_entry = ttk.Entry(audio_frame, width=40)
audio_message_entry.pack()

encode_audio_button = ttk.Button(audio_frame, text="Encode Audio", command=encode_audio)
encode_audio_button.pack(pady=10)

decode_audio_button = ttk.Button(audio_frame, text="Decode Audio", command=decode_audio)
decode_audio_button.pack(pady=10)

# Emoji Steganography Tab
emoji_frame = ttk.Frame(notebook)
notebook.add(emoji_frame, text="Emoji Steganography")

emoji_steganography_gui = EmojiSteganographyGUI(emoji_frame)

# Pack the notebook
notebook.pack(expand=True, fill="both")

root.mainloop()
