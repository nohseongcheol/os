#!/usr/bin/env python3
"""OpenJDK와 propio ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from ejecutarComando import raízProyecto


def ponerEnMarcha():
    salida = raízProyecto / 'build/verification/jvm'
    rutaClase = salida / 'classes'; rutaClase.mkdir(parents=True, exist_ok=True)
    paqueteJava = raízProyecto / 'dist/jkoros-native-korean.jar'
    ListaFuentes = sorted((raízProyecto / 'Pruebas/Java').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(paqueteJava), '-d', str(rutaClase)] + [str(datosCadena) for datosCadena in ListaFuentes])
    pruebaLista = [('pruebaObjetos', ['valorFondo', 'valorRama', 'puedeCalcular']), ('pruebaExcepciones', []), ('PruebaColección', []),
             ('pruebaHilosEjecución', ['valorContador', 'AcciónTarea', 'valorHiloEjecución']), ('pruebaHangul', []), ('pruebaConexiónRed', []), ('pruebaConexiónRedCoreano', []), ('pruebaExcepcionesCoreano', []), ('fuenteHangul', []), ('pruebaFronteras', []), ('validar.pruebaPaquete', []), ('PruebaCompatibilidadEntradaElemento', [])]
    informeValidación = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((raízProyecto / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(paqueteJava.read_bytes()).hexdigest(), 'tests': []}
    try:
        for nombre, inclusiones in pruebaLista:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as rutaTemporal:
                esperado = subprocess.check_output(['java', '-Xverify:all', '-cp', str(rutaClase) + ':' + str(paqueteJava), nombre], cwd=rutaTemporal, timeout=15).decode('utf-8')
            argumentosComando = ['python3', str(raízProyecto / 'Herramientas/ejecutarArchivo.py'), str(rutaClase / (nombre.replace('.', '/') + '.class'))]
            if '.' in nombre: argumentosComando += ['--class-name', nombre]
            for incluir in inclusiones: argumentosComando += ['--include', str(rutaClase / (incluir + '.class'))]
            if nombre == 'fuenteHangul': argumentosComando[2] = str(raízProyecto / 'Pruebas/Java/fuenteHangul.java')
            importeCompletado = subprocess.run(argumentosComando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            resultadoEfectivo = importeCompletado.stdout.decode('utf-8').replace('\r\n', '\n')
            (salida / (nombre + '.log')).write_text(resultadoEfectivo, encoding='utf-8')
            esIgual = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", resultadoEfectivo, re.S)
            assert importeCompletado.returncode == 0 and esIgual, (nombre, resultadoEfectivo)
            resultado = next(datosCadena for datosCadena in esIgual.groups() if datosCadena is not None) + '\n'
            assert resultado == esperado, (nombre, esperado, resultado)
            informeValidación['tests'].append({'name': nombre, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', nombre, flush=True)
        # propio JVM에 직접 연결한 español valorHiloEjecución/진입점은 OpenJDK용 래퍼가 아니다.
        importeCompletado = subprocess.run(['python3', str(raízProyecto/'Herramientas/ejecutarArchivo.py'), str(rutaClase/'pruebaHilosEjecuciónCoreano.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        resultado = importeCompletado.stdout.decode('utf-8').replace('\r\n', '\n')
        (salida/'pruebaHilosEjecuciónCoreano.log').write_text(resultado)
        assert importeCompletado.returncode == 0 and 'español 직접 valorHiloEjecución valorPaso\n' in resultado and '\nexit 0\n' in resultado, resultado
        informeValidación['direct_korean_thread_and_entry'] = True
        print('PASS: español 직접 valorHiloEjecución·ejecutarTarea·ponerEnMarcha puntoEntradaElemento', flush=True)
        válido = (rutaClase / 'pruebaObjetos.class').read_bytes()
        pruebaCaso = [('판거부', válido[:6] + b'\x00\x35' + válido[8:], 'supported class versions'),
                 ('잘린클래스', válido[:24], 'truncated class file')]
        informeValidación['rejection_tests'] = []
        for nombre, datosCargaÚtil, textoNotificación in pruebaCaso:
            pruebaDatos = salida / (nombre + '.class'); pruebaDatos.write_bytes(datosCargaÚtil)
            importeCompletado = subprocess.run(['python3', str(raízProyecto / 'Herramientas/ejecutarArchivo.py'), str(pruebaDatos)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            texto = importeCompletado.stdout.decode('utf-8').replace('\r\n', '\n')
            (salida / (nombre + '.log')).write_text(texto, encoding='utf-8')
            assert importeCompletado.returncode == 1 and textoNotificación in texto and 'exit 1\n' in texto, (nombre, texto)
            informeValidación['rejection_tests'].append({'name': nombre, 'passed': True})
            print('PASS (rejected):', nombre, flush=True)
        informeValidación['passed'] = True
    finally:
        (salida / 'report.json').write_text(json.dumps(informeValidación, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ponerEnMarcha()
