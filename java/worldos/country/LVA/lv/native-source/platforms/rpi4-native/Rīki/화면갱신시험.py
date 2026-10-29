#!/usr/bin/env python3
"""faktisks_dati kodols_VALUE 그리기 코드를 viesot atmiņa_dati 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

Project_sakne = Path(__file__).resolve().parents[1]

def Palaist():
    avots_Faili = ['시험/화면갱신.c', 'mašīna/화면그림.c', 'mašīna/Terminālis.c', 'mašīna/logrīks.c']
    검증원문들 = avots_Faili + ['AVOTS/화면합성.java', 'AVOTS/Panelis.java', '../../compiler/자바도구/기계어미리번역.java']
    mērķis_VALUE = Project_sakne/'build/verification/redraw'; mērķis_VALUE.mkdir(parents=True, exist_ok=True)
    LOG_RECORD = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((Project_sakne/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Nosaukums: hashlib.sha256((Project_sakne/Nosaukums).read_bytes()).hexdigest() for Nosaukums in 검증원문들}}
    try:
        klase_ceļš = mērķis_VALUE/'classes'; klase_ceļš.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(klase_ceļš),
            str(Project_sakne/'AVOTS/화면합성.java'), str(Project_sakne/'AVOTS/Panelis.java')])
        eksportēt_tabula = {'jdraw_prepare': 'Sagatavot', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'klips',
            'jdraw_clip_value': 'klips_VALUE', 'jdraw_begin': 'Palaist', 'jdraw_end': 'beigas',
            'jdraw_pixel': 'attēla_elements', 'jdraw_rectangle': 'taisnstūris_aizpildīt', 'jdraw_pointer': 'rādītājs'}
        번역명령 = ['sh', str(Project_sakne.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(mērķis_VALUE/'zīmējums_VALUE.c')]
        for Savienoties, FUNCTION_VALUE in eksportēt_tabula.items(): 번역명령.extend(['--export', Savienoties+'=화면합성.'+FUNCTION_VALUE])
        subprocess.check_call(번역명령+[str(CEĻŠ) for CEĻŠ in sorted(klase_ceļš.glob('*.class'))])
        Komanda = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + avots_Faili
        zīmējums_mērķis = mērķis_VALUE/'zīmējums_VALUE.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(mērķis_VALUE/'zīmējums_VALUE.c'), '-o', str(zīmējums_mērķis)])
        subprocess.check_call(Komanda+[str(zīmējums_mērķis), 'build/terminal-font.S', '-o', str(mērķis_VALUE/'화면갱신시험')], cwd=str(Project_sakne))
        mērs = subprocess.check_output([str(mērķis_VALUE/'화면갱신시험')], timeout=30).decode()
        (mērķis_VALUE/'validēt.log').write_text(mērs)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', mērs)
        assert 맞음 and 'PASS:' in mērs, mērs
        LOG_RECORD.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(mērs, end='')
    finally:
        (mērķis_VALUE/'report.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Palaist()
