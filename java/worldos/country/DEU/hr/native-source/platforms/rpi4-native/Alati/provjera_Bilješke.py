#!/usr/bin/env python3
"""redovno_artikl 커널과 stvaran_podaci 시험·배포물이 일치할 때에만 통합 potvrditi 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

akcija_korijen = Path(__file__).resolve().parents[1]

def raspršivanje_Datoteka(PUTANJA):
    계산 = hashlib.sha256()
    with PUTANJA.open('rb') as Datoteka:
        for podaci in iter(lambda: Datoteka.read(1048576), b''): 계산.update(podaci)
    return 계산.hexdigest()

def Pokreni():
    provjera_put = akcija_korijen/'build/verification'
    jezgra_sustava_raspršivanje = raspršivanje_Datoteka(akcija_korijen/'build/kernel8.img')
    기록들 = {}
    for Ime in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        relativni_put = 'report.json' if Ime == 'boot' else Ime+'/report.json'
        podaci = json.loads((provjera_put/relativni_put).read_text())
        if not podaci.get('passed') or podaci.get('kernel_sha256') != jezgra_sustava_raspršivanje:
            raise SystemExit('redovno_artikl 커널에 대한 성공 기록이 필요합니다: '+relativni_put)
        기록들[Ime] = {'passed': True, 'report': relativni_put}
    이름검사 = json.loads((provjera_put/'naming/report.json').read_text())
    if not 이름검사['passed'] or not 이름검사['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for PUTANJA, 기대값 in 이름검사['c_source_sha256'].items():
        if raspršivanje_Datoteka(akcija_korijen/PUTANJA) != 기대값: raise SystemExit('명명 검사 TRAG_VALUE 바뀐 C IZVOR: '+PUTANJA)
    자바검사 = json.loads((provjera_put/'jvm/report.json').read_text())
    직접화면 = json.loads((provjera_put/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('hrvatski 직접 화면 Izvrši_naredba 시험 필요')
    바이트검사 = json.loads((provjera_put/'naming/direct-bytecode.json').read_text())
    if not 바이트검사['passed'] or 바이트검사['jar_sha256'] != raspršivanje_Datoteka(akcija_korijen/'dist/jkoros-native-korean.jar'):
        raise SystemExit('redovno_artikl hrvatski 라이브러리의 직접 호출 바이트코드 provjeriti 필요')
    해상도검사 = json.loads((provjera_put/'resolution/report.json').read_text())
    크기검사 = json.loads((provjera_put/'resize/report.json').read_text())
    갱신검사 = json.loads((provjera_put/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != jezgra_sustava_raspršivanje:
        raise SystemExit('redovno_artikl 커널의 부분 osvježiti 시험 필요')
    for PUTANJA, 기대값 in 갱신검사['source_sha256'].items():
        if raspršivanje_Datoteka(akcija_korijen/PUTANJA) != 기대값: raise SystemExit('부분 osvježiti 시험 TRAG_VALUE 바뀐 IZVOR: '+PUTANJA)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('hrvatski 직접 가닥과 Pokreni unos_p 시험 필요')
    예제검사 = json.loads((provjera_put/'examples/report.json').read_text())
    if sorted(크기검사['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Veličina 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('hrvatski Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(해상도검사['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 stvaran_podaci 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != raspršivanje_Datoteka(akcija_korijen/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 TRAG_VALUE 라이브러리가 바뀌었습니다.')
    for Ime in ('한국어통신시험','한국어예외시험'):
        if not any(unos_VALUE['name']==Ime and unos_VALUE.get('openjdk_output_equal') for unos_VALUE in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Ime)
    iznimka_Popis = sorted(PUTANJA.stem for PUTANJA in (akcija_korijen/'한국어자바/hrvatski/vlastiti').glob('*iznimka.java'))
    iznimka_LOG = (provjera_put/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Ime in iznimka_Popis:
        if '\n'+Ime+'\n' not in iznimka_LOG: raise SystemExit('iznimka generirati·잡기·설명 시험 필요: '+Ime)
    명세 = json.loads((akcija_korijen/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != raspršivanje_Datoteka(akcija_korijen/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 IMAGE_VALUE raspršivanje_Datoteka 불일치')
    with zipfile.ZipFile(str(akcija_korijen/'dist/jkoros-native-rpi4-boot.zip')) as komplet:
        if hashlib.sha256(komplet.read('kernel8.img')).hexdigest() != jezgra_sustava_raspršivanje:
            raise SystemExit('부팅 ZIP jezgra_sustava_VALUE 불일치')
        부팅설정 = komplet.read('config.txt')
        for Ime, Veličina in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Ime+'='+str(Veličina) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Postavke 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(akcija_korijen/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(akcija_korijen/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if raspršivanje_Datoteka(복사본) != jezgra_sustava_raspršivanje: raise SystemExit('SD IMAGE_VALUE jezgra_sustava_VALUE 불일치')
        instanca_Postavke = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(akcija_korijen/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(instanca_Postavke)])
        if instanca_Postavke.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Postavke 불일치')
    LOG_zapis = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': jezgra_sustava_raspršivanje,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': iznimka_Popis, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(해상도검사['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Ime:raspršivanje_Datoteka(akcija_korijen/'dist'/Ime) for Ime in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (provjera_put/'native-runtime-summary.json').write_text(json.dumps(LOG_zapis,ensure_ascii=False,indent=2)+'\n')
    print('PASS: redovno_artikl 커널의',len(기록들),'개 통합 시험 LOG_zapis, hrvatski iznimka',len(iznimka_Popis),'poduka_definicija, SD IMAGE_VALUE·ZIP 일치')

if __name__ == '__main__': Pokreni()
