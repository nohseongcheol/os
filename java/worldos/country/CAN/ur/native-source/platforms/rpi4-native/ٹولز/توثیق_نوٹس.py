#!/usr/bin/env python3
"""현재 커널과 اصل_کوائف 시험·배포물이 일치할 때에만 통합 جواز_دہی_کریں 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

عکس_ڈالنا_روٹ = Path(__file__).resolve().parents[1]

def ہيش_فائل(راستہ_2):
    계산 = hashlib.sha256()
    with راستہ_2.open('rb') as فائل_کا_نام:
        for کوائف in iter(lambda: فائل_کا_نام.read(1048576), b''): 계산.update(کوائف)
    return 계산.hexdigest()

def چلائیں():
    توثیق_راہ = عکس_ڈالنا_روٹ/'build/verification'
    کرنیل_ہيش = ہيش_فائل(عکس_ڈالنا_روٹ/'build/kernel8.img')
    기록들 = {}
    for نام in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if نام == 'boot' else نام+'/report.json'
        کوائف = json.loads((توثیق_راہ/상대경로).read_text())
        if not کوائف.get('passed') or کوائف.get('kernel_sha256') != کرنیل_ہيش:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[نام] = {'passed': True, 'report': 상대경로}
    پڑتال_کریں_نام = json.loads((توثیق_راہ/'naming/report.json').read_text())
    if not پڑتال_کریں_نام['passed'] or not پڑتال_کریں_نام['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for راستہ_2, 기대값 in پڑتال_کریں_نام['c_source_sha256'].items():
        if ہيش_فائل(عکس_ڈالنا_روٹ/راستہ_2) != 기대값: raise SystemExit('명명 검사 واپس_قدر 바뀐 C ماخذ_فائل: '+راستہ_2)
    자바검사 = json.loads((توثیق_راہ/'jvm/report.json').read_text())
    직접화면 = json.loads((توثیق_راہ/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('اردو 직접 화면 نفاذ_کریں_حکم 시험 필요')
    پڑتال_کریں_بائٹ_قدر = json.loads((توثیق_راہ/'naming/direct-bytecode.json').read_text())
    if not پڑتال_کریں_بائٹ_قدر['passed'] or پڑتال_کریں_بائٹ_قدر['jar_sha256'] != ہيش_فائل(عکس_ڈالنا_روٹ/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 اردو 라이브러리의 직접 호출 바이트코드 تصدیق_کریں 필요')
    پڑتال_کریں_جزیات_کاری = json.loads((توثیق_راہ/'resolution/report.json').read_text())
    پڑتال_کریں_سائز_دیں = json.loads((توثیق_راہ/'resize/report.json').read_text())
    갱신검사 = json.loads((توثیق_راہ/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != کرنیل_ہيش:
        raise SystemExit('현재 커널의 부분 تازہ_کریں 시험 필요')
    for راستہ_2, 기대값 in 갱신검사['source_sha256'].items():
        if ہيش_فائل(عکس_ڈالنا_روٹ/راستہ_2) != 기대값: raise SystemExit('부분 تازہ_کریں 시험 واپس_قدر 바뀐 ماخذ_فائل: '+راستہ_2)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('اردو 직접 가닥과 چلائیں اندراج_نقطہ 시험 필요')
    예제검사 = json.loads((توثیق_راہ/'examples/report.json').read_text())
    if sorted(پڑتال_کریں_سائز_دیں['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 حجم 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('اردو Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(پڑتال_کریں_جزیات_کاری['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 اصل_کوائف 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != ہيش_فائل(عکس_ڈالنا_روٹ/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 واپس_قدر 라이브러리가 바뀌었습니다.')
    for نام in ('한국어통신시험','한국어예외시험'):
        if not any(اندراج_قدر['name']==نام and اندراج_قدر.get('openjdk_output_equal') for اندراج_قدر in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+نام)
    استثنا_فہرست = sorted(راستہ_2.stem for راستہ_2 in (عکس_ڈالنا_روٹ/'한국어자바/اردو/اپنا').glob('*استثنا.java'))
    استثنا_لاگ = (توثیق_راہ/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for نام in استثنا_فہرست:
        if '\n'+نام+'\n' not in استثنا_لاگ: raise SystemExit('استثنا تخلیق_کرنا·잡기·설명 시험 필요: '+نام)
    명세 = json.loads((عکس_ڈالنا_روٹ/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != ہيش_فائل(عکس_ڈالنا_روٹ/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 نقش_قدر ہيش_فائل 불일치')
    with zipfile.ZipFile(str(عکس_ڈالنا_روٹ/'dist/jkoros-native-rpi4-boot.zip')) as بنڈل:
        if hashlib.sha256(بنڈل.read('kernel8.img')).hexdigest() != کرنیل_ہيش:
            raise SystemExit('부팅 ZIP کرنیل_قدر 불일치')
        부팅설정 = بنڈل.read('config.txt')
        for نام, حجم in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+نام+'='+str(حجم) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 ترتیبات 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(عکس_ڈالنا_روٹ/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(عکس_ڈالنا_روٹ/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if ہيش_فائل(복사본) != کرنیل_ہيش: raise SystemExit('SD نقش_قدر کرنیل_قدر 불일치')
        نقل_سیٹنگز = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(عکس_ڈالنا_روٹ/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(نقل_سیٹنگز)])
        if نقل_سیٹنگز.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 ترتیبات 불일치')
    لاگ_صف = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': کرنیل_ہيش,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': استثنا_فہرست, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(پڑتال_کریں_جزیات_کاری['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {نام:ہيش_فائل(عکس_ڈالنا_روٹ/'dist'/نام) for نام in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (توثیق_راہ/'native-runtime-summary.json').write_text(json.dumps(لاگ_صف,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 لاگ_صف, اردو استثنا',len(استثنا_فہرست),'صنف_تعریف, SD نقش_قدر·ZIP 일치')

if __name__ == '__main__': چلائیں()
