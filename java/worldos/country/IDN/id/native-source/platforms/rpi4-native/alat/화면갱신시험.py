#!/usr/bin/env python3
"""aktual_data kernel_VALUE 그리기 코드를 host Memori_data 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

Tugas_akar = Path(__file__).resolve().parents[1]

def jalankan():
    sumber_File = ['pengujian/화면갱신.c', 'mesin/화면그림.c', 'mesin/terminal.c', 'mesin/unsur_layar.c']
    검증원문들 = sumber_File + ['kodeSumber/화면합성.java', 'kodeSumber/Papan.java', '../../compiler/자바도구/기계어미리번역.java']
    tujuan_VALUE = Tugas_akar/'build/verification/redraw'; tujuan_VALUE.mkdir(parents=True, exist_ok=True)
    LOG_baris = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((Tugas_akar/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Nama_2: hashlib.sha256((Tugas_akar/Nama_2).read_bytes()).hexdigest() for Nama_2 in 검증원문들}}
    try:
        Kelas_jalur = tujuan_VALUE/'classes'; Kelas_jalur.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Kelas_jalur),
            str(Tugas_akar/'kodeSumber/화면합성.java'), str(Tugas_akar/'kodeSumber/Papan.java')])
        Ekspor_tabel = {'jdraw_prepare': 'Siapkan', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'klip',
            'jdraw_clip_value': 'klip_VALUE', 'jdraw_begin': 'jalankan', 'jdraw_end': 'Selesai',
            'jdraw_pixel': 'elgam', 'jdraw_rectangle': 'persegi_isi', 'jdraw_pointer': 'pointer'}
        번역명령 = ['sh', str(Tugas_akar.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(tujuan_VALUE/'gambar_VALUE.c')]
        for Sambung, fungsi_VALUE in Ekspor_tabel.items(): 번역명령.extend(['--export', Sambung+'=화면합성.'+fungsi_VALUE])
        subprocess.check_call(번역명령+[str(jalur) for jalur in sorted(Kelas_jalur.glob('*.class'))])
        perintah = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + sumber_File
        gambar_tujuan = tujuan_VALUE/'gambar_VALUE.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(tujuan_VALUE/'gambar_VALUE.c'), '-o', str(gambar_tujuan)])
        subprocess.check_call(perintah+[str(gambar_tujuan), 'build/terminal-font.S', '-o', str(tujuan_VALUE/'화면갱신시험')], cwd=str(Tugas_akar))
        hasil = subprocess.check_output([str(tujuan_VALUE/'화면갱신시험')], timeout=30).decode()
        (tujuan_VALUE/'validasi.log').write_text(hasil)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', hasil)
        assert 맞음 and 'PASS:' in hasil, hasil
        LOG_baris.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(hasil, end='')
    finally:
        (tujuan_VALUE/'report.json').write_text(json.dumps(LOG_baris, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': jalankan()
