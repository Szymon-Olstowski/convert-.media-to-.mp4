# Konwersja .media do .mp4 dla kamer Tuya Smart

Ten program jest przeznaczony do konwersji plików wideo z rozszerzeniem `.media`, **często spotykanych w nagraniach z kamer IP Tuya Smart**, do popularnego formatu `.mp4`. Dodatkowo oferuje opcję spowolnienia przekonwertowanego wideo. Posiada prosty i intuicyjny interfejs graficzny oparty na bibliotece Tkinter.

## Główne funkcje:

1.  **Wybór folderu:** Użytkownik może wybrać folder zawierający pliki `.media` (np. pobrane z karty SD kamery Tuya Smart), które mają zostać przekonwertowane.
2.  **Automatyczna konwersja:** Program automatycznie wyszukuje wszystkie pliki z rozszerzeniem `.media` w wybranym folderze.
3.  **Konwersja do .mp4:** Każdy znaleziony plik `.media` jest konwertowany do formatu `.mp4` z użyciem narzędzia `ffmpeg`. Podczas konwersji ustawiana jest stała liczba klatek na sekundę (25), kodek wideo `libx264` z predefiniowanymi ustawieniami (preset: medium, CRF: 23) oraz kodek audio `aac` z bitrate 128k.
4.  **Automatyczne spowolnienie:** Po pomyślnej konwersji do `.mp4`, program automatycznie spowalnia nowo utworzony plik wideo dwukrotnie. **Jeśli oryginalny plik `.media` z kamery Tuya Smart nie zawierał informacji o ścieżce dźwiękowej w swoich metadanych, spowolnione wideo również będzie bez dźwięku.** Do spowolnienia również wykorzystywane jest narzędzie `ffmpeg`.
5.  **Nazewnictwo plików wyjściowych:** Skonwertowane i spowolnione pliki `.mp4` są zapisywane w tym samym folderze co pliki wejściowe, z dodanym znacznikiem czasu oraz sufiksem `_slow` dla spowolnionych wersji. Program dba o to, aby nie nadpisywać istniejących plików, dodając w razie potrzeby licznik do nazwy.
6.  **Wskaźnik postępu:** W trakcie konwersji i spowalniania, w oknie programu wyświetlany jest aktualny status przetwarzanego pliku.
7.  **Obsługa błędów:** Program informuje użytkownika o ewentualnych błędach, takich jak brak zainstalowanego programu `ffmpeg`, problemy z dekodowaniem JSON z `ffprobe` (używanego do sprawdzenia strumieni audio) lub inne nieoczekiwane błędy podczas procesu konwersji i spowalniania.

## Wymagania:

* Do poprawnego działania programu wymagane jest zainstalowanie narzędzia **ffmpeg** oraz **ffprobe** w systemie operacyjnym i dodanie ich do ścieżki systemowej. Program nie instaluje tych narzędzi automatycznie.
* System operacyjny z zainstalowanym interpreterem języka Python oraz biblioteką Tkinter (zazwyczaj jest standardowo instalowana z Pythonem).

## Instrukcja użycia:

1.  Uruchom skrypt Python.
2.  W oknie programu kliknij przycisk "Przeglądaj", aby wybrać folder zawierający pliki `.media` z Twojej kamery Tuya Smart.
3.  Po wybraniu folderu, kliknij przycisk "Uruchom Konwersję".
4.  Obserwuj etykietę postępu, która będzie informować o aktualnie przetwarzanym pliku.
5.  Po zakończeniu konwersji wszystkich plików, wyświetli się komunikat "Konwersja zakończona." W wybranym folderze pojawią się pliki `.mp4` oraz ich spowolnione wersje z sufiksem `_slow`. **Jeśli oryginalny plik `.media` z kamery Tuya Smart nie zawierał informacji o dźwięku, spowolnione wideo również będzie bez dźwięku.**

Ten program jest prostym narzędziem ułatwiającym konwersję nagrań z kamer **Tuya Smart** z formatu `.media` do bardziej uniwersalnego `.mp4`, z dodatkową opcją spowolnienia. **Brak dźwięku w spowolnionym wideo jest zazwyczaj spowodowany brakiem ścieżki dźwiękowej lub informacji o niej w oryginalnym pliku `.media` z kamery.** Należy to wziąć pod uwagę podczas korzystania z funkcji spowalniania.
