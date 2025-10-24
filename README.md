# Steganography Tool
A Python-based GUI application for hiding and extracting secret messages or files within images using steganography techniques. <br>
<img width="700" height="785" alt="image" src="https://github.com/user-attachments/assets/1f930647-005b-44cb-bb01-0e3a57dc2c49" /> <br>
<img width="700" height="783" alt="image" src="https://github.com/user-attachments/assets/b1d6b7e6-ac77-49e3-a41a-ffc00077ae79" />


## Features

- **Encode Messages**: Hide text messages or files within PNG or other images format
- **Decode Messages**: Extract hidden messages or files from encoded images
- **User-Friendly Interface**: Simple and intuitive GUI with drag-and-drop support
- **Supports Multiple Formats**: Works with PNG,BMP and other image formats as well
- **File Hiding**: Can hide any type of file within an image

## Installation

1. Clone this repository or download the source code
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python steganography_tool.py
   ```

### Encoding a Message

1. Click on the "Encode" tab
2. Click "Load Image" to select an image to hide your message in
3. Enter your secret message in the text area or select a file to hide
4. Click "Encode & Save" to save the encoded image

### Decoding a Message

1. Click on the "Decode" tab
2. Click "Load Image" to select an encoded image
3. Click "Decode" to extract the hidden message or file
4. If a file was hidden, click "Save to File" to save the extracted file

## How It Works

This tool uses the LSB (Least Significant Bit) steganography technique to hide data in the least significant bits of the image's pixel values. This makes the changes virtually undetectable to the human eye while allowing for the storage of significant amounts of data.

## Limitations

- The amount of data that can be hidden depends on the size of the image
- The encoded image must be saved in a lossless format to preserve the hidden data
