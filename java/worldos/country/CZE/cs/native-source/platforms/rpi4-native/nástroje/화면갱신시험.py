#!/usr/bin/env python3
"""skutečný_data jádro_HODNOTA 그리기 코드를 hostit Paměť_data 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

akce_kořen = Path(__file__).resolve().parents[1]

def Spustit_2():
    zdroj_Files = ['zkoušky/화면갱신.c', 'počítač/화면그림.c', 'počítač/interpret_příkazů.c', 'počítač/prvek_obrazovky.c']
    검증원문들 = zdroj_Files + ['zdrojový_soubor/화면합성.java', 'zdrojový_soubor/Panel.java', '../../compiler/자바도구/기계어미리번역.java']
    cíl_HODNOTA = akce_kořen/'build/verification/redraw'; cíl_HODNOTA.mkdir(parents=True, exist_ok=True)
    LOGZ_ZÁZNAM = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((akce_kořen/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Název: hashlib.sha256((akce_kořen/Název).read_bytes()).hexdigest() for Název in 검증원문들}}
    try:
        Třída_cesta = cíl_HODNOTA/'classes'; Třída_cesta.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Třída_cesta),
            str(akce_kořen/'zdrojový_soubor/화면합성.java'), str(akce_kořen/'zdrojový_soubor/Panel.java')])
        exportovat_tabulka = {'jdraw_prepare': 'Připravit', 'jdraw_width': '너비얻기', 'jdraw_height': 'get_výška',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'oříznout',
            'jdraw_clip_value': 'oříznout_HODNOTA', 'jdraw_begin': 'Spustit_2', 'jdraw_end': 'Dokončit',
            'jdraw_pixel': 'pixel', 'jdraw_rectangle': 'obdélník_výplň', 'jdraw_pointer': 'ukazatel'}
        번역명령 = ['sh', str(akce_kořen.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(cíl_HODNOTA/'kreslení_HODNOTA.c')]
        for Připojit, funkce_HODNOTA in exportovat_tabulka.items(): 번역명령.extend(['--export', Připojit+'=화면합성.'+funkce_HODNOTA])
        subprocess.check_call(번역명령+[str(cesta_2) for cesta_2 in sorted(Třída_cesta.glob('*.class'))])
        příkaz = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + zdroj_Files
        kreslení_cíl = cíl_HODNOTA/'kreslení_HODNOTA.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(cíl_HODNOTA/'kreslení_HODNOTA.c'), '-o', str(kreslení_cíl)])
        subprocess.check_call(příkaz+[str(kreslení_cíl), 'build/terminal-font.S', '-o', str(cíl_HODNOTA/'화면갱신시험')], cwd=str(akce_kořen))
        VÝSLEDEK = subprocess.check_output([str(cíl_HODNOTA/'화면갱신시험')], timeout=30).decode()
        (cíl_HODNOTA/'ověřit_5fb2b747.log').write_text(VÝSLEDEK)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', VÝSLEDEK)
        assert 맞음 and 'PASS:' in VÝSLEDEK, VÝSLEDEK
        LOGZ_ZÁZNAM.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(VÝSLEDEK, end='')
    finally:
        (cíl_HODNOTA/'report.json').write_text(json.dumps(LOGZ_ZÁZNAM, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Spustit_2()
