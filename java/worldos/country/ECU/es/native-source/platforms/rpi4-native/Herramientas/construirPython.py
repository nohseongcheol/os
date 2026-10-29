"""고정한 공식 MicroPython 소스로 propio SVC용 EL0 실행기를 빌드한다."""
import hashlib
import os
from pathlib import Path
import subprocess
import tarfile

valorEdición = '1.24.1'
resumenHashValidación = 'a291173de1d680786a66dd2381805b6d134defaecea670a560dc7e7d8de540ad'


def crearPython(rutaRaíz, CompiladorC, herramientaEnlazador):
    nombre = 'micropython-' + valorEdición
    archivoComprimido = rutaRaíz / 'vendor' / (nombre + '.tar.gz')
    if not archivoComprimido.is_file() or hashlib.sha256(archivoComprimido.read_bytes()).hexdigest() != resumenHashValidación:
        raise SystemExit('MicroPython árbolFuente métodoAusente/archivoResumenHash 불일치: ' + str(archivoComprimido))
    datosOriginal = rutaRaíz / 'build' / nombre
    if not (datosOriginal / '.jkoros-source-sha256').is_file():
        with tarfile.open(str(archivoComprimido)) as paqueteTAR:
            for miembro in paqueteTAR.getmembers():
                ruta = Path(miembro.name)
                if ruta.is_absolute() or '..' in ruta.parts or ruta.parts[0] != nombre:
                    raise SystemExit('안전하지 않은 árbolFuente ruta')
                if miembro.isfile() or miembro.isdir():
                    paqueteTAR.extract(miembro, str(rutaRaíz / 'build'))
        (datosOriginal / '.jkoros-source-sha256').write_text(resumenHashValidación + '\n')
    newlib = os.environ.get('NEWLIB_INCLUDE', '/usr/include/newlib')
    if not (Path(newlib) / 'stdio.h').is_file():
        raise SystemExit('libnewlib-dev 헤더 또는 NEWLIB_INCLUDE valorNecesario')
    subprocess.check_call(['make', '-j2', 'CC=' + CompiladorC, 'LD=' + herramientaEnlazador, 'NEWLIB_INCLUDE=' + newlib], cwd=str(rutaRaíz / 'puentePython'))
