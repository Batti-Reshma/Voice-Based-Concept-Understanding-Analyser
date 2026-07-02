import librosa
import numpy as np


def extract_audio_features(audio_path):
    """
    Extract basic audio features.
    """

    y, sr = librosa.load(audio_path)

    duration = librosa.get_duration(y=y, sr=sr)

    rms = np.mean(librosa.feature.rms(y=y))

    return {
        "duration": round(duration, 2),
        "rms_energy": round(float(rms), 4)
    }