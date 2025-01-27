import os
import requests

class WAVDownloader:
    def __init__(self, txt_file_path, project_name):
        self.txt_file_path = txt_file_path
        self.project_name = project_name
        self.output_dir = os.path.join("outputs", project_name)
        os.makedirs(self.output_dir, exist_ok=True)

    def process_lines(self):
        """Reads the .txt file line by line and processes each line."""
        try:
            with open(self.txt_file_path, 'r', encoding='utf-8') as file:
                for i, line in enumerate(file, start=1):
                    text = line.strip()
                    if text:
                        self.call_api_and_save_wav(text, i)
        except Exception as e:
            print(f"Error reading the file: {e}")

    def call_api_and_save_wav(self, text, number):
        """Calls the API and saves the WAV file locally."""
        api_url = "http://127.0.0.1:9880"
        payload = {
            "text": text,
            "text_language": "zh"
        }
        try:
            response = requests.post(api_url, json=payload)
            response.raise_for_status()
            wav_data = response.content
            output_path = os.path.join(self.output_dir, f"{number}.wav")
            with open(output_path, 'wb') as wav_file:
                wav_file.write(wav_data)
            print(f"Saved: {output_path}")
        except requests.exceptions.RequestException as e:
            print(f"API call failed for line {number}: {e}")
        except Exception as e:
            print(f"Failed to save WAV file for line {number}: {e}")

