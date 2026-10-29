#!/usr/bin/env python3
"""tegelik_andmed tuum_VALUE 그리기 코드를 host Mälu_andmed 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

Project_juur = Path(__file__).resolve().parents[1]

def Käivita_2():
    lähe_Failid = ['시험/화면갱신.c', 'arvuti/화면그림.c', 'arvuti/terminal.c', 'arvuti/vidin.c']
    검증원문들 = lähe_Failid + ['ALLIKAS/화면합성.java', 'ALLIKAS/Tahvel.java', '../../compiler/자바도구/기계어미리번역.java']
    sihtkoht_VALUE = Project_juur/'build/verification/redraw'; sihtkoht_VALUE.mkdir(parents=True, exist_ok=True)
    LOG_kirje = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((Project_juur/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Nimi_2: hashlib.sha256((Project_juur/Nimi_2).read_bytes()).hexdigest() for Nimi_2 in 검증원문들}}
    try:
        tund_tee = sihtkoht_VALUE/'classes'; tund_tee.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(tund_tee),
            str(Project_juur/'ALLIKAS/화면합성.java'), str(Project_juur/'ALLIKAS/Tahvel.java')])
        eksportima_tabel = {'jdraw_prepare': 'Ettevalmistamine', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'klipp',
            'jdraw_clip_value': 'klipp_VALUE', 'jdraw_begin': 'Käivita_2', 'jdraw_end': 'lõpp',
            'jdraw_pixel': 'piksel', 'jdraw_rectangle': 'ristkülik_täide', 'jdraw_pointer': 'kursor'}
        번역명령 = ['sh', str(Project_juur.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(sihtkoht_VALUE/'joonis_VALUE.c')]
        for Ühendu, FUNCTION_VALUE in eksportima_tabel.items(): 번역명령.extend(['--export', Ühendu+'=화면합성.'+FUNCTION_VALUE])
        subprocess.check_call(번역명령+[str(RADA) for RADA in sorted(tund_tee.glob('*.class'))])
        Käsk = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + lähe_Failid
        joonis_sihtkoht = sihtkoht_VALUE/'joonis_VALUE.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(sihtkoht_VALUE/'joonis_VALUE.c'), '-o', str(joonis_sihtkoht)])
        subprocess.check_call(Käsk+[str(joonis_sihtkoht), 'build/terminal-font.S', '-o', str(sihtkoht_VALUE/'화면갱신시험')], cwd=str(Project_juur))
        TULEMUS = subprocess.check_output([str(sihtkoht_VALUE/'화면갱신시험')], timeout=30).decode()
        (sihtkoht_VALUE/'valideerima.log').write_text(TULEMUS)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', TULEMUS)
        assert 맞음 and 'PASS:' in TULEMUS, TULEMUS
        LOG_kirje.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(TULEMUS, end='')
    finally:
        (sihtkoht_VALUE/'report.json').write_text(json.dumps(LOG_kirje, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Käivita_2()
