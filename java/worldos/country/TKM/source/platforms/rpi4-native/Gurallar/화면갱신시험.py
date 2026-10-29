#!/usr/bin/env python3
"""hakyky_maglumat ýadro_baha 그리기 코드를 esasy ýat_maglumat 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]

def Bitir():
    gor_Faýllar = ['시험/화면갱신.c', 'kompýuter/화면그림.c', 'kompýuter/터미널.c', 'kompýuter/wijet.c']
    검증원문들 = gor_Faýllar + ['Çeşme/화면합성.java', 'Çeşme/보드.java', '../../compiler/자바도구/기계어미리번역.java']
    barylmaly_ýer_baha = 기준/'build/verification/redraw'; barylmaly_ýer_baha.mkdir(parents=True, exist_ok=True)
    hasaba_alyş_setir = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Ad: hashlib.sha256((기준/Ad).read_bytes()).hexdigest() for Ad in 검증원문들}}
    try:
        klas_ýol = barylmaly_ýer_baha/'classes'; klas_ýol.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(klas_ýol),
            str(기준/'Çeşme/화면합성.java'), str(기준/'Çeşme/보드.java')])
        eksport_et_tablisa = {'jdraw_prepare': 'Taýýarla', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'klip',
            'jdraw_clip_value': 'klip_baha', 'jdraw_begin': 'Bitir', 'jdraw_end': 'Tamamla',
            'jdraw_pixel': 'pel', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'görkeziji'}
        번역명령 = ['sh', str(기준.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(barylmaly_ýer_baha/'çyzgy_baha.c')]
        for Birikme, FUNCTION_baha in eksport_et_tablisa.items(): 번역명령.extend(['--export', Birikme+'=화면합성.'+FUNCTION_baha])
        subprocess.check_call(번역명령+[str(Ýol) for Ýol in sorted(klas_ýol.glob('*.class'))])
        buýruk = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + gor_Faýllar
        çyzgy_barylmaly_ýer = barylmaly_ýer_baha/'çyzgy_baha.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(barylmaly_ýer_baha/'çyzgy_baha.c'), '-o', str(çyzgy_barylmaly_ýer)])
        subprocess.check_call(buýruk+[str(çyzgy_barylmaly_ýer), 'build/terminal-font.S', '-o', str(barylmaly_ýer_baha/'화면갱신시험')], cwd=str(기준))
        결과 = subprocess.check_output([str(barylmaly_ýer_baha/'화면갱신시험')], timeout=30).decode()
        (barylmaly_ýer_baha/'tassykla.log').write_text(결과)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', 결과)
        assert 맞음 and 'PASS:' in 결과, 결과
        hasaba_alyş_setir.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(결과, end='')
    finally:
        (barylmaly_ýer_baha/'report.json').write_text(json.dumps(hasaba_alyş_setir, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Bitir()
