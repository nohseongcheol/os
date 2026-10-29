#!/usr/bin/env python3
"""aktuel_vare 커널과 faktisk_data 시험·배포물이 일치할 때에만 통합 bekræfte_5fb2b747 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

To_do_rod = Path(__file__).resolve().parents[1]

def hash_fil(Sti):
    계산 = hashlib.sha256()
    with Sti.open('rb') as Fil:
        for data in iter(lambda: Fil.read(1048576), b''): 계산.update(data)
    return 계산.hexdigest()

def Kør_2():
    validering_sti = To_do_rod/'build/verification'
    kerne_hash = hash_fil(To_do_rod/'build/kernel8.img')
    기록들 = {}
    for Navn in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        relativ_sti = 'report.json' if Navn == 'boot' else Navn+'/report.json'
        data = json.loads((validering_sti/relativ_sti).read_text())
        if not data.get('passed') or data.get('kernel_sha256') != kerne_hash:
            raise SystemExit('aktuel_vare 커널에 대한 성공 기록이 필요합니다: '+relativ_sti)
        기록들[Navn] = {'passed': True, 'report': relativ_sti}
    check_navn = json.loads((validering_sti/'naming/report.json').read_text())
    if not check_navn['passed'] or not check_navn['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for Sti, 기대값 in check_navn['c_source_sha256'].items():
        if hash_fil(To_do_rod/Sti) != 기대값: raise SystemExit('명명 검사 BACK_VÆRDI 바뀐 C KILDE: '+Sti)
    자바검사 = json.loads((validering_sti/'jvm/report.json').read_text())
    직접화면 = json.loads((validering_sti/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('Dansk 직접 skærmbillede Udfør_kommando 시험 필요')
    check_byte_VÆRDI = json.loads((validering_sti/'naming/direct-bytecode.json').read_text())
    if not check_byte_VÆRDI['passed'] or check_byte_VÆRDI['jar_sha256'] != hash_fil(To_do_rod/'dist/jkoros-native-korean.jar'):
        raise SystemExit('aktuel_vare Dansk 라이브러리의 직접 호출 바이트코드 bekræfte 필요')
    check_opløsning = json.loads((validering_sti/'resolution/report.json').read_text())
    check_tilpasse_størrelse = json.loads((validering_sti/'resize/report.json').read_text())
    갱신검사 = json.loads((validering_sti/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != kerne_hash:
        raise SystemExit('aktuel_vare 커널의 부분 opdatere 시험 필요')
    for Sti, 기대값 in 갱신검사['source_sha256'].items():
        if hash_fil(To_do_rod/Sti) != 기대값: raise SystemExit('부분 opdatere 시험 BACK_VÆRDI 바뀐 KILDE: '+Sti)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('Dansk 직접 가닥과 Kør_2 indgangspunkt 시험 필요')
    예제검사 = json.loads((validering_sti/'examples/report.json').read_text())
    if sorted(check_tilpasse_størrelse['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Størrelse 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('Dansk Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(check_opløsning['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 faktisk_data skærmbillede 시험 필요')
    if 자바검사['korean_library_sha256'] != hash_fil(To_do_rod/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 BACK_VÆRDI 라이브러리가 바뀌었습니다.')
    for Navn in ('한국어통신시험','한국어예외시험'):
        if not any(post_VÆRDI_962f286b['name']==Navn and post_VÆRDI_962f286b.get('openjdk_output_equal') for post_VÆRDI_962f286b in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Navn)
    undtagelse_Liste = sorted(Sti.stem for Sti in (To_do_rod/'한국어자바/Dansk/eget').glob('*undtagelse.java'))
    undtagelse_LOG = (validering_sti/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Navn in undtagelse_Liste:
        if '\n'+Navn+'\n' not in undtagelse_LOG: raise SystemExit('undtagelse generere·잡기·설명 시험 필요: '+Navn)
    명세 = json.loads((To_do_rod/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != hash_fil(To_do_rod/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('distribution_VÆRDI Image_VÆRDI hash_fil 불일치')
    with zipfile.ZipFile(str(To_do_rod/'dist/jkoros-native-rpi4-boot.zip')) as bundt:
        if hashlib.sha256(bundt.read('kernel8.img')).hexdigest() != kerne_hash:
            raise SystemExit('부팅 ZIP kerne_VÆRDI 불일치')
        부팅설정 = bundt.read('config.txt')
        for Navn, Størrelse in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Navn+'='+str(Størrelse) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP skærmbillede Indstillinger 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(To_do_rod/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(To_do_rod/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if hash_fil(복사본) != kerne_hash: raise SystemExit('SD Image_VÆRDI kerne_VÆRDI 불일치')
        kopiere_Indstillinger = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(To_do_rod/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(kopiere_Indstillinger)])
        if kopiere_Indstillinger.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP skærmbillede Indstillinger 불일치')
    LOG_post = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': kerne_hash,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': undtagelse_Liste, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(check_opløsning['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Navn:hash_fil(To_do_rod/'dist'/Navn) for Navn in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (validering_sti/'native-runtime-summary.json').write_text(json.dumps(LOG_post,ensure_ascii=False,indent=2)+'\n')
    print('PASS: aktuel_vare 커널의',len(기록들),'개 통합 시험 LOG_post, Dansk undtagelse',len(undtagelse_Liste),'Hold_Definition, SD Image_VÆRDI·ZIP 일치')

if __name__ == '__main__': Kør_2()
