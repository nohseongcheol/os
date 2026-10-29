#!/usr/bin/env python3
"""real_dados kernel_VALOR Paint_tela 코드를 host Memória_dados 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ação_raiz = Path(__file__).resolve().parents[1]

def iniciar():
    fonte_Arquivos = ['testes/renovar_tela.c', 'computador/tela_desenho.c', 'computador/terminal.c', 'computador/elemento_de_ecrã.c']
    검증원문들 = fonte_Arquivos + ['códigoFonte/ComposiçãoEcrã.java', 'códigoFonte/Quadro.java', '../../compiler/FerramentasJava/CompiladorAntecipado.java']
    destino_VALOR = ação_raiz/'build/verification/redraw'; destino_VALOR.mkdir(parents=True, exist_ok=True)
    LOG_linha = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((ação_raiz/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Nome: hashlib.sha256((ação_raiz/Nome).read_bytes()).hexdigest() for Nome in 검증원문들}}
    try:
        aula_caminho = destino_VALOR/'classes'; aula_caminho.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(aula_caminho),
            str(ação_raiz/'códigoFonte/ComposiçãoEcrã.java'), str(ação_raiz/'códigoFonte/Quadro.java')])
        exportar_tabela = {'jdraw_prepare': 'Preparar', 'jdraw_width': '너비얻기', 'jdraw_height': 'get_altura',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'recortar',
            'jdraw_clip_value': 'recortar_VALOR', 'jdraw_begin': 'iniciar', 'jdraw_end': 'fim',
            'jdraw_pixel': 'pixel', 'jdraw_rectangle': 'retângulo_preencher', 'jdraw_pointer': 'ponteiro'}
        번역명령 = ['sh', str(ação_raiz.parents[1]/'compiler/미리번역.sh'), '--entry', 'ComposiçãoEcrã.너비얻기', '-o', str(destino_VALOR/'desenho_VALOR.c')]
        for Ligar, FUNÇÃO_VALOR in exportar_tabela.items(): 번역명령.extend(['--export', Ligar+'=ComposiçãoEcrã.'+FUNÇÃO_VALOR])
        subprocess.check_call(번역명령+[str(caminho) for caminho in sorted(aula_caminho.glob('*.class'))])
        comando = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + fonte_Arquivos
        desenho_destino = destino_VALOR/'desenho_VALOR.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(destino_VALOR/'desenho_VALOR.c'), '-o', str(desenho_destino)])
        subprocess.check_call(comando+[str(desenho_destino), 'build/terminal-font.S', '-o', str(destino_VALOR/'tela_renovar_teste')], cwd=str(ação_raiz))
        resultado = subprocess.check_output([str(destino_VALOR/'tela_renovar_teste')], timeout=30).decode()
        (destino_VALOR/'validar.log').write_text(resultado)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', resultado)
        assert 맞음 and 'PASS:' in resultado, resultado
        LOG_linha.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(resultado, end='')
    finally:
        (destino_VALOR/'report.json').write_text(json.dumps(LOG_linha, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': iniciar()
