#!/usr/bin/env python3
"""सध्याचे_आयटम 커널과 वास्तविक_डेटा चाचण्या·배포물이 일치할 때에만 통합 प्रमाणित 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

प्रोजेक्ट_मूळ = Path(__file__).resolve().parents[1]

def हॅश_संचिका(मार्ग):
    गणना = hashlib.sha256()
    with मार्ग.open('rb') as फाइल:
        for डेटा in iter(lambda: फाइल.read(1048576), b''): गणना.update(डेटा)
    return गणना.hexdigest()

def सुरू_करा():
    पडताळणी_पथ = प्रोजेक्ट_मूळ/'build/verification'
    गाभा_हॅश = हॅश_संचिका(प्रोजेक्ट_मूळ/'build/kernel8.img')
    लॉग_नोंदी = {}
    for नाव in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        सापेक्ष_पथ = 'report.json' if नाव == 'boot' else नाव+'/report.json'
        डेटा = json.loads((पडताळणी_पथ/सापेक्ष_पथ).read_text())
        if not डेटा.get('passed') or डेटा.get('kernel_sha256') != गाभा_हॅश:
            raise SystemExit('सध्याचे_आयटम 커널에 대한 यश_मूल्य 기록이 필요합니다: '+सापेक्ष_पथ)
        लॉग_नोंदी[नाव] = {'passed': True, 'report': सापेक्ष_पथ}
    नाव_तपासा = json.loads((पडताळणी_पथ/'naming/report.json').read_text())
    if not नाव_तपासा['passed'] or not नाव_तपासा['c_semantic_checked']: raise SystemExit('C 선언을 포함한 नामकरण पडताळण्या आवश्यक_मूल्य')
    for मार्ग, अपेक्षित_मूल्य in नाव_तपासा['c_source_sha256'].items():
        if हॅश_संचिका(प्रोजेक्ट_मूळ/मार्ग) != अपेक्षित_मूल्य: raise SystemExit('नामकरण पडताळण्या मागे_मूल्य 바뀐 C स्रोत: '+मार्ग)
    जावा_तपासा = json.loads((पडताळणी_पथ/'jvm/report.json').read_text())
    थेट_पडदा = json.loads((पडताळणी_पथ/'swing/report.json').read_text())
    if not थेट_पडदा.get('direct_korean_gui'): raise SystemExit('मराठी 직접 पडदा आज्ञा_कार्यवाही_करा चाचण्या आवश्यक_मूल्य')
    बाइट_मूल्य_तपासा = json.loads((पडताळणी_पथ/'naming/direct-bytecode.json').read_text())
    if not बाइट_मूल्य_तपासा['passed'] or बाइट_मूल्य_तपासा['jar_sha256'] != हॅश_संचिका(प्रोजेक्ट_मूळ/'dist/jkoros-native-korean.jar'):
        raise SystemExit('सध्याचे_आयटम मराठी 라이브러리의 직접 आवाहन बाइटसंहिता पडताळा आवश्यक_मूल्य')
    बिंदूघनता_तपासा = json.loads((पडताळणी_पथ/'resolution/report.json').read_text())
    आकारा_तपासा = json.loads((पडताळणी_पथ/'resize/report.json').read_text())
    साठी_अद्ययावते_तपासा = json.loads((पडताळणी_पथ/'redraw/report.json').read_text())
    if not साठी_अद्ययावते_तपासा['passed'] or साठी_अद्ययावते_तपासा['kernel_sha256'] != गाभा_हॅश:
        raise SystemExit('सध्याचे_आयटम 커널의 उपभाग_मूल्य ताजे_करा चाचण्या आवश्यक_मूल्य')
    for मार्ग, अपेक्षित_मूल्य in साठी_अद्ययावते_तपासा['source_sha256'].items():
        if हॅश_संचिका(प्रोजेक्ट_मूळ/मार्ग) != अपेक्षित_मूल्य: raise SystemExit('उपभाग_मूल्य ताजे_करा चाचण्या मागे_मूल्य 바뀐 स्रोत: '+मार्ग)
    if not जावा_तपासा.get('direct_korean_thread_and_entry'):
        raise SystemExit('मराठी 직접 가닥과 सुरू_करा प्रविष्टी_गुण चाचण्या आवश्यक_मूल्य')
    उदाहरण_तपासा = json.loads((पडताळणी_पथ/'examples/report.json').read_text())
    if sorted(आकारा_तपासा['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 कोपरा_मूल्य आकार 조절 चाचण्या आवश्यक_मूल्य')
    if not उदाहरण_तपासा.get('swing_example_korean_input_button_label_and_close') or उदाहरण_तपासा['examples_executed'] != 13:
        raise SystemExit('मराठी Swing 창을 포함한 उदाहरणे 13개 चाचण्या आवश्यक_मूल्य')
    if sorted(बिंदूघनता_तपासा['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 वास्तविक_डेटा पडदा चाचण्या आवश्यक_मूल्य')
    if जावा_तपासा['korean_library_sha256'] != हॅश_संचिका(प्रोजेक्ट_मूळ/'dist/jkoros-native-korean.jar'):
        raise SystemExit('जावा चाचण्या मागे_मूल्य 라이브러리가 바뀌었습니다.')
    for नाव in ('कोरियन_संचारजाळे_चाचणी','कोरियन_अपवाद_चाचणी'):
        if not any(प्रविष्टी_मूल्य['name']==नाव and प्रविष्टी_मूल्य.get('openjdk_output_equal') for प्रविष्टी_मूल्य in जावा_तपासा['tests']):
            raise SystemExit('OpenJDK 대조 चाचण्या आवश्यक_मूल्य: '+नाव)
    अपवाद_यादी = sorted(मार्ग.stem for मार्ग in (प्रोजेक्ट_मूळ/'स्वकीय_जावा/मराठी/स्वकीय').glob('*अपवाद.java'))
    अपवाद_लॉग = (पडताळणी_पथ/'jvm/कोरियन_अपवाद_चाचणी.log').read_text().replace('\r\n','\n')
    for नाव in अपवाद_यादी:
        if '\n'+नाव+'\n' not in अपवाद_लॉग: raise SystemExit('अपवाद तयार_करा·잡기·वर्णन चाचण्या आवश्यक_मूल्य: '+नाव)
    विनिर्देश = json.loads((प्रोजेक्ट_मूळ/'dist/manifest.json').read_text())
    if विनिर्देश['image_sha256'] != हॅश_संचिका(प्रोजेक्ट_मूळ/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('वितरण_मूल्य चित्र_मूल्य हॅश_संचिका 불일치')
    with zipfile.ZipFile(str(प्रोजेक्ट_मूळ/'dist/jkoros-native-rpi4-boot.zip')) as बंडल:
        if hashlib.sha256(बंडल.read('kernel8.img')).hexdigest() != गाभा_हॅश:
            raise SystemExit('प्रणालीप्रारंभ ZIP गाभा_मूल्य 불일치')
        प्रणालीप्रारंभ_सेटिंग्ज = बंडल.read('config.txt')
        for नाव, आकार in zip(('width', 'height'), विनिर्देश['framebuffer_resolution']):
            if 'framebuffer_'+नाव+'='+str(आकार) not in प्रणालीप्रारंभ_सेटिंग्ज.decode().splitlines():
                raise SystemExit('प्रणालीप्रारंभ ZIP पडदा संयोजना 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(प्रोजेक्ट_मूळ/'build')) as तात्पुरते_मूल्य:
        प्रतिलिपित_मूल्य = Path(तात्पुरते_मूल्य)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(प्रोजेक्ट_मूळ/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(प्रतिलिपित_मूल्य)])
        if हॅश_संचिका(प्रतिलिपित_मूल्य) != गाभा_हॅश: raise SystemExit('SD चित्र_मूल्य गाभा_मूल्य 불일치')
        इन्स्टन्स_सेटिंग्ज = Path(तात्पुरते_मूल्य)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(प्रोजेक्ट_मूळ/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(इन्स्टन्स_सेटिंग्ज)])
        if इन्स्टन्स_सेटिंग्ज.read_bytes() != प्रणालीप्रारंभ_सेटिंग्ज: raise SystemExit('SD 영상과 ZIP पडदा संयोजना 불일치')
    लॉग_नोंद = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': गाभा_हॅश,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': लॉग_नोंदी, 'naming_report': 'naming/report.json',
            'korean_exception_classes': अपवाद_यादी, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': उदाहरण_तपासा['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(बिंदूघनता_तपासा['resolutions']),
            'sd_framebuffer_resolution': विनिर्देश['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {नाव:हॅश_संचिका(प्रोजेक्ट_मूळ/'dist'/नाव) for नाव in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (पडताळणी_पथ/'native-runtime-summary.json').write_text(json.dumps(लॉग_नोंद,ensure_ascii=False,indent=2)+'\n')
    print('PASS: सध्याचे_आयटम 커널의',len(लॉग_नोंदी),'개 통합 चाचण्या लॉग_नोंद, मराठी अपवाद',len(अपवाद_यादी),'वर्ग_व्याख्या, SD चित्र_मूल्य·ZIP आहे_समान')

if __name__ == '__main__': सुरू_करा()
