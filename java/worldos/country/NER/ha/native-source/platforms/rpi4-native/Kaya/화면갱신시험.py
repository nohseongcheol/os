#!/usr/bin/env python3
"""Na_hakika_Tarin_bayani Kwara_Daraja 그리기 코드를 sauka Mahardatar_kwamfuta_Tarin_bayani 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]

def Tafiyar_da():
    tushe_Fayiloli = ['시험/화면갱신.c', 'na_ura_mai_kwakwalwa/화면그림.c', 'na_ura_mai_kwakwalwa/터미널.c', 'na_ura_mai_kwakwalwa/wijet.c']
    검증원문들 = tushe_Fayiloli + ['tushe/화면합성.java', 'tushe/보드.java', '../../compiler/자바도구/기계어미리번역.java']
    Zangon_ƙarshe_Daraja = 기준/'build/verification/redraw'; Zangon_ƙarshe_Daraja.mkdir(parents=True, exist_ok=True)
    logu_naɗa = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Suna: hashlib.sha256((기준/Suna).read_bytes()).hexdigest() for Suna in 검증원문들}}
    try:
        Aji_Hanyar_shiga = Zangon_ƙarshe_Daraja/'classes'; Aji_Hanyar_shiga.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Aji_Hanyar_shiga),
            str(기준/'tushe/화면합성.java'), str(기준/'tushe/보드.java')])
        Fitar_da_tebur = {'jdraw_prepare': 'Shirya', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'darfi',
            'jdraw_clip_value': 'darfi_Daraja', 'jdraw_begin': 'Tafiyar_da', 'jdraw_end': 'Gama',
            'jdraw_pixel': 'pel', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'manuni'}
        번역명령 = ['sh', str(기준.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(Zangon_ƙarshe_Daraja/'zane_Daraja.c')]
        for Haɗi, AIKI_Daraja in Fitar_da_tebur.items(): 번역명령.extend(['--export', Haɗi+'=화면합성.'+AIKI_Daraja])
        subprocess.check_call(번역명령+[str(Hanyar_shiga) for Hanyar_shiga in sorted(Aji_Hanyar_shiga.glob('*.class'))])
        Umarni = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + tushe_Fayiloli
        zane_Zangon_ƙarshe = Zangon_ƙarshe_Daraja/'zane_Daraja.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(Zangon_ƙarshe_Daraja/'zane_Daraja.c'), '-o', str(zane_Zangon_ƙarshe)])
        subprocess.check_call(Umarni+[str(zane_Zangon_ƙarshe), 'build/terminal-font.S', '-o', str(Zangon_ƙarshe_Daraja/'화면갱신시험')], cwd=str(기준))
        결과 = subprocess.check_output([str(Zangon_ƙarshe_Daraja/'화면갱신시험')], timeout=30).decode()
        (Zangon_ƙarshe_Daraja/'inganta.log').write_text(결과)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', 결과)
        assert 맞음 and 'PASS:' in 결과, 결과
        logu_naɗa.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(결과, end='')
    finally:
        (Zangon_ƙarshe_Daraja/'report.json').write_text(json.dumps(logu_naɗa, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Tafiyar_da()
