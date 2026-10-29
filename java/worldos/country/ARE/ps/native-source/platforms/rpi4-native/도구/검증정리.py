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

def 해시(يونلور):
    계산 = hashlib.sha256()
    with يونلور.open('rb') as دوتنه:
        for اومتوک in iter(lambda: دوتنه.read(1048576), b''): 계산.update(اومتوک)
    return 계산.hexdigest()

def ځغلول():
    باورکړن_يونلور = 기준/'build/verification'
    커널해시 = 해시(기준/'build/kernel8.img')
    기록들 = {}
    for نوم in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if نوم == 'boot' else نوم+'/report.json'
        اومتوک = json.loads((باورکړن_يونلور/상대경로).read_text())
        if not اومتوک.get('passed') or اومتوک.get('kernel_sha256') != 커널해시:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[نوم] = {'passed': True, 'report': 상대경로}
    이름검사 = json.loads((باورکړن_يونلور/'naming/report.json').read_text())
    if not 이름검사['passed'] or not 이름검사['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for يونلور, 기대값 in 이름검사['c_source_sha256'].items():
        if 해시(기준/يونلور) != 기대값: raise SystemExit('명명 검사 뒤 바뀐 C سرچينه: '+يونلور)
    자바검사 = json.loads((باورکړن_يونلور/'jvm/report.json').read_text())
    직접화면 = json.loads((باورکړن_يونلور/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 실행 시험 필요')
    کتل_بايټ_ارزښت = json.loads((باورکړن_يونلور/'naming/direct-bytecode.json').read_text())
    if not کتل_بايټ_ارزښت['passed'] or کتل_بايټ_ارزښت['jar_sha256'] != 해시(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 확인 필요')
    کتل_ژورليد = json.loads((باورکړن_يونلور/'resolution/report.json').read_text())
    크기검사 = json.loads((باورکړن_يونلور/'resize/report.json').read_text())
    갱신검사 = json.loads((باورکړن_يونلور/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != 커널해시:
        raise SystemExit('현재 커널의 부분 تاندول 시험 필요')
    for يونلور, 기대값 in 갱신검사['source_sha256'].items():
        if 해시(기준/يونلور) != 기대값: raise SystemExit('부분 تاندول 시험 뒤 바뀐 سرچينه: '+يونلور)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 ځغلول ننوت_ټکى 시험 필요')
    예제검사 = json.loads((باورکړن_يونلور/'examples/report.json').read_text())
    if sorted(크기검사['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 کچ 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(کتل_ژورليد['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 실제 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != 해시(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 뒤 라이브러리가 바뀌었습니다.')
    for نوم in ('한국어통신시험','한국어예외시험'):
        if not any(ننوت_ارزښت['name']==نوم and ننوت_ارزښت.get('openjdk_output_equal') for ننوت_ارزښت in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+نوم)
    예외들 = sorted(يونلور.stem for يونلور in (기준/'한국어자바/한국어/자체').glob('*예외.java'))
    예외기록 = (باورکړن_يونلور/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for نوم in 예외들:
        if '\n'+نوم+'\n' not in 예외기록: raise SystemExit('예외 생성·잡기·설명 시험 필요: '+نوم)
    명세 = json.loads((기준/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != 해시(기준/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 انځور_ارزښت 해시 불일치')
    with zipfile.ZipFile(str(기준/'dist/jkoros-native-rpi4-boot.zip')) as 꾸러미:
        if hashlib.sha256(꾸러미.read('kernel8.img')).hexdigest() != 커널해시:
            raise SystemExit('부팅 ZIP نوغی_ارزښت 불일치')
        부팅설정 = 꾸러미.read('config.txt')
        for نوم, کچ in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+نوم+'='+str(کچ) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 امستنې 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(기준/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if 해시(복사본) != 커널해시: raise SystemExit('SD انځور_ارزښت نوغی_ارزښت 불일치')
        설정복사 = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(설정복사)])
        if 설정복사.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 امستنې 불일치')
    خبرال_کیل = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
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
            'framebuffer_resolutions_tested': sorted(کتل_ژورليد['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {نوم:해시(기준/'dist'/نوم) for نوم in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (باورکړن_يونلور/'native-runtime-summary.json').write_text(json.dumps(خبرال_کیل,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 خبرال_کیل, 한국어 예외',len(예외들),'종, SD انځور_ارزښت·ZIP 일치')

if __name__ == '__main__': ځغلول()
