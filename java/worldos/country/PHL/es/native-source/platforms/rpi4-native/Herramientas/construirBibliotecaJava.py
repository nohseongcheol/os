"""propio JVM용 español class/JAR와 EL0에 넣을 leer 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def crearBibliotecaJava(rutaRaíz, ejecutarComando):
    (rutaRaíz / 'build/user').mkdir(parents=True, exist_ok=True)
    salida = rutaRaíz / 'build/java-library'
    rutaClase = salida / 'classes'
    rutaClase.mkdir(parents=True, exist_ok=True)
    ListaFuentes = sorted((rutaRaíz / 'JavaEspañol').rglob('*.java'))
    ejecutarComando(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', rutaClase] + ListaFuentes)
    listaEntradas = []
    for direcciónOriginal in ListaFuentes:
        rutaRelativo = direcciónOriginal.relative_to(rutaRaíz / 'JavaEspañol').with_suffix('.class')
        datosCargaÚtil = (rutaClase / rutaRelativo).read_bytes()
        nombre = str(rutaRelativo).replace('/', '.')
        if len(datosCargaÚtil) > 16384 or len(nombre.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + nombre)
        listaEntradas.append((rutaRelativo, nombre, datosCargaÚtil))
    valorEncabezado = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *nombre; const unsigned char *Datos; unsigned tamaño; } RecursoClaseJava;']
    for índiceOrdinal, (_, nombre, datosCargaÚtil) in enumerate(listaEntradas):
        valorEncabezado.append('static const unsigned char datosClaseJava%d[] = {%s};' % (índiceOrdinal, ','.join(str(valorSegundo) for valorSegundo in datosCargaÚtil)))
    valorEncabezado.append('static const RecursoClaseJava listaClaseJava[] = {')
    for índiceOrdinal, (_, nombre, datosCargaÚtil) in enumerate(listaEntradas):
        valorEncabezado.append('{%s, datosClaseJava%d, %d},' % (json.dumps(nombre, ensure_ascii=False), índiceOrdinal, len(datosCargaÚtil)))
    valorEncabezado.append('};')
    (rutaRaíz / 'build/user/java-resources.h').write_text('\n'.join(valorEncabezado) + '\n', encoding='utf-8')
    rutaDistribución = rutaRaíz / 'dist'; rutaDistribución.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(rutaDistribución / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as paqueteJava:
        for rutaRelativo, _, datosCargaÚtil in listaEntradas:
            informaciónSistema = zipfile.ZipInfo(str(rutaRelativo), date_time=(1980, 1, 1, 0, 0, 0)); informaciónSistema.compress_type = zipfile.ZIP_DEFLATED
            paqueteJava.writestr(informaciónSistema, datosCargaÚtil)
    with zipfile.ZipFile(str(rutaDistribución / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as archivoComprimido:
        for direcciónOriginal in ListaFuentes:
            informaciónSistema = zipfile.ZipInfo(str(direcciónOriginal.relative_to(rutaRaíz / 'JavaEspañol')), date_time=(1980, 1, 1, 0, 0, 0)); informaciónSistema.compress_type = zipfile.ZIP_DEFLATED
            archivoComprimido.writestr(informaciónSistema, direcciónOriginal.read_bytes())
