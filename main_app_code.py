import tkinter as tk
import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
from authtoken import auth_token

import torch
from torch import autocast
from diffusers import StableDiffusionPipeline, StableDiffusionXLPipeline

# Initialize app
app = ctk.CTk()
app.geometry("1200x600")  # Wider window for 4 images in a row
app.title("AI Image Generator with Stable Diffusion")
ctk.set_appearance_mode("dark")

# Create main frame
frame = ctk.CTkFrame(master=app, fg_color="#2a2d2e")
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Title Label
title_label = ctk.CTkLabel(master=frame, text="Stable Diffusion AI", font=("Arial", 24, "bold"))
title_label.pack(pady=10)

# Model selection dropdown
model_options = {
    "Stable Diffusion v1.4": "CompVis/stable-diffusion-v1-4",
    "Stable Diffusion v2.1": "stabilityai/stable-diffusion-2-1",
    "Stable Diffusion XL": "stabilityai/stable-diffusion-xl-base-1.0",
    "DreamShaper v7": "Lykon/dreamshaper-7"
}
selected_model = ctk.StringVar(value="DreamShaper v7")
model_menu = ctk.CTkOptionMenu(master=frame, values=list(model_options.keys()), variable=selected_model, command=lambda _: update_prompt_menu())
model_menu.pack(pady=5)

# Predefined prompts for each model
prompt_library = {
    "Stable Diffusion v1.4": [
        "A futuristic cityscape at sunset",
        "A beautiful fantasy castle on a mountain",
        "A cyberpunk street with neon lights",
        "A hyper-realistic portrait of an astronaut"
    ],
    "Stable Diffusion v2.1": [
        "An enchanted forest with glowing plants",
        "A surreal dreamscape with floating islands",
        "A sci-fi spaceship exploring deep space",
        "A magnificent waterfall in the jungle"
    ],
    "Stable Diffusion XL": [
        "A breathtaking landscape with aurora borealis",
        "A detailed steampunk city with airships",
        "A mystical dragon soaring over the clouds",
        "A cinematic cyberpunk scene with reflections"
    ],
    "DreamShaper v7": [
        "A fantasy warrior in golden armor",
        "A magical wizard casting a spell",
        "A majestic lion with a glowing mane",
        "A peaceful village in a winter wonderland"
    ]
}

# Dropdown for selectable prompts
selected_prompt = ctk.StringVar(value=prompt_library["DreamShaper v7"][0])
prompt_menu = ctk.CTkOptionMenu(master=frame, values=prompt_library["DreamShaper v7"], variable=selected_prompt, command=lambda _: update_prompt_box())
prompt_menu.pack(pady=5)

# Multi-line prompt input
prompt_box = ctk.CTkTextbox(master=frame, height=80, width=1100, font=("Arial", 16))
prompt_box.pack(pady=10)

# Update prompt box when a predefined prompt is selected
def update_prompt_box():
    prompt_box.delete("1.0", "end")
    prompt_box.insert("1.0", selected_prompt.get())

# Update prompt dropdown when model changes
def update_prompt_menu():
    new_model = selected_model.get()
    prompt_menu.configure(values=prompt_library[new_model])
    selected_prompt.set(prompt_library[new_model][0])
    update_prompt_box()

# Generate Button
generate_button = ctk.CTkButton(
    master=frame,
    text="Generate Images",
    command=lambda: generate(),
    fg_color="#007BFF",
    hover_color="#0056b3",
    font=("Arial", 16, "bold"),
    width=200,
    height=40
)
generate_button.pack(pady=10)

# Status label
status_label = ctk.CTkLabel(master=frame, text="", font=("Arial", 14))
status_label.pack(pady=5)

# Image Frame (for 4 images in a row)
image_frame = ctk.CTkFrame(master=frame, fg_color="transparent", width=1100, height=256)
image_frame.pack_propagate(False)
image_frame.pack(pady=10)

# Create 4 image placeholders
image_labels = []
for j in range(4):
    img_display = ctk.CTkLabel(master=image_frame, text="No Image", height=256, width=256, fg_color="gray")
    img_display.grid(row=0, column=j, padx=5, pady=5)
    image_labels.append(img_display)

# Load Stable Diffusion Model
device = "cuda"

# Generate image function
def generate():
    prompt = prompt_box.get("1.0", "end").strip()
    if not prompt:
        status_label.configure(text="⚠️ Please enter a prompt!", text_color="red")
        return
    
    status_label.configure(text="🛠️ Generating... Please wait.", text_color="yellow")
    app.update_idletasks()

    # Load selected model
    model_id = model_options[selected_model.get()]

    # Handle Stable Diffusion XL separately
    if model_id == "stabilityai/stable-diffusion-xl-base-1.0":
        pipe = StableDiffusionXLPipeline.from_pretrained(model_id, variant="fp16", torch_dtype=torch.float16, token=auth_token)
    else:
        pipe = StableDiffusionPipeline.from_pretrained(model_id, variant="fp16", torch_dtype=torch.float16, token=auth_token)

    pipe.to(device)

    images = []
    for _ in range(4):  # Generate 4 images
        with autocast(device):
            if model_id == "stabilityai/stable-diffusion-xl-base-1.0":
                result = pipe(prompt, guidance_scale=8.5, added_cond_kwargs={"text_embeds": torch.zeros(1, 768).to(device)})
            else:
                result = pipe(prompt, guidance_scale=8.5)
            images.append(result.images[0])

    # Display images in a row
    for j in range(4):
        img = images[j]
        img = img.resize((256, 256))  # Resize to fit UI
        img.save(f"generated_image_{j+1}.png")

        ctk_image = CTkImage(light_image=img, size=(256, 256))
        image_labels[j].configure(image=ctk_image, text="")
        image_labels[j].image = ctk_image  

    status_label.configure(text="✅ Images Generated!", text_color="green")

# Run app
app.mainloop()
