import streamlit as st

import whisper

from gpt_index import Document, GPTListIndex, GPTTreeIndex

import openai
openai.api_key = "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"

import os
os.environ["OPENAI_API_KEY"] = "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"

model = whisper.load_model("base")
#------------------------------------------------------------


#------------------------------------------------------------


#------------------------------------------------------------
st.write("""
         # Detect Themes in a Video
         """
         )

file = st.file_uploader("Upload a video file here:", type=["mp4"])

if file:
    vid_filename = file.name
    with open(vid_filename, mode='wb') as f:
        f.write(file.read())
        #------------------------------------------------------------
        # Extract themes:
        result = model.transcribe(vid_filename, language="en", without_timestamps =False)
        vid_text = result['text'].strip()
        doc = Document(vid_text)
        docs = [doc]
        index = GPTTreeIndex(docs)
        response = index.query("generate top 3 themes with their description", mode="summarize")
        markdown_string = f"<b>{response}</b>"
        string_without_markdown = markdown_string.replace("<b>", "").replace("</b>", "")
        list_of_themes = string_without_markdown.strip().split('\n\n')
        #------------------------------------------------------------
        videos = st.container()
        with videos:
            _left, _right = st.columns([1, 1])
             
            with _left:
                st.write('Uploaded Video')
                st.video(vid_filename)
            
            with _right:
                st.write('Themes')
                for _ in list_of_themes:
                    st.write(f"{_}")

    

