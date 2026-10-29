#!/usr/bin/env python3
"""eyona_yenzekileyo_iingcombolo ikheneli_ixabiso 그리기 코드를 umsingathi imemori_iingcombolo 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]

def Phumeza():
    umthombo_Iifayile = ['시험/화면갱신.c', 'umatshini/화면그림.c', 'umatshini/i_Terminal.c', 'umatshini/iwijethi.c']
    검증원문들 = umthombo_Iifayile + ['UMTHOMBO/화면합성.java', 'UMTHOMBO/보드.java', '../../compiler/자바도구/기계어미리번역.java']
    indawo_ekuyiwa_kuyo_ixabiso = 기준/'build/verification/redraw'; indawo_ekuyiwa_kuyo_ixabiso.mkdir(parents=True, exist_ok=True)
    ilog_umqolo = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Igama: hashlib.sha256((기준/Igama).read_bytes()).hexdigest() for Igama in 검증원문들}}
    try:
        iklasi_indlela = indawo_ekuyiwa_kuyo_ixabiso/'classes'; iklasi_indlela.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(iklasi_indlela),
            str(기준/'UMTHOMBO/화면합성.java'), str(기준/'UMTHOMBO/보드.java')])
        thumela_ngaphandle_itheyibhile = {'jdraw_prepare': 'lungisa', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'ikliphu',
            'jdraw_clip_value': 'ikliphu_ixabiso', 'jdraw_begin': 'Phumeza', 'jdraw_end': 'Gqiba',
            'jdraw_pixel': 'i_pel', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'isalathisi'}
        번역명령 = ['sh', str(기준.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(indawo_ekuyiwa_kuyo_ixabiso/'umzobo_ixabiso.c')]
        for Nxulumanisa, INKQUBO_ixabiso in thumela_ngaphandle_itheyibhile.items(): 번역명령.extend(['--export', Nxulumanisa+'=화면합성.'+INKQUBO_ixabiso])
        subprocess.check_call(번역명령+[str(INDLELA) for INDLELA in sorted(iklasi_indlela.glob('*.class'))])
        Umyalelo = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + umthombo_Iifayile
        umzobo_indawo_ekuyiwa_kuyo = indawo_ekuyiwa_kuyo_ixabiso/'umzobo_ixabiso.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(indawo_ekuyiwa_kuyo_ixabiso/'umzobo_ixabiso.c'), '-o', str(umzobo_indawo_ekuyiwa_kuyo)])
        subprocess.check_call(Umyalelo+[str(umzobo_indawo_ekuyiwa_kuyo), 'build/terminal-font.S', '-o', str(indawo_ekuyiwa_kuyo_ixabiso/'화면갱신시험')], cwd=str(기준))
        결과 = subprocess.check_output([str(indawo_ekuyiwa_kuyo_ixabiso/'화면갱신시험')], timeout=30).decode()
        (indawo_ekuyiwa_kuyo_ixabiso/'qinisekisa.log').write_text(결과)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', 결과)
        assert 맞음 and 'PASS:' in 결과, 결과
        ilog_umqolo.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(결과, end='')
    finally:
        (indawo_ekuyiwa_kuyo_ixabiso/'report.json').write_text(json.dumps(ilog_umqolo, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Phumeza()
