#!/usr/bin/env python3
"""현재 커널과 प्रत्यक्ष_डेटा 시험·배포물이 일치할 때에만 통합 पुनर्तपासणी_करची_5fb2b747 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

प्रॉजॅक्ट_रूट = Path(__file__).resolve().parents[1]

def हॅश_फायल(पाथ):
    계산 = hashlib.sha256()
    with पाथ.open('rb') as फायल:
        for डेटा in iter(lambda: फायल.read(1048576), b''): 계산.update(डेटा)
    return 계산.hexdigest()

def चलोवप():
    वैधताय_पाथ = प्रॉजॅक्ट_रूट/'build/verification'
    कर्नेल_हॅश = हॅश_फायल(प्रॉजॅक्ट_रूट/'build/kernel8.img')
    기록들 = {}
    for नांव in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if नांव == 'boot' else नांव+'/report.json'
        डेटा = json.loads((वैधताय_पाथ/상대경로).read_text())
        if not डेटा.get('passed') or डेटा.get('kernel_sha256') != कर्नेल_हॅश:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[नांव] = {'passed': True, 'report': 상대경로}
    तपासचें_नांव = json.loads((वैधताय_पाथ/'naming/report.json').read_text())
    if not तपासचें_नांव['passed'] or not तपासचें_नांव['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for पाथ, 기대값 in तपासचें_नांव['c_source_sha256'].items():
        if हॅश_फायल(प्रॉजॅक्ट_रूट/पाथ) != 기대값: raise SystemExit('명명 검사 फाटीं_मोल 바뀐 C स्त्रोत: '+पाथ)
    자바검사 = json.loads((वैधताय_पाथ/'jvm/report.json').read_text())
    직접화면 = json.loads((वैधताय_पाथ/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 पाळो_दिवचो_आदेश 시험 필요')
    तपासचें_बायट_मोल = json.loads((वैधताय_पाथ/'naming/direct-bytecode.json').read_text())
    if not तपासचें_बायट_मोल['passed'] or तपासचें_बायट_मोल['jar_sha256'] != हॅश_फायल(प्रॉजॅक्ट_रूट/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 पुनर्तपासणी_करची 필요')
    तपासचें_रिजोल्युशन = json.loads((वैधताय_पाथ/'resolution/report.json').read_text())
    तपासचें_आवाठ = json.loads((वैधताय_पाथ/'resize/report.json').read_text())
    갱신검사 = json.loads((वैधताय_पाथ/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != कर्नेल_हॅश:
        raise SystemExit('현재 커널의 부분 परतून_ताजें_करचें 시험 필요')
    for पाथ, 기대값 in 갱신검사['source_sha256'].items():
        if हॅश_फायल(प्रॉजॅक्ट_रूट/पाथ) != 기대값: raise SystemExit('부분 परतून_ताजें_करचें 시험 फाटीं_मोल 바뀐 स्त्रोत: '+पाथ)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 चलोवप प्रवेश_पॉयंट 시험 필요')
    예제검사 = json.loads((वैधताय_पाथ/'examples/report.json').read_text())
    if sorted(तपासचें_आवाठ['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 आवाठ 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(तपासचें_रिजोल्युशन['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 प्रत्यक्ष_डेटा 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != हॅश_फायल(प्रॉजॅक्ट_रूट/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 फाटीं_मोल 라이브러리가 바뀌었습니다.')
    for नांव in ('한국어통신시험','한국어예외시험'):
        if not any(प्रवेश_मोल['name']==नांव and प्रवेश_मोल.get('openjdk_output_equal') for प्रवेश_मोल in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+नांव)
    예외들 = sorted(पाथ.stem for पाथ in (प्रॉजॅक्ट_रूट/'한국어자바/한국어/자체').glob('*예외.java'))
    예외기록 = (वैधताय_पाथ/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for नांव in 예외들:
        if '\n'+नांव+'\n' not in 예외기록: raise SystemExit('예외 तयार_करचें·잡기·설명 시험 필요: '+नांव)
    명세 = json.loads((प्रॉजॅक्ट_रूट/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != हॅश_फायल(प्रॉजॅक्ट_रूट/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 IMAGE_मोल हॅश_फायल 불일치')
    with zipfile.ZipFile(str(प्रॉजॅक्ट_रूट/'dist/jkoros-native-rpi4-boot.zip')) as रास:
        if hashlib.sha256(रास.read('kernel8.img')).hexdigest() != कर्नेल_हॅश:
            raise SystemExit('부팅 ZIP कर्नेल_मोल 불일치')
        부팅설정 = रास.read('config.txt')
        for नांव, आवाठ in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+नांव+'='+str(आवाठ) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 मांडावळी 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(प्रॉजॅक्ट_रूट/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(प्रॉजॅक्ट_रूट/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if हॅश_फायल(복사본) != कर्नेल_हॅश: raise SystemExit('SD IMAGE_मोल कर्नेल_मोल 불일치')
        इन्सटन्स_मांडावळी = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(प्रॉजॅक्ट_रूट/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(इन्सटन्स_मांडावळी)])
        if इन्सटन्स_मांडावळी.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 मांडावळी 불일치')
    LOG_नोंद = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': कर्नेल_हॅश,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(तपासचें_रिजोल्युशन['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {नांव:हॅश_फायल(प्रॉजॅक्ट_रूट/'dist'/नांव) for नांव in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (वैधताय_पाथ/'native-runtime-summary.json').write_text(json.dumps(LOG_नोंद,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 LOG_नोंद, 한국어 예외',len(예외들),'वर्ग_परिभाशा, SD IMAGE_मोल·ZIP 일치')

if __name__ == '__main__': चलोवप()
