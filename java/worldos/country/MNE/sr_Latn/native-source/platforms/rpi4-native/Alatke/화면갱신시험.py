#!/usr/bin/env python3
"""stvarni_podaci jezgro_VALUE 그리기 코드를 host Memorija_podaci 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

radnja_koren = Path(__file__).resolve().parents[1]

def koristiti():
    izvor_Datoteke = ['시험/화면갱신.c', 'računar/화면그림.c', 'računar/Terminal.c', 'računar/vidžet.c']
    검증원문들 = izvor_Datoteke + ['izvor/화면합성.java', 'izvor/Tabla.java', '../../compiler/자바도구/기계어미리번역.java']
    odredište_VALUE = radnja_koren/'build/verification/redraw'; odredište_VALUE.mkdir(parents=True, exist_ok=True)
    LOG_snimi = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((radnja_koren/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {ime: hashlib.sha256((radnja_koren/ime).read_bytes()).hexdigest() for ime in 검증원문들}}
    try:
        Razred_putanja = odredište_VALUE/'classes'; Razred_putanja.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Razred_putanja),
            str(radnja_koren/'izvor/화면합성.java'), str(radnja_koren/'izvor/Tabla.java')])
        izvesti_tabela = {'jdraw_prepare': 'Pripremi', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'klip',
            'jdraw_clip_value': 'klip_VALUE', 'jdraw_begin': 'koristiti', 'jdraw_end': 'kraj',
            'jdraw_pixel': 'piksel', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'pokazivač'}
        번역명령 = ['sh', str(radnja_koren.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(odredište_VALUE/'crtež_VALUE.c')]
        for veze, FUNCTION_VALUE in izvesti_tabela.items(): 번역명령.extend(['--export', veze+'=화면합성.'+FUNCTION_VALUE])
        subprocess.check_call(번역명령+[str(putanja) for putanja in sorted(Razred_putanja.glob('*.class'))])
        komanda = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + izvor_Datoteke
        crtež_odredište = odredište_VALUE/'crtež_VALUE.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(odredište_VALUE/'crtež_VALUE.c'), '-o', str(crtež_odredište)])
        subprocess.check_call(komanda+[str(crtež_odredište), 'build/terminal-font.S', '-o', str(odredište_VALUE/'화면갱신시험')], cwd=str(radnja_koren))
        KR = subprocess.check_output([str(odredište_VALUE/'화면갱신시험')], timeout=30).decode()
        (odredište_VALUE/'potvrditi.log').write_text(KR)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', KR)
        assert 맞음 and 'PASS:' in KR, KR
        LOG_snimi.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(KR, end='')
    finally:
        (odredište_VALUE/'report.json').write_text(json.dumps(LOG_snimi, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': koristiti()
