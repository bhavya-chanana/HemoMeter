import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, WebRtcMode
import av
import cv2
import numpy as np
from PIL import Image
import ffmpeg
import os

class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.frames = []
        self.latest_frame = None

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        self.frames.append(img)
        self.latest_frame = img
        return img

    def get_latest_frame(self):
        return self.latest_frame

    def get_frames(self):
        return self.frames

def save_video(frames, filename, format):
    height, width, layers = frames[0].shape
    size = (width, height)
    
    if format == 'mov':
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    else:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    
    out = cv2.VideoWriter(filename, fourcc, 20.0, size)
    
    for frame in frames:
        out.write(frame)
    out.release()

def get_video_metadata(video_path):
    try:
        probe = ffmpeg.probe(video_path)
        return probe
    except ffmpeg.Error as e:
        st.error(f"An error occurred while reading the video metadata: {e}")
        return None

def extract_device_info(metadata):
    if metadata is None:
        return "Unknown"
    
    format_tags = metadata.get('format', {}).get('tags', {})
    device_info = format_tags.get('com.apple.quicktime.make', None)
    if device_info is None:
        device_info = format_tags.get('make', None)
    
    if device_info is None:
        return "Unknown"
    
    return "iOS" if "Apple" in device_info else "Android"

st.title("Video Recorder/Selector")

# Record video
if st.button("Record/Select Video"):
    webrtc_ctx = webrtc_streamer(
        key="example",
        mode=WebRtcMode.SENDRECV,
        video_transformer_factory=VideoTransformer,
        async_transform=True,
    )
    
    if webrtc_ctx.video_transformer:
        frames = webrtc_ctx.video_transformer.get_frames()
        if frames:
            st.image(frames[-1], channels="BGR")
            save_button = st.button("Save Video")
            if save_button:
                # Save the video temporarily
                temp_filename = "temp_video.mp4"
                save_video(frames, temp_filename, "mp4")
                st.success("Video saved temporarily")
                
                # Determine the device type
                metadata = get_video_metadata(temp_filename)
                device_type = extract_device_info(metadata)
                
                # Save in the appropriate format
                if device_type == "iOS":
                    final_filename = "recorded_video.mov"
                    save_video(frames, final_filename, "mov")
                else:
                    final_filename = "recorded_video.mp4"
                    save_video(frames, final_filename, "mp4")
                
                os.remove(temp_filename)
                st.success(f"Video saved as {final_filename}")

# Capture static photo
if st.button("Capture Photo"):
    webrtc_ctx = webrtc_streamer(
        key="photo",
        mode=WebRtcMode.SENDRECV,
        video_transformer_factory=VideoTransformer,
        async_transform=True,
    )

    if webrtc_ctx.video_transformer:
        latest_frame = webrtc_ctx.video_transformer.get_latest_frame()
        if latest_frame is not None:
            st.image(latest_frame, channels="BGR")
            photo_button = st.button("Save Photo")
            if photo_button:
                img = Image.fromarray(cv2.cvtColor(latest_frame, cv2.COLOR_BGR2RGB))
                img.save("captured_photo.jpg")
                st.success("Photo saved as captured_photo.jpg")

# Option to upload video
uploaded_video = st.file_uploader("Or upload a video", type=["mp4", "mov", "avi", "mkv"])

if uploaded_video is not None:
    st.video(uploaded_video)
    with open("uploaded_video.mp4", "wb") as f:
        f.write(uploaded_video.getbuffer())
    st.success("Video uploaded as uploaded_video.mp4")
    
    metadata = get_video_metadata("uploaded_video.mp4")
    device_type = extract_device_info(metadata)
    st.info(f"The video was recorded on a(n) {device_type} device.")
