#!/usr/bin/env python3
"""skutočný_údaje jadro_VALUE 그리기 코드를 hostiteľ Pamäť_údaje 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

akcia_koreň = Path(__file__).resolve().parents[1]

def Spustiť_2():
    zdroj_Súbory = ['시험/화면갱신.c', 'počítač_5eb260fa/화면그림.c', 'počítač_5eb260fa/Terminál.c', 'počítač_5eb260fa/widget.c']
    검증원문들 = zdroj_Súbory + ['ZDROJ/화면합성.java', 'ZDROJ/Panel.java', '../../compiler/자바도구/기계어미리번역.java']
    cieľ_VALUE = akcia_koreň/'build/verification/redraw'; cieľ_VALUE.mkdir(parents=True, exist_ok=True)
    LOG_RECORD = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((akcia_koreň/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Názov: hashlib.sha256((akcia_koreň/Názov).read_bytes()).hexdigest() for Názov in 검증원문들}}
    try:
        lekcia_cesta = cieľ_VALUE/'classes'; lekcia_cesta.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(lekcia_cesta),
            str(akcia_koreň/'ZDROJ/화면합성.java'), str(akcia_koreň/'ZDROJ/Panel.java')])
        exportovať_tabuľka = {'jdraw_prepare': 'Pripraviť', 'jdraw_width': '너비얻기', 'jdraw_height': 'načítať_výška',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'klip',
            'jdraw_clip_value': 'klip_VALUE', 'jdraw_begin': 'Spustiť_2', 'jdraw_end': 'Dokončiť',
            'jdraw_pixel': 'pixel', 'jdraw_rectangle': 'obdĺžnik_výplň', 'jdraw_pointer': 'ukazovateľ'}
        번역명령 = ['sh', str(akcia_koreň.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(cieľ_VALUE/'kresba_VALUE.c')]
        for Pripojiť, funkcia_VALUE in exportovať_tabuľka.items(): 번역명령.extend(['--export', Pripojiť+'=화면합성.'+funkcia_VALUE])
        subprocess.check_call(번역명령+[str(Cesta) for Cesta in sorted(lekcia_cesta.glob('*.class'))])
        Príkaz = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + zdroj_Súbory
        kresba_cieľ = cieľ_VALUE/'kresba_VALUE.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(cieľ_VALUE/'kresba_VALUE.c'), '-o', str(kresba_cieľ)])
        subprocess.check_call(Príkaz+[str(kresba_cieľ), 'build/terminal-font.S', '-o', str(cieľ_VALUE/'화면갱신시험')], cwd=str(akcia_koreň))
        KR = subprocess.check_output([str(cieľ_VALUE/'화면갱신시험')], timeout=30).decode()
        (cieľ_VALUE/'overiť_5fb2b747.log').write_text(KR)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', KR)
        assert 맞음 and 'PASS:' in KR, KR
        LOG_RECORD.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(KR, end='')
    finally:
        (cieľ_VALUE/'report.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Spustiť_2()
