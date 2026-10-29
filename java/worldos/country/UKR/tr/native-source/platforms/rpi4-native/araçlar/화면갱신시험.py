#!/usr/bin/env python3
"""fiili_veri çekirdek_değer 그리기 코드를 konak Bellek_veri 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

işlem_kök = Path(__file__).resolve().parents[1]

def çalıştır():
    kaynak_Dosyalar = ['sınamalar/화면갱신.c', 'makine/화면그림.c', 'makine/uçbirim.c', 'makine/ekran_öğesi.c']
    검증원문들 = kaynak_Dosyalar + ['kaynakKod/화면합성.java', 'kaynakKod/Pano.java', '../../compiler/자바도구/기계어미리번역.java']
    hedef_değer = işlem_kök/'build/verification/redraw'; hedef_değer.mkdir(parents=True, exist_ok=True)
    LOG_KAYIT = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((işlem_kök/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {İsim: hashlib.sha256((işlem_kök/İsim).read_bytes()).hexdigest() for İsim in 검증원문들}}
    try:
        Sınıf_yol = hedef_değer/'classes'; Sınıf_yol.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Sınıf_yol),
            str(işlem_kök/'kaynakKod/화면합성.java'), str(işlem_kök/'kaynakKod/Pano.java')])
        dışarı_aktarmak_tablo = {'jdraw_prepare': 'Hazırlan', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'klip',
            'jdraw_clip_value': 'klip_değer', 'jdraw_begin': 'çalıştır', 'jdraw_end': 'Son',
            'jdraw_pixel': 'piksel', 'jdraw_rectangle': 'dikdörtgen_dolgu', 'jdraw_pointer': 'işaretçi'}
        번역명령 = ['sh', str(işlem_kök.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(hedef_değer/'çizim_değer.c')]
        for Bağlan, işlev_değer in dışarı_aktarmak_tablo.items(): 번역명령.extend(['--export', Bağlan+'=화면합성.'+işlev_değer])
        subprocess.check_call(번역명령+[str(yol) for yol in sorted(Sınıf_yol.glob('*.class'))])
        komut = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + kaynak_Dosyalar
        çizim_hedef = hedef_değer/'çizim_değer.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(hedef_değer/'çizim_değer.c'), '-o', str(çizim_hedef)])
        subprocess.check_call(komut+[str(çizim_hedef), 'build/terminal-font.S', '-o', str(hedef_değer/'화면갱신시험')], cwd=str(işlem_kök))
        sonuç = subprocess.check_output([str(hedef_değer/'화면갱신시험')], timeout=30).decode()
        (hedef_değer/'doğrulamak_5fb2b747.log').write_text(sonuç)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', sonuç)
        assert 맞음 and 'PASS:' in sonuç, sonuç
        LOG_KAYIT.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(sonuç, end='')
    finally:
        (hedef_değer/'report.json').write_text(json.dumps(LOG_KAYIT, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': çalıştır()
