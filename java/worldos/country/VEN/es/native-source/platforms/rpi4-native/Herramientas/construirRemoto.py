"""LGPL libassh와 MIT BearSSL을 각각 보존하여 extremoReconectar 가능한 valorEstático 묶음을 만든다."""
from pathlib import Path
import json
import tempfile
from ajustesRemoto import preparar


def crearRemoto(raízProyecto, herramientaCompilador, herramientaArchivoComprimido, ajustes, ejecutarComando):
    Salida = raízProyecto / 'build/remote'
    Salida.mkdir(exist_ok=True)
    preparar(raízProyecto)
    intérpreteComandosAsegurar = raízProyecto / 'vendor/libassh/src'
    valorContraseña = raízProyecto / 'vendor/bearssl'
    Núcleo = ('deps context session packet event transport kex sign hash algo key service map bignum '
            'connection debug buffer alloc prng userauth_server userauth_server_password').split()
    listaOriginales = [intérpreteComandosAsegurar / ('assh_' + nombre + '.c') for nombre in Núcleo]
    for valorPatrón in ('bignum_builtin*.c', 'kex_builtin*.c', 'key_builtin*.c', 'sign_builtin*.c', 'hash_builtin*.c'):
        listaOriginales += sorted(intérpreteComandosAsegurar.glob(valorPatrón))
    listaOriginales += [intérpreteComandosAsegurar / (nombre + '.c') for nombre in (
        'ecc_weierstrass', 'cipher_builtin_aes', 'cipher_builtin_arc4', 'cipher_builtin_chachapoly',
        'mac_builtin', 'compress_none', 'cipher_none', 'mac_none', 'sign_none', 'key_none')]
    argumentos = ajustes + ['-ffunction-sections', '-fdata-sections', '-std=c11', '-DNDEBUG',
                    '-I', raízProyecto / 'valorRemoto', '-I', Salida, '-I', intérpreteComandosAsegurar,
                    '-I', valorContraseña / 'inc', '-I', valorContraseña / 'src', '-isystem', '/usr/include/newlib']
    def EmpaquetarEjecutables(nombre, listaRuta, valorPrefijo):
        destinos = []
        for ruta in listaRuta:
            valorDestino = Salida / (valorPrefijo + ruta.stem + '.o')
            ejecutarComando([herramientaCompilador] + argumentos + ['-c', ruta, '-o', valorDestino])
            destinos.append(valorDestino)
        with tempfile.TemporaryDirectory(dir=str(Salida)) as valorTemporal:
            valorGrupo = Path(valorTemporal) / nombre
            ejecutarComando([herramientaArchivoComprimido, 'rcs', valorGrupo] + destinos)
            valorGrupo.replace(Salida / nombre)
        return Salida / nombre
    EmpaquetarEjecutables('libassh.a', listaOriginales, 'assh-')
    (Salida / 'libassh-build.json').write_text(json.dumps({
        'sources': [str(ruta.relative_to(raízProyecto)) for ruta in listaOriginales],
        'flags': list(map(str, ajustes)), 'license': 'LGPL-2.1-or-later',
    }, ensure_ascii=False, indent=2) + '\n')
    fuenteMáquinaDirectaDesnudo = [valorContraseña / 'src' / (nombre + '.c') for nombre in (
        'codec/dec32be', 'codec/enc32be', 'codec/enc64be', 'hash/sha2small',
        'symcipher/des_support', 'symcipher/des_ct', 'symcipher/des_ct_cbcenc')]
    EmpaquetarEjecutables('libbearssl.a', fuenteMáquinaDirectaDesnudo, 'bear-')
    return EmpaquetarEjecutables('libremote.a', sorted((raízProyecto / 'valorRemoto').glob('*.c')), '')
