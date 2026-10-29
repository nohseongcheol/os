#!/usr/bin/env python3
"""real_dades nucli_VALOR 그리기 코드를 allotjar Memòria_dades 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

Project_rel = Path(__file__).resolve().parents[1]

def Executa_2():
    font_Fitxers = ['시험/화면갱신.c', 'màquina/화면그림.c', 'màquina/Terminal.c', 'màquina/giny.c']
    검증원문들 = font_Fitxers + ['FONT/화면합성.java', 'FONT/Tauler.java', '../../compiler/자바도구/기계어미리번역.java']
    destinació_VALOR = Project_rel/'build/verification/redraw'; destinació_VALOR.mkdir(parents=True, exist_ok=True)
    LOG_fila = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((Project_rel/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Nom: hashlib.sha256((Project_rel/Nom).read_bytes()).hexdigest() for Nom in 검증원문들}}
    try:
        Classe_camí = destinació_VALOR/'classes'; Classe_camí.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Classe_camí),
            str(Project_rel/'FONT/화면합성.java'), str(Project_rel/'FONT/Tauler.java')])
        exportar_taula = {'jdraw_prepare': 'Prepara', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'clip',
            'jdraw_clip_value': 'clip_VALOR', 'jdraw_begin': 'Executa_2', 'jdraw_end': 'fi',
            'jdraw_pixel': 'píxel', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'punter'}
        번역명령 = ['sh', str(Project_rel.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(destinació_VALOR/'dibuix_VALOR.c')]
        for Connecta, FUNCIÓ_VALOR in exportar_taula.items(): 번역명령.extend(['--export', Connecta+'=화면합성.'+FUNCIÓ_VALOR])
        subprocess.check_call(번역명령+[str(Camí) for Camí in sorted(Classe_camí.glob('*.class'))])
        Ordre = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + font_Fitxers
        dibuix_destinació = destinació_VALOR/'dibuix_VALOR.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(destinació_VALOR/'dibuix_VALOR.c'), '-o', str(dibuix_destinació)])
        subprocess.check_call(Ordre+[str(dibuix_destinació), 'build/terminal-font.S', '-o', str(destinació_VALOR/'화면갱신시험')], cwd=str(Project_rel))
        RESULTAT = subprocess.check_output([str(destinació_VALOR/'화면갱신시험')], timeout=30).decode()
        (destinació_VALOR/'validar.log').write_text(RESULTAT)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', RESULTAT)
        assert 맞음 and 'PASS:' in RESULTAT, RESULTAT
        LOG_fila.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(RESULTAT, end='')
    finally:
        (destinació_VALOR/'report.json').write_text(json.dumps(LOG_fila, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Executa_2()
