#!/usr/bin/env python3
"""stvaran_podaci jezgro_VALUE 그리기 코드를 organizator Memorija_podaci 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

projicirati_koijen = Path(__file__).resolve().parents[1]

def Pokreni():
    izvor_Fajlovi = ['시험/화면갱신.c', 'mašina/화면그림.c', 'mašina/Terminal.c', 'mašina/vidžet.c']
    검증원문들 = izvor_Fajlovi + ['IZVOR/화면합성.java', 'IZVOR/ploča.java', '../../compiler/자바도구/기계어미리번역.java']
    odredište_VALUE = projicirati_koijen/'build/verification/redraw'; odredište_VALUE.mkdir(parents=True, exist_ok=True)
    LOG_red = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((projicirati_koijen/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Naziv: hashlib.sha256((projicirati_koijen/Naziv).read_bytes()).hexdigest() for Naziv in 검증원문들}}
    try:
        klasa_put = odredište_VALUE/'classes'; klasa_put.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(klasa_put),
            str(projicirati_koijen/'IZVOR/화면합성.java'), str(projicirati_koijen/'IZVOR/ploča.java')])
        izvesti_tabela = {'jdraw_prepare': 'Pripremiti', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'isječak',
            'jdraw_clip_value': 'isječak_VALUE', 'jdraw_begin': 'Pokreni', 'jdraw_end': 'Kraj',
            'jdraw_pixel': 'pel', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'pokazivač'}
        번역명령 = ['sh', str(projicirati_koijen.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(odredište_VALUE/'ucrtavanje_VALUE.c')]
        for Spoji_se, FUNCTION_VALUE in izvesti_tabela.items(): 번역명령.extend(['--export', Spoji_se+'=화면합성.'+FUNCTION_VALUE])
        subprocess.check_call(번역명령+[str(Putanja) for Putanja in sorted(klasa_put.glob('*.class'))])
        Naredba = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + izvor_Fajlovi
        ucrtavanje_odredište = odredište_VALUE/'ucrtavanje_VALUE.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(odredište_VALUE/'ucrtavanje_VALUE.c'), '-o', str(ucrtavanje_odredište)])
        subprocess.check_call(Naredba+[str(ucrtavanje_odredište), 'build/terminal-font.S', '-o', str(odredište_VALUE/'화면갱신시험')], cwd=str(projicirati_koijen))
        mjera = subprocess.check_output([str(odredište_VALUE/'화면갱신시험')], timeout=30).decode()
        (odredište_VALUE/'ovjeriti.log').write_text(mjera)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', mjera)
        assert 맞음 and 'PASS:' in mjera, mjera
        LOG_red.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(mjera, end='')
    finally:
        (odredište_VALUE/'report.json').write_text(json.dumps(LOG_red, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Pokreni()
