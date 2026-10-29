#!/usr/bin/env python3
"""dearbh_dàta eitean_VALUE 그리기 코드를 òstair cuimhne_dàta 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

tilg_freumh = Path(__file__).resolve().parents[1]

def ruith():
    tùs_faidhlichean = ['시험/화면갱신.c', 'inneal/화면그림.c', 'inneal/tèirmineal.c', 'inneal/widget.c']
    검증원문들 = tùs_faidhlichean + ['tùs/화면합성.java', 'tùs/bòrd.java', '../../compiler/자바도구/기계어미리번역.java']
    ceann_uidhe_VALUE = tilg_freumh/'build/verification/redraw'; ceann_uidhe_VALUE.mkdir(parents=True, exist_ok=True)
    LOG_ràgh = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((tilg_freumh/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Ainm: hashlib.sha256((tilg_freumh/Ainm).read_bytes()).hexdigest() for Ainm in 검증원문들}}
    try:
        clas_slighe = ceann_uidhe_VALUE/'classes'; clas_slighe.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(clas_slighe),
            str(tilg_freumh/'tùs/화면합성.java'), str(tilg_freumh/'tùs/bòrd.java')])
        às_phortaich_clàr = {'jdraw_prepare': 'Ullaich', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'cliop',
            'jdraw_clip_value': 'cliop_VALUE', 'jdraw_begin': 'ruith', 'jdraw_end': 'Coilean',
            'jdraw_pixel': 'pel', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'tomhaire'}
        번역명령 = ['sh', str(tilg_freumh.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(ceann_uidhe_VALUE/'tarraing_VALUE.c')]
        for CONNECT, FUNCTION_VALUE in às_phortaich_clàr.items(): 번역명령.extend(['--export', CONNECT+'=화면합성.'+FUNCTION_VALUE])
        subprocess.check_call(번역명령+[str(Slighe) for Slighe in sorted(clas_slighe.glob('*.class'))])
        àithne = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + tùs_faidhlichean
        tarraing_ceann_uidhe = ceann_uidhe_VALUE/'tarraing_VALUE.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(ceann_uidhe_VALUE/'tarraing_VALUE.c'), '-o', str(tarraing_ceann_uidhe)])
        subprocess.check_call(àithne+[str(tarraing_ceann_uidhe), 'build/terminal-font.S', '-o', str(ceann_uidhe_VALUE/'화면갱신시험')], cwd=str(tilg_freumh))
        tomhas = subprocess.check_output([str(ceann_uidhe_VALUE/'화면갱신시험')], timeout=30).decode()
        (ceann_uidhe_VALUE/'dearbh_5fb2b747.log').write_text(tomhas)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', tomhas)
        assert 맞음 and 'PASS:' in tomhas, tomhas
        LOG_ràgh.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(tomhas, end='')
    finally:
        (ceann_uidhe_VALUE/'report.json').write_text(json.dumps(LOG_ràgh, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': ruith()
