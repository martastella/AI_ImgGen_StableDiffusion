# AI Image Generator with Stable Diffusion

This project allows you to generate images using Stable Diffusion models. It's built using Python, the `customtkinter` library for the UI, and the `diffusers` library for interacting with Stable Diffusion models.

## Features
- Generate up to 4 images at once.
- Select between different Stable Diffusion models (v1.4, v2.1, XL, DreamShaper).
- Use predefined prompts or custom input.
- Easy-to-use GUI built with `customtkinter`.

## Requirements
Before running the project, make sure you have the following dependencies installed. You can install them using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Setup

### 1. **Create `authtoken.py`**
To access the Stable Diffusion models, you will need an authentication token. Create a file named `authtoken.py` in the same directory as your main project file (`main_app_code.py`). The file should contain the following line:

```python
auth_token = 'your_auth_token_here'
```

You can get the auth token by registering on [Hugging Face](https://huggingface.co/) and visiting your [settings page](https://huggingface.co/settings/tokens).

### 2. **Run the App**
Once everything is set up, you can run the application with:

```bash
python main_app_code.py
```

This will open the GUI, where you can select models, input prompts, and generate images.

### How to Use
- **Model Selection**: Choose the model you want to use from the dropdown (e.g., "Stable Diffusion v1.4", "Stable Diffusion v2.1", "Stable Diffusion XL", or "DreamShaper v7").
- **Prompt Selection**: Either choose a predefined prompt from the dropdown or type your own custom prompt into the textbox.
- **Generate Images**: Once you’ve chosen the model and prompt, click on the "Generate Images" button to start the generation process. The generated images will be displayed on the screen.

### Generated Files
Once images are generated, they will be saved in the local directory as `generated_image_1.png`, `generated_image_2.png`, etc.

![Generated Image 1](generated_image_2.png)

![Generated Image 2](generated_image_4.png)

### Video Demo
You can watch a demo of the application in action below:

<video controls>
  <source src="20250309-1146-17.3600820.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

### Troubleshooting
- If the application fails to load or generate images, make sure the `authtoken.py` file is properly set up.
- Ensure that you have all the dependencies installed via `requirements.txt`.
