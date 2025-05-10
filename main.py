import os
import subprocess
import json
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

def spowolnij_mp4(sciezka_wejsciowa, sciezka_wyjsciowa, okno_glowne, label_postepu):
    try:
        nazwa_pliku = os.path.basename(sciezka_wejsciowa)
        nazwa_wyjsciowa_pliku = os.path.basename(sciezka_wyjsciowa)
        label_postepu.config(text=f"Spowalnianie: {nazwa_pliku} -> {nazwa_wyjsciowa_pliku}")
        okno_glowne.update()

        polecenie_sprawdzenia_audio = [
            'ffprobe',
            '-i', sciezka_wejsciowa,
            '-show_streams',
            '-print_format', 'json',
            '-loglevel', 'error'
        ]
        wynik_sprawdzenia_audio = subprocess.run(polecenie_sprawdzenia_audio, capture_output=True, text=True, check=True)
        metadane_audio = json.loads(wynik_sprawdzenia_audio.stdout)

        ma_audio = False
        if 'streams' in metadane_audio:
            for stream in metadane_audio['streams']:
                if stream.get('codec_type') == 'audio':
                    ma_audio = True
                    break

        polecenie_spowolnienia = [
            'ffmpeg',
            '-i', sciezka_wejsciowa,
            '-map', '0:v',
            '-filter:v', 'setpts=2*PTS'
        ]

        if ma_audio:
            polecenie_spowolnienia.extend(['-map', '0:a', '-filter:a', 'atempo=1'])

        polecenie_spowolnienia.extend([
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '128k',
            sciezka_wyjsciowa
        ])

        subprocess.run(polecenie_spowolnienia, check=True)
        label_postepu.config(text=f"Spowolniono i zapisano jako: {nazwa_wyjsciowa_pliku}")
        okno_glowne.update()
        return True
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Błąd", f"Błąd podczas spowalniania pliku MP4: {e}")
        return False
    except FileNotFoundError:
        messagebox.showerror("Błąd", "Program ffmpeg nie został znaleziony. Upewnij się, że jest zainstalowany i dodany do ścieżki systemowej.")
        return False
    except json.JSONDecodeError:
        messagebox.showerror("Błąd", "Błąd podczas dekodowania JSON z ffprobe.")
        return False
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił inny błąd podczas spowalniania: {e}")
        return False

def konwertuj_jeden_plik(sciezka_wejsciowa_media, folder_wyjsciowy, okno_glowne, label_postepu):
    teraz = datetime.now().strftime("%Y%m%d_%H%M%S")
    nazwa_pliku_bez_rozszerzenia = os.path.splitext(os.path.basename(sciezka_wejsciowa_media))[0]
    nazwa_wyjsciowa_bez_rozszerzenia = os.path.join(folder_wyjsciowy, f"{teraz}_{nazwa_pliku_bez_rozszerzenia}")

    nazwa_wyjsciowa_mp4 = f"{nazwa_wyjsciowa_bez_rozszerzenia}.mp4"
    licznik = 1
    while os.path.exists(nazwa_wyjsciowa_mp4):
        nazwa_wyjsciowa_mp4 = f"{nazwa_wyjsciowa_bez_rozszerzenia}_{licznik}.mp4"
        licznik += 1

    try:
        nazwa_wejsciowa_pliku = os.path.basename(sciezka_wejsciowa_media)
        nazwa_wyjsciowa_pliku = os.path.basename(nazwa_wyjsciowa_mp4)
        label_postepu.config(text=f"Konwertowanie: {nazwa_wejsciowa_pliku} -> {nazwa_wyjsciowa_pliku}")
        okno_glowne.update()

        polecenie_konwersji = [
            'ffmpeg',
            '-i', sciezka_wejsciowa_media,
            '-r', '25',
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '128k',
            nazwa_wyjsciowa_mp4
        ]
        subprocess.run(polecenie_konwersji, check=True)
        label_postepu.config(text=f"Skonwertowano: {nazwa_wejsciowa_pliku} -> {nazwa_wyjsciowa_pliku}")
        okno_glowne.update()

        # Teraz spowolnij wygenerowany plik MP4
        nazwa_wyjsciowa_slow_mp4 = f"{nazwa_wyjsciowa_bez_rozszerzenia}_slow.mp4"
        licznik_slow = 1
        while os.path.exists(nazwa_wyjsciowa_slow_mp4):
            nazwa_wyjsciowa_slow_mp4 = f"{nazwa_wyjsciowa_bez_rozszerzenia}_slow_{licznik_slow}.mp4"
            licznik_slow += 1

        spowolnij_mp4(nazwa_wyjsciowa_mp4, nazwa_wyjsciowa_slow_mp4, okno_glowne, label_postepu)

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Błąd", f"Błąd podczas konwersji {nazwa_wejsciowa_pliku}: {e}")
    except FileNotFoundError:
        messagebox.showerror("Błąd", "Program ffmpeg nie został znaleziony. Upewnij się, że jest zainstalowany i dodany do ścieżki systemowej.")
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił błąd podczas konwersji {nazwa_wejsciowa_pliku}: {e}")

def wybierz_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder)

def uruchom_konwersje():
    folder_do_konwersji = folder_entry.get()
    if not folder_do_konwersji:
        messagebox.showerror("Błąd", "Proszę wybrać folder.")
        return

    pliki_media = [plik for plik in os.listdir(folder_do_konwersji) if plik.endswith(".media")]
    if not pliki_media:
        messagebox.showinfo("Informacja", "Nie znaleziono plików .media w wybranym folderze.")
        return

    for plik in pliki_media:
        sciezka_wejsciowa_media = os.path.join(folder_do_konwersji, plik)
        konwertuj_jeden_plik(sciezka_wejsciowa_media, folder_do_konwersji, okno, label_postepu)

    messagebox.showinfo("Zakończono", "Konwersja zakończona.")

# Tworzenie okna głównego
okno = tk.Tk()
okno.title("Konwerter .media do .mp4 (ze spowolnieniem)")

# Wybór folderu
folder_label = tk.Label(okno, text="Wybierz folder z plikami .media:")
folder_label.pack(pady=5)

folder_entry = tk.Entry(okno, width=50)
folder_entry.pack(padx=10, pady=5)

folder_button = tk.Button(okno, text="Przeglądaj", command=wybierz_folder)
folder_button.pack(pady=5)

# Przycisk uruchamiający konwersję
uruchom_button = tk.Button(okno, text="Uruchom Konwersję", command=uruchom_konwersje)
uruchom_button.pack(pady=10)

# Etykieta postępu
label_postepu = tk.Label(okno, text="")
label_postepu.pack(pady=5)

okno.mainloop()