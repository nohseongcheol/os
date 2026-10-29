#!/usr/bin/env python3
"""real_datos kernel_VALOR 그리기 코드를 hospedar Memoria_datos 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

Project_raíz = Path(__file__).resolve().parents[1]

def Executar_2():
    fonte_Ficheiros = ['시험/화면갱신.c', 'máquina/화면그림.c', 'máquina/Terminal.c', 'máquina/widget.c']
    검증원문들 = fonte_Ficheiros + ['FONTE/화면합성.java', 'FONTE/Panel.java', '../../compiler/자바도구/기계어미리번역.java']
    destino_VALOR = Project_raíz/'build/verification/redraw'; destino_VALOR.mkdir(parents=True, exist_ok=True)
    LOG_fila = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((Project_raíz/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Nome: hashlib.sha256((Project_raíz/Nome).read_bytes()).hexdigest() for Nome in 검증원문들}}
    try:
        Clase_camiño = destino_VALOR/'classes'; Clase_camiño.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Clase_camiño),
            str(Project_raíz/'FONTE/화면합성.java'), str(Project_raíz/'FONTE/Panel.java')])
        exportar_táboa = {'jdraw_prepare': '준비', 'jdraw_width': '너비얻기', 'jdraw_height': '높이얻기',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'clip',
            'jdraw_clip_value': 'clip_VALOR', 'jdraw_begin': 'Executar_2', 'jdraw_end': 'fin',
            'jdraw_pixel': 'píxel', 'jdraw_rectangle': '사각그림', 'jdraw_pointer': 'punteiro'}
        번역명령 = ['sh', str(Project_raíz.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(destino_VALOR/'그림.c')]
        for Conectar, FUNCIÓN_VALOR in exportar_táboa.items(): 번역명령.extend(['--export', Conectar+'=화면합성.'+FUNCIÓN_VALOR])
        subprocess.check_call(번역명령+[str(CAMIÑO) for CAMIÑO in sorted(Clase_camiño.glob('*.class'))])
        Orde = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + fonte_Ficheiros
        그림목적 = destino_VALOR/'그림.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(destino_VALOR/'그림.c'), '-o', str(그림목적)])
        subprocess.check_call(Orde+[str(그림목적), 'build/terminal-font.S', '-o', str(destino_VALOR/'화면갱신시험')], cwd=str(Project_raíz))
        RESULTANTE = subprocess.check_output([str(destino_VALOR/'화면갱신시험')], timeout=30).decode()
        (destino_VALOR/'validar.log').write_text(RESULTANTE)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', RESULTANTE)
        assert 맞음 and 'PASS:' in RESULTANTE, RESULTANTE
        LOG_fila.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(RESULTANTE, end='')
    finally:
        (destino_VALOR/'report.json').write_text(json.dumps(LOG_fila, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': Executar_2()
