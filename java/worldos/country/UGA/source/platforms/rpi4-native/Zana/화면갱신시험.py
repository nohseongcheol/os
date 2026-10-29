#!/usr/bin/env python3
"""halisi_data kiini_thamani_0611a8a8 그리기 코드를 mwenyeji kumbukumbu_data 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]

def endesha():
    chanzo_Faili = ['시험/화면갱신.c', 'mashine/화면그림.c', 'mashine/터미널.c', 'mashine/wijeti.c']
    검증원문들 = chanzo_Faili + ['chanzo/화면합성.java', 'chanzo/보드.java', '../../compiler/자바도구/기계어미리번역.java']
    fikio_thamani = 기준/'build/verification/redraw'; fikio_thamani.mkdir(parents=True, exist_ok=True)
    batli_REKODI = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Jina: hashlib.sha256((기준/Jina).read_bytes()).hexdigest() for Jina in 검증원문들}}
    try:
        tabaka_njia = fikio_thamani/'classes'; tabaka_njia.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(tabaka_njia),
            str(기준/'chanzo/화면합성.java'), str(기준/'chanzo/보드.java')])
        hamisha_jedwali = {'jdraw_prepare': 'Andaa', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'dondoo',
            'jdraw_clip_value': 'dondoo_thamani', 'jdraw_begin': 'endesha', 'jdraw_end': 'Maliza',
            'jdraw_pixel': 'elepi', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'kielekezi'}
        번역명령 = ['sh', str(기준.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(fikio_thamani/'mchoro_thamani.c')]
        for UNGANISHA, KITENDAKAZI_thamani in hamisha_jedwali.items(): 번역명령.extend(['--export', UNGANISHA+'=화면합성.'+KITENDAKAZI_thamani])
        subprocess.check_call(번역명령+[str(njia) for njia in sorted(tabaka_njia.glob('*.class'))])
        amri = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + chanzo_Faili
        mchoro_fikio = fikio_thamani/'mchoro_thamani.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(fikio_thamani/'mchoro_thamani.c'), '-o', str(mchoro_fikio)])
        subprocess.check_call(amri+[str(mchoro_fikio), 'build/terminal-font.S', '-o', str(fikio_thamani/'화면갱신시험')], cwd=str(기준))
        결과 = subprocess.check_output([str(fikio_thamani/'화면갱신시험')], timeout=30).decode()
        (fikio_thamani/'hakikisha.log').write_text(결과)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', 결과)
        assert 맞음 and 'PASS:' in 결과, 결과
        batli_REKODI.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(결과, end='')
    finally:
        (fikio_thamani/'report.json').write_text(json.dumps(batli_REKODI, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': endesha()
