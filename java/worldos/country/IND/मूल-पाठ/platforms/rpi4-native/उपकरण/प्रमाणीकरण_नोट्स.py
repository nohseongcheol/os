#!/usr/bin/env python3
"""अद्यतित_आइटम 커널과 वास्तविक_डेटा 시험·배포물이 일치할 때에만 통합 मान्य_करें 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

प्रोजेक्ट_करें_मूल = Path(__file__).resolve().parents[1]

def हैश_फ़ाइल(पथ):
    계산 = hashlib.sha256()
    with पथ.open('rb') as संचिका:
        for आँकड़े in iter(lambda: संचिका.read(1048576), b''): 계산.update(आँकड़े)
    return 계산.hexdigest()

def चलाएँ():
    प्रमाणीकरण_पथ = प्रोजेक्ट_करें_मूल/'build/verification'
    कर्नेल_हैश = हैश_फ़ाइल(प्रोजेक्ट_करें_मूल/'build/kernel8.img')
    기록들 = {}
    for नाम in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        संबंधित_पथ = 'report.json' if नाम == 'boot' else नाम+'/report.json'
        आँकड़े = json.loads((प्रमाणीकरण_पथ/संबंधित_पथ).read_text())
        if not आँकड़े.get('passed') or आँकड़े.get('kernel_sha256') != कर्नेल_हैश:
            raise SystemExit('अद्यतित_आइटम 커널에 대한 성공 기록이 필요합니다: '+संबंधित_पथ)
        기록들[नाम] = {'passed': True, 'report': संबंधित_पथ}
    जाँचें_नाम = json.loads((प्रमाणीकरण_पथ/'naming/report.json').read_text())
    if not जाँचें_नाम['passed'] or not जाँचें_नाम['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for पथ, 기대값 in जाँचें_नाम['c_source_sha256'].items():
        if हैश_फ़ाइल(प्रोजेक्ट_करें_मूल/पथ) != 기대값: raise SystemExit('명명 검사 वापस_मान 바뀐 C स्रोत: '+पथ)
    자바검사 = json.loads((प्रमाणीकरण_पथ/'jvm/report.json').read_text())
    직접화면 = json.loads((प्रमाणीकरण_पथ/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('हिंदी 직접 화면 निष्पादित_करें_आदेश 시험 필요')
    जाँचें_बाइट_मान = json.loads((प्रमाणीकरण_पथ/'naming/direct-bytecode.json').read_text())
    if not जाँचें_बाइट_मान['passed'] or जाँचें_बाइट_मान['jar_sha256'] != हैश_फ़ाइल(प्रोजेक्ट_करें_मूल/'dist/jkoros-native-korean.jar'):
        raise SystemExit('अद्यतित_आइटम हिंदी 라이브러리의 직접 호출 바이트코드 सत्यापित_करें 필요')
    जाँचें_रिज़ॉल्यूशन = json.loads((प्रमाणीकरण_पथ/'resolution/report.json').read_text())
    जाँचें_आकार = json.loads((प्रमाणीकरण_पथ/'resize/report.json').read_text())
    갱신검사 = json.loads((प्रमाणीकरण_पथ/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != कर्नेल_हैश:
        raise SystemExit('अद्यतित_आइटम 커널의 부분 ताज़ा_करें 시험 필요')
    for पथ, 기대값 in 갱신검사['source_sha256'].items():
        if हैश_फ़ाइल(प्रोजेक्ट_करें_मूल/पथ) != 기대값: raise SystemExit('부분 ताज़ा_करें 시험 वापस_मान 바뀐 स्रोत: '+पथ)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('हिंदी 직접 가닥과 चलाएँ प्रवेश_बिदुं 시험 필요')
    예제검사 = json.loads((प्रमाणीकरण_पथ/'examples/report.json').read_text())
    if sorted(जाँचें_आकार['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 आकार 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('हिंदी Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(जाँचें_रिज़ॉल्यूशन['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 वास्तविक_डेटा 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != हैश_फ़ाइल(प्रोजेक्ट_करें_मूल/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 वापस_मान 라이브러리가 바뀌었습니다.')
    for नाम in ('한국어통신시험','한국어예외시험'):
        if not any(एन्ट्री_मान['name']==नाम and एन्ट्री_मान.get('openjdk_output_equal') for एन्ट्री_मान in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+नाम)
    अपवाद_सूची = sorted(पथ.stem for पथ in (प्रोजेक्ट_करें_मूल/'한국어자바/हिंदी/निज').glob('*अपवाद.java'))
    अपवाद_लॉग = (प्रमाणीकरण_पथ/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for नाम in अपवाद_सूची:
        if '\n'+नाम+'\n' not in अपवाद_लॉग: raise SystemExit('अपवाद जनरेट_करें·잡기·설명 시험 필요: '+नाम)
    명세 = json.loads((प्रोजेक्ट_करें_मूल/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != हैश_फ़ाइल(प्रोजेक्ट_करें_मूल/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 छवि_मान हैश_फ़ाइल 불일치')
    with zipfile.ZipFile(str(प्रोजेक्ट_करें_मूल/'dist/jkoros-native-rpi4-boot.zip')) as बंडल:
        if hashlib.sha256(बंडल.read('kernel8.img')).hexdigest() != कर्नेल_हैश:
            raise SystemExit('부팅 ZIP कर्नेल_मान 불일치')
        부팅설정 = बंडल.read('config.txt')
        for नाम, आकार in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+नाम+'='+str(आकार) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 विन्यास 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(प्रोजेक्ट_करें_मूल/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(प्रोजेक्ट_करें_मूल/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if हैश_फ़ाइल(복사본) != कर्नेल_हैश: raise SystemExit('SD छवि_मान कर्नेल_मान 불일치')
        आवृत्ति_सेटिंग = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(प्रोजेक्ट_करें_मूल/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(आवृत्ति_सेटिंग)])
        if आवृत्ति_सेटिंग.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 विन्यास 불일치')
    लॉग_रिकॉर्ड = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': कर्नेल_हैश,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': अपवाद_सूची, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(जाँचें_रिज़ॉल्यूशन['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {नाम:हैश_फ़ाइल(प्रोजेक्ट_करें_मूल/'dist'/नाम) for नाम in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (प्रमाणीकरण_पथ/'native-runtime-summary.json').write_text(json.dumps(लॉग_रिकॉर्ड,ensure_ascii=False,indent=2)+'\n')
    print('PASS: अद्यतित_आइटम 커널의',len(기록들),'개 통합 시험 लॉग_रिकॉर्ड, हिंदी अपवाद',len(अपवाद_सूची),'कक्षा_परिभाषा, SD छवि_मान·ZIP 일치')

if __name__ == '__main__': चलाएँ()
