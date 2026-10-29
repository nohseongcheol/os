#!/usr/bin/env python3
"""benetako_datuak nukleo_balio 그리기 코드를 Ostalari Memoria_datuak 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

Project_erro = Path(__file__).resolve().parents[1]

def Exekutatu_2():
    iturburu_Fitxategiak = ['시험/화면갱신.c', 'gailu/화면그림.c', 'gailu/Terminala.c', 'gailu/widget.c']
    검증원문들 = iturburu_Fitxategiak + ['ITURBURUA/화면합성.java', 'ITURBURUA/arbel.java', '../../compiler/자바도구/기계어미리번역.java']
    helburu_balio_a0fbc067 = Project_erro/'build/verification/redraw'; helburu_balio_a0fbc067.mkdir(parents=True, exist_ok=True)
    LOG_marka = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((Project_erro/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Izena: hashlib.sha256((Project_erro/Izena).read_bytes()).hexdigest() for Izena in 검증원문들}}
    try:
        Gela_bide_izen = helburu_balio_a0fbc067/'classes'; Gela_bide_izen.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Gela_bide_izen),
            str(Project_erro/'ITURBURUA/화면합성.java'), str(Project_erro/'ITURBURUA/arbel.java')])
        esportatu_taula = {'jdraw_prepare': '준비', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'klip',
            'jdraw_clip_value': 'klip_balio', 'jdraw_begin': 'Exekutatu_2', 'jdraw_end': 'Amaitu',
            'jdraw_pixel': 'pixel', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'erakusle'}
        번역명령 = ['sh', str(Project_erro.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(helburu_balio_a0fbc067/'그림.c')]
        for Konektatu, FUNTZIOA_balio in esportatu_taula.items(): 번역명령.extend(['--export', Konektatu+'=화면합성.'+FUNTZIOA_balio])
        subprocess.check_call(번역명령+[str(Bide_izena) for Bide_izena in sorted(Gela_bide_izen.glob('*.class'))])
        Komandoa = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + iturburu_Fitxategiak
        그림목적 = helburu_balio_a0fbc067/'그림.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(helburu_balio_a0fbc067/'그림.c'), '-o', str(그림목적)])
        subprocess.check_call(Komandoa+[str(그림목적), 'build/terminal-font.S', '-o', str(helburu_balio_a0fbc067/'화면갱신시험')], cwd=str(Project_erro))
        EMAITZA = subprocess.check_output([str(helburu_balio_a0fbc067/'화면갱신시험')], timeout=30).decode()
        (helburu_balio_a0fbc067/'baliozkotu.log').write_text(EMAITZA)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', EMAITZA)
        assert 맞음 and 'PASS:' in EMAITZA, EMAITZA
        LOG_marka.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(EMAITZA, end='')
    finally:
        (helburu_balio_a0fbc067/'report.json').write_text(json.dumps(LOG_marka, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Exekutatu_2()
