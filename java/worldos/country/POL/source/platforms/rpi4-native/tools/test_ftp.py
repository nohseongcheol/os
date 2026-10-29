#!/usr/bin/env python3
"""기존 ścieżka_2 호환 punkt_wejścia. rzeczywisty_dane implementacja: ../narzędzia/test_FTP.py"""
import importlib as WYCINEK_WARTOŚĆ
import sys as system_operacyjny_WARTOŚĆ
from pathlib import Path as ścieżka_2
system_operacyjny_WARTOŚĆ.path.insert(0, str(ścieżka_2(__file__).resolve().parents[1] / 'narzędzia'))
if __name__ == '__main__':
    import runpy as program_Launcher
    program_Launcher.run_module('test_FTP', run_name='__main__', alter_sys=True)
else:
    implementacja = WYCINEK_WARTOŚĆ.import_module('test_FTP')
    mapowanie_WARTOŚĆ = {'timeout': 'wykonanie_TIMEOUT', 'payload': 'ładunek_dane', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': 'fragment_WARTOŚĆ_652d4b53', 'data': 'dane', 'proc': 'Proces', 'code': 'instrukcja_SEKWENCJA', 'linux': '리눅스파일', 'archive': 'Archiwum', 'main': 'Uruchom_2', 'net_source': 'NET_źródło', 'temporary': '임시자원', 'static_source': 'statyczny_źródło', 'java_source': '자바원문', 'echo': 'echo_serwer_wpis', 'ROOT': 'Project_korzeń', 'text': 'tekst', 'marker': 'pisak', 'EchoFixture': 'echo_warunki_początkowe', 'command': 'polecenie', 'out': 'KR_dane', 'expected': '예상결과', 'server_source': 'serwer_źródło', 'shell': 'powłoka', 'upload': 'Upload_Files', 'transcript': 'transkrypcja', 'port': 'numer_portu', 'native': 'natywny', 'elf': 'plik_wykonywalny', 'server_udp_port': 'serwer_datagram_port', 'packed': '묶인자료', 'bridge': 'mostek', 'selector': 'selektor', 'end': 'Koniec_przesunąć', 'e': '보조항목', 'ftp': 'transfer_plików_połączenie', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'węzeł_równorzędny_WARTOŚĆ', 'result': 'WYNIK', 'unchanged': '보존자료', 'line': 'wiersz_wejścia', 'server_tcp_port': 'serwer_Stream_port', 'source': '원본자료', 'NetworkBridge': 'mostek_3de4fe3a', 'jar': '자바꾸러미', 'receive': 'odbierać_e_mail', 'report': 'walidacja_Raport'}
    for Wstecz_towar, bieżący_towar in mapowanie_WARTOŚĆ.items():
        if hasattr(implementacja, bieżący_towar): globals()[Wstecz_towar] = getattr(implementacja, bieżący_towar)
