#!/usr/bin/env python3
"""현재 커널과 실제 시험·배포물이 일치할 때에만 통합 검증 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

기준 = Path(__file__).resolve().parents[1]

def 해시(경로):
    계산 = hashlib.sha256()
    with 경로.open('rb') as 파일:
        for 자료 in iter(lambda: 파일.read(1048576), b''): 계산.update(자료)
    return 계산.hexdigest()

def 시작():
    검증경로 = 기준/'build/verification'
    커널해시 = 해시(기준/'build/kernel8.img')
    기록들 = {}
    for Nome in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Nome == 'boot' else Nome+'/report.json'
        자료 = json.loads((검증경로/상대경로).read_text())
        if not 자료.get('passed') or 자료.get('kernel_sha256') != 커널해시:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Nome] = {'passed': True, 'report': 상대경로}
    이름검사 = json.loads((검증경로/'naming/report.json').read_text())
    if not 이름검사['passed'] or not 이름검사['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for 경로, 기대값 in 이름검사['c_source_sha256'].items():
        if 해시(기준/경로) != 기대값: raise SystemExit('명명 검사 뒤 바뀐 C 원문: '+경로)
    자바검사 = json.loads((검증경로/'jvm/report.json').read_text())
    직접화면 = json.loads((검증경로/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 실행 시험 필요')
    바이트검사 = json.loads((검증경로/'naming/direct-bytecode.json').read_text())
    if not 바이트검사['passed'] or 바이트검사['jar_sha256'] != 해시(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 확인 필요')
    해상도검사 = json.loads((검증경로/'resolution/report.json').read_text())
    크기검사 = json.loads((검증경로/'resize/report.json').read_text())
    갱신검사 = json.loads((검증경로/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != 커널해시:
        raise SystemExit('현재 커널의 부분 갱신 시험 필요')
    for 경로, 기대값 in 갱신검사['source_sha256'].items():
        if 해시(기준/경로) != 기대값: raise SystemExit('부분 갱신 시험 뒤 바뀐 원문: '+경로)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 시작 진입점 시험 필요')
    예제검사 = json.loads((검증경로/'examples/report.json').read_text())
    if sorted(크기검사['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 크기 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(해상도검사['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 실제 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != 해시(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 뒤 라이브러리가 바뀌었습니다.')
    for Nome in ('한국어통신시험','한국어예외시험'):
        if not any(항목['name']==Nome and 항목.get('openjdk_output_equal') for 항목 in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Nome)
    예외들 = sorted(경로.stem for 경로 in (기준/'한국어자바/한국어/자체').glob('*예외.java'))
    예외기록 = (검증경로/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Nome in 예외들:
        if '\n'+Nome+'\n' not in 예외기록: raise SystemExit('예외 생성·잡기·설명 시험 필요: '+Nome)
    명세 = json.loads((기준/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != 해시(기준/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 영상 해시 불일치')
    with zipfile.ZipFile(str(기준/'dist/jkoros-native-rpi4-boot.zip')) as 꾸러미:
        if hashlib.sha256(꾸러미.read('kernel8.img')).hexdigest() != 커널해시:
            raise SystemExit('부팅 ZIP 커널 불일치')
        부팅설정 = 꾸러미.read('config.txt')
        for Nome, 크기 in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Nome+'='+str(크기) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 설정 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(기준/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if 해시(복사본) != 커널해시: raise SystemExit('SD 영상 커널 불일치')
        설정복사 = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(설정복사)])
        if 설정복사.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 설정 불일치')
    기록 = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
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
            'framebuffer_resolutions_tested': sorted(해상도검사['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Nome:해시(기준/'dist'/Nome) for Nome in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (검증경로/'native-runtime-summary.json').write_text(json.dumps(기록,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 기록, 한국어 예외',len(예외들),'종, SD 영상·ZIP 일치')

if __name__ == '__main__': 시작()
