from src.core.audio_engine import WAVDownloader

def main():
    # Define the path to the text file and the project name
    txt_file_path = "/script_example/1.txt"  # Update this to the correct absolute or relative path
    project_name = "example_project"

    # Initialize the WAVDownloader
    downloader = WAVDownloader(txt_file_path, project_name)

    # Process the text file to generate audio files and configuration JSON
    downloader.process_lines()

if __name__ == "__main__":
    main()
