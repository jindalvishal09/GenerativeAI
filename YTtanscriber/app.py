import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


prompt= """You are Youtube Video summarizer. You will be taking the transcript text and summarize 
the entire video and provide the important summary in points within 250 words. 
Please provide the summary of the text given here:: """


# Getting transcript from YT videos
def extract_transcritp_details(video_id):

    try:
        # video_id = youtube_video_URL.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ""

        for i in transcript_text:
            transcript = transcript + i["text"]
                                        
        return transcript

    except Exception as e:
        raise e


#Getting summary from based on prompt

def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    resposne = model.generate_content(prompt+transcript_text)
    return resposne.text


st.title ("Youtube Transcript to Detailed Notes converter")
youtube_link = st.text_input("Enter Youtube video URL")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)


if st.button("Get Detailed Notes"):
    transcript_text = extract_transcritp_details(video_id)

    if transcript_text:
        summary = generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)



