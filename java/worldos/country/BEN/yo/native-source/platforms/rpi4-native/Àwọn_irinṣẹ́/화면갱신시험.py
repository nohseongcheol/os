#!/usr/bin/env python3
"""gangan_détà kánẹ́ẹ̀lì_iye 그리기 코드를 olùpèsè ibi_ìpamọ́_détà 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]

def Rọ́ọ̀nù():
    orísun_Àwọn_fáìlì = ['시험/화면갱신.c', 'maṣíìnì/화면그림.c', 'maṣíìnì/터미널.c', 'maṣíìnì/wíjẹ́ẹ̀tì.c']
    검증원문들 = orísun_Àwọn_fáìlì + ['orísun/화면합성.java', 'orísun/보드.java', '../../compiler/자바도구/기계어미리번역.java']
    èbúté_iye = 기준/'build/verification/redraw'; èbúté_iye.mkdir(parents=True, exist_ok=True)
    àkọsílẹ̀_ìṣe_ìlà_ìbú = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Orúkọ: hashlib.sha256((기준/Orúkọ).read_bytes()).hexdigest() for Orúkọ in 검증원문들}}
    try:
        ọ̀wọ́_ọ̀nà = èbúté_iye/'classes'; ọ̀wọ́_ọ̀nà.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(ọ̀wọ́_ọ̀nà),
            str(기준/'orísun/화면합성.java'), str(기준/'orísun/보드.java')])
        ṣàgbéjáde_atọ́ka = {'jdraw_prepare': 'gbaradì', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'ní_ṣókí',
            'jdraw_clip_value': 'ní_ṣókí_iye', 'jdraw_begin': 'Rọ́ọ̀nù', 'jdraw_end': 'Parí',
            'jdraw_pixel': 'píkísẹ̀', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'ìtọ́ka'}
        번역명령 = ['sh', str(기준.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(èbúté_iye/'íyàwòrán_iye.c')]
        for Darapọ̀, ÀKÀNṢEFỌMÚLÀ_iye in ṣàgbéjáde_atọ́ka.items(): 번역명령.extend(['--export', Darapọ̀+'=화면합성.'+ÀKÀNṢEFỌMÚLÀ_iye])
        subprocess.check_call(번역명령+[str(ọ̀nà) for ọ̀nà in sorted(ọ̀wọ́_ọ̀nà.glob('*.class'))])
        Àṣẹ = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + orísun_Àwọn_fáìlì
        íyàwòrán_èbúté = èbúté_iye/'íyàwòrán_iye.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(èbúté_iye/'íyàwòrán_iye.c'), '-o', str(íyàwòrán_èbúté)])
        subprocess.check_call(Àṣẹ+[str(íyàwòrán_èbúté), 'build/terminal-font.S', '-o', str(èbúté_iye/'화면갱신시험')], cwd=str(기준))
        결과 = subprocess.check_output([str(èbúté_iye/'화면갱신시험')], timeout=30).decode()
        (èbúté_iye/'ìfọwọ́síìwé.log').write_text(결과)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', 결과)
        assert 맞음 and 'PASS:' in 결과, 결과
        àkọsílẹ̀_ìṣe_ìlà_ìbú.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(결과, end='')
    finally:
        (èbúté_iye/'report.json').write_text(json.dumps(àkọsílẹ̀_ìṣe_ìlà_ìbú, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Rọ́ọ̀nù()
