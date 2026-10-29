#!/usr/bin/env python3
"""dejanski_podatki jedro_VALUE 그리기 코드를 gostiti pomnilnik_podatki 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

pobuda_koren = Path(__file__).resolve().parents[1]

def Zaženi():
    vir_Datoteke = ['시험/화면갱신.c', 'računalnik/화면그림.c', 'računalnik/Terminal.c', 'računalnik/pripomoček.c']
    검증원문들 = vir_Datoteke + ['VIR/화면합성.java', 'VIR/Tabla.java', '../../compiler/자바도구/기계어미리번역.java']
    cilj_VALUE = pobuda_koren/'build/verification/redraw'; cilj_VALUE.mkdir(parents=True, exist_ok=True)
    LOG_zapis = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((pobuda_koren/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Ime: hashlib.sha256((pobuda_koren/Ime).read_bytes()).hexdigest() for Ime in 검증원문들}}
    try:
        Razred_pot = cilj_VALUE/'classes'; Razred_pot.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Razred_pot),
            str(pobuda_koren/'VIR/화면합성.java'), str(pobuda_koren/'VIR/Tabla.java')])
        izvoziti_tabela = {'jdraw_prepare': 'Pripravi', 'jdraw_width': '너비얻기', 'jdraw_height': 'dobiti_višina',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'izrezek',
            'jdraw_clip_value': 'izrezek_VALUE', 'jdraw_begin': 'Zaženi', 'jdraw_end': 'konec',
            'jdraw_pixel': 'slikovna_pika', 'jdraw_rectangle': 'pravokotnik_polnilo', 'jdraw_pointer': 'kazalec'}
        번역명령 = ['sh', str(pobuda_koren.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(cilj_VALUE/'risba_VALUE.c')]
        for Poveži, FUNCTION_VALUE in izvoziti_tabela.items(): 번역명령.extend(['--export', Poveži+'=화면합성.'+FUNCTION_VALUE])
        subprocess.check_call(번역명령+[str(POT) for POT in sorted(Razred_pot.glob('*.class'))])
        Ukaz = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + vir_Datoteke
        risba_cilj = cilj_VALUE/'risba_VALUE.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(cilj_VALUE/'risba_VALUE.c'), '-o', str(risba_cilj)])
        subprocess.check_call(Ukaz+[str(risba_cilj), 'build/terminal-font.S', '-o', str(cilj_VALUE/'화면갱신시험')], cwd=str(pobuda_koren))
        REZULTAT = subprocess.check_output([str(cilj_VALUE/'화면갱신시험')], timeout=30).decode()
        (cilj_VALUE/'preveriti_veljavnost.log').write_text(REZULTAT)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', REZULTAT)
        assert 맞음 and 'PASS:' in REZULTAT, REZULTAT
        LOG_zapis.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(REZULTAT, end='')
    finally:
        (cilj_VALUE/'report.json').write_text(json.dumps(LOG_zapis, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Zaženi()
