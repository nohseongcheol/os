#!/usr/bin/env python3
"""현재 커널과 প্রকৃত_ডাটা 시험·배포물이 일치할 때에만 통합 বৈধ_করুন 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

প্রকল্প_মূল = Path(__file__).resolve().parents[1]

def হ্যাশ_ফাইল(পথ_2):
    계산 = hashlib.sha256()
    with পথ_2.open('rb') as নথির_নাম:
        for ডাটা in iter(lambda: নথির_নাম.read(1048576), b''): 계산.update(ডাটা)
    return 계산.hexdigest()

def চালনা():
    বৈধকরণ_পথ = প্রকল্প_মূল/'build/verification'
    কারনেল_হ্যাশ = হ্যাশ_ফাইল(প্রকল্প_মূল/'build/kernel8.img')
    기록들 = {}
    for নাম in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if নাম == 'boot' else নাম+'/report.json'
        ডাটা = json.loads((বৈধকরণ_পথ/상대경로).read_text())
        if not ডাটা.get('passed') or ডাটা.get('kernel_sha256') != কারনেল_হ্যাশ:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[নাম] = {'passed': True, 'report': 상대경로}
    চেক_নাম = json.loads((বৈধকরণ_পথ/'naming/report.json').read_text())
    if not চেক_নাম['passed'] or not চেক_নাম['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for পথ_2, 기대값 in চেক_নাম['c_source_sha256'].items():
        if হ্যাশ_ফাইল(প্রকল্প_মূল/পথ_2) != 기대값: raise SystemExit('명명 검사 ফিরে_যান_মান 바뀐 C উৎস_নথি: '+পথ_2)
    자바검사 = json.loads((বৈধকরণ_পথ/'jvm/report.json').read_text())
    직접화면 = json.loads((বৈধকরণ_পথ/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('বাংলা 직접 화면 কার্যকর_করুন_আদেশ 시험 필요')
    চেক_বাইট_মান = json.loads((বৈধকরণ_পথ/'naming/direct-bytecode.json').read_text())
    if not চেক_বাইট_মান['passed'] or চেক_বাইট_মান['jar_sha256'] != হ্যাশ_ফাইল(প্রকল্প_মূল/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 বাংলা 라이브러리의 직접 호출 바이트코드 যাচাই_করা 필요')
    চেক_রেজোলিউশন = json.loads((বৈধকরণ_পথ/'resolution/report.json').read_text())
    চেক_আয়তন = json.loads((বৈধকরণ_পথ/'resize/report.json').read_text())
    갱신검사 = json.loads((বৈধকরণ_পথ/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != কারনেল_হ্যাশ:
        raise SystemExit('현재 커널의 부분 রিফ্রেশ 시험 필요')
    for পথ_2, 기대값 in 갱신검사['source_sha256'].items():
        if হ্যাশ_ফাইল(প্রকল্প_মূল/পথ_2) != 기대값: raise SystemExit('부분 রিফ্রেশ 시험 ফিরে_যান_মান 바뀐 উৎস_নথি: '+পথ_2)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('বাংলা 직접 가닥과 চালনা ভুক্তি_বিন্দু 시험 필요')
    예제검사 = json.loads((বৈধকরণ_পথ/'examples/report.json').read_text())
    if sorted(চেক_আয়তন['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 আকার 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('বাংলা Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(চেক_রেজোলিউশন['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 প্রকৃত_ডাটা 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != হ্যাশ_ফাইল(প্রকল্প_মূল/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 ফিরে_যান_মান 라이브러리가 바뀌었습니다.')
    for নাম in ('한국어통신시험','한국어예외시험'):
        if not any(ভুক্তি_মান['name']==নাম and ভুক্তি_মান.get('openjdk_output_equal') for ভুক্তি_মান in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+নাম)
    ব্যতিক্রম_তালিকা = sorted(পথ_2.stem for পথ_2 in (প্রকল্প_মূল/'한국어자바/বাংলা/নিজ').glob('*ব্যতিক্রম.java'))
    ব্যতিক্রম_লগ = (বৈধকরণ_পথ/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for নাম in ব্যতিক্রম_তালিকা:
        if '\n'+নাম+'\n' not in ব্যতিক্রম_লগ: raise SystemExit('ব্যতিক্রম সৃষ্টি_করুন·잡기·설명 시험 필요: '+নাম)
    명세 = json.loads((প্রকল্প_মূল/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != হ্যাশ_ফাইল(প্রকল্প_মূল/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 ছবি_মান হ্যাশ_ফাইল 불일치')
    with zipfile.ZipFile(str(প্রকল্প_মূল/'dist/jkoros-native-rpi4-boot.zip')) as পাঁজা:
        if hashlib.sha256(পাঁজা.read('kernel8.img')).hexdigest() != কারনেল_হ্যাশ:
            raise SystemExit('부팅 ZIP কারনেল_মান 불일치')
        부팅설정 = পাঁজা.read('config.txt')
        for নাম, আকার in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+নাম+'='+str(আকার) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 সেটিংস 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(প্রকল্প_মূল/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(প্রকল্প_মূল/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if হ্যাশ_ফাইল(복사본) != কারনেল_হ্যাশ: raise SystemExit('SD ছবি_মান কারনেল_মান 불일치')
        নজির_সেটিংস = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(প্রকল্প_মূল/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(নজির_সেটিংস)])
        if নজির_সেটিংস.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 সেটিংস 불일치')
    লগ_সারি = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': কারনেল_হ্যাশ,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': ব্যতিক্রম_তালিকা, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(চেক_রেজোলিউশন['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {নাম:হ্যাশ_ফাইল(প্রকল্প_মূল/'dist'/নাম) for নাম in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (বৈধকরণ_পথ/'native-runtime-summary.json').write_text(json.dumps(লগ_সারি,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 লগ_সারি, বাংলা ব্যতিক্রম',len(ব্যতিক্রম_তালিকা),'শ্রেণী_সংজ্ঞা, SD ছবি_মান·ZIP 일치')

if __name__ == '__main__': চালনা()
