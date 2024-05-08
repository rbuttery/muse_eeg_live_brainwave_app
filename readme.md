# Live Brainwave EEG App

## Overview
The Live Brainwave EEG App is a visualization tool designed to display real-time EEG data from the Muse headband. This application leverages the Muse headband to capture EEG signals, which are then processed and visualized dynamically, providing insights into brain activity. This app is particularly useful for researchers, educators, and enthusiasts interested in neurofeedback and brain-computer interfaces.

### Muse Receiver App
This is a PyQt6 app built to simply visualize in real-time the output from our Muse device.

#### Run & Select which channel you want to see first. 
<p align="center">
  <img src="demo\app2.png" width="750" title="hover text">
</p>

#### Visualize your brainwaves!
<p align="center">
  <img src="demo\app.gif" width="750" title="hover text">
</p>

## Prerequisites
- **Muse Headband**: This application requires a Muse headband to capture EEG data.
- **SDK Access**: You must have access to the Muse SDK or use a compatible application such as Mind Monitor (app store, costs money) to fetch and stream EEG data.
- **Python Environment**: The application is developed in Python, requiring an environment with Python 3.6 or later.
- **PyQt6 and Other Dependencies**: Installation of PyQt6 and other required libraries.

## Installation on Windows
This is how you do it on windows with pip, but this will work in any python environment.
```bash
git clone https://github.com/rbuttery/live_eeg_visualization_app.git
cd live_eeg_visualization_app
python -m venv env
env\scripts\activate
pip install -r requirements.txt
```

#### To Run The App:
```bash
python muse_receiver_app.py
```


### Bonus: EEG Data Stream -> to CSV
This will just print the output of the eeg channels to the terminal. At this stage, this is the boilerplate needed to simply extract the data from the headband.
```bash
python eeg_data_stream.py
```
```bash
# Use --to-csv to stream to a local csv file instead!
python eeg_data_stream.py --to-csv
```

