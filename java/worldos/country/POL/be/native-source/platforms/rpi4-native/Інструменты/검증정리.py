#!/usr/bin/env python3
"""현재 커널과 фактычны_дадзеныя 시험·배포물이 일치할 때에만 통합 праверыць_5fb2b747 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

기준 = Path(__file__).resolve().parents[1]

def хэш_файл(ШЛЯХ):
    계산 = hashlib.sha256()
    with ШЛЯХ.open('rb') as Файл:
        for дадзеныя in iter(lambda: Файл.read(1048576), b''): 계산.update(дадзеныя)
    return 계산.hexdigest()

def Выканаць():
    праверка_шлях = 기준/'build/verification'
    ядро_хэш = хэш_файл(기준/'build/kernel8.img')
    기록들 = {}
    for Назва in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Назва == 'boot' else Назва+'/report.json'
        дадзеныя = json.loads((праверка_шлях/상대경로).read_text())
        if not дадзеныя.get('passed') or дадзеныя.get('kernel_sha256') != ядро_хэш:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Назва] = {'passed': True, 'report': 상대경로}
    чэк_імя = json.loads((праверка_шлях/'naming/report.json').read_text())
    if not чэк_імя['passed'] or not чэк_імя['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for ШЛЯХ, 기대값 in чэк_імя['c_source_sha256'].items():
        if хэш_файл(기준/ШЛЯХ) != 기대값: raise SystemExit('명명 검사 Назад_значэнне 바뀐 C КРЫНІЦА: '+ШЛЯХ)
    자바검사 = json.loads((праверка_шлях/'jvm/report.json').read_text())
    직접화면 = json.loads((праверка_шлях/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 выканаць_каманда 시험 필요')
    чэк_байт_значэнне = json.loads((праверка_шлях/'naming/direct-bytecode.json').read_text())
    if not чэк_байт_значэнне['passed'] or чэк_байт_значэнне['jar_sha256'] != хэш_файл(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 праверыць 필요')
    чэк_разрознасць = json.loads((праверка_шлях/'resolution/report.json').read_text())
    чэк_памер = json.loads((праверка_шлях/'resize/report.json').read_text())
    갱신검사 = json.loads((праверка_шлях/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != ядро_хэш:
        raise SystemExit('현재 커널의 부분 абнавіць 시험 필요')
    for ШЛЯХ, 기대값 in 갱신검사['source_sha256'].items():
        if хэш_файл(기준/ШЛЯХ) != 기대값: raise SystemExit('부분 абнавіць 시험 Назад_значэнне 바뀐 КРЫНІЦА: '+ШЛЯХ)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 Выканаць увядзенне_бал 시험 필요')
    예제검사 = json.loads((праверка_шлях/'examples/report.json').read_text())
    if sorted(чэк_памер['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Памер 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(чэк_разрознасць['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 фактычны_дадзеныя 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != хэш_файл(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 Назад_значэнне 라이브러리가 바뀌었습니다.')
    for Назва in ('한국어통신시험','한국어예외시험'):
        if not any(увядзенне_значэнне['name']==Назва and увядзенне_значэнне.get('openjdk_output_equal') for увядзенне_значэнне in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Назва)
    выключэнне_Спіс = sorted(ШЛЯХ.stem for ШЛЯХ in (기준/'한국어자바/한국어/자체').glob('*выключэнне.java'))
    выключэнне_журнал = (праверка_шлях/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Назва in выключэнне_Спіс:
        if '\n'+Назва+'\n' not in выключэнне_журнал: raise SystemExit('выключэнне 생성·잡기·설명 시험 필요: '+Назва)
    명세 = json.loads((기준/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != хэш_файл(기준/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 выява_значэнне хэш_файл 불일치')
    with zipfile.ZipFile(str(기준/'dist/jkoros-native-rpi4-boot.zip')) as пакет:
        if hashlib.sha256(пакет.read('kernel8.img')).hexdigest() != ядро_хэш:
            raise SystemExit('부팅 ZIP ядро_значэнне 불일치')
        부팅설정 = пакет.read('config.txt')
        for Назва, Памер in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Назва+'='+str(Памер) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Усталёўкі 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(기준/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if хэш_файл(복사본) != ядро_хэш: raise SystemExit('SD выява_значэнне ядро_значэнне 불일치')
        капіяваць_Налады = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(капіяваць_Налады)])
        if капіяваць_Налады.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Усталёўкі 불일치')
    журнал_запіс = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': ядро_хэш,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': выключэнне_Спіс, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(чэк_разрознасць['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Назва:хэш_файл(기준/'dist'/Назва) for Назва in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (праверка_шлях/'native-runtime-summary.json').write_text(json.dumps(журнал_запіс,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 журнал_запіс, 한국어 выключэнне',len(выключэнне_Спіс),'клас_Азначэнне, SD выява_значэнне·ZIP 일치')

if __name__ == '__main__': Выканаць()
