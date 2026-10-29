#!/usr/bin/env python3
"""현재 커널과 اصلي_ڪوائف 시험·배포물이 일치할 때에만 통합 ڪارگر_ڪريو 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

기준 = Path(__file__).resolve().parents[1]

def هيش_فائل(راههه):
    계산 = hashlib.sha256()
    with راههه.open('rb') as فائل:
        for ڪوائف in iter(lambda: فائل.read(1048576), b''): 계산.update(ڪوائف)
    return 계산.hexdigest()

def هلائڻ():
    ڪارگر_راههه = 기준/'build/verification'
    ڪرنل_هيش = هيش_فائل(기준/'build/kernel8.img')
    기록들 = {}
    for نالو in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if نالو == 'boot' else نالو+'/report.json'
        ڪوائف = json.loads((ڪارگر_راههه/상대경로).read_text())
        if not ڪوائف.get('passed') or ڪوائف.get('kernel_sha256') != ڪرنل_هيش:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[نالو] = {'passed': True, 'report': 상대경로}
    پڙتال_ڪريو_نالو = json.loads((ڪارگر_راههه/'naming/report.json').read_text())
    if not پڙتال_ڪريو_نالو['passed'] or not پڙتال_ڪريو_نالو['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for راههه, 기대값 in پڙتال_ڪريو_نالو['c_source_sha256'].items():
        if هيش_فائل(기준/راههه) != 기대값: raise SystemExit('명명 검사 واپس_قدر 바뀐 C ماخذ: '+راههه)
    자바검사 = json.loads((ڪارگر_راههه/'jvm/report.json').read_text())
    직접화면 = json.loads((ڪارگر_راههه/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 تعميل_ڪرڻ_حڪم 시험 필요')
    پڙتال_ڪريو_بائٽ_قدر = json.loads((ڪارگر_راههه/'naming/direct-bytecode.json').read_text())
    if not پڙتال_ڪريو_بائٽ_قدر['passed'] or پڙتال_ڪريو_بائٽ_قدر['jar_sha256'] != هيش_فائل(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 تصديق_ڪريو 필요')
    پڙتال_ڪريو_جزيت_ڪاري = json.loads((ڪارگر_راههه/'resolution/report.json').read_text())
    پڙتال_ڪريو_سائيز = json.loads((ڪارگر_راههه/'resize/report.json').read_text())
    갱신검사 = json.loads((ڪارگر_راههه/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != ڪرنل_هيش:
        raise SystemExit('현재 커널의 부분 ٻيهر_تازو_ڪريو 시험 필요')
    for راههه, 기대값 in 갱신검사['source_sha256'].items():
        if هيش_فائل(기준/راههه) != 기대값: raise SystemExit('부분 ٻيهر_تازو_ڪريو 시험 واپس_قدر 바뀐 ماخذ: '+راههه)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 هلائڻ داخلا_هنڌ 시험 필요')
    예제검사 = json.loads((ڪارگر_راههه/'examples/report.json').read_text())
    if sorted(پڙتال_ڪريو_سائيز['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 سائيز 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(پڙتال_ڪريو_جزيت_ڪاري['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 اصلي_ڪوائف 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != هيش_فائل(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 واپس_قدر 라이브러리가 바뀌었습니다.')
    for نالو in ('한국어통신시험','한국어예외시험'):
        if not any(داخلا_قدر['name']==نالو and داخلا_قدر.get('openjdk_output_equal') for داخلا_قدر in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+نالو)
    예외들 = sorted(راههه.stem for راههه in (기준/'한국어자바/한국어/자체').glob('*예외.java'))
    예외기록 = (ڪارگر_راههه/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for نالو in 예외들:
        if '\n'+نالو+'\n' not in 예외기록: raise SystemExit('예외 생성·잡기·설명 시험 필요: '+نالو)
    명세 = json.loads((기준/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != هيش_فائل(기준/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 نقش_قدر هيش_فائل 불일치')
    with zipfile.ZipFile(str(기준/'dist/jkoros-native-rpi4-boot.zip')) as بنڊل:
        if hashlib.sha256(بنڊل.read('kernel8.img')).hexdigest() != ڪرنل_هيش:
            raise SystemExit('부팅 ZIP ڪرنل_قدر 불일치')
        부팅설정 = بنڊل.read('config.txt')
        for نالو, سائيز in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+نالو+'='+str(سائيز) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 سيٽنگون 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(기준/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if هيش_فائل(복사본) != ڪرنل_هيش: raise SystemExit('SD نقش_قدر ڪرنل_قدر 불일치')
        نقل_سيٽنگون = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(نقل_سيٽنگون)])
        if نقل_سيٽنگون.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 سيٽنگون 불일치')
    لاگ_صف = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': ڪرنل_هيش,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(پڙتال_ڪريو_جزيت_ڪاري['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {نالو:هيش_فائل(기준/'dist'/نالو) for نالو in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (ڪارگر_راههه/'native-runtime-summary.json').write_text(json.dumps(لاگ_صف,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 لاگ_صف, 한국어 예외',len(예외들),'درجو_وصف, SD نقش_قدر·ZIP 일치')

if __name__ == '__main__': هلائڻ()
