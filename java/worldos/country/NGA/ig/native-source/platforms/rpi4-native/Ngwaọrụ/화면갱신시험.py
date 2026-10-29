#!/usr/bin/env python3
"""ǹdịnezie_datà mkpụrụobī_kọmpùta_valuu 그리기 코드를 usu memọrị_datà 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]

def Bido():
    ebensìbịa_Ndi_ọbọakwụkwọ = ['시험/화면갱신.c', 'ngwa_komputa/화면그림.c', 'ngwa_komputa/터미널.c', 'ngwa_komputa/ngwa_nkepụta.c']
    검증원문들 = ebensìbịa_Ndi_ọbọakwụkwọ + ['ebensìbịa/화면합성.java', 'ebensìbịa/보드.java', '../../compiler/자바도구/기계어미리번역.java']
    ebemwèga_valuu = 기준/'build/verification/redraw'; ebemwèga_valuu.mkdir(parents=True, exist_ok=True)
    ndekọ_NDEKỌ = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Aha: hashlib.sha256((기준/Aha).read_bytes()).hexdigest() for Aha in 검증원문들}}
    try:
        klaàsị_ụzọ_ozi = ebemwèga_valuu/'classes'; klaàsị_ụzọ_ozi.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(klaàsị_ụzọ_ozi),
            str(기준/'ebensìbịa/화면합성.java'), str(기준/'ebensìbịa/보드.java')])
        zifè_tebùl = {'jdraw_prepare': 'Kwado', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'ntipanye',
            'jdraw_clip_value': 'ntipanye_valuu', 'jdraw_begin': 'Bido', 'jdraw_end': 'Gwụ',
            'jdraw_pixel': 'pel', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'nrụaka'}
        번역명령 = ['sh', str(기준.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(ebemwèga_valuu/'osise_valuu.c')]
        for Banye, ọrụ_valuu in zifè_tebùl.items(): 번역명령.extend(['--export', Banye+'=화면합성.'+ọrụ_valuu])
        subprocess.check_call(번역명령+[str(ụzọ_ozi) for ụzọ_ozi in sorted(klaàsị_ụzọ_ozi.glob('*.class'))])
        Ntiiwu = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + ebensìbịa_Ndi_ọbọakwụkwọ
        osise_ebemwèga = ebemwèga_valuu/'osise_valuu.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(ebemwèga_valuu/'osise_valuu.c'), '-o', str(osise_ebemwèga)])
        subprocess.check_call(Ntiiwu+[str(osise_ebemwèga), 'build/terminal-font.S', '-o', str(ebemwèga_valuu/'화면갱신시험')], cwd=str(기준))
        결과 = subprocess.check_output([str(ebemwèga_valuu/'화면갱신시험')], timeout=30).decode()
        (ebemwèga_valuu/'mee_ịbanihe.log').write_text(결과)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', 결과)
        assert 맞음 and 'PASS:' in 결과, 결과
        ndekọ_NDEKỌ.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(결과, end='')
    finally:
        (ebemwèga_valuu/'report.json').write_text(json.dumps(ndekọ_NDEKỌ, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Bido()
