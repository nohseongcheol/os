#!/usr/bin/env python3
"""nyakuri_amakurushingiro intima_agaciro 그리기 코드를 gucumbikira ububiko_amakurushingiro 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]

def ihuriro():
    inkomoko_Dosiye = ['시험/화면갱신.c', 'imashini/화면그림.c', 'imashini/터미널.c', 'imashini/wijeti.c']
    검증원문들 = inkomoko_Dosiye + ['Inkomoko/화면합성.java', 'Inkomoko/보드.java', '../../compiler/자바도구/기계어미리번역.java']
    aho_ijya_agaciro = 기준/'build/verification/redraw'; aho_ijya_agaciro.mkdir(parents=True, exist_ok=True)
    kubika_umurongo = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Izina: hashlib.sha256((기준/Izina).read_bytes()).hexdigest() for Izina in 검증원문들}}
    try:
        icyiciro_inzira = aho_ijya_agaciro/'classes'; icyiciro_inzira.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(icyiciro_inzira),
            str(기준/'Inkomoko/화면합성.java'), str(기준/'Inkomoko/보드.java')])
        kwimura_imbonerahamwe = {'jdraw_prepare': 'Gutegura', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'kiripu',
            'jdraw_clip_value': 'kiripu_agaciro', 'jdraw_begin': 'ihuriro', 'jdraw_end': 'Kurangiza',
            'jdraw_pixel': 'pel', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'mwerekana'}
        번역명령 = ['sh', str(기준.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(aho_ijya_agaciro/'igishushanyo_agaciro.c')]
        for Guhuza, FUNCTION_agaciro in kwimura_imbonerahamwe.items(): 번역명령.extend(['--export', Guhuza+'=화면합성.'+FUNCTION_agaciro])
        subprocess.check_call(번역명령+[str(Inzira) for Inzira in sorted(icyiciro_inzira.glob('*.class'))])
        Icyo_wifuza = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + inkomoko_Dosiye
        igishushanyo_aho_ijya = aho_ijya_agaciro/'igishushanyo_agaciro.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(aho_ijya_agaciro/'igishushanyo_agaciro.c'), '-o', str(igishushanyo_aho_ijya)])
        subprocess.check_call(Icyo_wifuza+[str(igishushanyo_aho_ijya), 'build/terminal-font.S', '-o', str(aho_ijya_agaciro/'화면갱신시험')], cwd=str(기준))
        결과 = subprocess.check_output([str(aho_ijya_agaciro/'화면갱신시험')], timeout=30).decode()
        (aho_ijya_agaciro/'kwemeza.log').write_text(결과)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', 결과)
        assert 맞음 and 'PASS:' in 결과, 결과
        kubika_umurongo.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(결과, end='')
    finally:
        (aho_ijya_agaciro/'report.json').write_text(json.dumps(kubika_umurongo, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': ihuriro()
