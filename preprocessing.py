import os
from pydub import AudioSegment

def trim_and_resample_all_audio_files():
    """Processes ChoralSynth dataset: trims and resamples SATB parts and creates mixture.wav."""
    audio_dir = os.path.join(os.getcwd(), "ChoralSynth")
    output_dir = os.path.join(os.getcwd(), "trimmed_audio")
    os.makedirs(output_dir, exist_ok=True)

    target_duration_ms = 30000  # 30 seconds
    target_sample_rate = 16000
    parts = ["soprano", "alto", "tenor", "bass"]

    for song_folder in os.listdir(audio_dir):
        song_path = os.path.join(audio_dir, song_folder)
        voices_dir = os.path.join(song_path, "voices")

        if not os.path.isdir(voices_dir):
            print(f"Skipping {song_folder}: no 'voices' directory found.")
            continue

        output_song_dir = os.path.join(output_dir, song_folder)
        os.makedirs(output_song_dir, exist_ok=True)
        
        combined_audio = AudioSegment.silent(duration=target_duration_ms)

        for part in parts:
            input_file = os.path.join(voices_dir, f"{part}.mp3")
            if not os.path.isfile(input_file):
                print(f"Warning: {input_file} not found.")
                continue

            audio = AudioSegment.from_file(input_file)
            mono_audio = audio.set_channels(1)
            trimmed = mono_audio[:target_duration_ms]

            if len(trimmed) < target_duration_ms:
                padding = target_duration_ms - len(trimmed)
                trimmed += AudioSegment.silent(duration=padding)

            resampled = trimmed.set_frame_rate(target_sample_rate)

            # Save individual trimmed & resampled stem
            out_path = os.path.join(output_song_dir, f"{part}.wav")
            resampled.export(out_path, format="wav")

            # Add to the mixture
            combined_audio = combined_audio.overlay(resampled)

        # Save combined mixture
        mono_combined_audio = combined_audio.set_channels(1)
        mixture_path = os.path.join(output_song_dir, "mixture.wav")
        mono_combined_audio.export(mixture_path, format="wav")

trim_and_resample_all_audio_files()