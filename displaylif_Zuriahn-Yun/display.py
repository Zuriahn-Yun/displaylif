from readlif.reader import LifFile
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import time
from plotly.subplots import make_subplots
import pandas as pd 

def analyze_lif(file_path):
    try:
        lif_file = LifFile(file_path)
        
        """ Display How many Images """
        image_count = lif_file
        print(image_count)
        
        """ Retrieve a frame from the lif image """
        lif_image = lif_file.get_image(0)
        pil_image = lif_image.get_frame(z=0)
        
        """ Convert to numpy array """
        np_image = np.array(pil_image)
        print(np_image.shape)
        
        """ Display Image """
        fig = px.imshow(np_image)
        print(fig)
        fig.show()        
         
    except Exception as e:
        print('Error: ' + str(e))

def display_lif(file_path,rows,columns):
    
    lif = LifFile(file_path)
    fig = make_subplots(rows,columns)
    print(lif)
    curr_row = 1
    curr_column = 1
    for image in lif.get_iter_image():
        print(image)
        for frame in image.get_iter_t():
            print(frame)
            np_image = np.array(frame)
            curr_px = px.imshow(np_image)
            trace = curr_px.data[0]
            fig.add_trace(trace, row=curr_row, col=curr_column)
            
            curr_column +=1 
            if curr_column == columns + 1:
                curr_row +=1
                curr_column = 1
            print(curr_row)
            print(curr_column)
            # fig.show()
            # time.sleep(60)
            # fig.add_trace(go.Image(z=np_image), row=1, col=2)
    fig.update_layout(height=512 * rows, width=512 * columns, showlegend=False)
    fig.show()
            
def display(file_path,rows,columns):
    """ This displays a lif file in plotly

    Args:
        file_path (_type_): _description_
        rows (_type_): _description_
        columns (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    # add all the images to one list
    images = []
    lif = LifFile(file_path)
    for image in lif.get_iter_image():
        print(image)
        for frame in image.get_iter_t():
            np_image = np.array(frame)
            images.append(np_image)
    
    # Concat every row and add to a list
    row_dataframes = []

    for i in range(rows):
        curr = []
        for k in range(columns):
            df = pd.DataFrame(images[(i * columns) + k])
            curr.append(df)
        curr_row = pd.concat(curr,axis=1,ignore_index=True)
        row_dataframes.append(curr_row)
    
    # Concat all the rows into one very large dataframe
    result = pd.concat(row_dataframes, axis=0,ignore_index=True)

    # Display the final image
    fig = px.imshow(result)
    fig.show()   
    
    # Return the Dataframe
    return result