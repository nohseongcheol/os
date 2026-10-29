#!/usr/bin/env python3
"""현재 커널과 totoo_data 시험·배포물이 일치할 때에만 통합 patunayan 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

Project_root = Path(__file__).resolve().parents[1]

def hash_file(path):
    계산 = hashlib.sha256()
    with path.open('rb') as file:
        for data in iter(lambda: file.read(1048576), b''): 계산.update(data)
    return 계산.hexdigest()

def run():
    pagpapatibay_path = Project_root/'build/verification'
    kernel_hash = hash_file(Project_root/'build/kernel8.img')
    기록들 = {}
    for pangalan in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if pangalan == 'boot' else pangalan+'/report.json'
        data = json.loads((pagpapatibay_path/상대경로).read_text())
        if not data.get('passed') or data.get('kernel_sha256') != kernel_hash:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[pangalan] = {'passed': True, 'report': 상대경로}
    tseke_pangalan = json.loads((pagpapatibay_path/'naming/report.json').read_text())
    if not tseke_pangalan['passed'] or not tseke_pangalan['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for path, 기대값 in tseke_pangalan['c_source_sha256'].items():
        if hash_file(Project_root/path) != 기대값: raise SystemExit('명명 검사 Bumalik_VALUE 바뀐 C pinagmulan: '+path)
    자바검사 = json.loads((pagpapatibay_path/'jvm/report.json').read_text())
    직접화면 = json.loads((pagpapatibay_path/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 Mag_execute_utos 시험 필요')
    tseke_byte_VALUE = json.loads((pagpapatibay_path/'naming/direct-bytecode.json').read_text())
    if not tseke_byte_VALUE['passed'] or tseke_byte_VALUE['jar_sha256'] != hash_file(Project_root/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 tiyakin_kumpirmahin 필요')
    tseke_resolution = json.loads((pagpapatibay_path/'resolution/report.json').read_text())
    tseke_sukat = json.loads((pagpapatibay_path/'resize/report.json').read_text())
    갱신검사 = json.loads((pagpapatibay_path/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != kernel_hash:
        raise SystemExit('현재 커널의 부분 i_refresh 시험 필요')
    for path, 기대값 in 갱신검사['source_sha256'].items():
        if hash_file(Project_root/path) != 기대값: raise SystemExit('부분 i_refresh 시험 Bumalik_VALUE 바뀐 pinagmulan: '+path)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 run pagpasok_point 시험 필요')
    예제검사 = json.loads((pagpapatibay_path/'examples/report.json').read_text())
    if sorted(tseke_sukat['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 sukat_82232621 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(tseke_resolution['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 totoo_data 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != hash_file(Project_root/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 Bumalik_VALUE 라이브러리가 바뀌었습니다.')
    for pangalan in ('한국어통신시험','한국어예외시험'):
        if not any(pagpasok_VALUE['name']==pangalan and pagpasok_VALUE.get('openjdk_output_equal') for pagpasok_VALUE in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+pangalan)
    pagbubukod_list = sorted(path.stem for path in (Project_root/'한국어자바/한국어/자체').glob('*pagbubukod.java'))
    pagbubukod_LOG = (pagpapatibay_path/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for pangalan in pagbubukod_list:
        if '\n'+pangalan+'\n' not in pagbubukod_LOG: raise SystemExit('pagbubukod mag_generate·잡기·설명 시험 필요: '+pangalan)
    명세 = json.loads((Project_root/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != hash_file(Project_root/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 IMAGE_VALUE hash_file 불일치')
    with zipfile.ZipFile(str(Project_root/'dist/jkoros-native-rpi4-boot.zip')) as bundle:
        if hashlib.sha256(bundle.read('kernel8.img')).hexdigest() != kernel_hash:
            raise SystemExit('부팅 ZIP kernel_VALUE 불일치')
        부팅설정 = bundle.read('config.txt')
        for pangalan, sukat_82232621 in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+pangalan+'='+str(sukat_82232621) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Mga_Setting 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(Project_root/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(Project_root/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if hash_file(복사본) != kernel_hash: raise SystemExit('SD IMAGE_VALUE kernel_VALUE 불일치')
        gumawa_ng_kopya_Mga_Setting = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(Project_root/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(gumawa_ng_kopya_Mga_Setting)])
        if gumawa_ng_kopya_Mga_Setting.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Mga_Setting 불일치')
    LOG_hanay = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': kernel_hash,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': pagbubukod_list, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(tseke_resolution['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {pangalan:hash_file(Project_root/'dist'/pangalan) for pangalan in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (pagpapatibay_path/'native-runtime-summary.json').write_text(json.dumps(LOG_hanay,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 LOG_hanay, 한국어 pagbubukod',len(pagbubukod_list),'kategorya_Kahulugan, SD IMAGE_VALUE·ZIP 일치')

if __name__ == '__main__': run()
