#!/usr/bin/env python3
"""개인 conexión 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from ajustesRemoto import preparar
from DistribuciónCOSL import nombreDestino, biblioteca

raízProyecto = Path(__file__).resolve().parents[1]


def ponerEnMarcha():
    Salida = raízProyecto / 'build/verification/password-length'
    Salida.mkdir(parents=True, exist_ok=True)
    ajustesPersonal = raízProyecto / 'build/remote/access.json'
    ajustesOriginal = ajustesPersonal.read_bytes()
    valorInforme = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as valorTemporal:
            pruebaEspacioTrabajo = Path(valorTemporal)
            rutaAjustes = pruebaEspacioTrabajo / 'build/remote'
            rutaAjustes.mkdir(parents=True)
            archivoAjustes = rutaAjustes / 'access.json'
            def escribirAjustes(Datos):
                archivoAjustes.write_text(json.dumps(Datos, ensure_ascii=False) + '\n')
                archivoAjustes.chmod(0o600)
            def verificarAjustes(intérpreteComandos, Pantalla):
                escribirAjustes({'user': 'user', 'ssh_password': intérpreteComandos, 'vnc_password': Pantalla})
                original = archivoAjustes.read_bytes()
                preparar(pruebaEspacioTrabajo)
                assert archivoAjustes.read_bytes() == original, 'Settings were rewritten'
                valorCabecera = (rutaAjustes / 'perfil.h').read_text()
                esIgual = re.search(r'contraseñaPantalla\[\] = \{([^}]+)\}', valorCabecera)
                assert esIgual and len(esIgual.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (rutaAjustes / 'perfil.h').stat().st_mode & 0o777 == 0o600
            for intérpreteComandos, Pantalla in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                verificarAjustes(intérpreteComandos, Pantalla)
            valorInforme['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for cambiarValor, valorEntradaElemento in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                Datos = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                Datos.update(cambiarValor)
                escribirAjustes(Datos)
                try:
                    preparar(pruebaEspacioTrabajo)
                except SystemExit as error:
                    assert valorEntradaElemento in str(error), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + valorEntradaElemento)
            valorInforme['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            ajustes = json.loads((raízProyecto / 'build/remote/libassh-build.json').read_text())['flags']
            herramientaCompilador = os.environ.get('ARM64_CC', 'clang')
            conector = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            herramientaArchivoComprimido = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def ejecutarComando(argumentos, registroEntradaDiario):
                subprocess.run(list(map(str, argumentos)), cwd=str(raízProyecto), stdout=registroEntradaDiario,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for nombre, intérpreteComandos, Pantalla in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + nombre, flush=True)
                verificarAjustes(intérpreteComandos, Pantalla)
                resultado = Salida / nombre
                resultado.mkdir(exist_ok=True)
                with (resultado / 'build.log').open('wb') as registroEntradaDiario:
                    destinos = []
                    for original in sorted((raízProyecto / 'valorRemoto').glob('*.c')):
                        valorDestino = pruebaEspacioTrabajo / (original.stem + '.o')
                        ejecutarComando([herramientaCompilador] + ajustes + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', rutaAjustes, '-I', raízProyecto / 'valorRemoto', '-I', raízProyecto / 'vendor/libassh/src',
                             '-I', raízProyecto / 'vendor/bearssl/inc', '-I', raízProyecto / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', original, '-o', valorDestino], registroEntradaDiario)
                        destinos.append(valorDestino)
                    paqueteRemoto = pruebaEspacioTrabajo / 'libremote.a'
                    ejecutarComando([herramientaArchivoComprimido, 'rcs', paqueteRemoto] + destinos, registroEntradaDiario)
                    ejecutarComando([conector, '--gc-sections', '-T', raízProyecto / 'Arranque/DisposiciónEnlace.ld', '-o', pruebaEspacioTrabajo / 'kernel.elf'] +
                         [raízProyecto / 'build' / (nombre + '.o') for nombre in nombreDestino] + ['--start-group'] +
                         [paqueteRemoto if ruta == 'remote/libremote.a' else raízProyecto / 'build' / ruta for ruta in biblioteca] + ['--end-group'], registroEntradaDiario)
                    ejecutarComando([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         pruebaEspacioTrabajo / 'kernel.elf', pruebaEspacioTrabajo / 'kernel8.img'], registroEntradaDiario)
                with (resultado / 'remote-test.log').open('wb') as registroEntradaDiario:
                    ejecutarComando(['python3', raízProyecto / 'Herramientas/PruebaConexiónRemoto.py', '--kernel', pruebaEspacioTrabajo / 'kernel8.img',
                         '--access', archivoAjustes, '--output', resultado], registroEntradaDiario)
                validar = json.loads((resultado / 'report.json').read_text())
                assert validar['passed']
                valorInforme['checks'].append(nombre + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        valorInforme['passed'] = True
    finally:
        valorInforme['personal_settings_unchanged'] = ajustesPersonal.read_bytes() == ajustesOriginal
        if not valorInforme['personal_settings_unchanged']:
            valorInforme['passed'] = False
        valorInforme['kernel_sha256'] = hashlib.sha256((raízProyecto / 'build/kernel8.img').read_bytes()).hexdigest()
        (Salida / 'report.json').write_text(json.dumps(valorInforme, ensure_ascii=False, indent=2) + '\n')
    assert valorInforme['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(valorInforme, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ponerEnMarcha()
