#!/usr/bin/env python3
"""현재 커널과 அசல்_தரவு 시험·배포물이 일치할 때에만 통합 சரிபார்_5fb2b747 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

திட்டப்பணி_மூலம் = Path(__file__).resolve().parents[1]

def ஹாஷ்_கோப்பு(பாதை_2):
    계산 = hashlib.sha256()
    with பாதை_2.open('rb') as கோப்பின்_பெயர்:
        for தரவு in iter(lambda: கோப்பின்_பெயர்.read(1048576), b''): 계산.update(தரவு)
    return 계산.hexdigest()

def செயல்படுத்துக():
    செல்லுபடியாக்கம்_பாதை = திட்டப்பணி_மூலம்/'build/verification'
    கரு_ஹாஷ் = ஹாஷ்_கோப்பு(திட்டப்பணி_மூலம்/'build/kernel8.img')
    기록들 = {}
    for பெயர் in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        தொடர்புடைய_பாதை = 'report.json' if பெயர் == 'boot' else பெயர்+'/report.json'
        தரவு = json.loads((செல்லுபடியாக்கம்_பாதை/தொடர்புடைய_பாதை).read_text())
        if not தரவு.get('passed') or தரவு.get('kernel_sha256') != கரு_ஹாஷ்:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+தொடர்புடைய_பாதை)
        기록들[பெயர்] = {'passed': True, 'report': தொடர்புடைய_பாதை}
    காசோலை_பெயர் = json.loads((செல்லுபடியாக்கம்_பாதை/'naming/report.json').read_text())
    if not காசோலை_பெயர்['passed'] or not காசோலை_பெயர்['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for பாதை_2, 기대값 in காசோலை_பெயர்['c_source_sha256'].items():
        if ஹாஷ்_கோப்பு(திட்டப்பணி_மூலம்/பாதை_2) != 기대값: raise SystemExit('명명 검사 பின்_மதிப்பு 바뀐 C மூலக்_கோப்பு: '+பாதை_2)
    자바검사 = json.loads((செல்லுபடியாக்கம்_பாதை/'jvm/report.json').read_text())
    직접화면 = json.loads((செல்லுபடியாக்கம்_பாதை/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('தமிழ் 직접 화면 இயக்கு_கட்டளை 시험 필요')
    காசோலை_பைட்_மதிப்பு = json.loads((செல்லுபடியாக்கம்_பாதை/'naming/direct-bytecode.json').read_text())
    if not காசோலை_பைட்_மதிப்பு['passed'] or காசோலை_பைட்_மதிப்பு['jar_sha256'] != ஹாஷ்_கோப்பு(திட்டப்பணி_மூலம்/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 தமிழ் 라이브러리의 직접 호출 바이트코드 சரிபார் 필요')
    காசோலை_தெளிவுத்திறன் = json.loads((செல்லுபடியாக்கம்_பாதை/'resolution/report.json').read_text())
    காசோலை_அளவு = json.loads((செல்லுபடியாக்கம்_பாதை/'resize/report.json').read_text())
    갱신검사 = json.loads((செல்லுபடியாக்கம்_பாதை/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != கரு_ஹாஷ்:
        raise SystemExit('현재 커널의 부분 புதுப்பி 시험 필요')
    for பாதை_2, 기대값 in 갱신검사['source_sha256'].items():
        if ஹாஷ்_கோப்பு(திட்டப்பணி_மூலம்/பாதை_2) != 기대값: raise SystemExit('부분 புதுப்பி 시험 பின்_மதிப்பு 바뀐 மூலக்_கோப்பு: '+பாதை_2)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('தமிழ் 직접 가닥과 செயல்படுத்துக நுழைவுப்_புள்ளி 시험 필요')
    예제검사 = json.loads((செல்லுபடியாக்கம்_பாதை/'examples/report.json').read_text())
    if sorted(காசோலை_அளவு['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 அளவு 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('தமிழ் Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(காசோலை_தெளிவுத்திறன்['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 அசல்_தரவு 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != ஹாஷ்_கோப்பு(திட்டப்பணி_மூலம்/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 பின்_மதிப்பு 라이브러리가 바뀌었습니다.')
    for பெயர் in ('한국어통신시험','한국어예외시험'):
        if not any(உள்ளீடு_மதிப்பு['name']==பெயர் and உள்ளீடு_மதிப்பு.get('openjdk_output_equal') for உள்ளீடு_மதிப்பு in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+பெயர்)
    விதிவிலக்கு_பட்டியல் = sorted(பாதை_2.stem for பாதை_2 in (திட்டப்பணி_மூலம்/'한국어자바/தமிழ்/자체').glob('*விதிவிலக்கு.java'))
    விதிவிலக்கு_பதிவு = (செல்லுபடியாக்கம்_பாதை/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for பெயர் in விதிவிலக்கு_பட்டியல்:
        if '\n'+பெயர்+'\n' not in விதிவிலக்கு_பதிவு: raise SystemExit('விதிவிலக்கு உருவாக்குக·잡기·설명 시험 필요: '+பெயர்)
    명세 = json.loads((திட்டப்பணி_மூலம்/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != ஹாஷ்_கோப்பு(திட்டப்பணி_மூலம்/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 படம்_மதிப்பு ஹாஷ்_கோப்பு 불일치')
    with zipfile.ZipFile(str(திட்டப்பணி_மூலம்/'dist/jkoros-native-rpi4-boot.zip')) as மூட்டை:
        if hashlib.sha256(மூட்டை.read('kernel8.img')).hexdigest() != கரு_ஹாஷ்:
            raise SystemExit('부팅 ZIP கரு_மதிப்பு 불일치')
        부팅설정 = மூட்டை.read('config.txt')
        for பெயர், அளவு in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+பெயர்+'='+str(அளவு) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 அமைப்புகள் 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(திட்டப்பணி_மூலம்/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(திட்டப்பணி_மூலம்/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if ஹாஷ்_கோப்பு(복사본) != கரு_ஹாஷ்: raise SystemExit('SD படம்_மதிப்பு கரு_மதிப்பு 불일치')
        நகலெடு_அமைப்புகள் = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(திட்டப்பணி_மூலம்/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(நகலெடு_அமைப்புகள்)])
        if நகலெடு_அமைப்புகள்.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 அமைப்புகள் 불일치')
    பதிவு_பதிவு = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': கரு_ஹாஷ்,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': விதிவிலக்கு_பட்டியல், 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(காசோலை_தெளிவுத்திறன்['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {பெயர்:ஹாஷ்_கோப்பு(திட்டப்பணி_மூலம்/'dist'/பெயர்) for பெயர் in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (செல்லுபடியாக்கம்_பாதை/'native-runtime-summary.json').write_text(json.dumps(பதிவு_பதிவு,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 பதிவு_பதிவு, தமிழ் விதிவிலக்கு',len(விதிவிலக்கு_பட்டியல்),'பிரிவு_சொற்பொருள்_விளக்கம், SD படம்_மதிப்பு·ZIP 일치')

if __name__ == '__main__': செயல்படுத்துக()
