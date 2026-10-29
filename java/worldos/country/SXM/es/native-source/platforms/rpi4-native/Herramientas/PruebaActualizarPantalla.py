#!/usr/bin/env python3
"""datosEfectivo valorNúcleo pantallaPintar 코드를 Anfitrión datosMemoria 화면에 연결해 valorSubparte 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

raízProyecto = Path(__file__).resolve().parents[1]

def ponerEnMarcha():
    archivosFuente = ['Pruebas/actualizarPantalla.c', 'máquina/dibujoPantalla.c', 'máquina/terminal.c', 'máquina/ComponenteVisual.c']
    fuentesValidación = archivosFuente + ['fuente/ComponedorBúferImagen.java', 'fuente/Placa.java', '../../compiler/HerramientaJava/CompilaciónAnticipada.java']
    valorDestino = raízProyecto/'build/verification/redraw'; valorDestino.mkdir(parents=True, exist_ok=True)
    registroEntradaDiario = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((raízProyecto/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {nombre: hashlib.sha256((raízProyecto/nombre).read_bytes()).hexdigest() for nombre in fuentesValidación}}
    try:
        rutaClase = valorDestino/'classes'; rutaClase.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(rutaClase),
            str(raízProyecto/'fuente/ComponedorBúferImagen.java'), str(raízProyecto/'fuente/Placa.java')])
        tablaExportar = {'jdraw_prepare': 'preparar', 'jdraw_width': 'obtenerAnchura', 'jdraw_height': 'obtenerAltura',
            'jdraw_count_low': 'obtenerBajoContador', 'jdraw_count_high': 'obtenerAltoContador', 'jdraw_clip': 'recortar',
            'jdraw_clip_value': 'valorRecortar', 'jdraw_begin': 'ponerEnMarcha', 'jdraw_end': 'terminar',
            'jdraw_pixel': 'píxel', 'jdraw_rectangle': 'rellenarRectángulo', 'jdraw_pointer': 'puntero'}
        comandoCompilación = ['sh', str(raízProyecto.parents[1]/'compiler/tiempoDeAnticipado.sh'), '--entry', 'ComponedorBúferImagen.obtenerAnchura', '-o', str(valorDestino/'Dibujo.c')]
        for conectar, Función in tablaExportar.items(): comandoCompilación.extend(['--export', conectar+'=ComponedorBúferImagen.'+Función])
        subprocess.check_call(comandoCompilación+[str(ruta) for ruta in sorted(rutaClase.glob('*.class'))])
        comando = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + archivosFuente
        destinoDibujo = valorDestino/'Dibujo.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(valorDestino/'Dibujo.c'), '-o', str(destinoDibujo)])
        subprocess.check_call(comando+[str(destinoDibujo), 'build/terminal-font.S', '-o', str(valorDestino/'PruebaActualizarPantalla')], cwd=str(raízProyecto))
        resultado = subprocess.check_output([str(valorDestino/'PruebaActualizarPantalla')], timeout=30).decode()
        (valorDestino/'validar.log').write_text(resultado)
        esCoincidente = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', resultado)
        assert esCoincidente and 'PASS:' in resultado, resultado
        registroEntradaDiario.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(esCoincidente[1]), mean_framebuffer_writes_per_move=int(esCoincidente[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(resultado, end='')
    finally:
        (valorDestino/'report.json').write_text(json.dumps(registroEntradaDiario, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': ponerEnMarcha()
