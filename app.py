import os
import sys
import time
from zipfile import ZipFile
import json
import nltk
import requests
import streamlit as st
from nltk.corpus import stopwords
from pytube import YouTube
import glob
import os
import pandas as pd
import numpy as np
from time import process_time
from math import sqrt, acos, cos

nltk.download('stopwords')

st.markdown('# 📝 **Multi-Level deduplication**')
bar = st.progress(0)


# Custom functions

# 2. Retrieving audio file from YouTube video


def get_yt(URL):
    video = YouTube(URL)
    yt = video.streams.get_audio_only()
    yt.download()

    # st.info('2. Audio file has been retrieved from YouTube video')
    bar.progress(10)


# 3. Upload YouTube audio file to AssemblyAI


def transcribe_yt():
    current_dir = os.getcwd()

    for file in os.listdir(current_dir):
        if file.endswith(".mp4"):
            mp4_file = os.path.join(current_dir, file)
            # print(mp4_file)
    filename = mp4_file
    bar.progress(20)

    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    headers = {'authorization': api_key}
    response = requests.post('https://api.assemblyai.com/v2/upload',
                             headers=headers,
                             data=read_file(filename))
    audio_url = response.json()['upload_url']
    # st.info('3. YouTube audio file has been uploaded to AssemblyAI')
    bar.progress(30)

    # 4. Transcribe uploaded audio file
    endpoint = "https://api.assemblyai.com/v2/transcript"

    json1 = {
        "audio_url": audio_url
    }

    headers = {
        "authorization": api_key,
        "content-type": "application/json"
    }

    transcript_input_response = requests.post(
        endpoint, json=json1, headers=headers)

    # st.info('4. Transcribing uploaded file')
    bar.progress(40)

    # 5. Extract transcript ID
    transcript_id = transcript_input_response.json()["id"]
    # st.info('5. Extract transcript ID')
    bar.progress(50)

    # 6. Retrieve transcription results
    endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    headers = {
        "authorization": api_key,
    }
    transcript_output_response = requests.get(endpoint, headers=headers)
    # st.info('6. Retrieve transcription results')
    bar.progress(60)

    # Check if transcription is complete
    from time import sleep

    while transcript_output_response.json()['status'] != 'completed':
        sleep(5)
        st.warning('Transcription is processing ...')
        transcript_output_response = requests.get(endpoint, headers=headers)

    bar.progress(100)

    # 7. Print transcribed text
    st.header('Output')
    st.success(transcript_output_response.json()["text"])

    # 8. Save transcribed text to file

    # Save as TXT file
    yt_txt = open('yt.txt', 'w')
    yt_txt.write(transcript_output_response.json()["text"])
    yt_txt.close()

    # Save as SRT file
    srt_endpoint = endpoint + "/srt"
    srt_response = requests.get(srt_endpoint, headers=headers)
    with open("yt.srt", "w") as _file:
        _file.write(srt_response.text)

    zip_file = ZipFile('transcription.zip', 'w')
    zip_file.write('yt.txt')
    zip_file.write('yt.srt')
    zip_file.close()

    # transcribe local


api_key = st.secrets['api_key']


def transcribe_upload(file):
    filename = file

    def read_file(filename, chunk_size=5242880):
        with open(filename, "rb") as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    headers = {'authorization': api_key}
    response = requests.post('https://api.assemblyai.com/v2/upload',
                             headers=headers,
                             data=read_file(filename))
    audio_url = response.json()['upload_url']
    bar.progress(40)

    endpoint = "https://api.assemblyai.com/v2/transcript"

    json1 = {
        "audio_url": audio_url,
        "iab_categories": True
    }

    headers = {
        "authorization": api_key,
        "content-type": "application/json"
    }
    #####
    transcript_input_response = requests.post(
        endpoint,
        headers=headers,
        json=json1
    )

    transcript_id = transcript_input_response.json()["id"]

    endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    headers = {
        "authorization": api_key
    }
    bar.progress(60)
    transcript_response = requests.get(endpoint, headers=headers)

    bar.progress(80)
    while transcript_response.json()['status'] != 'completed':
        time.sleep(5)
        st.info(transcript_response.json()['status'])
        transcript_response = requests.get(endpoint, headers=headers)

    bar.progress(100)

    st.success(transcript_response.json()["text"])
    # st.success(str(transcript_response.json()["iab_categories_result"]["summary"]))

    # print(str(transcript_response.json()))

    # for items in transcript_response.json()["iab_categories_result"]:
    # print(items)

    text_file = filename.replace(".mp4", ".txt")

    # save as txt removing stop words
    text = transcript_response.json()["text"]
    sw_nltk = stopwords.words('english')
    words = [word for word in text.split() if word.lower() not in sw_nltk]
    new_text = " ".join(words)

    with open(os.path.join('transcripts', f'{text_file}'), 'w') as transcript_txt:
        transcript_txt.write(new_text)
        transcript_txt.close()

    summary = transcript_response.json()["iab_categories_result"]["summary"]
    # keys = list(summary.keys())
    # # for i in keys:
    # #     print(i)

    with open(os.path.join('summary', f'summary_{text_file}'), 'w') as summary_txt:
        for key in summary.keys():
            print(str(key.split(">")).strip("[]"), file=summary_txt)

    # with open(f'summary_{text_file}', 'w') as summary_txt:
    #     for key in summary.keys():
    #         print(str(key.split(">")).strip("[]"), file=summary_txt)

    ### SUMMARY TRANSCRIPT MATCHING

    def text_matching(text_filename, folder_path):
        file1 = open(f'{text_filename}', 'r')
        fl1 = file1\
            .read().split()
        dict_file1 = {}
        for i in fl1:
            if i not in dict_file1:
                dict_file1[i.lower()] = 0
            dict_file1[i.lower()] += 1

        def get_file_match(filepath):
            file2 = open(filepath, 'r')
            fl2 = file2.read().split()
            dict_file2 = {}
            for i in fl2:
                if i not in dict_file2:
                    dict_file2[i.lower()] = 0
                dict_file2[i.lower()] += 1

            sum1 = sum(i * i for i in dict_file1.values())
            sum2 = sum(i * i for i in dict_file2.values())
            mod_fl1 = sqrt(sum1)
            mod_fl2 = sqrt(sum2)
            dotProduct = 0
            for key in dict_file2:
                if key in dict_file1:
                    dotProduct += dict_file1[key] * dict_file2[key]
            distance = acos(dotProduct / int(mod_fl1 * mod_fl2))
            match = (1.57 - distance) / 1.57 * 100;
            return match
            file2.close()

        names = []
        a = []
        for filepath in glob.iglob(fr'{folder_path}\*.txt'):
            # print(filepath.replace('/content/drive/MyDrive/video_feed/', ''))
            file = (filepath)
            size = get_file_match(file)
            return size
            # names.append(filepath.replace('/content/drive/MyDrive/video_feed/', ''))
        # df = pd.DataFrame({"Video File Names" : names,"Size" : a})
        # df.to_csv("ObjectDetectionDetails.csv", index=True)

        file1.close()

    summary_folder_path = r"C:\Users\ManishP\transcriber-app\summary"
    transcript_folder_path = r"C:\Users\ManishP\transcriber-app\transcripts"
    summary_match = text_matching(text_filename=f'summary/summary_{text_file}', folder_path=summary_folder_path)

    def upload_to_drive():
        headers = {
            "Authorization": "Bearer ya29.a0ARrdaM-iyTRm_bNozcQoMPagahrGUaRm7J-PVWrQSrSezJw35mGiP2bb3VCoRVguGOE2RgBiYevSzOt14I5a48gXjTep5pwpg1osoL1vyvWCfRzooAPfa1xJemP_doV6-6csnVOjoH8OI4CFFYP4xgumlIMK"}
        para = {
            "name": filename,
            "parents": ["16cZXDXhjKvHJFnRT-tmyQRFKZLM2xJVW"]
        }

        files = {
            'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
            'file': open("./video.mp4", "rb")
        }
        r = requests.post(
            "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
            headers=headers,
            files=files
        )
        print(r.text)
        st.success("File uploaded")

    if summary_match > 60:
        st.info("Topic Detection crosses our threshold. Starting Transcript match...")
        transcript_match = text_matching(text_filename=f'transcripts/{text_file}', folder_path=transcript_folder_path)
        if transcript_match > 50:
            st.error("Cannot upload your file as it is a possible duplicate existing in our database.")
        else:
            st.success("File passes all validations. Uploading file to our database...")
            upload_to_drive()
    else:
        st.spinner("Topic detection below our Threshold. uploading your file to database...")



# The App


# 1. Read API from text file
api_key = st.secrets['api_key']

# st.info('1. API is read ...')
st.warning('Awaiting URL input in the sidebar.')

# Sidebar
st.sidebar.header('Input parameter')

with st.sidebar.form(key='my_form'):
    URL = st.text_input('Enter URL of YouTube video:')
    submit_button = st.form_submit_button(label='Go')

with st.sidebar.form(key='upload'):
    file = st.file_uploader('Upload a file from your system')
    # tfile = tempfile.NamedTemporaryFile(delete=False)
    # print(tfile)
    # tfile.write(tfile.read())
    # my_clip = mp.VideoFileClip(r"{}".format(tfile))
    # my_clip.audio.write_audiofile(r"my_result.mp3")
    upload = st.form_submit_button(label='upload')

# Run custom functions if URL is entered
if submit_button:
    get_yt(URL)
    transcribe_yt()

if upload:
    st.success(file)
    # my_clip = mp.VideoFileClip(r"{}".format(file.name))
    # audio = my_clip.audio.write_audiofile(f"{file.name}.mp3")
    # print(audio)
    transcribe_upload(file.name)
    st.success("File write successfull")

    with open("transcription.zip", "rb") as zip_download:
        btn = st.download_button(
            label="Download ZIP",
            data=zip_download,
            file_name="transcription.zip",
            mime="application/zip"
        )