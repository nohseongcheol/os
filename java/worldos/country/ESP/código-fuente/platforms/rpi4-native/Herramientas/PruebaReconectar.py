#!/usr/bin/env python3
"""valorDistribución 자료만으로 LGPL 재연결과 수정한 TinyCC의 datosEfectivo 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from ejecutarComando import raízProyecto, comando


def ponerEnMarcha():
    Analizador = argparse.ArgumentParser(description=__doc__)
    Analizador.add_argument('--sdk', type=Path, default=raízProyecto.parent / 'rpi4/build/rootfs')
    argumentos = Analizador.parse_args()
    Salida = raízProyecto / 'build/verification/cosl-relink'
    Salida.mkdir(parents=True, exist_ok=True)
    valorInforme = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((raízProyecto / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as valorTemporal:
            ruta = Path(valorTemporal)
            with tarfile.open(str(raízProyecto / 'dist/jkoros-native-relink.tar.gz')) as valorGrupo:
                for valorEntradaElemento in valorGrupo.getmembers():
                    if ruta not in (ruta / valorEntradaElemento.name).resolve().parents or valorEntradaElemento.issym() or valorEntradaElemento.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + valorEntradaElemento.name)
                valorGrupo.extractall(str(ruta))
            fuente = ruta / 'jkoros-native-relink'
            def extremoReconectar(nombre, listaArgumentos):
                with (Salida / nombre).open('wb') as registroEntradaDiario:
                    subprocess.run(['python3', 'relink.py'] + listaArgumentos, cwd=str(fuente),
                                   stdout=registroEntradaDiario, stderr=subprocess.STDOUT, check=True, timeout=180)
            extremoReconectar('original.log', ['--verify'])
            valorInforme['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            herramientaCompilador = fuente / 'vendor/tinycc/libtcc.c'
            textoCuerpo = herramientaCompilador.read_text()
            posición = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert textoCuerpo.count(posición) == 1
            herramientaCompilador.write_text(textoCuerpo.replace(posición, posición + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            extremoReconectar('modified-tinycc.log', ['--tinycc', '--sdk', str(argumentos.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            valorImagen = fuente / 'build/relinked/kernel8.img'
            valorInforme['modified_kernel_sha256'] = hashlib.sha256(valorImagen.read_bytes()).hexdigest()
            assert valorInforme['modified_kernel_sha256'] != valorInforme['kernel_sha256']
            valorInforme['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            listaArgumentos = comando()
            listaArgumentos[listaArgumentos.index('-kernel') + 1] = str(valorImagen)
            valorProceso = subprocess.Popen(listaArgumentos + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            registroEntradaDiario = bytearray()
            valorSelección = selectors.DefaultSelector()
            valorSelección.register(valorProceso.stdout, selectors.EVENT_READ)
            def esperarEstadoValor(mostrarValor=b'jkoros-native> ', elementoListaInicialValor=0):
                terminación = time.monotonic() + 40
                while mostrarValor not in registroEntradaDiario[elementoListaInicialValor:]:
                    if time.monotonic() > terminación or valorProceso.poll() is not None:
                        raise AssertionError('Missing ' + repr(mostrarValor) + '\n' + registroEntradaDiario[elementoListaInicialValor:].decode('utf-8', 'replace'))
                    for valorEntradaElemento, _ in valorSelección.select(.1):
                        Datos = valorEntradaElemento.fileobj.read(65536)
                        if Datos:
                            registroEntradaDiario.extend(Datos)
                return bytes(registroEntradaDiario[elementoListaInicialValor:])
            def enviar(textoPalabra, mostrarValor=b'jkoros-native> '):
                elementoListaInicialValor = len(registroEntradaDiario)
                valorProceso.stdin.write(textoPalabra.encode() + b'\n')
                valorProceso.stdin.flush()
                return esperarEstadoValor(mostrarValor, elementoListaInicialValor)
            try:
                esperarEstadoValor()
                Pruebas = '#include <ABIArchivo.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return escribirDatosArchivo(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                enviar('load /relink.c', b'hex> ')
                for índicePosición in range(0, len(Pruebas), 64):
                    enviar(Pruebas[índicePosición:índicePosición+64].hex(), b'hex> ')
                assert b'LOADED' in enviar('.')
                resultado = enviar('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in resultado, resultado
                resultado = enviar('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in resultado and b'exit 0' in resultado, resultado
                valorInforme['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                valorSelección.close()
                if valorProceso.poll() is None:
                    valorProceso.terminate()
                    try:
                        valorProceso.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        valorProceso.kill()
                        valorProceso.wait()
                (Salida / 'guest.log').write_bytes(registroEntradaDiario)
        valorInforme['passed'] = True
        print(json.dumps(valorInforme, ensure_ascii=False, indent=2))
    finally:
        (Salida / 'report.json').write_text(json.dumps(valorInforme, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    ponerEnMarcha()
