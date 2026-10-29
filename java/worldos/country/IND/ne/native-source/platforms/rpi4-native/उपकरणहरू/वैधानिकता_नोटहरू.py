#!/usr/bin/env python3
"""현재 커널과 वास्तविक_लगत 시험·배포물이 일치할 때에만 통합 वैध_गर्नुहोस् 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

परियोजना_रूट = Path(__file__).resolve().parents[1]

def ह्यास_फाइल(मार्ग):
    계산 = hashlib.sha256()
    with मार्ग.open('rb') as फाइल:
        for लगत in iter(lambda: फाइल.read(1048576), b''): 계산.update(लगत)
    return 계산.hexdigest()

def चलाउनुहोस्():
    वैधानिकता_बाटो = परियोजना_रूट/'build/verification'
    कर्णेल_ह्यास = ह्यास_फाइल(परियोजना_रूट/'build/kernel8.img')
    기록들 = {}
    for नाम in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if नाम == 'boot' else नाम+'/report.json'
        लगत = json.loads((वैधानिकता_बाटो/상대경로).read_text())
        if not लगत.get('passed') or लगत.get('kernel_sha256') != कर्णेल_ह्यास:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[नाम] = {'passed': True, 'report': 상대경로}
    चेक_नाम = json.loads((वैधानिकता_बाटो/'naming/report.json').read_text())
    if not चेक_नाम['passed'] or not चेक_नाम['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for मार्ग, 기대값 in चेक_नाम['c_source_sha256'].items():
        if ह्यास_फाइल(परियोजना_रूट/मार्ग) != 기대값: raise SystemExit('명명 검사 पछाडि_मान 바뀐 C स्रोत: '+मार्ग)
    자바검사 = json.loads((वैधानिकता_बाटो/'jvm/report.json').read_text())
    직접화면 = json.loads((वैधानिकता_बाटो/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('नेपाली 직접 화면 कार्यान्वयन_गर्नुहोस्_आदेश 시험 필요')
    चेक_बाइट_मान = json.loads((वैधानिकता_बाटो/'naming/direct-bytecode.json').read_text())
    if not चेक_बाइट_मान['passed'] or चेक_बाइट_मान['jar_sha256'] != ह्यास_फाइल(परियोजना_रूट/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 नेपाली 라이브러리의 직접 호출 바이트코드 रुजू_गर्नुहोस् 필요')
    चेक_रिजोल्यूशन = json.loads((वैधानिकता_बाटो/'resolution/report.json').read_text())
    चेक_साइज = json.loads((वैधानिकता_बाटो/'resize/report.json').read_text())
    갱신검사 = json.loads((वैधानिकता_बाटो/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != कर्णेल_ह्यास:
        raise SystemExit('현재 커널의 부분 ताजा_गर्नुहोस् 시험 필요')
    for मार्ग, 기대값 in 갱신검사['source_sha256'].items():
        if ह्यास_फाइल(परियोजना_रूट/मार्ग) != 기대값: raise SystemExit('부분 ताजा_गर्नुहोस् 시험 पछाडि_मान 바뀐 स्रोत: '+मार्ग)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('नेपाली 직접 가닥과 चलाउनुहोस् प्रविष्टि_अंक 시험 필요')
    예제검사 = json.loads((वैधानिकता_बाटो/'examples/report.json').read_text())
    if sorted(चेक_साइज['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 आकार 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('नेपाली Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(चेक_रिजोल्यूशन['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 वास्तविक_लगत 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != ह्यास_फाइल(परियोजना_रूट/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 पछाडि_मान 라이브러리가 바뀌었습니다.')
    for नाम in ('한국어통신시험','한국어예외시험'):
        if not any(प्रविष्टि_मान['name']==नाम and प्रविष्टि_मान.get('openjdk_output_equal') for प्रविष्टि_मान in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+नाम)
    예외들 = sorted(मार्ग.stem for मार्ग in (परियोजना_रूट/'한국어자바/नेपाली/निज').glob('*예외.java'))
    예외기록 = (वैधानिकता_बाटो/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for नाम in 예외들:
        if '\n'+नाम+'\n' not in 예외기록: raise SystemExit('예외 सिर्जना_गर्नुहोस्·잡기·설명 시험 필요: '+नाम)
    명세 = json.loads((परियोजना_रूट/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != ह्यास_फाइल(परियोजना_रूट/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 छवि_मान ह्यास_फाइल 불일치')
    with zipfile.ZipFile(str(परियोजना_रूट/'dist/jkoros-native-rpi4-boot.zip')) as पोको:
        if hashlib.sha256(पोको.read('kernel8.img')).hexdigest() != कर्णेल_ह्यास:
            raise SystemExit('부팅 ZIP कर्णेल_मान 불일치')
        부팅설정 = पोको.read('config.txt')
        for नाम, आकार in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+नाम+'='+str(आकार) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 सेटिङ 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(परियोजना_रूट/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(परियोजना_रूट/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if ह्यास_फाइल(복사본) != कर्णेल_ह्यास: raise SystemExit('SD छवि_मान कर्णेल_मान 불일치')
        उद्धरण_सेटिङहरू = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(परियोजना_रूट/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(उद्धरण_सेटिङहरू)])
        if उद्धरण_सेटिङहरू.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 सेटिङ 불일치')
    लग_रेकर्ड = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': कर्णेल_ह्यास,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(चेक_रिजोल्यूशन['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {नाम:ह्यास_फाइल(परियोजना_रूट/'dist'/नाम) for नाम in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (वैधानिकता_बाटो/'native-runtime-summary.json').write_text(json.dumps(लग_रेकर्ड,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 लग_रेकर्ड, नेपाली 예외',len(예외들),'वर्ग_परिभाषा, SD छवि_मान·ZIP 일치')

if __name__ == '__main__': चलाउनुहोस्()
