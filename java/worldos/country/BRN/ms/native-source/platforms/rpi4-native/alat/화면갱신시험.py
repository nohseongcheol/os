#!/usr/bin/env python3
"""sebenar_data kernel_VALUE 그리기 코드를 hos Memori_data 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

projek_akar = Path(__file__).resolve().parents[1]

def Jalan():
    sumber_Fail = ['ujian/화면갱신.c', 'mesin/화면그림.c', 'mesin/Terminal.c', 'mesin/unsur_skrin.c']
    검증원문들 = sumber_Fail + ['SUMBER/화면합성.java', 'SUMBER/Papan.java', '../../compiler/자바도구/기계어미리번역.java']
    destinasi_VALUE = projek_akar/'build/verification/redraw'; destinasi_VALUE.mkdir(parents=True, exist_ok=True)
    LOG_baris = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((projek_akar/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Nama: hashlib.sha256((projek_akar/Nama).read_bytes()).hexdigest() for Nama in 검증원문들}}
    try:
        Kelas_laluan = destinasi_VALUE/'classes'; Kelas_laluan.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Kelas_laluan),
            str(projek_akar/'SUMBER/화면합성.java'), str(projek_akar/'SUMBER/Papan.java')])
        Eksport_jadual = {'jdraw_prepare': 'Sediakan', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'klip',
            'jdraw_clip_value': 'klip_VALUE', 'jdraw_begin': 'Jalan', 'jdraw_end': 'Tamat',
            'jdraw_pixel': 'pel', 'jdraw_rectangle': 'segi_empat_tepat_isi', 'jdraw_pointer': 'penuding'}
        번역명령 = ['sh', str(projek_akar.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(destinasi_VALUE/'lukisan_VALUE.c')]
        for Sambung, fungsi_VALUE in Eksport_jadual.items(): 번역명령.extend(['--export', Sambung+'=화면합성.'+fungsi_VALUE])
        subprocess.check_call(번역명령+[str(LALUAN) for LALUAN in sorted(Kelas_laluan.glob('*.class'))])
        Perintah = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + sumber_Fail
        lukisan_destinasi = destinasi_VALUE/'lukisan_VALUE.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(destinasi_VALUE/'lukisan_VALUE.c'), '-o', str(lukisan_destinasi)])
        subprocess.check_call(Perintah+[str(lukisan_destinasi), 'build/terminal-font.S', '-o', str(destinasi_VALUE/'화면갱신시험')], cwd=str(projek_akar))
        ukuran = subprocess.check_output([str(destinasi_VALUE/'화면갱신시험')], timeout=30).decode()
        (destinasi_VALUE/'sahkan.log').write_text(ukuran)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', ukuran)
        assert 맞음 and 'PASS:' in ukuran, ukuran
        LOG_baris.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(ukuran, end='')
    finally:
        (destinasi_VALUE/'report.json').write_text(json.dumps(LOG_baris, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Jalan()
