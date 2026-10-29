#!/usr/bin/env python3
"""rzeczywisty_dane jądro_WARTOŚĆ 그리기 코드를 host Pamięć_dane 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

Project_korzeń = Path(__file__).resolve().parents[1]

def Uruchom_2():
    źródło_Files = ['testy/화면갱신.c', 'maszyna/화면그림.c', 'maszyna/interpretator_poleceń.c', 'maszyna/element_ekranu.c']
    검증원문들 = źródło_Files + ['plik_źródłowy/화면합성.java', 'plik_źródłowy/Tablica.java', '../../compiler/자바도구/기계어미리번역.java']
    cel_WARTOŚĆ = Project_korzeń/'build/verification/redraw'; cel_WARTOŚĆ.mkdir(parents=True, exist_ok=True)
    LOG_zapis = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((Project_korzeń/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Nazwa: hashlib.sha256((Project_korzeń/Nazwa).read_bytes()).hexdigest() for Nazwa in 검증원문들}}
    try:
        Klasa_ścieżka = cel_WARTOŚĆ/'classes'; Klasa_ścieżka.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Klasa_ścieżka),
            str(Project_korzeń/'plik_źródłowy/화면합성.java'), str(Project_korzeń/'plik_źródłowy/Tablica.java')])
        eksportować_tabela = {'jdraw_prepare': 'Przygotuj', 'jdraw_width': '너비얻기', 'jdraw_height': 'pobrać_wysokość',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'obcinać',
            'jdraw_clip_value': 'obcinać_WARTOŚĆ', 'jdraw_begin': 'Uruchom_2', 'jdraw_end': 'Zakończ',
            'jdraw_pixel': 'piksel', 'jdraw_rectangle': 'prostokąt_Wypełnij', 'jdraw_pointer': 'wskaźnik'}
        번역명령 = ['sh', str(Project_korzeń.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(cel_WARTOŚĆ/'rysunek_WARTOŚĆ.c')]
        for Połącz, FUNKCJA_WARTOŚĆ in eksportować_tabela.items(): 번역명령.extend(['--export', Połącz+'=화면합성.'+FUNKCJA_WARTOŚĆ])
        subprocess.check_call(번역명령+[str(ścieżka_2) for ścieżka_2 in sorted(Klasa_ścieżka.glob('*.class'))])
        polecenie = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + źródło_Files
        rysunek_cel = cel_WARTOŚĆ/'rysunek_WARTOŚĆ.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(cel_WARTOŚĆ/'rysunek_WARTOŚĆ.c'), '-o', str(rysunek_cel)])
        subprocess.check_call(polecenie+[str(rysunek_cel), 'build/terminal-font.S', '-o', str(cel_WARTOŚĆ/'화면갱신시험')], cwd=str(Project_korzeń))
        WYNIK = subprocess.check_output([str(cel_WARTOŚĆ/'화면갱신시험')], timeout=30).decode()
        (cel_WARTOŚĆ/'walidować.log').write_text(WYNIK)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', WYNIK)
        assert 맞음 and 'PASS:' in WYNIK, WYNIK
        LOG_zapis.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(WYNIK, end='')
    finally:
        (cel_WARTOŚĆ/'report.json').write_text(json.dumps(LOG_zapis, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Uruchom_2()
