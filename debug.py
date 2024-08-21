import os
import random
import logging
from pydub import AudioSegment

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def debug_animalize(text, language, output_stream):
    # Set the path to your sound folder
    sound_folder = './sounds/korean'  # Adjust this path as needed
    
    # List of sound files with normalized paths
    sound_files = [os.path.join(sound_folder, f"sound{i:02d}.wav") for i in range(1, 71)]
    sound_files = [os.path.normpath(path).replace('\\', '/') for path in sound_files]  # Convert \ to /
    logging.debug(f"Available sound files: {sound_files}")

    # Randomly choose a sound file
    chosen_sound = random.choice(sound_files)
    logging.debug(f"Chosen sound file: {chosen_sound}")

    # Check if the chosen sound file exists
    if not os.path.exists(chosen_sound):
        logging.error(f"Sound file not found: {chosen_sound}")
        return

    # Load and save the chosen sound to the output stream
    try:
        sound = AudioSegment.from_wav(chosen_sound)
        sound.export(output_stream, format='wav')
        logging.info(f"Sound file exported successfully to the output stream.")
    except Exception as e:
        logging.error(f"Error exporting sound file: {type(e).__name__} - {e}")

# Example usage
if __name__ == "__main__":
    from io import BytesIO
    # Create an in-memory stream to hold the audio data
    audio_stream = BytesIO()
    debug_animalize("test text", "korean", audio_stream)
    audio_stream.seek(0)  # Go to the beginning of the stream
    with open("test_output.wav", "wb") as f:
        f.write(audio_stream.read())
    print("Debugging complete. Check 'test_output.wav' for results.")