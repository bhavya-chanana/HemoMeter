import pyPPG
from pyPPG.example import ppg_example
from pyPPG import PPG, Fiducials, Biomarkers
from pyPPG.datahandling import load_data, plot_fiducials, save_data
import pyPPG.preproc as PP
import pyPPG.fiducials as FP
import pyPPG.biomarkers as BM
import pyPPG.ppg_sqi as SQI
import pyPPG.example as PE

import numpy as np
import pandas as pd
import cv2
import os
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, resample, find_peaks
import csv 

from predict import predict_hb

def extract_ppg_from_video(video_path, start_time, duration):
    # extract red and green ppg signals
    
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Calculate the starting frame based on start_time
    start_frame = int(start_time * fps)

    # Set the video to start at the correct frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    red_ppg = []
    green_ppg = []
    frame_count = 0
    
    while cap.isOpened() and frame_count < duration * fps:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        # Extract red and green channels
        red_channel = frame[:, :, 2]
        green_channel = frame[:, :, 1]
        
        # Calculate the mean value of each channel as PPG signal
        red_mean = np.mean(red_channel)
        green_mean = np.mean(green_channel)
        
        red_ppg.append(-red_mean)
        green_ppg.append(-green_mean)
        
        frame_count += 1
    
    cap.release()
    return red_ppg, green_ppg, fps

def plot_ppg(red_ppg, green_ppg, fps):
    # plot ppg signals
    
    time = np.arange(len(red_ppg)) / fps

    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(time, red_ppg, 'r', label='Red Channel PPG')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(time, green_ppg, 'g', label='Green Channel PPG')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend()

    plt.tight_layout()
    plt.show()

def convert_csv(ppg, video_name):
    # convert ppg signals into csv file: dir -> ppgData -> ppgData\{video_name}.csv

    os.makedirs("ppgData", exist_ok=True)
    # Specify the file path where you want to save the CSV file
    csv_file_path = f"ppgData\{video_name}.csv"

    # Open the CSV file for writing
    with open(csv_file_path, mode='w', newline='') as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)

        # Write each value as a separate row in the CSV file
        for value in ppg:
            csv_writer.writerow([value])

    print(f"CSV file '{csv_file_path}' has been created with each value on a new line.")

def pyppgFeatures(video_name):
    # somefunction - renamed - pyppg function - save ppg features to csv files in temp dir
    
    data_path = f"ppgData\{video_name}.csv"
    start_sig = 0 # the first sample of the signal to be analysed
    end_sig = -1 # the last sample of the signal to be analysed (here a value of '-1' indicates the last sample)
    savingfolder = 'temp_dir'
    savingformat = 'csv'
    fs=60

    signal = load_data(data_path=data_path, fs=fs, start_sig=start_sig, end_sig=end_sig, use_tk=False)
    
    start_index = 0  # Start at the beginning
    end_index = 20 * signal.fs  # End after 20 seconds

    # Slice the signal from start_index to end_index
    signal.v = signal.v[start_index:end_index] # 20 second long signal to be analysed


    # plt raw ppg: pyPPG website  
    # setup figure
    fig_show, ax = plt.subplots()

    # create time vector
    t = np.arange(0, len(signal.v))/signal.fs

    # plot raw PPG signal
    ax.plot(t, signal.v, color = 'blue')
    ax.set(xlabel = 'Time (s)', ylabel = 'raw PPG')

    # show plot
    plt.show()

    # prepare the signal: preprocessing butterworth
    signal.filtering = True # whether or not to filter the PPG signal
    signal.fL=0.5000001 # Lower cutoff frequency (Hz)
    signal.fH=5 # Upper cutoff frequency (Hz)
    signal.order=4 # Filter order
    signal.sm_wins={'ppg':50,'vpg':10,'apg':10,'jpg':10} # smoothing windows in millisecond for the PPG, PPG', PPG", and PPG'"

    prep = PP.Preprocess(fL=signal.fL, fH=signal.fH, order=signal.order, sm_wins=signal.sm_wins)
    signal.ppg, signal.vpg, signal.apg, signal.jpg = prep.get_signals(s=signal)

    # plt preprocessed ppg, first, second, third derivate
    # setup figure
    fig, (ax1,ax2,ax3,ax4) = plt.subplots(4, 1, sharex = True, sharey = False)

    # create time vector
    t = np.arange(0, len(signal.ppg))/signal.fs

    # plot filtered PPG signal
    ax1.plot(t, signal.ppg)
    ax1.set(xlabel = '', ylabel = 'PPG')

    # plot first derivative
    ax2.plot(t, signal.vpg)
    ax2.set(xlabel = '', ylabel = 'PPG\'')

    # plot second derivative
    ax3.plot(t, signal.apg)
    ax3.set(xlabel = '', ylabel = 'PPG\'\'')

    # # plot third derivative
    # ax4.plot(t, signal.jpg)
    # ax4.set(xlabel = 'Time (s)', ylabel = 'PPG\'\'\'')

    # show plot
    # plt.show()

    # Store the derived signals in a class
    # Initialise the correction for fiducial points
    corr_on = ['on', 'dn', 'dp', 'v', 'w', 'f']
    correction=pd.DataFrame()
    correction.loc[0, corr_on] = True
    signal.correction=correction

    # Create a PPG class
    s = PPG(signal)

    # Initialize the fidicuals package
    fpex = FP.FpCollection(s=s)

    # Extract fidicuals points
    fiducials = fpex.get_fiducials(s=s)

    # Display the results
    print("Fiducial points:\n",fiducials + s.start_sig) # here the starting sample is added so that the results are relative to the start of the original signal (rather than the start of the analysed segment)

    # Plot the fiducial points
    # Create a fiducials class
    fp = Fiducials(fp=fiducials)

    # Plot fiducial points
    plot_fiducials(s, fp, savingfolder, legend_fontsize=12)

    # Get PPG SQI
    ppgSQI = round(np.mean(SQI.get_ppgSQI(ppg=s.ppg, fs=s.fs, annotation=fp.sp)) * 100, 2)
    print('Mean PPG SQI: ', ppgSQI, '%')

    # Init the biomarkers package
    bmex = BM.BmCollection(s=s, fp=fp)

    # Extract biomarkers
    bm_defs, bm_vals, bm_stats = bmex.get_biomarkers()
    tmp_keys=bm_stats.keys()
    print('Statistics of the biomarkers:')
    for i in tmp_keys: print(i,'\n',bm_stats[i])

    # Create a biomarkers class
    bm = Biomarkers(bm_defs=bm_defs, bm_vals=bm_vals, bm_stats=bm_stats)

    # Save PPG struct, fiducial points, biomarkers
    fp_new = Fiducials(fp.get_fp() + s.start_sig) # here the starting sample is added so that the results are relative to the start of the original signal (rather than the start of the analysed segment)
    save_data(s=s, fp=fp_new, bm=bm, savingformat=savingformat, savingfolder=savingfolder)
    return fig_show

def FeaturesDict(videoDetailsDict):
    ''' converts features into dictionary/hashmap
    videoDetailsDict is a hashmap with structure {'Age': row['Age'], 'Gender': row['Gender'], 'Video': row['video']}
    edit file name'''

    # temp_dirs = ['Fiducial_points', 'Biomarker_vals', 'Biomarker_stats', 'Biomarker_defs', 'PPG_struct']
    # finalFeatures = "finalFeatures"
    # os.makedirs(finalFeatures, exist_ok=True)

    video_name = videoDetailsDict['Video']

    # file_name = f"dynamic_file_{some_variable}.txt"
                    #emp_dir\Biomarker_vals\20231217_121614_derivs_processed.csv

    base_dir = os.path.dirname(os.path.abspath(__file__))
    temp_dir = os.path.join(base_dir, 'temp_dir', 'Biomarker_vals')
    derivs_ratios = os.path.join(temp_dir, f'{video_name}_derivs_ratios_processed.csv')
    ppg_derivs = os.path.join(temp_dir, f'{video_name}_ppg_derivs_processed.csv')
    ppg_sig = os.path.join(temp_dir, f'{video_name}_ppg_sig_processed.csv')
    sig_ratios = os.path.join(temp_dir, f'{video_name}_sig_ratios_processed.csv')

    try:
        # df1 = pd.read_csv(fiducials)
        df2 = pd.read_csv(derivs_ratios)
        df3 = pd.read_csv(ppg_derivs)
        df4 = pd.read_csv(ppg_sig)
        df5 = pd.read_csv(sig_ratios)

        derivs_ratio_columns = ['Tu/Tpi', 'Tv/Tpi', 'Tw/Tpi']  
        ppg_derivs_columns = ['Tu', 'Tv', 'Tw']  
        ppg_sig_columns = ['Asp','Adn', 'Adp', 'Tpi', 'Tsp', 'Tsys', 'Tdp', 'deltaT']  
        sig_ratios_columns = ['Tsp/Tpi']  



        # Calculate the average of each column
        df7 = df2[derivs_ratio_columns].mean()
        df8 = df3[ppg_derivs_columns].mean()
        df9 = df4[ppg_sig_columns].mean()
        df10 = df5[sig_ratios_columns].mean()

        df = pd.concat([df7, df8, df9, df10], axis=0)

        df_dict = df.to_dict()

        df_dict.update(videoDetailsDict)

        return df_dict
    except FileNotFoundError:
        print(f'file not found')

def videoDetails(video_name, age, gender):
    '''
    param videoname
    input age, gender: M = 1, F = 2 
    returns dict/hashmap - videoDetailsDict =  {'Age': age, 'Gender': gender(1 or 2), 'Video': video_name}
    '''

    #map gender to M = 1 and F = 2
    if gender == 'M' or gender == 'm':
        gender = 1
    elif gender == 'F' or gender == 'f':
        gender = 2
    else:
        raise ValueError("Input appropriate gender")

    videoDetailsDict = {'Age': age, 'Gender': gender, 'Video': video_name}

    return videoDetailsDict


'''
example useage of process_vid.py
'''
if __name__ == "__main__":
    video_path = "videos\\test_bhavya_01.mov"

    video_file = os.path.basename(video_path)
    video_name = os.path.splitext(video_file)[0]
    video_extension = os.path.splitext(video_file)[1]
    
    videoDetailsDict = videoDetails(video_name)

    red_ppg, green_ppg, fps = extract_ppg_from_video(video_path, start_time=0, duration=20)
    # green_ppg = green_ppg[51:550] 
    # newFiltered_green_ppg, merged_cycle_green, time_green = analyze_and_select_ppg_cycles(green_ppg, fps, "Green")
    # print(green_ppg)
    if video_extension == ".mov":
        convert_csv(red_ppg, video_name)
    else:
        convert_csv(green_ppg, video_name)

    pyppgFeatures(video_name) # gets features and plots them

    features_dict = FeaturesDict(videoDetailsDict)

    print(features_dict)
    
    Hb_predicted = predict_hb(features_dict)
    print(Hb_predicted)
    

