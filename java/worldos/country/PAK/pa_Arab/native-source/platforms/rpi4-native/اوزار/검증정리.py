#!/usr/bin/env python3
"""현재 커널과 اصلی_کوائف 시험·배포물이 일치할 때에만 통합 تریخ_دے_مطابق_کرو 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

기준 = Path(__file__).resolve().parents[1]

def ہیش_فائل(راہ):
    계산 = hashlib.sha256()
    with راہ.open('rb') as فائل:
        for کوائف in iter(lambda: فائل.read(1048576), b''): 계산.update(کوائف)
    return 계산.hexdigest()

def چلاؤ():
    جواز_دہی_راہ = 기준/'build/verification'
    کرنل_ہیش = ہیش_فائل(기준/'build/kernel8.img')
    기록들 = {}
    for ناں in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if ناں == 'boot' else ناں+'/report.json'
        کوائف = json.loads((جواز_دہی_راہ/상대경로).read_text())
        if not کوائف.get('passed') or کوائف.get('kernel_sha256') != کرنل_ہیش:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[ناں] = {'passed': True, 'report': 상대경로}
    پڑتال_ناں = json.loads((جواز_دہی_راہ/'naming/report.json').read_text())
    if not پڑتال_ناں['passed'] or not پڑتال_ناں['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for راہ, 기대값 in پڑتال_ناں['c_source_sha256'].items():
        if ہیش_فائل(기준/راہ) != 기대값: raise SystemExit('명명 검사 پیچھے_قدر 바뀐 C ماخذ: '+راہ)
    자바검사 = json.loads((جواز_دہی_راہ/'jvm/report.json').read_text())
    직접화면 = json.loads((جواز_دہی_راہ/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 نفاذ_کرو_حکم 시험 필요')
    پڑتال_بائٹ_قدر = json.loads((جواز_دہی_راہ/'naming/direct-bytecode.json').read_text())
    if not پڑتال_بائٹ_قدر['passed'] or پڑتال_بائٹ_قدر['jar_sha256'] != ہیش_فائل(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 تصدیق_کرو 필요')
    پڑتال_جزیات_کاری = json.loads((جواز_دہی_راہ/'resolution/report.json').read_text())
    پڑتال_سائز = json.loads((جواز_دہی_راہ/'resize/report.json').read_text())
    갱신검사 = json.loads((جواز_دہی_راہ/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != کرنل_ہیش:
        raise SystemExit('현재 커널의 부분 پھر_تازہ_کرو 시험 필요')
    for راہ, 기대값 in 갱신검사['source_sha256'].items():
        if ہیش_فائل(기준/راہ) != 기대값: raise SystemExit('부분 پھر_تازہ_کرو 시험 پیچھے_قدر 바뀐 ماخذ: '+راہ)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 چلاؤ داخلہ_مقام 시험 필요')
    예제검사 = json.loads((جواز_دہی_راہ/'examples/report.json').read_text())
    if sorted(پڑتال_سائز['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 سائز 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(پڑتال_جزیات_کاری['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 اصلی_کوائف 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != ہیش_فائل(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 پیچھے_قدر 라이브러리가 바뀌었습니다.')
    for ناں in ('한국어통신시험','한국어예외시험'):
        if not any(داخلہ_قدر['name']==ناں and داخلہ_قدر.get('openjdk_output_equal') for داخلہ_قدر in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+ناں)
    예외들 = sorted(راہ.stem for راہ in (기준/'한국어자바/한국어/자체').glob('*예외.java'))
    예외기록 = (جواز_دہی_راہ/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for ناں in 예외들:
        if '\n'+ناں+'\n' not in 예외기록: raise SystemExit('예외 생성·잡기·설명 시험 필요: '+ناں)
    명세 = json.loads((기준/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != ہیش_فائل(기준/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 نقش_قدر ہیش_فائل 불일치')
    with zipfile.ZipFile(str(기준/'dist/jkoros-native-rpi4-boot.zip')) as گٹھ:
        if hashlib.sha256(گٹھ.read('kernel8.img')).hexdigest() != کرنل_ہیش:
            raise SystemExit('부팅 ZIP کرنل_قدر 불일치')
        부팅설정 = گٹھ.read('config.txt')
        for ناں, سائز in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+ناں+'='+str(سائز) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 سیٹنگاں 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(기준/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if ہیش_فائل(복사본) != کرنل_ہیش: raise SystemExit('SD نقش_قدر کرنل_قدر 불일치')
        نقل_سیٹنگاں = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(نقل_سیٹنگاں)])
        if نقل_سیٹنگاں.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 سیٹنگاں 불일치')
    لاگ_صف = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': کرنل_ہیش,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(پڑتال_جزیات_کاری['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {ناں:ہیش_فائل(기준/'dist'/ناں) for ناں in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (جواز_دہی_راہ/'native-runtime-summary.json').write_text(json.dumps(لاگ_صف,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 لاگ_صف, 한국어 예외',len(예외들),'درجہ_تعریف, SD نقش_قدر·ZIP 일치')

if __name__ == '__main__': چلاؤ()
