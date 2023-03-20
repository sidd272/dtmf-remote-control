from scipy.io import wavfile as wav
from scipy.fftpack import fft
import pyaudio
import wave
import numpy as np
import os
import webbrowser

def isNumberInArray(array, number):
    offset = 5
    for i in range(number - offset, number + offset):
        if i in array:
            return True
    return False

DTMF_TABLE = {
    '1': [1209, 697],
    '2': [1336, 697],
    '3': [1477, 697],
    'A': [1633, 697],

    '4': [1209, 770],
    '5': [1336, 770],
    '6': [1477, 770],
    'B': [1633, 770],

    '7': [1209, 852],
    '8': [1336, 852],
    '9': [1477, 852],
    'C': [1633, 852],

    '*': [1209, 941],
    '0': [1336, 941],
    '#': [1477, 941],
    'D': [1633, 941],
} 

FORMAT = pyaudio.paInt16 
CHANNELS = 1 # number of channels it means number of sample in every sampling
RATE = 20000 # number of sample in 1 second sampling
CHUNK = 1024 # length of every chunk
RECORD_SECONDS = 0.4 # time of recording in seconds
WAVE_OUTPUT_FILENAME = "file.wav" # file name
 
audio = pyaudio.PyAudio()
print("1:Open Google")
print("2:Open NITK site")
print("3:Open IRIS")
print("4:Open Youtube")
print("5:Open Terminal")
print("6:Open Notepad")
print("7:Open Calculator")
print("8:Open Calendar")
print("9:Shutdown computer")
while (True):
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    # stop Recording
    stream.stop_stream()
    stream.close()

    # storing voice
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    # reading voice
    rate, data = wav.read('file.wav')
    # data is voice signal. its type is list(or numpy array)

    # Calculate fourier trasform of data
    FourierTransformOfData = np.fft.fft(data, 20000)

    # Convert fourier transform complex number to integer numbers
    for i in range(len(FourierTransformOfData)):
        FourierTransformOfData[i] = int(np.absolute(FourierTransformOfData[i]))

    # Calculate lower bound for filtering fourier trasform numbers
    LowerBound = 20 * np.average(FourierTransformOfData)

    # Filter fourier transform data (only select frequencies that X(jw) is greater than LowerBound)
    FilteredFrequencies = []
    for i in range(len(FourierTransformOfData)):
        if (FourierTransformOfData[i] > LowerBound):
            FilteredFrequencies.append(i)
    
    # Detect and print pressed button
    for char, frequency_pair in DTMF_TABLE.items():
        if (isNumberInArray(FilteredFrequencies, frequency_pair[0]) and
            isNumberInArray(FilteredFrequencies, frequency_pair[1])):
            print (char)
            if(char=="1"):
                webbrowser.open('https://www.google.com',new=2)
            if(char=="2"):
                webbrowser.open('https://www.nitk.ac.in/',new=1)
            if(char=="3"):
                webbrowser.open("https://iris.nitk.ac.in/hrms",new=1)  
            if(char=="4"):
                webbrowser.open('https://www.youtube.com/',new=1)
            if(char=="5"):
                os.system("gnome-terminal")
            if(char=="6"):
                os.system('gedit') 
            if(char=="7"):
                os.system("gnome-calculator") 
            if(char=="8"):
                os.system("gnome-calendar")
            if(char=="9"):
                os.system("shutdown") 
audio.terminate()
