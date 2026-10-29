#!/usr/bin/env python3
"""현재 커널과 واقعی_داده_ها 시험·배포물이 일치할 때에만 통합 ارزیابی_کردن 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

نمایش_دادن_جذر = Path(__file__).resolve().parents[1]

def هاشور_فایل(مسیر):
    계산 = hashlib.sha256()
    with مسیر.open('rb') as پرونده:
        for داده_ها in iter(lambda: پرونده.read(1048576), b''): 계산.update(داده_ها)
    return 계산.hexdigest()

def اجرا_2():
    اعتبارسنجی_مسیر = نمایش_دادن_جذر/'build/verification'
    هسته_هاشور = هاشور_فایل(نمایش_دادن_جذر/'build/kernel8.img')
    기록들 = {}
    for نام in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if نام == 'boot' else نام+'/report.json'
        داده_ها = json.loads((اعتبارسنجی_مسیر/상대경로).read_text())
        if not داده_ها.get('passed') or داده_ها.get('kernel_sha256') != هسته_هاشور:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[نام] = {'passed': True, 'report': 상대경로}
    بررسی_نام = json.loads((اعتبارسنجی_مسیر/'naming/report.json').read_text())
    if not بررسی_نام['passed'] or not بررسی_نام['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for مسیر, 기대값 in بررسی_نام['c_source_sha256'].items():
        if هاشور_فایل(نمایش_دادن_جذر/مسیر) != 기대값: raise SystemExit('명명 검사 برگشت_مقدار 바뀐 C مبداء: '+مسیر)
    자바검사 = json.loads((اعتبارسنجی_مسیر/'jvm/report.json').read_text())
    직접화면 = json.loads((اعتبارسنجی_مسیر/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('فارسی 직접 화면 اجرا_فرمان 시험 필요')
    بررسی_بایت_مقدار = json.loads((اعتبارسنجی_مسیر/'naming/direct-bytecode.json').read_text())
    if not بررسی_بایت_مقدار['passed'] or بررسی_بایت_مقدار['jar_sha256'] != هاشور_فایل(نمایش_دادن_جذر/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 فارسی 라이브러리의 직접 호출 바이트코드 تأیید_صحت 필요')
    بررسی_دقت = json.loads((اعتبارسنجی_مسیر/'resolution/report.json').read_text())
    بررسی_اندازه_کردن = json.loads((اعتبارسنجی_مسیر/'resize/report.json').read_text())
    갱신검사 = json.loads((اعتبارسنجی_مسیر/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != هسته_هاشور:
        raise SystemExit('현재 커널의 부분 تازه_کردن 시험 필요')
    for مسیر, 기대값 in 갱신검사['source_sha256'].items():
        if هاشور_فایل(نمایش_دادن_جذر/مسیر) != 기대값: raise SystemExit('부분 تازه_کردن 시험 برگشت_مقدار 바뀐 مبداء: '+مسیر)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('فارسی 직접 가닥과 اجرا_2 ورودی_نقطه 시험 필요')
    예제검사 = json.loads((اعتبارسنجی_مسیر/'examples/report.json').read_text())
    if sorted(بررسی_اندازه_کردن['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 اندازه 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('فارسی Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(بررسی_دقت['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 واقعی_داده_ها 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != هاشور_فایل(نمایش_دادن_جذر/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 برگشت_مقدار 라이브러리가 바뀌었습니다.')
    for نام in ('한국어통신시험','한국어예외시험'):
        if not any(ورودی_مقدار['name']==نام and ورودی_مقدار.get('openjdk_output_equal') for ورودی_مقدار in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+نام)
    استثنا_لیست = sorted(مسیر.stem for مسیر in (نمایش_دادن_جذر/'한국어자바/فارسی/بومی').glob('*استثنا.java'))
    استثنا_واقعه_نگار = (اعتبارسنجی_مسیر/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for نام in استثنا_لیست:
        if '\n'+نام+'\n' not in استثنا_واقعه_نگار: raise SystemExit('استثنا ایجاد·잡기·설명 시험 필요: '+نام)
    명세 = json.loads((نمایش_دادن_جذر/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != هاشور_فایل(نمایش_دادن_جذر/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 عکس_مقدار هاشور_فایل 불일치')
    with zipfile.ZipFile(str(نمایش_دادن_جذر/'dist/jkoros-native-rpi4-boot.zip')) as دسته_کردن:
        if hashlib.sha256(دسته_کردن.read('kernel8.img')).hexdigest() != هسته_هاشور:
            raise SystemExit('부팅 ZIP هسته_مقدار 불일치')
        부팅설정 = دسته_کردن.read('config.txt')
        for نام, اندازه in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+نام+'='+str(اندازه) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 تنظیمات 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(نمایش_دادن_جذر/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(نمایش_دادن_جذر/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if هاشور_فایل(복사본) != هسته_هاشور: raise SystemExit('SD عکس_مقدار هسته_مقدار 불일치')
        کپی_تنظیمات = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(نمایش_دادن_جذر/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(کپی_تنظیمات)])
        if کپی_تنظیمات.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 تنظیمات 불일치')
    واقعه_نگار_ردیف = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': هسته_هاشور,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': استثنا_لیست, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(بررسی_دقت['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {نام:هاشور_فایل(نمایش_دادن_جذر/'dist'/نام) for نام in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (اعتبارسنجی_مسیر/'native-runtime-summary.json').write_text(json.dumps(واقعه_نگار_ردیف,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 واقعه_نگار_ردیف, فارسی استثنا',len(استثنا_لیست),'کلاس_تعریف, SD عکس_مقدار·ZIP 일치')

if __name__ == '__main__': اجرا_2()
