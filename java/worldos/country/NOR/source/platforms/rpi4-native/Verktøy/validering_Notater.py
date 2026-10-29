#!/usr/bin/env python3
"""betalt_vare 커널과 faktisk_data 시험·배포물이 일치할 때에만 통합 bekrefte_5fb2b747 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

speile_rot = Path(__file__).resolve().parents[1]

def hash_Fil(Sti):
    계산 = hashlib.sha256()
    with Sti.open('rb') as Fil:
        for data in iter(lambda: Fil.read(1048576), b''): 계산.update(data)
    return 계산.hexdigest()

def Kjør_2():
    validering_bane = speile_rot/'build/verification'
    kjerne_hash = hash_Fil(speile_rot/'build/kernel8.img')
    기록들 = {}
    for Navn in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        relativ_bane = 'report.json' if Navn == 'boot' else Navn+'/report.json'
        data = json.loads((validering_bane/relativ_bane).read_text())
        if not data.get('passed') or data.get('kernel_sha256') != kjerne_hash:
            raise SystemExit('betalt_vare 커널에 대한 성공 기록이 필요합니다: '+relativ_bane)
        기록들[Navn] = {'passed': True, 'report': relativ_bane}
    sjekk_navn = json.loads((validering_bane/'naming/report.json').read_text())
    if not sjekk_navn['passed'] or not sjekk_navn['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for Sti, 기대값 in sjekk_navn['c_source_sha256'].items():
        if hash_Fil(speile_rot/Sti) != 기대값: raise SystemExit('명명 검사 TILBAKE_VERDI 바뀐 C KILDE: '+Sti)
    자바검사 = json.loads((validering_bane/'jvm/report.json').read_text())
    직접화면 = json.loads((validering_bane/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('norsk 직접 skjermbilde Utfør_kommando 시험 필요')
    sjekk_byte_VERDI = json.loads((validering_bane/'naming/direct-bytecode.json').read_text())
    if not sjekk_byte_VERDI['passed'] or sjekk_byte_VERDI['jar_sha256'] != hash_Fil(speile_rot/'dist/jkoros-native-korean.jar'):
        raise SystemExit('betalt_vare norsk 라이브러리의 직접 호출 바이트코드 bekrefte 필요')
    sjekk_oppløsning = json.loads((validering_bane/'resolution/report.json').read_text())
    sjekk_skalere = json.loads((validering_bane/'resize/report.json').read_text())
    갱신검사 = json.loads((validering_bane/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != kjerne_hash:
        raise SystemExit('betalt_vare 커널의 부분 oppdatere 시험 필요')
    for Sti, 기대값 in 갱신검사['source_sha256'].items():
        if hash_Fil(speile_rot/Sti) != 기대값: raise SystemExit('부분 oppdatere 시험 TILBAKE_VERDI 바뀐 KILDE: '+Sti)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('norsk 직접 가닥과 Kjør_2 inngangspunkt 시험 필요')
    예제검사 = json.loads((validering_bane/'examples/report.json').read_text())
    if sorted(sjekk_skalere['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Størrelse 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('norsk Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(sjekk_oppløsning['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 faktisk_data skjermbilde 시험 필요')
    if 자바검사['korean_library_sha256'] != hash_Fil(speile_rot/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 TILBAKE_VERDI 라이브러리가 바뀌었습니다.')
    for Navn in ('한국어통신시험','한국어예외시험'):
        if not any(oppføring_VERDI['name']==Navn and oppføring_VERDI.get('openjdk_output_equal') for oppføring_VERDI in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Navn)
    unntak_Liste = sorted(Sti.stem for Sti in (speile_rot/'한국어자바/norsk/eget').glob('*unntak.java'))
    unntak_LOG = (validering_bane/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Navn in unntak_Liste:
        if '\n'+Navn+'\n' not in unntak_LOG: raise SystemExit('unntak generere·잡기·설명 시험 필요: '+Navn)
    명세 = json.loads((speile_rot/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != hash_Fil(speile_rot/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('distribusjon_VERDI BILDE_VERDI hash_Fil 불일치')
    with zipfile.ZipFile(str(speile_rot/'dist/jkoros-native-rpi4-boot.zip')) as bunt:
        if hashlib.sha256(bunt.read('kernel8.img')).hexdigest() != kjerne_hash:
            raise SystemExit('부팅 ZIP kjerne_VERDI 불일치')
        부팅설정 = bunt.read('config.txt')
        for Navn, Størrelse in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Navn+'='+str(Størrelse) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP skjermbilde Innstillinger 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(speile_rot/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(speile_rot/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if hash_Fil(복사본) != kjerne_hash: raise SystemExit('SD BILDE_VERDI kjerne_VERDI 불일치')
        kopiere_Innstillinger = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(speile_rot/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(kopiere_Innstillinger)])
        if kopiere_Innstillinger.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP skjermbilde Innstillinger 불일치')
    LOG_POST = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
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
            'framebuffer_resolutions_tested': sorted(sjekk_oppløsning['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Navn:hash_Fil(speile_rot/'dist'/Navn) for Navn in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (validering_bane/'native-runtime-summary.json').write_text(json.dumps(LOG_POST,ensure_ascii=False,indent=2)+'\n')
    print('PASS: betalt_vare 커널의',len(기록들),'개 통합 시험 LOG_POST, norsk unntak',len(unntak_Liste),'time_Definisjon, SD BILDE_VERDI·ZIP 일치')

if __name__ == '__main__': Kjør_2()
