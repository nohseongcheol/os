#!/usr/bin/env python3
"""ao_corrente_elemento 커널과 real_datos 시험·배포물이 일치할 때에만 통합 validar 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

Project_raíz = Path(__file__).resolve().parents[1]

def hash_Ficheiro(CAMIÑO):
    계산 = hashlib.sha256()
    with CAMIÑO.open('rb') as Ficheiro:
        for datos in iter(lambda: Ficheiro.read(1048576), b''): 계산.update(datos)
    return 계산.hexdigest()

def Executar_2():
    validación_camiño = Project_raíz/'build/verification'
    kernel_hash = hash_Ficheiro(Project_raíz/'build/kernel8.img')
    기록들 = {}
    for Nome in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Nome == 'boot' else Nome+'/report.json'
        datos = json.loads((validación_camiño/상대경로).read_text())
        if not datos.get('passed') or datos.get('kernel_sha256') != kernel_hash:
            raise SystemExit('ao_corrente_elemento 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Nome] = {'passed': True, 'report': 상대경로}
    cheque_nome = json.loads((validación_camiño/'naming/report.json').read_text())
    if not cheque_nome['passed'] or not cheque_nome['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for CAMIÑO, 기대값 in cheque_nome['c_source_sha256'].items():
        if hash_Ficheiro(Project_raíz/CAMIÑO) != 기대값: raise SystemExit('명명 검사 ATRÁS_VALOR 바뀐 C FONTE: '+CAMIÑO)
    자바검사 = json.loads((validación_camiño/'jvm/report.json').read_text())
    직접화면 = json.loads((validación_camiño/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('Galego 직접 화면 executar_comando 시험 필요')
    cheque_byte_VALOR = json.loads((validación_camiño/'naming/direct-bytecode.json').read_text())
    if not cheque_byte_VALOR['passed'] or cheque_byte_VALOR['jar_sha256'] != hash_Ficheiro(Project_raíz/'dist/jkoros-native-korean.jar'):
        raise SystemExit('ao_corrente_elemento Galego 라이브러리의 직접 호출 바이트코드 verificar 필요')
    cheque_resolución = json.loads((validación_camiño/'resolution/report.json').read_text())
    크기검사 = json.loads((validación_camiño/'resize/report.json').read_text())
    갱신검사 = json.loads((validación_camiño/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != kernel_hash:
        raise SystemExit('ao_corrente_elemento 커널의 부분 actualizar 시험 필요')
    for CAMIÑO, 기대값 in 갱신검사['source_sha256'].items():
        if hash_Ficheiro(Project_raíz/CAMIÑO) != 기대값: raise SystemExit('부분 actualizar 시험 ATRÁS_VALOR 바뀐 FONTE: '+CAMIÑO)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('Galego 직접 가닥과 Executar_2 introdución_p 시험 필요')
    예제검사 = json.loads((validación_camiño/'examples/report.json').read_text())
    if sorted(크기검사['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Tamaño 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('Galego Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(cheque_resolución['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 real_datos 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != hash_Ficheiro(Project_raíz/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 ATRÁS_VALOR 라이브러리가 바뀌었습니다.')
    for Nome in ('한국어통신시험','한국어예외시험'):
        if not any(introdución_VALOR['name']==Nome and introdución_VALOR.get('openjdk_output_equal') for introdución_VALOR in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Nome)
    excepción_Lista = sorted(CAMIÑO.stem for CAMIÑO in (Project_raíz/'한국어자바/Galego/자체').glob('*excepción.java'))
    excepción_LOG = (validación_camiño/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Nome in excepción_Lista:
        if '\n'+Nome+'\n' not in excepción_LOG: raise SystemExit('excepción xerar·잡기·설명 시험 필요: '+Nome)
    명세 = json.loads((Project_raíz/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != hash_Ficheiro(Project_raíz/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 IMAXE_VALOR hash_Ficheiro 불일치')
    with zipfile.ZipFile(str(Project_raíz/'dist/jkoros-native-rpi4-boot.zip')) as paquete:
        if hashlib.sha256(paquete.read('kernel8.img')).hexdigest() != kernel_hash:
            raise SystemExit('부팅 ZIP kernel_VALOR 불일치')
        부팅설정 = paquete.read('config.txt')
        for Nome, Tamaño in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Nome+'='+str(Tamaño) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Configuración 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(Project_raíz/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(Project_raíz/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if hash_Ficheiro(복사본) != kernel_hash: raise SystemExit('SD IMAXE_VALOR kernel_VALOR 불일치')
        copiar_Configuración = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(Project_raíz/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(copiar_Configuración)])
        if copiar_Configuración.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Configuración 불일치')
    LOG_fila = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': kernel_hash,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': excepción_Lista, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(cheque_resolución['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Nome:hash_Ficheiro(Project_raíz/'dist'/Nome) for Nome in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (validación_camiño/'native-runtime-summary.json').write_text(json.dumps(LOG_fila,ensure_ascii=False,indent=2)+'\n')
    print('PASS: ao_corrente_elemento 커널의',len(기록들),'개 통합 시험 LOG_fila, Galego excepción',len(excepción_Lista),'Clase_Definición, SD IMAXE_VALOR·ZIP 일치')

if __name__ == '__main__': Executar_2()
