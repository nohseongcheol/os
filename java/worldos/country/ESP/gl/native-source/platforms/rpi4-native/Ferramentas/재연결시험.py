#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 real_datos 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from executar_comando import Project_raíz, Orde


def Executar_2():
    analizador_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizador_48ee4b1b.add_argument('--sdk', type=Path, default=Project_raíz.parent / 'rpi4/build/rootfs')
    Argumentos = analizador_48ee4b1b.parse_args()
    Saída = Project_raíz / 'build/verification/cosl-relink'
    Saída.mkdir(parents=True, exist_ok=True)
    informe_VALOR = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Project_raíz / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            CAMIÑO = Path(임시)
            with tarfile.open(str(Project_raíz / 'dist/jkoros-native-relink.tar.gz')) as Grupo_VALOR:
                for introdución_VALOR in Grupo_VALOR.getmembers():
                    if CAMIÑO not in (CAMIÑO / introdución_VALOR.name).resolve().parents or introdución_VALOR.issym() or introdución_VALOR.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + introdución_VALOR.name)
                Grupo_VALOR.extractall(str(CAMIÑO))
            FONTE = CAMIÑO / 'jkoros-native-relink'
            def 재연결(Nome, 인수들):
                with (Saída / Nome).open('wb') as LOG_fila:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(FONTE),
                                   stdout=LOG_fila, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            informe_VALOR['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = FONTE / 'vendor/tinycc/libtcc.c'
            corpo_do_texto = 번역기.read_text()
            Posición = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert corpo_do_texto.count(Posición) == 1
            번역기.write_text(corpo_do_texto.replace(Posición, Posición + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(Argumentos.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            IMAXE_VALOR = FONTE / 'build/relinked/kernel8.img'
            informe_VALOR['modified_kernel_sha256'] = hashlib.sha256(IMAXE_VALOR.read_bytes()).hexdigest()
            assert informe_VALOR['modified_kernel_sha256'] != informe_VALOR['kernel_sha256']
            informe_VALOR['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = Orde()
            인수들[인수들.index('-kernel') + 1] = str(IMAXE_VALOR)
            Proceso_VALOR = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            LOG_fila = bytearray()
            selección_VALOR = selectors.DefaultSelector()
            selección_VALOR.register(Proceso_VALOR.stdout, selectors.EVENT_READ)
            def agarda_Estado(mostrar_VALOR=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while mostrar_VALOR not in LOG_fila[처음:]:
                    if time.monotonic() > 끝 or Proceso_VALOR.poll() is not None:
                        raise AssertionError('Missing ' + repr(mostrar_VALOR) + '\n' + LOG_fila[처음:].decode('utf-8', 'replace'))
                    for introdución_VALOR, _ in selección_VALOR.select(.1):
                        datos = introdución_VALOR.fileobj.read(65536)
                        if datos:
                            LOG_fila.extend(datos)
                return bytes(LOG_fila[처음:])
            def enviar(Word_SMS, mostrar_VALOR=b'jkoros-native> '):
                처음 = len(LOG_fila)
                Proceso_VALOR.stdin.write(Word_SMS.encode() + b'\n')
                Proceso_VALOR.stdin.flush()
                return agarda_Estado(mostrar_VALOR, 처음)
            try:
                agarda_Estado()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return escribir_Ficheiro_datos(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                enviar('load /relink.c', b'hex> ')
                for cargo_ÍNDICE in range(0, len(시험), 64):
                    enviar(시험[cargo_ÍNDICE:cargo_ÍNDICE+64].hex(), b'hex> ')
                assert b'LOADED' in enviar('.')
                RESULTANTE = enviar('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in RESULTANTE, RESULTANTE
                RESULTANTE = enviar('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in RESULTANTE and b'exit 0' in RESULTANTE, RESULTANTE
                informe_VALOR['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                selección_VALOR.close()
                if Proceso_VALOR.poll() is None:
                    Proceso_VALOR.terminate()
                    try:
                        Proceso_VALOR.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        Proceso_VALOR.kill()
                        Proceso_VALOR.wait()
                (Saída / 'guest.log').write_bytes(LOG_fila)
        informe_VALOR['passed'] = True
        print(json.dumps(informe_VALOR, ensure_ascii=False, indent=2))
    finally:
        (Saída / 'report.json').write_text(json.dumps(informe_VALOR, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    Executar_2()
