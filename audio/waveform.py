import librosa
import librosa.display
import matplotlib.pyplot as plt


def plot_waveform(audio_path):

    y, sr = librosa.load(audio_path)

    fig, ax = plt.subplots(figsize=(10, 3))

    librosa.display.waveshow(
        y,
        sr=sr,
        ax=ax
    )

    ax.set_title("Audio Waveform")

    return fig