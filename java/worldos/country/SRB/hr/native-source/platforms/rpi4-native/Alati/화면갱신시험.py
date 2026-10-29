#!/usr/bin/env python3
"""stvaran_podaci jezgra_sustava_VALUE 그리기 코드를 domaćin Memorija_podaci 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

akcija_korijen = Path(__file__).resolve().parents[1]

def Pokreni():
    izvor_Datoteke = ['시험/화면갱신.c', 'stroj/화면그림.c', 'stroj/Terminal.c', 'stroj/widget.c']
    검증원문들 = izvor_Datoteke + ['IZVOR/화면합성.java', 'IZVOR/pano.java', '../../compiler/자바도구/기계어미리번역.java']
    odredište_VALUE = akcija_korijen/'build/verification/redraw'; odredište_VALUE.mkdir(parents=True, exist_ok=True)
    LOG_zapis = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((akcija_korijen/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Ime: hashlib.sha256((akcija_korijen/Ime).read_bytes()).hexdigest() for Ime in 검증원문들}}
    try:
        poduka_put = odredište_VALUE/'classes'; poduka_put.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(poduka_put),
            str(akcija_korijen/'IZVOR/화면합성.java'), str(akcija_korijen/'IZVOR/pano.java')])
        izvezi_tablica = {'jdraw_prepare': 'Pripremi', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'isječak',
            'jdraw_clip_value': 'isječak_VALUE', 'jdraw_begin': 'Pokreni', 'jdraw_end': 'Završi',
            'jdraw_pixel': 'slikovni_element', 'jdraw_rectangle': 'pravokutnik_ispuna', 'jdraw_pointer': 'pokazivač'}
        번역명령 = ['sh', str(akcija_korijen.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(odredište_VALUE/'crtež_VALUE.c')]
        for Spoji_se, FUNCTION_VALUE in izvezi_tablica.items(): 번역명령.extend(['--export', Spoji_se+'=화면합성.'+FUNCTION_VALUE])
        subprocess.check_call(번역명령+[str(PUTANJA) for PUTANJA in sorted(poduka_put.glob('*.class'))])
        Naredba = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + izvor_Datoteke
        crtež_odredište = odredište_VALUE/'crtež_VALUE.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(odredište_VALUE/'crtež_VALUE.c'), '-o', str(crtež_odredište)])
        subprocess.check_call(Naredba+[str(crtež_odredište), 'build/terminal-font.S', '-o', str(odredište_VALUE/'화면갱신시험')], cwd=str(akcija_korijen))
        REZULTAT = subprocess.check_output([str(odredište_VALUE/'화면갱신시험')], timeout=30).decode()
        (odredište_VALUE/'potvrditi.log').write_text(REZULTAT)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', REZULTAT)
        assert 맞음 and 'PASS:' in REZULTAT, REZULTAT
        LOG_zapis.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(REZULTAT, end='')
    finally:
        (odredište_VALUE/'report.json').write_text(json.dumps(LOG_zapis, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Pokreni()
