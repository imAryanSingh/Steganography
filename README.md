# Image, Audio & Emoji Steganography
 
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Status](https://img.shields.io/badge/Status-Complete-1D9E75?style=for-the-badge)
![IIT Ropar](https://img.shields.io/badge/Built_at-IIT_Ropar-orange?style=for-the-badge)
<div align="center">
**A Python toolkit for hiding secret messages inside images, audio files, and emojis — three independent steganography techniques in one project.**
 
*Developed as part of the AI Vicharana Shala programme at IIT Ropar (CSE Dept. × iHub-AWaDH)*
 
[Overview](#overview) · [Techniques](#techniques) · [Demo](#demo) · [Setup](#setup) · [How It Works](#how-it-works) · [Use Cases](#use-cases)
 
</div>
---
 
## Overview
 
Steganography is the art of hiding information inside other data so that its very existence is secret — unlike encryption, which hides the *content*, steganography hides the *fact* that a message exists at all. This project implements three distinct steganography techniques in Python:
 
| Technique | Cover Medium | Method | Detection Resistance |
|-----------|-------------|--------|---------------------|
| **Image** | PNG / BMP | LSB (Least Significant Bit) | High — no visible change |
| **Audio** | WAV | LSB in audio samples | High — inaudible |
| **Emoji** | Unicode text | Zero-width characters | Very high — invisible |
 
---
 
## Demo
 
### Image Steganography — before and after
 
**Original image → image with hidden message embedded**
 
| Original | With hidden message |
|----------|-------------------|
| ![Original](Screenshot%202024-09-24%20230401.png) | ![Encoded](Screenshot%202024-09-24%20230424.png) |
 
> The two images are visually identical. The difference exists only at the binary level (LSB of pixel values).
 
**Decoded output — message successfully extracted:**
 
![Decoded](Screenshot%202024-09-24%20230440.png)
 
---
 
## Techniques
 
### 1. Image Steganography (LSB)
 
```
Original pixel:  [10110110]  [11001010]  [10101011]
                     R           G           B
 
Secret bit:          1           0           1
 
Modified pixel:  [10110111]  [11001010]  [10101011]
                     ↑                       ↑
               bit flipped            bit flipped
               (imperceptible change of 1/255 in brightness)
```
 
- Embeds 1 bit per colour channel (RGB) per pixel
- 3 megapixel image = ~1.1 MB of hidden data capacity
- Uses OpenCV to read/write pixel values
- Extraction reverses the process — reads LSB of each channel
### 2. Audio Steganography (LSB)
 
```
Audio sample (16-bit):  1001101010110110
Secret bit:                             1
 
Modified sample:        1001101010110111
                                        ↑
                              last bit changed
                    (change = 1/65536 of full scale — completely inaudible)
```
 
- Embeds 1 bit per audio sample using Python's `wave` module
- Human hearing threshold: changes below ~0.003% amplitude are inaudible
- LSB modification = 0.0015% change — well below detection threshold
- Works on uncompressed WAV files
### 3. Emoji Steganography (Zero-Width Characters)
 
```
Visible text:    "Hello!"
Hidden message:  "secret"
 
Encoded:         "Hello!​‌‍​‌‍​‌‍..."
                        ↑↑↑↑↑↑↑↑
            Zero-width characters invisible to human eye
            but present in Unicode string
```
 
- Maps each character to a sequence of zero-width Unicode characters
  - `\u200b` (Zero Width Space) = binary 0
  - `\u200c` (Zero Width Non-Joiner) = binary 1
- Hidden message is completely invisible in any text display
- Useful for watermarking text documents
---
 
## Setup
 
### Requirements
 
```bash
pip install opencv-python numpy emoji
```
 
Full dependencies:
```
opencv-python>=4.5.0
numpy>=1.21.0
emoji>=2.0.0
```
> **Note:** Audio steganography uses Python's built-in `wave` module — no additional install needed.
 
### Clone and run
 
```bash
git clone https://github.com/imAryanSingh/Steganography.git
cd Steganography
pip install opencv-python numpy emoji
python Steganography.py
```
 
---
 
## How It Works
 
### Image — encode & decode
 
```python
# ENCODE: hide message in image
python Steganography.py
# Select option 1 (Image Steganography)
# Enter: input image path, secret message, output image path
 
# DECODE: extract message from image
# Select option 1 → decode
# Enter: encoded image path
# Output: original secret message
```
 
### Audio — encode & decode
 
```python
# ENCODE: hide message in audio
# Select option 2 (Audio Steganography)
# Enter: input WAV file, secret message, output WAV file
 
# DECODE: extract from audio
# Select option 2 → decode
# Enter: encoded WAV file
# Output: original secret message
```
 
### Emoji — encode & decode
 
```python
# ENCODE: hide message in text using emojis/zero-width chars
# Select option 3 (Emoji Steganography)
# Enter: cover text, secret message
 
# DECODE: extract from emoji text
# Select option 3 → decode
# Enter: encoded text
# Output: original secret message
```
 
---
 
## Project Architecture
 
```
Steganography.py
│
├── ImageSteganography class
│   ├── encode(image_path, message, output_path)
│   │     → reads pixels → embeds bits → saves new image
│   └── decode(image_path)
│         → reads pixels → extracts LSBs → reconstructs message
│
├── AudioSteganography class
│   ├── encode(audio_path, message, output_path)
│   │     → reads WAV samples → embeds bits → writes new WAV
│   └── decode(audio_path)
│         → reads WAV samples → extracts LSBs → reconstructs message
│
└── EmojiSteganography class
    ├── encode(cover_text, secret_message)
    │     → converts chars to binary → inserts zero-width chars
    └── decode(encoded_text)
          → extracts zero-width chars → converts binary → message
```
 
---
 
## Capacity Calculator
 
How much data can you hide?
 
| Cover Medium | File Size | Hidden Capacity |
|-------------|-----------|----------------|
| 1MP image (PNG) | ~3 MB | ~375 KB of text |
| 5MP image (PNG) | ~15 MB | ~1.87 MB of text |
| 1 min WAV (CD quality) | ~10 MB | ~1.25 MB |
| 5 min WAV | ~50 MB | ~6.25 MB |
 
---
 
## Use Cases
 
| Application | Technique | Why |
|-------------|-----------|-----|
| Digital watermarking | Image LSB | Embed copyright info invisibly |
| Covert communication | Any | Message existence is deniable |
| Document authentication | Emoji/text | Hidden integrity check |
| CTF / security challenges | All three | Classic steganography puzzle |
| Research in ML-based steganalysis | Image | Generate training data |
 
---
 
## Security Note
 
LSB steganography is a *basic* technique — it can be detected by statistical analysis (steganalysis tools like StegExpose). This project is educational and demonstrates the core principles. Production-grade steganography uses more sophisticated approaches (DCT domain embedding, adaptive bit allocation, deep learning-based methods).
 
---
 
## Technologies
 
| Library | Purpose |
|---------|---------|
| OpenCV | Image read/write, pixel manipulation |
| NumPy | Array operations on pixel/sample data |
| wave (stdlib) | WAV audio file read/write |
| emoji | Emoji character lookup and encoding |
 
---
 
## About the Author
 
**Aryan Singh** — AI/ML Engineer
 
[![LinkedIn](https://img.shields.io/badge/LinkedIn-im--aryan--singh-0A66C2?style=flat&logo=linkedin)](https://linkedin.com/in/im-aryan-singh)
[![GitHub](https://img.shields.io/badge/GitHub-imAryanSingh-181717?style=flat&logo=github)](https://github.com/imAryanSingh)
[![Portfolio](https://img.shields.io/badge/Portfolio-imAryanSingh.github.io-534AB7?style=flat)](https://imAryanSingh.github.io)
 
*Developed during the AI Vicharana Shala residential programme at IIT Ropar (May–Jul 2024)*
 
---
 
## Also see
 
- [Wake-Word Detection for ISRO TRISHNA Satellite](https://github.com/imAryanSingh/Wakeup-Word-Detection-Model-for-voice-commanding-system) — CNN + MFCC, built at ISRO SAC Ahmedabad
- [Recommendation System for Retail Stores](https://github.com/imAryanSingh/Recommendation-System-for-Retail-Stores) — Collaborative filtering, IIT Ropar
- [Smart Vision Quality Control](https://github.com/imAryanSingh) — Top 0.3% Flipkart GRID 6.0
 



