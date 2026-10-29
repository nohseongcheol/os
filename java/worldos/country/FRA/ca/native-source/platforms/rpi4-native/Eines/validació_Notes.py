#!/usr/bin/env python3
"""현재 커널과 real_dades 시험·배포물이 일치할 때에만 통합 validar 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

Project_rel = Path(__file__).resolve().parents[1]

def hash_arxiu(Camí):
    계산 = hashlib.sha256()
    with Camí.open('rb') as Fitxer:
        for dades in iter(lambda: Fitxer.read(1048576), b''): 계산.update(dades)
    return 계산.hexdigest()

def Executa_2():
    validació_camí = Project_rel/'build/verification'
    nucli_hash = hash_arxiu(Project_rel/'build/kernel8.img')
    기록들 = {}
    for Nom in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Nom == 'boot' else Nom+'/report.json'
        dades = json.loads((validació_camí/상대경로).read_text())
        if not dades.get('passed') or dades.get('kernel_sha256') != nucli_hash:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Nom] = {'passed': True, 'report': 상대경로}
    xec_nom = json.loads((validació_camí/'naming/report.json').read_text())
    if not xec_nom['passed'] or not xec_nom['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for Camí, 기대값 in xec_nom['c_source_sha256'].items():
        if hash_arxiu(Project_rel/Camí) != 기대값: raise SystemExit('명명 검사 ENRERE_VALOR 바뀐 C FONT: '+Camí)
    자바검사 = json.loads((validació_camí/'jvm/report.json').read_text())
    직접화면 = json.loads((validació_camí/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('Català 직접 화면 Executa_ordre 시험 필요')
    xec_byte_VALOR = json.loads((validació_camí/'naming/direct-bytecode.json').read_text())
    if not xec_byte_VALOR['passed'] or xec_byte_VALOR['jar_sha256'] != hash_arxiu(Project_rel/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 Català 라이브러리의 직접 호출 바이트코드 verificar 필요')
    xec_resolució = json.loads((validació_camí/'resolution/report.json').read_text())
    xec_canviar_la_mida = json.loads((validació_camí/'resize/report.json').read_text())
    갱신검사 = json.loads((validació_camí/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != nucli_hash:
        raise SystemExit('현재 커널의 부분 actualitzar 시험 필요')
    for Camí, 기대값 in 갱신검사['source_sha256'].items():
        if hash_arxiu(Project_rel/Camí) != 기대값: raise SystemExit('부분 actualitzar 시험 ENRERE_VALOR 바뀐 FONT: '+Camí)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('Català 직접 가닥과 Executa_2 introducció_p 시험 필요')
    예제검사 = json.loads((validació_camí/'examples/report.json').read_text())
    if sorted(xec_canviar_la_mida['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Mida 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('Català Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(xec_resolució['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 real_dades 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != hash_arxiu(Project_rel/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 ENRERE_VALOR 라이브러리가 바뀌었습니다.')
    for Nom in ('한국어통신시험','한국어예외시험'):
        if not any(introducció_VALOR['name']==Nom and introducció_VALOR.get('openjdk_output_equal') for introducció_VALOR in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Nom)
    excepció_Llista = sorted(Camí.stem for Camí in (Project_rel/'한국어자바/Català/propi').glob('*excepció.java'))
    excepció_LOG = (validació_camí/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Nom in excepció_Llista:
        if '\n'+Nom+'\n' not in excepció_LOG: raise SystemExit('excepció generar·잡기·설명 시험 필요: '+Nom)
    명세 = json.loads((Project_rel/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != hash_arxiu(Project_rel/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 IMATGE_VALOR hash_arxiu 불일치')
    with zipfile.ZipFile(str(Project_rel/'dist/jkoros-native-rpi4-boot.zip')) as paquet:
        if hashlib.sha256(paquet.read('kernel8.img')).hexdigest() != nucli_hash:
            raise SystemExit('부팅 ZIP nucli_VALOR 불일치')
        부팅설정 = paquet.read('config.txt')
        for Nom, Mida in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Nom+'='+str(Mida) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Ajusts 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(Project_rel/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(Project_rel/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if hash_arxiu(복사본) != nucli_hash: raise SystemExit('SD IMATGE_VALOR nucli_VALOR 불일치')
        copiar_Configuració = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(Project_rel/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(copiar_Configuració)])
        if copiar_Configuració.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Ajusts 불일치')
    LOG_fila = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': nucli_hash,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': excepció_Llista, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(xec_resolució['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Nom:hash_arxiu(Project_rel/'dist'/Nom) for Nom in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (validació_camí/'native-runtime-summary.json').write_text(json.dumps(LOG_fila,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 LOG_fila, Català excepció',len(excepció_Llista),'Classe_Definició, SD IMATGE_VALOR·ZIP 일치')

if __name__ == '__main__': Executa_2()
