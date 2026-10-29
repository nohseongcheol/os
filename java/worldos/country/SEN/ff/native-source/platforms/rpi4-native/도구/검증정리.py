#!/usr/bin/env python3
"""현재 커널과 laatii_keɓe 시험·배포물이 일치할 때에만 통합 검증 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

기준 = Path(__file__).resolve().parents[1]

def 해시(laawol):
    계산 = hashlib.sha256()
    with laawol.open('rb') as fiilde:
        for keɓe in iter(lambda: fiilde.read(1048576), b''): 계산.update(keɓe)
    return 계산.hexdigest()

def huutoraade():
    teeŋtingol_laawol = 기준/'build/verification'
    커널해시 = 해시(기준/'build/kernel8.img')
    기록들 = {}
    for innde in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if innde == 'boot' else innde+'/report.json'
        keɓe = json.loads((teeŋtingol_laawol/상대경로).read_text())
        if not keɓe.get('passed') or keɓe.get('kernel_sha256') != 커널해시:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[innde] = {'passed': True, 'report': 상대경로}
    sek_innde = json.loads((teeŋtingol_laawol/'naming/report.json').read_text())
    if not sek_innde['passed'] or not sek_innde['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for laawol, 기대값 in sek_innde['c_source_sha256'].items():
        if 해시(기준/laawol) != 기대값: raise SystemExit('명명 검사 Caggal_njaru 바뀐 C sewnde: '+laawol)
    자바검사 = json.loads((teeŋtingol_laawol/'jvm/report.json').read_text())
    직접화면 = json.loads((teeŋtingol_laawol/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 실행 시험 필요')
    sek_oktee_njaru = json.loads((teeŋtingol_laawol/'naming/direct-bytecode.json').read_text())
    if not sek_oktee_njaru['passed'] or sek_oktee_njaru['jar_sha256'] != 해시(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 ƴeewtaade 필요')
    sek_laaɓtugol = json.loads((teeŋtingol_laawol/'resolution/report.json').read_text())
    sek_waylude_etannde = json.loads((teeŋtingol_laawol/'resize/report.json').read_text())
    갱신검사 = json.loads((teeŋtingol_laawol/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != 커널해시:
        raise SystemExit('현재 커널의 부분 ɓamtude 시험 필요')
    for laawol, 기대값 in 갱신검사['source_sha256'].items():
        if 해시(기준/laawol) != 기대값: raise SystemExit('부분 ɓamtude 시험 Caggal_njaru 바뀐 sewnde: '+laawol)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 huutoraade naatnugol_toɓɓere 시험 필요')
    예제검사 = json.loads((teeŋtingol_laawol/'examples/report.json').read_text())
    if sorted(sek_waylude_etannde['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 waylude_etannde 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(sek_laaɓtugol['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 laatii_keɓe 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != 해시(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 Caggal_njaru 라이브러리가 바뀌었습니다.')
    for innde in ('한국어통신시험','한국어예외시험'):
        if not any(naatnugol_njaru['name']==innde and naatnugol_njaru.get('openjdk_output_equal') for naatnugol_njaru in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+innde)
    예외들 = sorted(laawol.stem for laawol in (기준/'한국어자바/한국어/자체').glob('*예외.java'))
    예외기록 = (teeŋtingol_laawol/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for innde in 예외들:
        if '\n'+innde+'\n' not in 예외기록: raise SystemExit('예외 생성·잡기·설명 시험 필요: '+innde)
    명세 = json.loads((기준/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != 해시(기준/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 natal_njaru 해시 불일치')
    with zipfile.ZipFile(str(기준/'dist/jkoros-native-rpi4-boot.zip')) as 꾸러미:
        if hashlib.sha256(꾸러미.read('kernel8.img')).hexdigest() != 커널해시:
            raise SystemExit('부팅 ZIP aaluude_njaru 불일치')
        부팅설정 = 꾸러미.read('config.txt')
        for innde, waylude_etannde in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+innde+'='+str(waylude_etannde) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 설정 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(기준/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if 해시(복사본) != 커널해시: raise SystemExit('SD natal_njaru aaluude_njaru 불일치')
        설정복사 = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(설정복사)])
        if 설정복사.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 설정 불일치')
    suurnal_winndande = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': 커널해시,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(sek_laaɓtugol['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {innde:해시(기준/'dist'/innde) for innde in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (teeŋtingol_laawol/'native-runtime-summary.json').write_text(json.dumps(suurnal_winndande,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 suurnal_winndande, 한국어 예외',len(예외들),'종, SD natal_njaru·ZIP 일치')

if __name__ == '__main__': huutoraade()
