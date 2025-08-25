from readlif.reader import LifFile
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots
import pandas as pd 
from readlif.reader import LifFile
import numpy as np
from PIL import Image
import readlif
import pandas as pd 
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Percentiles 75 = 0.75 percent
red_percentile = 75
green_percentile = 30
blue_percentile = 30

# Display LIF using Median Projection
def displaylif(filepath):

    lif = LifFile(filepath)

    image_list = []

    for image_idx, image in enumerate(lif.get_iter_image()):
        print(f"Processing image {image_idx + 1}/48")
        print(f"Image Dimensions {image.dims}")
        z_stack_size = image.dims[2]  # 75 Z-Slices
        
        # Grab each Channel to process
        channel_max_projections = []
        
        for channel in range(3):  # 3 channels (Red, Green, Blue)
            # GRab all the Z-Slices
            z_slices = []
            for z in range(z_stack_size):
                frame = image.get_frame(z=z, t=0, c=channel)
                z_slices.append(np.array(frame))
            
            # Stack and take maximum projection for this channel
            # np.max -> for Maximum Intensity Projection
            # np.mean -> for Average Intensity Projection
            # np.sum -> for Sum Projection
            # np.median -> for median Projection
            # Could also try PCA
            z_stack = np.stack(z_slices, axis=0)  # Shape: (75, 512, 512)
            max_projection = np.median(z_stack, axis=0)  # Shape: (512, 512)
            channel_max_projections.append(max_projection)
        
        # Combine 3 channels into RGB
        rgb_image = np.stack([
            channel_max_projections[0],  # Red 
            channel_max_projections[1],  # Green 
            channel_max_projections[2]   # Blue 
        ], axis=2)                      # Shape: (512, 512, 3)
        
        # Normalize and convert to uint8
        rgb_image = (rgb_image / rgb_image.max() * 255).astype(np.uint8)
        
        # Convert to PIL and display
        composite_image = Image.fromarray(rgb_image)
        image_list.append(composite_image)
        
    np_images = [np.array(img) for img in image_list]
    total = len(np_images)
    cols = 6 
    rows = (total + cols - 1) // cols

    fig = make_subplots(rows=rows, cols=cols, subplot_titles=[f"Image {i+1}" for i in range(total)])

    for idx, img in enumerate(image_list):
        row = idx // cols + 1
        col = idx % cols + 1

        # Add image to subplot
        fig.add_trace(
            go.Image(z=img),
            row=row, col=col
        )

    fig.update_layout(height=512*rows, width=512*cols, title_text="IHC Cohort 2 6-4-25: Using Median Projection")
    fig.show()
