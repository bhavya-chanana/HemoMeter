# HemoMeter - Calculating Hemoglobin is now as easy as placing your finger on the camera, literally.

## Overview
HemoMeter is a research project developed at IIIT-Naya Raipur by me - Bhavya Chanana during my research internship. This project enables users to calculate their hemoglobin levels by simply recording a video of their finger using their smartphone camera. This innovative approach leverages advanced photoplethysmography (PPG) techniques to provide a non-invasive method for hemoglobin estimation.

## Project URL
Visit the project at: [HemoMeter](https://hemometer-4cc5491fd867.herokuapp.com/)

## Features
- User-friendly interface
- Real-time video processing
- Accurate hemoglobin prediction
- Supports video uploads in MP4 and MOV formats

## Dataset
The model was created using a custom-built dataset by collecting hemoglobin levels using traditional methods and corresponding 30-second video samples of the subjects' fingers.


## Getting Started

### Prerequisites
- Python 3.10.0
- Streamlit
- Required Python libraries (listed in `requirements.txt`)

### Installation

1. **Clone the Repository:**
    ```sh
    git clone https://github.com/bhavya-chanana/HemoMeter.git
    cd HemoMeter
    ```

2. **Create a Virtual Environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

### Running the App Locally

1. **Start the Streamlit App:**
    ```sh
    streamlit run app.py
    ```

2. **Access the App:**
    Open your web browser and navigate to `http://localhost:8501`.

## How to Use HemoMeter

### Steps to Calculate Hemoglobin

1. **Cover the Camera and Flash with Your Finger:**
    - Ensure no external light is detected by the camera to avoid interference.

2. **Record a Video:**
    - Record a video of your finger for at least 25-30 seconds. Alternatively, you can upload an existing video.

3. **Submit for Analysis:**
    - Click the **"Calculate Hb"** button to process the video and calculate your hemoglobin level.

### Detailed Steps:

1. **Cover the Camera and Flash:**
    - Place your finger over the camera and flash on your smartphone, ensuring no external light is detected by the camera.
  
2. **Record the Video:**
    - Record a video of your finger for more than 25-30 seconds to ensure a stable reading.
    - Alternatively, you can upload a pre-recorded video from your device.

3. **Calculate Hemoglobin:**
    - Once the video is uploaded or recorded, click on the **"Calculate Hb"** button.
    - The app will process the video and display the predicted hemoglobin level on the screen.

## Contributing
We welcome contributions from the community. If you'd like to contribute, please fork the repository and create a pull request with your changes. Ensure that your code follows the project's coding standards and passes all tests.

## License


## Contributor
- Bhavya Chanana - https://www.linkedin.com/in/bhavya-chanana/ - https://github.com/bhavya-chanana
