#!/usr/bin/env python3
"""현재 커널과 প্ৰকৃত_ডাটা 시험·배포물이 일치할 때에만 통합 বৈধকৰণ_কৰক 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

기준 = Path(__file__).resolve().parents[1]

def হেচ_ফাইল(পথ):
    계산 = hashlib.sha256()
    with পথ.open('rb') as নথিপত্ৰ:
        for ডাটা in iter(lambda: নথিপত্ৰ.read(1048576), b''): 계산.update(ডাটা)
    return 계산.hexdigest()

def সঞ্চালন():
    বৈধতা_পথ = 기준/'build/verification'
    কাৰ্ণেল_হেচ = হেচ_ফাইল(기준/'build/kernel8.img')
    기록들 = {}
    for নাম in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if নাম == 'boot' else নাম+'/report.json'
        ডাটা = json.loads((বৈধতা_পথ/상대경로).read_text())
        if not ডাটা.get('passed') or ডাটা.get('kernel_sha256') != কাৰ্ণেল_হেচ:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[নাম] = {'passed': True, 'report': 상대경로}
    পৰীক্ষণ_নাম = json.loads((বৈধতা_পথ/'naming/report.json').read_text())
    if not পৰীক্ষণ_নাম['passed'] or not পৰীক্ষণ_নাম['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for পথ, 기대값 in পৰীক্ষণ_নাম['c_source_sha256'].items():
        if হেচ_ফাইল(기준/পথ) != 기대값: raise SystemExit('명명 검사 পাছলৈ_মান 바뀐 C উৎস: '+পথ)
    자바검사 = json.loads((বৈধতা_পথ/'jvm/report.json').read_text())
    직접화면 = json.loads((বৈধতা_পথ/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 নিষ্পাদন_আদেশ 시험 필요')
    পৰীক্ষণ_বাইট_মান = json.loads((বৈধতা_পথ/'naming/direct-bytecode.json').read_text())
    if not পৰীক্ষণ_বাইট_মান['passed'] or পৰীক্ষণ_বাইট_মান['jar_sha256'] != হেচ_ফাইল(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 প্ৰমাণিত_কৰক 필요')
    পৰীক্ষণ_প্রতিচ্ছায়া = json.loads((বৈধতা_পথ/'resolution/report.json').read_text())
    পৰীক্ষণ_আকাৰ_কৰক = json.loads((বৈধতা_পথ/'resize/report.json').read_text())
    갱신검사 = json.loads((বৈধতা_পথ/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != কাৰ্ণেল_হেচ:
        raise SystemExit('현재 커널의 부분 সতেজ_কৰক 시험 필요')
    for পথ, 기대값 in 갱신검사['source_sha256'].items():
        if হেচ_ফাইল(기준/পথ) != 기대값: raise SystemExit('부분 সতেজ_কৰক 시험 পাছলৈ_মান 바뀐 উৎস: '+পথ)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 সঞ্চালন প্রবিষ্ট_পইণ্ট 시험 필요')
    예제검사 = json.loads((বৈধতা_পথ/'examples/report.json').read_text())
    if sorted(পৰীক্ষণ_আকাৰ_কৰক['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 মাপ 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(পৰীক্ষণ_প্রতিচ্ছায়া['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 প্ৰকৃত_ডাটা 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != হেচ_ফাইল(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 পাছলৈ_মান 라이브러리가 바뀌었습니다.')
    for নাম in ('한국어통신시험','한국어예외시험'):
        if not any(প্রবিষ্ট_মান['name']==নাম and প্রবিষ্ট_মান.get('openjdk_output_equal') for প্রবিষ্ট_মান in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+নাম)
    예외들 = sorted(পথ.stem for পথ in (기준/'한국어자바/한국어/자체').glob('*예외.java'))
    예외기록 = (বৈধতা_পথ/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for নাম in 예외들:
        if '\n'+নাম+'\n' not in 예외기록: raise SystemExit('예외 সৃষ্টি_কৰক·잡기·설명 시험 필요: '+নাম)
    명세 = json.loads((기준/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != হেচ_ফাইল(기준/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 ছবি_মান হেচ_ফাইল 불일치')
    with zipfile.ZipFile(str(기준/'dist/jkoros-native-rpi4-boot.zip')) as বাণ্ডল:
        if hashlib.sha256(বাণ্ডল.read('kernel8.img')).hexdigest() != কাৰ্ণেল_হেচ:
            raise SystemExit('부팅 ZIP কাৰ্ণেল_মান 불일치')
        부팅설정 = বাণ্ডল.read('config.txt')
        for নাম, মাপ in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+নাম+'='+str(মাপ) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 বৈশিষ্ট্য 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(기준/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if হেচ_ফাইল(복사본) != কাৰ্ণেল_হেচ: raise SystemExit('SD ছবি_মান কাৰ্ণেল_মান 불일치')
        নজিৰ_ছেটিংছ = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(নজিৰ_ছেটিংছ)])
        if নজিৰ_ছেটিংছ.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 বৈশিষ্ট্য 불일치')
    লগ_শাৰী = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': কাৰ্ণেল_হেচ,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(পৰীক্ষণ_প্রতিচ্ছায়া['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {নাম:হেচ_ফাইল(기준/'dist'/নাম) for নাম in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (বৈধতা_পথ/'native-runtime-summary.json').write_text(json.dumps(লগ_শাৰী,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 লগ_শাৰী, 한국어 예외',len(예외들),'শ্ৰেণী_সংজ্ঞা, SD ছবি_মান·ZIP 일치')

if __name__ == '__main__': সঞ্চালন()
