import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
from PIL import Image

basket=pd.read_csv("groceries.csv",header=None)
basket=basket.astype(str)

basket.replace({
    'cling film/bags': 'cling bags',
    'flower soil/fertilizer': 'flower soil',
    'fruit/vegetable juice': 'fruit juice',
    'nuts/prunes': 'nuts',
    'packaged fruit/vegetables': 'packed fruits and vegetables',
    'photo/film': 'photo film',
    'red/blush wine': 'red wine',
    'rolls/buns': 'buns',
    'whipped/sour cream': 'whipped cream'
}, inplace=True)

groceries_list=np.unique(basket.values)
groceries_unique_list=groceries_list[groceries_list!='nan']

# Background image path
background_image_path="C:\\Users\\srisa\\Desktop\\Coapps Project\\BasketAnalysis-\\bg image.png"

# Path to the folder containing item images
item_images_folder="C:\\Users\\srisa\\Desktop\\Coapps Project\\BasketAnalysis-\\Images"

# Loading the association rules from pickle file
pickle_file_path='association_rules.pkl'
try:
    with open(pickle_file_path, 'rb') as f:
        rules_set = pickle.load(f)
except FileNotFoundError:
    st.error("Association rules pickle file not found")
    rules_set=None

def main():
    # Streamlit app title with scrolling
    st.markdown("""
        <style>
            @keyframes scroll {
                0% {
                    transform: translateX(100%);
                }
                100% {
                    transform: translateX(-100%);
                }
            }
            .scrolling-title {
                white-space: nowrap;
                overflow: hidden;
                animation: scroll 10s linear infinite;
            }
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="scrolling-title">Welcome to Market Basket Analysis</h1>',unsafe_allow_html=True)
  
    # Adding background image to the streamlit interface
    image = Image.open(background_image_path)

    # Field For Selecting Items
    st.sidebar.header('Select Items')
    selected_items=st.sidebar.multiselect('Choose items:',groceries_unique_list)
    show_background=True
    if st.sidebar.button('Get Recommendations'):
        if len(selected_items)==0:
            st.warning("Please select at least one item.")
        elif rules_set is not None:
            selected_rules = rules_set[
                rules_set['antecedents'].apply(lambda x: all(item in x for item in selected_items))
            ]
            if not selected_rules.empty:
                recommended_items = get_recommendations(selected_rules)
                if recommended_items:
                    st.header('Recommended Items:')
                    display_images(recommended_items)
                    show_background=False
                else:
                    st.write('No recommendations found for selected items.')
            else:
                st.write('No recommendations found for selected items.')
        else:
            st.error("No association rules to display")
    
    # Display the background image only if show_background is True
    if show_background:
        # Increased Width Of The Background Image
        st.image(image, caption='Background', width=800)

# Function to get recommended items with image  based on selected rules
def get_recommendations(selected_rules):
    recommended_items={}
    for i,row in selected_rules.iterrows():
        consequents=row['consequents']
        for item in consequents:
            item_image_path=os.path.join(item_images_folder,f"{item}.jpeg")
            if os.path.exists(item_image_path):
                recommended_items[item]=item_image_path
            else:
                pass
    return recommended_items

# Function to display images
def display_images(recommended_items):
    num_columns=3
    num_items=len(recommended_items)
    rows=num_items//num_columns+(num_items%num_columns>0)
    column_items=st.columns(num_columns)
    image_width=200
    image_height=150

    item_index = 0
    for row in range(rows):
        for col in range(len(column_items)):
            if item_index>=num_items:
                break
            item,image_path=list(recommended_items.items())[item_index]
            if image_path and os.path.exists(image_path):
                image=Image.open(image_path)
                image=image.resize((image_width, image_height))
                with column_items[col]:
                    st.image(image, caption=item, use_column_width=True)
            else:
                with column_items[col]:
                    st.write(item)
            item_index+=1

if __name__ == "__main__":
    main()
