#!/usr/bin/env python3
"""aktuelno_stavka 커널과 stvarni_podaci 시험·배포물이 일치할 때에만 통합 potvrditi 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

radnja_koren = Path(__file__).resolve().parents[1]

def heš_Datoteka(putanja):
    계산 = hashlib.sha256()
    with putanja.open('rb') as Datoteka:
        for podaci in iter(lambda: Datoteka.read(1048576), b''): 계산.update(podaci)
    return 계산.hexdigest()

def koristiti():
    provera_valjanosti_putanja = radnja_koren/'build/verification'
    jezgro_heš = heš_Datoteka(radnja_koren/'build/kernel8.img')
    기록들 = {}
    for ime in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        relativna_putanja = 'report.json' if ime == 'boot' else ime+'/report.json'
        podaci = json.loads((provera_valjanosti_putanja/relativna_putanja).read_text())
        if not podaci.get('passed') or podaci.get('kernel_sha256') != jezgro_heš:
            raise SystemExit('aktuelno_stavka 커널에 대한 성공 기록이 필요합니다: '+relativna_putanja)
        기록들[ime] = {'passed': True, 'report': relativna_putanja}
    proveriti_ime = json.loads((provera_valjanosti_putanja/'naming/report.json').read_text())
    if not proveriti_ime['passed'] or not proveriti_ime['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for putanja, 기대값 in proveriti_ime['c_source_sha256'].items():
        if heš_Datoteka(radnja_koren/putanja) != 기대값: raise SystemExit('명명 검사 NAZAD_VALUE 바뀐 C izvor: '+putanja)
    자바검사 = json.loads((provera_valjanosti_putanja/'jvm/report.json').read_text())
    직접화면 = json.loads((provera_valjanosti_putanja/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 Izvrši_komanda 시험 필요')
    proveriti_bajt_VALUE = json.loads((provera_valjanosti_putanja/'naming/direct-bytecode.json').read_text())
    if not proveriti_bajt_VALUE['passed'] or proveriti_bajt_VALUE['jar_sha256'] != heš_Datoteka(radnja_koren/'dist/jkoros-native-korean.jar'):
        raise SystemExit('aktuelno_stavka 한국어 라이브러리의 직접 호출 바이트코드 verifikovati 필요')
    proveriti_rezolucija = json.loads((provera_valjanosti_putanja/'resolution/report.json').read_text())
    proveriti_promeniti_veličinu = json.loads((provera_valjanosti_putanja/'resize/report.json').read_text())
    갱신검사 = json.loads((provera_valjanosti_putanja/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != jezgro_heš:
        raise SystemExit('aktuelno_stavka 커널의 부분 osvežiti 시험 필요')
    for putanja, 기대값 in 갱신검사['source_sha256'].items():
        if heš_Datoteka(radnja_koren/putanja) != 기대값: raise SystemExit('부분 osvežiti 시험 NAZAD_VALUE 바뀐 izvor: '+putanja)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 koristiti stavka_p 시험 필요')
    예제검사 = json.loads((provera_valjanosti_putanja/'examples/report.json').read_text())
    if sorted(proveriti_promeniti_veličinu['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 promeniti_veličinu 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(proveriti_rezolucija['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 stvarni_podaci 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != heš_Datoteka(radnja_koren/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 NAZAD_VALUE 라이브러리가 바뀌었습니다.')
    for ime in ('한국어통신시험','한국어예외시험'):
        if not any(stavka_VALUE['name']==ime and stavka_VALUE.get('openjdk_output_equal') for stavka_VALUE in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+ime)
    izuzetak_Lista = sorted(putanja.stem for putanja in (radnja_koren/'한국어자바/한국어/자체').glob('*izuzetak.java'))
    izuzetak_LOG = (provera_valjanosti_putanja/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for ime in izuzetak_Lista:
        if '\n'+ime+'\n' not in izuzetak_LOG: raise SystemExit('izuzetak generisati·잡기·설명 시험 필요: '+ime)
    명세 = json.loads((radnja_koren/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != heš_Datoteka(radnja_koren/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 IMAGE_VALUE heš_Datoteka 불일치')
    with zipfile.ZipFile(str(radnja_koren/'dist/jkoros-native-rpi4-boot.zip')) as komplet:
        if hashlib.sha256(komplet.read('kernel8.img')).hexdigest() != jezgro_heš:
            raise SystemExit('부팅 ZIP jezgro_VALUE 불일치')
        부팅설정 = komplet.read('config.txt')
        for ime, promeniti_veličinu in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+ime+'='+str(promeniti_veličinu) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Postavke 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(radnja_koren/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(radnja_koren/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if heš_Datoteka(복사본) != jezgro_heš: raise SystemExit('SD IMAGE_VALUE jezgro_VALUE 불일치')
        instanca_Postavke = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(radnja_koren/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(instanca_Postavke)])
        if instanca_Postavke.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Postavke 불일치')
    LOG_snimi = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': jezgro_heš,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': izuzetak_Lista, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(proveriti_rezolucija['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {ime:heš_Datoteka(radnja_koren/'dist'/ime) for ime in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (provera_valjanosti_putanja/'native-runtime-summary.json').write_text(json.dumps(LOG_snimi,ensure_ascii=False,indent=2)+'\n')
    print('PASS: aktuelno_stavka 커널의',len(기록들),'개 통합 시험 LOG_snimi, 한국어 izuzetak',len(izuzetak_Lista),'Razred_Definicija, SD IMAGE_VALUE·ZIP 일치')

if __name__ == '__main__': koristiti()
