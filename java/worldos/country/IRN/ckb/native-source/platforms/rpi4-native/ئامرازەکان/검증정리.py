#!/usr/bin/env python3
"""현재 커널과 ڕاستەکی_دەیتا 시험·배포물이 일치할 때에만 통합 ڕەوایی 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

기준 = Path(__file__).resolve().parents[1]

def دەرەنجام_فایل(گوزەر):
    계산 = hashlib.sha256()
    with گوزەر.open('rb') as فایل:
        for دەیتا in iter(lambda: فایل.read(1048576), b''): 계산.update(دەیتا)
    return 계산.hexdigest()

def ڕادان():
    ڕەواکردن_گوزەر = 기준/'build/verification'
    کوورەک_دەرەنجام = دەرەنجام_فایل(기준/'build/kernel8.img')
    기록들 = {}
    for ناو in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if ناو == 'boot' else ناو+'/report.json'
        دەیتا = json.loads((ڕەواکردن_گوزەر/상대경로).read_text())
        if not دەیتا.get('passed') or دەیتا.get('kernel_sha256') != کوورەک_دەرەنجام:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[ناو] = {'passed': True, 'report': 상대경로}
    پشکنین_ناو = json.loads((ڕەواکردن_گوزەر/'naming/report.json').read_text())
    if not پشکنین_ناو['passed'] or not پشکنین_ناو['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for گوزەر, 기대값 in پشکنین_ناو['c_source_sha256'].items():
        if دەرەنجام_فایل(기준/گوزەر) != 기대값: raise SystemExit('명명 검사 دواوە_نرخ 바뀐 C ژێدەر: '+گوزەر)
    자바검사 = json.loads((ڕەواکردن_گوزەر/'jvm/report.json').read_text())
    직접화면 = json.loads((ڕەواکردن_گوزەر/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 جێبەجێکردن_فەرمان 시험 필요')
    پشکنین_بایت_نرخ = json.loads((ڕەواکردن_گوزەر/'naming/direct-bytecode.json').read_text())
    if not پشکنین_بایت_نرخ['passed'] or پشکنین_بایت_نرخ['jar_sha256'] != دەرەنجام_فایل(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 سەلماندن 필요')
    پشکنین_وردبینی = json.loads((ڕەواکردن_گوزەر/'resolution/report.json').read_text())
    پشکنین_گۆڕینی_ئەندازە = json.loads((ڕەواکردن_گوزەر/'resize/report.json').read_text())
    갱신검사 = json.loads((ڕەواکردن_گوزەر/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != کوورەک_دەرەنجام:
        raise SystemExit('현재 커널의 부분 تازە_کردنەوە 시험 필요')
    for گوزەر, 기대값 in 갱신검사['source_sha256'].items():
        if دەرەنجام_فایل(기준/گوزەر) != 기대값: raise SystemExit('부분 تازە_کردنەوە 시험 دواوە_نرخ 바뀐 ژێدەر: '+گوزەر)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 ڕادان تێنووسین_خاڵ 시험 필요')
    예제검사 = json.loads((ڕەواکردن_گوزەر/'examples/report.json').read_text())
    if sorted(پشکنین_گۆڕینی_ئەندازە['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 گۆڕینی_ئەندازە 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(پشکنین_وردبینی['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 ڕاستەکی_دەیتا 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != دەرەنجام_فایل(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 دواوە_نرخ 라이브러리가 바뀌었습니다.')
    for ناو in ('한국어통신시험','한국어예외시험'):
        if not any(تێنووسین_نرخ['name']==ناو and تێنووسین_نرخ.get('openjdk_output_equal') for تێنووسین_نرخ in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+ناو)
    예외들 = sorted(گوزەر.stem for گوزەر in (기준/'한국어자바/한국어/자체').glob('*예외.java'))
    예외기록 = (ڕەواکردن_گوزەر/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for ناو in 예외들:
        if '\n'+ناو+'\n' not in 예외기록: raise SystemExit('예외 생성·잡기·설명 시험 필요: '+ناو)
    명세 = json.loads((기준/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != دەرەنجام_فایل(기준/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 وێنە_نرخ دەرەنجام_فایل 불일치')
    with zipfile.ZipFile(str(기준/'dist/jkoros-native-rpi4-boot.zip')) as گورزە:
        if hashlib.sha256(گورزە.read('kernel8.img')).hexdigest() != کوورەک_دەرەنجام:
            raise SystemExit('부팅 ZIP کوورەک_نرخ 불일치')
        부팅설정 = گورزە.read('config.txt')
        for ناو, گۆڕینی_ئەندازە in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+ناو+'='+str(گۆڕینی_ئەندازە) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 ڕێكبەندەكان 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(기준/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if دەرەنجام_فایل(복사본) != کوورەک_دەرەنجام: raise SystemExit('SD وێنە_نرخ کوورەک_نرخ 불일치')
        کۆپی_ڕێكبەندەكان = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(کۆپی_ڕێكبەندەكان)])
        if کۆپی_ڕێكبەندەكان.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 ڕێكبەندەكان 불일치')
    تۆمار_ڕزن = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': کوورەک_دەرەنجام,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(پشکنین_وردبینی['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {ناو:دەرەنجام_فایل(기준/'dist'/ناو) for ناو in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (ڕەواکردن_گوزەر/'native-runtime-summary.json').write_text(json.dumps(تۆمار_ڕزن,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 تۆمار_ڕزن, 한국어 예외',len(예외들),'کلاس_پێناسە, SD وێنە_نرخ·ZIP 일치')

if __name__ == '__main__': ڕادان()
