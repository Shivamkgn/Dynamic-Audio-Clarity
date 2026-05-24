
import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
import noisereduce as nr  # Import noise reduction library
from scipy.io.wavfile import write  # To save numpy array as a wav file

# Merge Sort Function
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2  # Finding the middle of the array
        L = arr[:mid]        # Dividing the array elements into 2 halves
        R = arr[mid:]

        merge_sort(L)  # Sorting the first half
        merge_sort(R)  # Sorting the second half

        i = j = k = 0

        # Copy data to temporary arrays L[] and R[]
        while i < len(L) and j < len(R):
            if L[i][1] < R[j][1]:  # Sorting based on the second element (duration)
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

# Load your dataset from a directory
def load_audio_files(path):
    audio_files = []
    for file in os.listdir(path):
        if file.endswith(".wav"):
            # Load the audio file to get its duration
            y, sr = librosa.load(os.path.join(path, file), sr=None)
            duration = librosa.get_duration(y=y, sr=sr)
            audio_files.append((file, duration))
    return audio_files

# Enhance audio clarity with dynamic noise reduction
def enhance_audio(audio_path):
    # Load the audio with a consistent sample rate
    y, sr = librosa.load(audio_path, sr=16000)

    # Perform noise reduction dynamically
    reduced_noise = nr.reduce_noise(y=y, sr=sr)

    # Normalize audio
    reduced_noise = librosa.util.normalize(reduced_noise)

    # Save the reduced noise audio as a WAV file first
    temp_wav_path = "temp_reduced_noise.wav"
    write(temp_wav_path, sr, (reduced_noise * 32767).astype(np.int16))  # Convert to 16-bit PCM

    # Load the WAV file into pydub's AudioSegment
    audio = AudioSegment.from_wav(temp_wav_path)

    # Apply gain (increase volume)
    adjusted_audio = audio.apply_gain(10)  # Example: Increase volume by 10 dB

    # Save the processed audio with a "processed_" prefix
    output_path = "processed_" + os.path.basename(audio_path)
    adjusted_audio.export(output_path, format="wav")
    print(f"Processed audio saved at: {output_path}")

    # Optionally, delete the temporary WAV file
    os.remove(temp_wav_path)

    return output_path

# Example usage
audio_dataset_path =path = r"D:\semester 1 topics\vs_code\python\project\dynamic audio clarity\data"
 # Change this to your dataset path
audio_files = load_audio_files(audio_dataset_path)

# Sort audio files by duration using merge sort
merge_sort(audio_files)
#print("Audio files sorted by duration:", audio_files)

# Process all audio files
for file, _ in audio_files: 
    file_path = os.path.join(audio_dataset_path, file)
    processed_file = enhance_audio(file_path)
