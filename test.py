from gradio_client import Client
from PIL import Image

# Create a client and specify the API URL
client = Client("https://huggingface-projects-qr-code-ai-art-generator--58b6vlwzv.hf.space/")

# Make a prediction
result = client.predict(
    "https://my-url-here.com",      # str  in 'QR Code Content' Textbox component
    "red bus",                 # str  in 'Prompt' Textbox component
    "blue",                    # str  in 'Negative Prompt' Textbox component
    1,                         # int | float (numeric value between 0.0 and 50.0) in 'Guidance Scale' Slider component
    1,                         # int | float (numeric value between 0.0 and 5.0) in 'Controlnet Conditioning Scale' Slider component
    0.9,                       # int | float (numeric value between 0.0 and 1.0) in 'Strength' Slider component
    -1,                        # int | float (numeric value between -1 and 9999999999) in 'Seed' Slider component
    "https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png",    # str (filepath or URL to image) in 'Init Image (Optional). Leave blank to generate image with SD 2.1' Image component
    "https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png",    # str (filepath or URL to image) in 'QR Code Image (Optional). Leave blank to automatically generate QR code' Image component
    True,                      # bool  in 'Use QR code as init image' Checkbox component
    "DPM++ Karras SDE",        # str (Option from: ['DPM++ Karras SDE', 'DPM++ Karras', 'Heun', 'Euler', 'DDIM', 'DEIS']) in 'Sampler' Dropdown component
    fn_index=0
)

# View the image
Image.open(result)
