#!/usr/bin/env python3
"""현재 커널과 werklik_data 시험·배포물이 일치할 때에만 통합 valideer 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

Project_wortel = Path(__file__).resolve().parents[1]

def huts_lêer(Pad):
    계산 = hashlib.sha256()
    with Pad.open('rb') as Lêer:
        for data in iter(lambda: Lêer.read(1048576), b''): 계산.update(data)
    return 계산.hexdigest()

def Loop():
    validering_pad = Project_wortel/'build/verification'
    kern_huts = huts_lêer(Project_wortel/'build/kernel8.img')
    기록들 = {}
    for Naam in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Naam == 'boot' else Naam+'/report.json'
        data = json.loads((validering_pad/상대경로).read_text())
        if not data.get('passed') or data.get('kernel_sha256') != kern_huts:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Naam] = {'passed': True, 'report': 상대경로}
    tjek_naam = json.loads((validering_pad/'naming/report.json').read_text())
    if not tjek_naam['passed'] or not tjek_naam['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for Pad, 기대값 in tjek_naam['c_source_sha256'].items():
        if huts_lêer(Project_wortel/Pad) != 기대값: raise SystemExit('명명 검사 TERUG_VALUE 바뀐 C Bron: '+Pad)
    자바검사 = json.loads((validering_pad/'jvm/report.json').read_text())
    직접화면 = json.loads((validering_pad/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 uitvoer_bevel 시험 필요')
    tjek_greep_VALUE = json.loads((validering_pad/'naming/direct-bytecode.json').read_text())
    if not tjek_greep_VALUE['passed'] or tjek_greep_VALUE['jar_sha256'] != huts_lêer(Project_wortel/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 verifieer 필요')
    tjek_resolusie = json.loads((validering_pad/'resolution/report.json').read_text())
    tjek_verstel = json.loads((validering_pad/'resize/report.json').read_text())
    갱신검사 = json.loads((validering_pad/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != kern_huts:
        raise SystemExit('현재 커널의 부분 verfris 시험 필요')
    for Pad, 기대값 in 갱신검사['source_sha256'].items():
        if huts_lêer(Project_wortel/Pad) != 기대값: raise SystemExit('부분 verfris 시험 TERUG_VALUE 바뀐 Bron: '+Pad)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 Loop inskrywing_p 시험 필요')
    예제검사 = json.loads((validering_pad/'examples/report.json').read_text())
    if sorted(tjek_verstel['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Grootte 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(tjek_resolusie['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 werklik_data 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != huts_lêer(Project_wortel/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 TERUG_VALUE 라이브러리가 바뀌었습니다.')
    for Naam in ('한국어통신시험','한국어예외시험'):
        if not any(inskrywing_VALUE['name']==Naam and inskrywing_VALUE.get('openjdk_output_equal') for inskrywing_VALUE in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Naam)
    uitsondering_Lys = sorted(Pad.stem for Pad in (Project_wortel/'한국어자바/한국어/자체').glob('*uitsondering.java'))
    uitsondering_LOG = (validering_pad/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Naam in uitsondering_Lys:
        if '\n'+Naam+'\n' not in uitsondering_LOG: raise SystemExit('uitsondering genereer·잡기·설명 시험 필요: '+Naam)
    명세 = json.loads((Project_wortel/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != huts_lêer(Project_wortel/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 foto_VALUE huts_lêer 불일치')
    with zipfile.ZipFile(str(Project_wortel/'dist/jkoros-native-rpi4-boot.zip')) as bondel:
        if hashlib.sha256(bondel.read('kernel8.img')).hexdigest() != kern_huts:
            raise SystemExit('부팅 ZIP kern_VALUE 불일치')
        부팅설정 = bondel.read('config.txt')
        for Naam, Grootte in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Naam+'='+str(Grootte) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Instellings 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(Project_wortel/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(Project_wortel/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if huts_lêer(복사본) != kern_huts: raise SystemExit('SD foto_VALUE kern_VALUE 불일치')
        geval_Instellings = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(Project_wortel/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(geval_Instellings)])
        if geval_Instellings.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Instellings 불일치')
    LOG_ry = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': kern_huts,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': uitsondering_Lys, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(tjek_resolusie['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Naam:huts_lêer(Project_wortel/'dist'/Naam) for Naam in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (validering_pad/'native-runtime-summary.json').write_text(json.dumps(LOG_ry,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 LOG_ry, 한국어 uitsondering',len(uitsondering_Lys),'Klas_Definisie, SD foto_VALUE·ZIP 일치')

if __name__ == '__main__': Loop()
