#!/usr/bin/env python3
"""betalt_vare 커널과 faktisk_data 시험·배포물이 일치할 때에만 통합 bekrefte 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

spegle_rot = Path(__file__).resolve().parents[1]

def hash_fil(STIGE):
    계산 = hashlib.sha256()
    with STIGE.open('rb') as Fil:
        for data in iter(lambda: Fil.read(1048576), b''): 계산.update(data)
    return 계산.hexdigest()

def Køyr_2():
    validering_bane = spegle_rot/'build/verification'
    kjerne_hash = hash_fil(spegle_rot/'build/kernel8.img')
    기록들 = {}
    for Namn in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Namn == 'boot' else Namn+'/report.json'
        data = json.loads((validering_bane/상대경로).read_text())
        if not data.get('passed') or data.get('kernel_sha256') != kjerne_hash:
            raise SystemExit('betalt_vare 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Namn] = {'passed': True, 'report': 상대경로}
    sjekk_namn = json.loads((validering_bane/'naming/report.json').read_text())
    if not sjekk_namn['passed'] or not sjekk_namn['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for STIGE, 기대값 in sjekk_namn['c_source_sha256'].items():
        if hash_fil(spegle_rot/STIGE) != 기대값: raise SystemExit('명명 검사 TILBAKE_VALUE 바뀐 C KJELDE: '+STIGE)
    자바검사 = json.loads((validering_bane/'jvm/report.json').read_text())
    직접화면 = json.loads((validering_bane/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 Utfør_kommando 시험 필요')
    sjekk_byte_VALUE = json.loads((validering_bane/'naming/direct-bytecode.json').read_text())
    if not sjekk_byte_VALUE['passed'] or sjekk_byte_VALUE['jar_sha256'] != hash_fil(spegle_rot/'dist/jkoros-native-korean.jar'):
        raise SystemExit('betalt_vare 한국어 라이브러리의 직접 호출 바이트코드 stadfeste 필요')
    sjekk_oppløysing = json.loads((validering_bane/'resolution/report.json').read_text())
    sjekk_endre_storleik = json.loads((validering_bane/'resize/report.json').read_text())
    갱신검사 = json.loads((validering_bane/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != kjerne_hash:
        raise SystemExit('betalt_vare 커널의 부분 oppdatere 시험 필요')
    for STIGE, 기대값 in 갱신검사['source_sha256'].items():
        if hash_fil(spegle_rot/STIGE) != 기대값: raise SystemExit('부분 oppdatere 시험 TILBAKE_VALUE 바뀐 KJELDE: '+STIGE)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 Køyr_2 oppføring_p 시험 필요')
    예제검사 = json.loads((validering_bane/'examples/report.json').read_text())
    if sorted(sjekk_endre_storleik['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Storleik 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(sjekk_oppløysing['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 faktisk_data 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != hash_fil(spegle_rot/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 TILBAKE_VALUE 라이브러리가 바뀌었습니다.')
    for Namn in ('한국어통신시험','한국어예외시험'):
        if not any(oppføring_VALUE['name']==Namn and oppføring_VALUE.get('openjdk_output_equal') for oppføring_VALUE in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Namn)
    unntak_Liste = sorted(STIGE.stem for STIGE in (spegle_rot/'한국어자바/한국어/자체').glob('*unntak.java'))
    unntak_LOG = (validering_bane/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Namn in unntak_Liste:
        if '\n'+Namn+'\n' not in unntak_LOG: raise SystemExit('unntak generere·잡기·설명 시험 필요: '+Namn)
    명세 = json.loads((spegle_rot/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != hash_fil(spegle_rot/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 IMAGE_VALUE hash_fil 불일치')
    with zipfile.ZipFile(str(spegle_rot/'dist/jkoros-native-rpi4-boot.zip')) as bunt:
        if hashlib.sha256(bunt.read('kernel8.img')).hexdigest() != kjerne_hash:
            raise SystemExit('부팅 ZIP kjerne_VALUE 불일치')
        부팅설정 = bunt.read('config.txt')
        for Namn, Storleik in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Namn+'='+str(Storleik) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Innstillingar 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(spegle_rot/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(spegle_rot/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if hash_fil(복사본) != kjerne_hash: raise SystemExit('SD IMAGE_VALUE kjerne_VALUE 불일치')
        kopiere_Innstillingar = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(spegle_rot/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(kopiere_Innstillingar)])
        if kopiere_Innstillingar.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Innstillingar 불일치')
    LOG_rad = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': kjerne_hash,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': unntak_Liste, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(sjekk_oppløysing['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Namn:hash_fil(spegle_rot/'dist'/Namn) for Namn in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (validering_bane/'native-runtime-summary.json').write_text(json.dumps(LOG_rad,ensure_ascii=False,indent=2)+'\n')
    print('PASS: betalt_vare 커널의',len(기록들),'개 통합 시험 LOG_rad, 한국어 unntak',len(unntak_Liste),'종, SD IMAGE_VALUE·ZIP 일치')

if __name__ == '__main__': Køyr_2()
