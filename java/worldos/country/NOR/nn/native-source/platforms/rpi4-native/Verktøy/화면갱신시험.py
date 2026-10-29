#!/usr/bin/env python3
"""faktisk_data kjerne_VALUE 그리기 코드를 vert Minne_data 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

spegle_rot = Path(__file__).resolve().parents[1]

def Køyr_2():
    kjelde_Filer = ['시험/화면갱신.c', 'maskin/화면그림.c', 'maskin/Terminal.c', 'maskin/miniprogram.c']
    검증원문들 = kjelde_Filer + ['KJELDE/화면합성.java', 'KJELDE/Tavle.java', '../../compiler/자바도구/기계어미리번역.java']
    mål_VALUE = spegle_rot/'build/verification/redraw'; mål_VALUE.mkdir(parents=True, exist_ok=True)
    LOG_rad = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((spegle_rot/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Namn: hashlib.sha256((spegle_rot/Namn).read_bytes()).hexdigest() for Namn in 검증원문들}}
    try:
        time_bane = mål_VALUE/'classes'; time_bane.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(time_bane),
            str(spegle_rot/'KJELDE/화면합성.java'), str(spegle_rot/'KJELDE/Tavle.java')])
        eksportere_tabell = {'jdraw_prepare': 'Klargjer', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'klipp',
            'jdraw_clip_value': 'klipp_VALUE', 'jdraw_begin': 'Køyr_2', 'jdraw_end': 'Ferdig',
            'jdraw_pixel': 'piksel', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'peikar'}
        번역명령 = ['sh', str(spegle_rot.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(mål_VALUE/'teikning_VALUE.c')]
        for Kopla_til, FUNCTION_VALUE in eksportere_tabell.items(): 번역명령.extend(['--export', Kopla_til+'=화면합성.'+FUNCTION_VALUE])
        subprocess.check_call(번역명령+[str(STIGE) for STIGE in sorted(time_bane.glob('*.class'))])
        Kommando = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + kjelde_Filer
        teikning_mål = mål_VALUE/'teikning_VALUE.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(mål_VALUE/'teikning_VALUE.c'), '-o', str(teikning_mål)])
        subprocess.check_call(Kommando+[str(teikning_mål), 'build/terminal-font.S', '-o', str(mål_VALUE/'화면갱신시험')], cwd=str(spegle_rot))
        forretningsmål = subprocess.check_output([str(mål_VALUE/'화면갱신시험')], timeout=30).decode()
        (mål_VALUE/'bekrefte.log').write_text(forretningsmål)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', forretningsmål)
        assert 맞음 and 'PASS:' in forretningsmål, forretningsmål
        LOG_rad.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(forretningsmål, end='')
    finally:
        (mål_VALUE/'report.json').write_text(json.dumps(LOG_rad, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Køyr_2()
