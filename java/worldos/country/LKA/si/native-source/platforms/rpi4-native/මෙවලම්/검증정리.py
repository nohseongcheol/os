#!/usr/bin/env python3
"""현재 커널과 තථ්_ය_දත්ත 시험·배포물이 일치할 때에만 통합 වලංගු_කරන්න 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

기준 = Path(__file__).resolve().parents[1]

def හෑෂ්_ගොනුව(මාර්_ගය):
    계산 = hashlib.sha256()
    with මාර්_ගය.open('rb') as ගොනු:
        for දත්ත in iter(lambda: ගොනු.read(1048576), b''): 계산.update(දත්ත)
    return 계산.hexdigest()

def ක්_රියාත්මක_කරන්න_2():
    වලංගුකරණය_පෙත = 기준/'build/verification'
    කර්නලය_හෑෂ් = හෑෂ්_ගොනුව(기준/'build/kernel8.img')
    기록들 = {}
    for නම in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if නම == 'boot' else නම+'/report.json'
        දත්ත = json.loads((වලංගුකරණය_පෙත/상대경로).read_text())
        if not දත්ත.get('passed') or දත්ත.get('kernel_sha256') != කර්නලය_හෑෂ්:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[නම] = {'passed': True, 'report': 상대경로}
    චෙක්පත_නම = json.loads((වලංගුකරණය_පෙත/'naming/report.json').read_text())
    if not චෙක්පත_නම['passed'] or not චෙක්පත_නම['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for මාර්_ගය, 기대값 in චෙක්පත_නම['c_source_sha256'].items():
        if හෑෂ්_ගොනුව(기준/මාර්_ගය) != 기대값: raise SystemExit('명명 검사 ආපසු_අගය 바뀐 C මූලය: '+මාර්_ගය)
    자바검사 = json.loads((වලංගුකරණය_පෙත/'jvm/report.json').read_text())
    직접화면 = json.loads((වලංගුකරණය_පෙත/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 ක්_රියාත්මක_කරන්න_විධානය 시험 필요')
    චෙක්පත_බයිටය_අගය = json.loads((වලංගුකරණය_පෙත/'naming/direct-bytecode.json').read_text())
    if not චෙක්පත_බයිටය_අගය['passed'] or චෙක්පත_බයිටය_අගය['jar_sha256'] != හෑෂ්_ගොනුව(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 තහවුරු_කරන්න 필요')
    චෙක්පත_විභේදනය = json.loads((වලංගුකරණය_පෙත/'resolution/report.json').read_text())
    චෙක්පත_ප්_රමාණනය = json.loads((වලංගුකරණය_පෙත/'resize/report.json').read_text())
    갱신검사 = json.loads((වලංගුකරණය_පෙත/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != කර්නලය_හෑෂ්:
        raise SystemExit('현재 커널의 부분 නැවුම්_කරන්න 시험 필요')
    for මාර්_ගය, 기대값 in 갱신검사['source_sha256'].items():
        if හෑෂ්_ගොනුව(기준/මාර්_ගය) != 기대값: raise SystemExit('부분 නැවුම්_කරන්න 시험 ආපසු_අගය 바뀐 මූලය: '+මාර්_ගය)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 ක්_රියාත්මක_කරන්න_2 පිවිසුම_ලකුණ 시험 필요')
    예제검사 = json.loads((වලංගුකරණය_පෙත/'examples/report.json').read_text())
    if sorted(චෙක්පත_ප්_රමාණනය['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 ප්_රමාණය 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(චෙක්පත_විභේදනය['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 තථ්_ය_දත්ත 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != හෑෂ්_ගොනුව(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 ආපසු_අගය 라이브러리가 바뀌었습니다.')
    for නම in ('한국어통신시험','한국어예외시험'):
        if not any(පිවිසුම_අගය['name']==නම and පිවිසුම_අගය.get('openjdk_output_equal') for පිවිසුම_අගය in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+නම)
    예외들 = sorted(මාර්_ගය.stem for මාර්_ගය in (기준/'한국어자바/한국어/자체').glob('*예외.java'))
    예외기록 = (වලංගුකරණය_පෙත/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for නම in 예외들:
        if '\n'+නම+'\n' not in 예외기록: raise SystemExit('예외 생성·잡기·설명 시험 필요: '+නම)
    명세 = json.loads((기준/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != හෑෂ්_ගොනුව(기준/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 අනුරුව_අගය හෑෂ්_ගොනුව 불일치')
    with zipfile.ZipFile(str(기준/'dist/jkoros-native-rpi4-boot.zip')) as පොදිය:
        if hashlib.sha256(පොදිය.read('kernel8.img')).hexdigest() != කර්නලය_හෑෂ්:
            raise SystemExit('부팅 ZIP කර්නලය_අගය 불일치')
        부팅설정 = පොදිය.read('config.txt')
        for නම, ප්_රමාණය in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+නම+'='+str(ප්_රමාණය) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 සැකසුම් 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(기준/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if හෑෂ්_ගොනුව(복사본) != කර්නලය_හෑෂ්: raise SystemExit('SD අනුරුව_අගය කර්නලය_අගය 불일치')
        ප්_රස්තාව_පසුතල = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(ප්_රස්තාව_පසුතල)])
        if ප්_රස්තාව_පසුතල.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 සැකසුම් 불일치')
    ලොගය_පේළිය = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': කර්නලය_හෑෂ්,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(චෙක්පත_විභේදනය['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {නම:හෑෂ්_ගොනුව(기준/'dist'/නම) for නම in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (වලංගුකරණය_පෙත/'native-runtime-summary.json').write_text(json.dumps(ලොගය_පේළිය,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 ලොගය_පේළිය, 한국어 예외',len(예외들),'පන්තිය_නිර්වචනය, SD අනුරුව_අගය·ZIP 일치')

if __name__ == '__main__': ක්_රියාත්මක_කරන්න_2()
