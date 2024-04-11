import streamlit as st
import pandas as pd
import numpy as np
import pickle

basket=pd.read_csv("groceries.csv", header=None)
basket=basket.astype(str)

groceries_list=np.unique(basket.values)
groceries_unique_list=groceries_list[groceries_list!='nan']
pickle_file_path='association_rules.pkl'
try:
    with open(pickle_file_path, 'rb') as f:
        rules_set=pickle.load(f)
except FileNotFoundError:
    st.error("Association rules pickle file not found. Please run the analysis script first.")
    rules_set=None

def main():
    st.markdown(
        """
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
                color: #000000; /* Change color to black */
            }
        </style>
        """
    ,unsafe_allow_html=True)

    st.markdown('<h1 class="scrolling-title">Welcome to Market Basket Analysis</h1>',unsafe_allow_html=True)
    st.sidebar.header('Select Items')
    selected_items=st.sidebar.multiselect('Choose items:', groceries_unique_list)

    if st.sidebar.button('Get Recommendations'):
        if rules_set is not None:
            selected_rules=rules_set[
                rules_set['antecedents'].apply(lambda x: all(item in x for item in selected_items))
            ]

            if not selected_rules.empty:
                recommended_items = get_recommendations(selected_rules)
                if len(recommended_items) > 0:
                    st.header('Recommended Items:')
                    st.write(recommended_items)
                else:
                    st.write('No recommendations found for selected items.')
            else:
                st.write('No recommendations found for selected items.')
        else:
            st.error("No association rules to display. Please run the analysis script first.")

def get_recommendations(selected_rules):
    recommended_items = set()
    for i, row in selected_rules.iterrows():
        consequents = row['consequents']
        for item in consequents:
            recommended_items.add(item)
    return list(recommended_items)

if __name__ == "__main__":
    main()
