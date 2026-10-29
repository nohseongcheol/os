#!/usr/bin/env python3
"""aktuellt_objekt 커널과 verklig_data tester·배포물이 일치할 때에만 통합 validera 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

åtgärd_rot = Path(__file__).resolve().parents[1]

def hash_fil(sökväg_2):
    계산 = hashlib.sha256()
    with sökväg_2.open('rb') as filnamn:
        for data in iter(lambda: filnamn.read(1048576), b''): 계산.update(data)
    return 계산.hexdigest()

def Kör():
    validering_väg = åtgärd_rot/'build/verification'
    kärna_hash = hash_fil(åtgärd_rot/'build/kernel8.img')
    기록들 = {}
    for Namn in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        relativ_sökväg = 'report.json' if Namn == 'boot' else Namn+'/report.json'
        data = json.loads((validering_väg/relativ_sökväg).read_text())
        if not data.get('passed') or data.get('kernel_sha256') != kärna_hash:
            raise SystemExit('aktuellt_objekt 커널에 대한 성공 기록이 필요합니다: '+relativ_sökväg)
        기록들[Namn] = {'passed': True, 'report': relativ_sökväg}
    check_namn = json.loads((validering_väg/'naming/report.json').read_text())
    if not check_namn['passed'] or not check_namn['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for sökväg_2, 기대값 in check_namn['c_source_sha256'].items():
        if hash_fil(åtgärd_rot/sökväg_2) != 기대값: raise SystemExit('명명 검사 BACK_värde 바뀐 C källfil: '+sökväg_2)
    자바검사 = json.loads((validering_väg/'jvm/report.json').read_text())
    직접화면 = json.loads((validering_väg/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('Svenska 직접 skärmbild köra_kommando tester 필요')
    check_byte_värde = json.loads((validering_väg/'naming/direct-bytecode.json').read_text())
    if not check_byte_värde['passed'] or check_byte_värde['jar_sha256'] != hash_fil(åtgärd_rot/'dist/jkoros-native-korean.jar'):
        raise SystemExit('aktuellt_objekt Svenska 라이브러리의 직접 호출 바이트코드 verifiera 필요')
    check_upplösning = json.loads((validering_väg/'resolution/report.json').read_text())
    check_storlek = json.loads((validering_väg/'resize/report.json').read_text())
    갱신검사 = json.loads((validering_väg/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != kärna_hash:
        raise SystemExit('aktuellt_objekt 커널의 부분 uppdatera tester 필요')
    for sökväg_2, 기대값 in 갱신검사['source_sha256'].items():
        if hash_fil(åtgärd_rot/sökväg_2) != 기대값: raise SystemExit('부분 uppdatera tester BACK_värde 바뀐 källfil: '+sökväg_2)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('Svenska 직접 가닥과 Kör startpunkt tester 필요')
    예제검사 = json.loads((validering_väg/'examples/report.json').read_text())
    if sorted(check_storlek['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Storlek 조절 tester 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('Svenska Swing 창을 포함한 예제 13개 tester 필요')
    if sorted(check_upplösning['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 verklig_data skärmbild tester 필요')
    if 자바검사['korean_library_sha256'] != hash_fil(åtgärd_rot/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 tester BACK_värde 라이브러리가 바뀌었습니다.')
    for Namn in ('한국어통신시험','한국어예외시험'):
        if not any(post_värde['name']==Namn and post_värde.get('openjdk_output_equal') for post_värde in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 tester 필요: '+Namn)
    fel_ange = sorted(sökväg_2.stem for sökväg_2 in (åtgärd_rot/'한국어자바/Svenska/eget').glob('*fel_31f743d2.java'))
    fel_LOG = (validering_väg/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Namn in fel_ange:
        if '\n'+Namn+'\n' not in fel_LOG: raise SystemExit('fel_31f743d2 generera·잡기·설명 tester 필요: '+Namn)
    명세 = json.loads((åtgärd_rot/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != hash_fil(åtgärd_rot/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('fördelning_värde BILD_värde hash_fil 불일치')
    with zipfile.ZipFile(str(åtgärd_rot/'dist/jkoros-native-rpi4-boot.zip')) as bunt:
        if hashlib.sha256(bunt.read('kernel8.img')).hexdigest() != kärna_hash:
            raise SystemExit('maskinstart ZIP kärna_värde 불일치')
        부팅설정 = bunt.read('config.txt')
        for Namn, Storlek in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Namn+'='+str(Storlek) not in 부팅설정.decode().splitlines():
                raise SystemExit('maskinstart ZIP skärmbild Inställningar 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(åtgärd_rot/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(åtgärd_rot/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if hash_fil(복사본) != kärna_hash: raise SystemExit('SD BILD_värde kärna_värde 불일치')
        kopia_Inställningar = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(åtgärd_rot/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(kopia_Inställningar)])
        if kopia_Inställningar.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP skärmbild Inställningar 불일치')
    LOG_POST = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': kärna_hash,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': fel_ange, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(check_upplösning['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Namn:hash_fil(åtgärd_rot/'dist'/Namn) for Namn in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (validering_väg/'native-runtime-summary.json').write_text(json.dumps(LOG_POST,ensure_ascii=False,indent=2)+'\n')
    print('PASS: aktuellt_objekt 커널의',len(기록들),'개 통합 tester LOG_POST, Svenska fel_31f743d2',len(fel_ange),'Kurs_Definition, SD BILD_värde·ZIP 일치')

if __name__ == '__main__': Kör()
