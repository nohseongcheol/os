from pathlib import Path
import tempfile
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import write_header


def crearRed(rutaRaíz, CompiladorC, herramientaArchivoComprimido, bitsConfiguración, ejecutarComando):
    datosOriginal = rutaRaíz / 'vendor/lwip/src'
    númeroPuerto = rutaRaíz / 'PilaRed'
    salida = rutaRaíz / 'build/network'
    salida.mkdir(exist_ok=True)
    write_header(rutaRaíz, salida / 'ip_config.h')
    listaArchivo = sorted((datosOriginal / 'core').glob('*.c')) + sorted((datosOriginal / 'core/ipv4').glob('*.c'))
    listaArchivo += [datosOriginal / 'netif/ethernet.c']
    listaArchivo += sorted(númeroPuerto.glob('*.c'))
    archivosDestino = []
    for ruta in listaArchivo:
        archivoDestino = salida / (ruta.stem + '.o')
        ejecutarComando([CompiladorC] + bitsConfiguración + ['-include', salida / 'ip_config.h', '-std=c11', '-I', númeroPuerto, '-I', datosOriginal / 'include',
             '-I', rutaRaíz.parents[1] / 'posix-kor/arm64-native/Encabezados', '-c', ruta, '-o', archivoDestino])
        archivosDestino.append(archivoDestino)
    biblioteca = salida / 'libnetwork.a'
    # ar rcs retains members removed or renamed in the source tree. Build a
    # fresh archive so old English/Korean object names cannot coexist.
    with tempfile.TemporaryDirectory(prefix='archive-', dir=str(salida)) as rutaTemporal:
        bibliotecaNuevo=Path(rutaTemporal)/'libnetwork.a'
        ejecutarComando([herramientaArchivoComprimido, 'rcs', bibliotecaNuevo] + archivosDestino)
        bibliotecaNuevo.replace(biblioteca)
    return biblioteca
