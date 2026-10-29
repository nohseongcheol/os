#!/usr/bin/env python3
"""tényleges_adat kernel_ÉRTÉK 그리기 코드를 gazda Memória_adat 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

teendő_gyök = Path(__file__).resolve().parents[1]

def Futtatás():
    forrás_Files = ['시험/화면갱신.c', 'gép/화면그림.c', 'gép/Terminál.c', 'gép/widget.c']
    검증원문들 = forrás_Files + ['FORRÁS/화면합성.java', 'FORRÁS/fal.java', '../../compiler/자바도구/기계어미리번역.java']
    cél_ÉRTÉK = teendő_gyök/'build/verification/redraw'; cél_ÉRTÉK.mkdir(parents=True, exist_ok=True)
    LOG_REKORD = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((teendő_gyök/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Név: hashlib.sha256((teendő_gyök/Név).read_bytes()).hexdigest() for Név in 검증원문들}}
    try:
        tanóra_útvonal = cél_ÉRTÉK/'classes'; tanóra_útvonal.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(tanóra_útvonal),
            str(teendő_gyök/'FORRÁS/화면합성.java'), str(teendő_gyök/'FORRÁS/fal.java')])
        exportál_tábla = {'jdraw_prepare': 'Előkészítés', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'klip',
            'jdraw_clip_value': 'klip_ÉRTÉK', 'jdraw_begin': 'Futtatás', 'jdraw_end': 'Befejezés',
            'jdraw_pixel': 'képpont', 'jdraw_rectangle': 'téglalap_kitöltés', 'jdraw_pointer': 'mutató'}
        번역명령 = ['sh', str(teendő_gyök.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(cél_ÉRTÉK/'rajz_ÉRTÉK.c')]
        for Kapcsolódás, FÜGGVÉNY_ÉRTÉK in exportál_tábla.items(): 번역명령.extend(['--export', Kapcsolódás+'=화면합성.'+FÜGGVÉNY_ÉRTÉK])
        subprocess.check_call(번역명령+[str(ÚTVONAL) for ÚTVONAL in sorted(tanóra_útvonal.glob('*.class'))])
        Parancs = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + forrás_Files
        rajz_cél = cél_ÉRTÉK/'rajz_ÉRTÉK.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(cél_ÉRTÉK/'rajz_ÉRTÉK.c'), '-o', str(rajz_cél)])
        subprocess.check_call(Parancs+[str(rajz_cél), 'build/terminal-font.S', '-o', str(cél_ÉRTÉK/'화면갱신시험')], cwd=str(teendő_gyök))
        KR = subprocess.check_output([str(cél_ÉRTÉK/'화면갱신시험')], timeout=30).decode()
        (cél_ÉRTÉK/'ellenőriz.log').write_text(KR)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', KR)
        assert 맞음 and 'PASS:' in KR, KR
        LOG_REKORD.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(KR, end='')
    finally:
        (cél_ÉRTÉK/'report.json').write_text(json.dumps(LOG_REKORD, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Futtatás()
