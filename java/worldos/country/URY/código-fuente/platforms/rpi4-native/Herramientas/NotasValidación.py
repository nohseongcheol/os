#!/usr/bin/env python3
"""elementoListaActual 커널과 datosEfectivo Pruebas·배포물이 일치할 때에만 통합 validar 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

raízProyecto = Path(__file__).resolve().parents[1]

def archivoResumenHash(ruta):
    resultadoCálculo = hashlib.sha256()
    with ruta.open('rb') as Archivo:
        for Datos in iter(lambda: Archivo.read(1048576), b''): resultadoCálculo.update(Datos)
    return resultadoCálculo.hexdigest()

def ponerEnMarcha():
    rutaValidación = raízProyecto/'build/verification'
    resumenHashNúcleo = archivoResumenHash(raízProyecto/'build/kernel8.img')
    registrosDiario = {}
    for nombre in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        rutaRelativo = 'report.json' if nombre == 'boot' else nombre+'/report.json'
        Datos = json.loads((rutaValidación/rutaRelativo).read_text())
        if not Datos.get('passed') or Datos.get('kernel_sha256') != resumenHashNúcleo:
            raise SystemExit('elementoListaActual 커널에 대한 valorÉxito 기록이 필요합니다: '+rutaRelativo)
        registrosDiario[nombre] = {'passed': True, 'report': rutaRelativo}
    comprobarNombre = json.loads((rutaValidación/'naming/report.json').read_text())
    if not comprobarNombre['passed'] or not comprobarNombre['c_semantic_checked']: raise SystemExit('C 선언을 포함한 denominación Comprobaciones valorNecesario')
    for ruta, valorEsperado in comprobarNombre['c_source_sha256'].items():
        if archivoResumenHash(raízProyecto/ruta) != valorEsperado: raise SystemExit('denominación Comprobaciones valorLadoPosterior 바뀐 C fuente: '+ruta)
    comprobarJava = json.loads((rutaValidación/'jvm/report.json').read_text())
    PantallaDirecto = json.loads((rutaValidación/'swing/report.json').read_text())
    if not PantallaDirecto.get('direct_korean_gui'): raise SystemExit('español 직접 Pantalla ejecutarComando Pruebas valorNecesario')
    comprobarValorByte = json.loads((rutaValidación/'naming/direct-bytecode.json').read_text())
    if not comprobarValorByte['passed'] or comprobarValorByte['jar_sha256'] != archivoResumenHash(raízProyecto/'dist/jkoros-native-korean.jar'):
        raise SystemExit('elementoListaActual español 라이브러리의 직접 invocar códigoBytes verificar valorNecesario')
    comprobarResolución = json.loads((rutaValidación/'resolution/report.json').read_text())
    comprobarTamaño = json.loads((rutaValidación/'resize/report.json').read_text())
    comprobarActualizacionesPara = json.loads((rutaValidación/'redraw/report.json').read_text())
    if not comprobarActualizacionesPara['passed'] or comprobarActualizacionesPara['kernel_sha256'] != resumenHashNúcleo:
        raise SystemExit('elementoListaActual 커널의 valorSubparte actualizar Pruebas valorNecesario')
    for ruta, valorEsperado in comprobarActualizacionesPara['source_sha256'].items():
        if archivoResumenHash(raízProyecto/ruta) != valorEsperado: raise SystemExit('valorSubparte actualizar Pruebas valorLadoPosterior 바뀐 fuente: '+ruta)
    if not comprobarJava.get('direct_korean_thread_and_entry'):
        raise SystemExit('español 직접 가닥과 ponerEnMarcha puntoEntradaElemento Pruebas valorNecesario')
    comprobarEjemplo = json.loads((rutaValidación/'examples/report.json').read_text())
    if sorted(comprobarTamaño['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 valorEsquina tamaño 조절 Pruebas valorNecesario')
    if not comprobarEjemplo.get('swing_example_korean_input_button_label_and_close') or comprobarEjemplo['examples_executed'] != 13:
        raise SystemExit('español Swing 창을 포함한 Ejemplos 13개 Pruebas valorNecesario')
    if sorted(comprobarResolución['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 datosEfectivo Pantalla Pruebas valorNecesario')
    if comprobarJava['korean_library_sha256'] != archivoResumenHash(raízProyecto/'dist/jkoros-native-korean.jar'):
        raise SystemExit('Java Pruebas valorLadoPosterior 라이브러리가 바뀌었습니다.')
    for nombre in ('pruebaConexiónRedCoreano','pruebaExcepcionesCoreano'):
        if not any(valorEntradaElemento['name']==nombre and valorEntradaElemento.get('openjdk_output_equal') for valorEntradaElemento in comprobarJava['tests']):
            raise SystemExit('OpenJDK 대조 Pruebas valorNecesario: '+nombre)
    listaExcepción = sorted(ruta.stem for ruta in (raízProyecto/'JavaEspañol/español/propio').glob('*excepción.java'))
    diarioExcepción = (rutaValidación/'jvm/pruebaExcepcionesCoreano.log').read_text().replace('\r\n','\n')
    for nombre in listaExcepción:
        if '\n'+nombre+'\n' not in diarioExcepción: raise SystemExit('excepción generar·잡기·descripción Pruebas valorNecesario: '+nombre)
    especificación = json.loads((raízProyecto/'dist/manifest.json').read_text())
    if especificación['image_sha256'] != archivoResumenHash(raízProyecto/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('valorDistribución valorImagen archivoResumenHash 불일치')
    with zipfile.ZipFile(str(raízProyecto/'dist/jkoros-native-rpi4-boot.zip')) as Paquete:
        if hashlib.sha256(Paquete.read('kernel8.img')).hexdigest() != resumenHashNúcleo:
            raise SystemExit('Arranque ZIP valorNúcleo 불일치')
        ajustesArranque = Paquete.read('config.txt')
        for nombre, tamaño in zip(('width', 'height'), especificación['framebuffer_resolution']):
            if 'framebuffer_'+nombre+'='+str(tamaño) not in ajustesArranque.decode().splitlines():
                raise SystemExit('Arranque ZIP Pantalla ajustes 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(raízProyecto/'build')) as valorTemporal:
        valorCopiado = Path(valorTemporal)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(raízProyecto/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(valorCopiado)])
        if archivoResumenHash(valorCopiado) != resumenHashNúcleo: raise SystemExit('SD valorImagen valorNúcleo 불일치')
        copiarAjustes = Path(valorTemporal)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(raízProyecto/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(copiarAjustes)])
        if copiarAjustes.read_bytes() != ajustesArranque: raise SystemExit('SD 영상과 ZIP Pantalla ajustes 불일치')
    registroEntradaDiario = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': resumenHashNúcleo,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': registrosDiario, 'naming_report': 'naming/report.json',
            'korean_exception_classes': listaExcepción, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': comprobarEjemplo['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(comprobarResolución['resolutions']),
            'sd_framebuffer_resolution': especificación['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {nombre:archivoResumenHash(raízProyecto/'dist'/nombre) for nombre in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (rutaValidación/'native-runtime-summary.json').write_text(json.dumps(registroEntradaDiario,ensure_ascii=False,indent=2)+'\n')
    print('PASS: elementoListaActual 커널의',len(registrosDiario),'개 통합 Pruebas registroEntradaDiario, español excepción',len(listaExcepción),'definiciónClase, SD valorImagen·ZIP esIgual')

if __name__ == '__main__': ponerEnMarcha()
