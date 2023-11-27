import streamlit as st
import streamlit.components.v1 as components
import steiner_tree_demo

st.set_page_config(page_title="Jake's Net Graph Lab")

st.title(':cat2: Multi-modal relation resolution with Steiner tree traversal! :cat2:')
    
def main():
    
    similarity_index_control = st.slider('Similarity Index Relation Threashold',min_value=0.00,max_value=1.01, value=1.01)
    
    # Check if the state variables exist, otherwise initialize them
    if 'start-nodes-key' not in st.session_state:
        st.session_state['start-nodes-key'] =  'users.email'
    if 'target-nodes-key' not in st.session_state:
        st.session_state['target-nodes-key'] = 'order_details.product_id'

    # Create two text input fields
    start_nodes = st.text_input("Starting Node(s)", 'users.email')
    target_nodes = st.text_input("Target Node(s)", 'order_details.product_id')
    if start_nodes is not None:
        st.session_state['start-nodes-key'] = start_nodes
    if target_nodes is not None:
        st.session_state['target-nodes-key'] = target_nodes
        
    if st.button("Draw Graph"):
        steiner_tree_demo.auto_relation(similarity_index_control,st.session_state['start-nodes-key'],st.session_state['target-nodes-key'])
        HtmlFile = open("front.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read() 
        components.html(source_code)
            
main()
