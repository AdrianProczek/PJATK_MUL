import wave
import os
import pyaudio
from unidecode import unidecode


def delete_diac(text):
    return unidecode(text)


def play_audio(filename):
    chunk = 1024
    wf = wave.open(filename, 'rb')
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pa.get_format_from_width(wf.getsampwidth()),
                     channels=wf.getnchannels(),
                     rate=wf.getframerate(),
                     output=True)
    data = wf.readframes(chunk)
    while data:
        stream.write(data)
        data = wf.readframes(chunk)
    stream.stop_stream()
    stream.close()
    pa.terminate()


def load_audio_files(directory):
    audio_files = {}
    for filename in os.listdir(directory):
        if filename.endswith(".wav"):
            name = filename[:-4]
            audio_files[name] = os.path.join(directory, filename)
    return audio_files


def find_audio_segment(components):
    audio_sequence = []
    index = 0

    while index < len(components):
        keyword = components[index]
        if keyword in stacje:
            audio_sequence.append(stacje[keyword])
        elif keyword in perony_i_tory:
            audio_sequence.append(perony_i_tory[keyword])
        elif keyword in do_z_stacji:
            audio_sequence.append(do_z_stacji[keyword])
        else:
            if index + 1 < len(components):
                compound_keyword_2 = f"{keyword}_{components[index + 1]}"
                if compound_keyword_2 in stacje:
                    audio_sequence.append(stacje[compound_keyword_2])
                    index += 1
                elif compound_keyword_2 in perony_i_tory:
                    audio_sequence.append(perony_i_tory[compound_keyword_2])
                    index += 1
                elif compound_keyword_2 in do_z_stacji:
                    audio_sequence.append(do_z_stacji[compound_keyword_2])
                    index += 1
                else:
                    if index + 2 < len(components):
                        compound_keyword_3 = f"{keyword}_{components[index + 1]}_{components[index + 2]}"
                        if compound_keyword_3 in stacje:
                            audio_sequence.append(stacje[compound_keyword_3])
                            index += 2
                        elif compound_keyword_3 in perony_i_tory:
                            audio_sequence.append(perony_i_tory[compound_keyword_3])
                            index += 2
                        elif compound_keyword_3 in do_z_stacji:
                            audio_sequence.append(do_z_stacji[compound_keyword_3])
                            index += 2
                        else:
                            print(f"Error: '{keyword}' not found in audio files.")
                    else:
                        print(f"Error: '{keyword}' not found in audio files.")
            else:
                print(f"Error: '{keyword}' not found in audio files.")
        index += 1

    return audio_sequence
# Pociąg ze stacji Warszawa Centralna do stacji Białystok przez stację bohumin odjedzie z toru siódmego przy peronie czwartym

stacje = load_audio_files("stacje")
perony_i_tory = load_audio_files("perony_i_tory")
do_z_stacji = load_audio_files("do_z_stacji")


def main():
    # input_text = ("Pociąg ze stacji Warszawa Wschodnia do stacji Poznań Główny przez stacje Kutno, Konin, odjedzie z toru drugiego przy peronie trzecim.")



    input_text = str(input("Wprowadź komunikat: "))

    components = delete_diac(input_text).lower().replace(",", "").replace(".", "").split()

    print(components)

    audio_sequence = find_audio_segment(components)

    for segment in audio_sequence:
        if segment:
            play_audio(segment)


if __name__ == "__main__":
    main()
