from pydub import AudioSegment
import speech_recognition as sr
import tempfile
import os

def silence_based_conversion(path="./what-can-i-do-for-you-npc-british-male-99751.wav"):
    # open the audio file stored in the local system as a wav file.
    song = AudioSegment.from_wav(path)

    # open a file where we will concatenate and store the recognized text
    fh = open("recognized.txt", "w+")

    # split track where silence is 0.5 seconds or more and get chunks
    chunks = []
    chunk_length = 2000  # in milliseconds, adjust as needed
    for i in range(0, len(song), chunk_length):
        chunk = song[i:i + chunk_length]
        chunks.append(chunk)

    # create a speech recognition object
    r = sr.Recognizer()

    # recognize each chunk
    for i, chunk in enumerate(chunks):
        # Save the chunk as a temporary audio file
        temp_filename = f"temp_chunk_{i}.wav"
        chunk.export(temp_filename, format="wav")

        with sr.AudioFile(temp_filename) as source:
            # r.adjust_for_ambient_noise(source)
            r.adjust_for_ambient_noise(source, duration=0.5)  # adjust as needed

            audio_listened = r.listen(source)

        # Remove the temporary file
        os.remove(temp_filename)

        try:
            # try converting it to text
            rec = r.recognize_google(audio_listened)
            # write the output to the file.
            print(f"Chunk {i + 1}: {rec}")
            fh.write(rec + ". ")

        # catch any errors.
        except sr.UnknownValueError:
            print(f"Could not understand audio in Chunk {i + 1}")

        except sr.RequestError as e:
            print(f"Could not request results. Check your internet connection in Chunk {i + 1}")

if __name__ == '__main__':
    silence_based_conversion()
