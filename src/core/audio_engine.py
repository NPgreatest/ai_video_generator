import json
import os
import wave

import requests
from pydub import AudioSegment

class WAVDownloader:
    def __init__(self, txt_file_path, project_name):
        self.txt_file_path = txt_file_path
        self.project_name = project_name
        self.output_dir = os.path.join("outputs", project_name)
        os.makedirs(self.output_dir, exist_ok=True)
        self.audio_clips = []

    def process_lines(self):
        """Reads the .txt file line by line and processes each line."""
        try:
            with open(self.txt_file_path, 'r', encoding='utf-8') as file:
                for i, line in enumerate(file, start=1):
                    text = line.strip()
                    if text:
                        self.call_api_and_save_wav(text, i)
            self.generate_config_json()
        except Exception as e:
            print(f"Error reading the file: {e}")

    def call_api_and_save_wav(self, text, number):
        """Calls the API and saves the WAV file locally."""
        # Construct the API URL
        api_url = "http://127.0.0.1:9880/tts"
        params = {
            "text": text,
            "text_lang": "zh",
            "ref_audio_path": "output/reference.wav",
            "prompt_lang": "zh",
            "prompt_text": "就是跟他这个成长的外部环境有关系，和本身的素质也有关系，他是一个",
            "text_split_method": "cut5",
            "batch_size": "1",
            "media_type": "wav",
        }

        print(f"Trying to get WAV for line {number}: {text}")
        try:
            # Make the API call
            response = requests.get(api_url, params=params)
            print(f"Response: {response.status_code}")

            # Check if the response is successful
            response.raise_for_status()
            wav_data = response.content

            # Save the WAV file locally
            output_path = os.path.join(self.output_dir, f"{number}.wav")
            with open(output_path, 'wb') as wav_file:
                wav_file.write(wav_data)
            print(f"Saved WAV file to {output_path}")

            # Determine the start time for this audio clip
            if self.audio_clips:
                # Calculate start time based on the last clip
                last_clip = self.audio_clips[-1]
                start_time = last_clip["start"] + (last_clip["end"] - last_clip["start"])
            else:
                # First clip starts at 0
                start_time = 0.0

            try:
                with wave.open(output_path, 'rb') as wav_file:
                    frames = wav_file.getnframes()
                    rate = wav_file.getframerate()
                    duration = frames / float(rate)
            except Exception as e:
                print(f"Failed to calculate WAV duration using wave: {e}")
                # Fallback to pydub for duration calculation
                audio = AudioSegment.from_file(output_path)
                duration = len(audio) / 1000.0
            # Calculate end time (assuming each clip has a fixed duration; adjust as needed)
            # For demonstration purposes, we use 10 seconds as a default duration
            end_time = start_time + duration

            # Append metadata to the audio_clips list
            self.audio_clips.append({
                "source": f"{number}.wav",
                "start": start_time,
                "end": end_time,
                "volume": 1.0,
                "audio_start": 0.0
            })
        except requests.exceptions.RequestException as e:
            print(f"API call failed for line {number}: {e}")
        except Exception as e:
            print(f"Failed to save WAV file for line {number}: {e}")

    def generate_config_json(self):
        """Generates a JSON configuration file based on the generated WAV files."""
        config = {
            "audio_tracks": self.audio_clips
        }
        config_path = os.path.join(self.output_dir, "config_example.json")
        try:
            with open(config_path, 'w', encoding='utf-8') as json_file:
                json.dump(config, json_file, indent=2, ensure_ascii=False)
            print(f"Configuration JSON saved at: {config_path}")
        except Exception as e:
            print(f"Failed to save configuration JSON: {e}")

