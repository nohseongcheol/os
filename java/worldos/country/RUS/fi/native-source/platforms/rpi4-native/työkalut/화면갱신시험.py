#!/usr/bin/env python3
"""todellinen_data ydin_ARVO 그리기 코드를 isäntä Muisti_data 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

aloite_juuri = Path(__file__).resolve().parents[1]

def Suorita_2():
    lähde_Files = ['testit/화면갱신.c', 'kone/화면그림.c', 'kone/komentotulkki.c', 'kone/näyttöelementti.c']
    검증원문들 = lähde_Files + ['lähdetiedosto/화면합성.java', 'lähdetiedosto/Taulu.java', '../../compiler/자바도구/기계어미리번역.java']
    kohde_ARVO = aloite_juuri/'build/verification/redraw'; kohde_ARVO.mkdir(parents=True, exist_ok=True)
    LOG_TIETUE = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((aloite_juuri/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Nimi: hashlib.sha256((aloite_juuri/Nimi).read_bytes()).hexdigest() for Nimi in 검증원문들}}
    try:
        Luokka_polku = kohde_ARVO/'classes'; Luokka_polku.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Luokka_polku),
            str(aloite_juuri/'lähdetiedosto/화면합성.java'), str(aloite_juuri/'lähdetiedosto/Taulu.java')])
        viedä_taulukko = {'jdraw_prepare': 'Valmistele', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'leikata',
            'jdraw_clip_value': 'leikata_ARVO', 'jdraw_begin': 'Suorita_2', 'jdraw_end': 'loppu',
            'jdraw_pixel': 'kuvapiste', 'jdraw_rectangle': 'suorakulmio_täyttö', 'jdraw_pointer': 'osoitin'}
        번역명령 = ['sh', str(aloite_juuri.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(kohde_ARVO/'piirustus_ARVO.c')]
        for Yhdistä, funktio_ARVO in viedä_taulukko.items(): 번역명령.extend(['--export', Yhdistä+'=화면합성.'+funktio_ARVO])
        subprocess.check_call(번역명령+[str(polku_2) for polku_2 in sorted(Luokka_polku.glob('*.class'))])
        komento = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + lähde_Files
        piirustus_kohde = kohde_ARVO/'piirustus_ARVO.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(kohde_ARVO/'piirustus_ARVO.c'), '-o', str(piirustus_kohde)])
        subprocess.check_call(komento+[str(piirustus_kohde), 'build/terminal-font.S', '-o', str(kohde_ARVO/'화면갱신시험')], cwd=str(aloite_juuri))
        TULOS = subprocess.check_output([str(kohde_ARVO/'화면갱신시험')], timeout=30).decode()
        (kohde_ARVO/'vahvista.log').write_text(TULOS)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', TULOS)
        assert 맞음 and 'PASS:' in TULOS, TULOS
        LOG_TIETUE.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(TULOS, end='')
    finally:
        (kohde_ARVO/'report.json').write_text(json.dumps(LOG_TIETUE, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Suorita_2()
