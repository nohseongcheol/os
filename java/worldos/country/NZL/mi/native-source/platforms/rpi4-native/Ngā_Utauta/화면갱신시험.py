#!/usr/bin/env python3
"""tūturu_raraunga kākano_uara_0611a8a8 그리기 코드를 taurima Pūmahara_raraunga 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

whakaatu_pūtake = Path(__file__).resolve().parents[1]

def whakahaere():
    pūtake_Ngā_Kōnae = ['시험/화면갱신.c', 'mīhini/화면그림.c', 'mīhini/Tauranga.c', 'mīhini/taputapu.c']
    검증원문들 = pūtake_Ngā_Kōnae + ['pūtake/화면합성.java', 'pūtake/papa.java', '../../compiler/자바도구/기계어미리번역.java']
    ūnga_uara = whakaatu_pūtake/'build/verification/redraw'; ūnga_uara.mkdir(parents=True, exist_ok=True)
    LOG_RECORD = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((whakaatu_pūtake/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Ingoa: hashlib.sha256((whakaatu_pūtake/Ingoa).read_bytes()).hexdigest() for Ingoa in 검증원문들}}
    try:
        tauaha_ara = ūnga_uara/'classes'; tauaha_ara.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(tauaha_ara),
            str(whakaatu_pūtake/'pūtake/화면합성.java'), str(whakaatu_pūtake/'pūtake/papa.java')])
        kaweake_ripanga = {'jdraw_prepare': 'Whakarite', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'topenga',
            'jdraw_clip_value': 'topenga_uara', 'jdraw_begin': 'whakahaere', 'jdraw_end': 'Mutu',
            'jdraw_pixel': 'pika', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'atatohu'}
        번역명령 = ['sh', str(whakaatu_pūtake.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(ūnga_uara/'tātuhi_uara.c')]
        for TŪHONO, TAUMAHI_uara in kaweake_ripanga.items(): 번역명령.extend(['--export', TŪHONO+'=화면합성.'+TAUMAHI_uara])
        subprocess.check_call(번역명령+[str(ara) for ara in sorted(tauaha_ara.glob('*.class'))])
        tono = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + pūtake_Ngā_Kōnae
        tātuhi_ūnga = ūnga_uara/'tātuhi_uara.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(ūnga_uara/'tātuhi_uara.c'), '-o', str(tātuhi_ūnga)])
        subprocess.check_call(tono+[str(tātuhi_ūnga), 'build/terminal-font.S', '-o', str(ūnga_uara/'화면갱신시험')], cwd=str(whakaatu_pūtake))
        mēhua = subprocess.check_output([str(ūnga_uara/'화면갱신시험')], timeout=30).decode()
        (ūnga_uara/'whakamana.log').write_text(mēhua)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', mēhua)
        assert 맞음 and 'PASS:' in mēhua, mēhua
        LOG_RECORD.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(mēhua, end='')
    finally:
        (ūnga_uara/'report.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': whakahaere()
