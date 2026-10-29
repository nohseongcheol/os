#!/usr/bin/env python3
"""현재 커널과 фактик_мәгълүмат 시험·배포물이 일치할 때에만 통합 тикшерү 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

экранга_җибәрү_тамыр = Path(__file__).resolve().parents[1]

def Хәш_файл(Yul):
    계산 = hashlib.sha256()
    with Yul.open('rb') as Birem:
        for мәгълүмат in iter(lambda: Birem.read(1048576), b''): 계산.update(мәгълүмат)
    return 계산.hexdigest()

def эшләтү():
    раслау_юл = экранга_җибәрү_тамыр/'build/verification'
    төш_Хәш = Хәш_файл(экранга_җибәрү_тамыр/'build/kernel8.img')
    기록들 = {}
    for исем in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if исем == 'boot' else исем+'/report.json'
        мәгълүмат = json.loads((раслау_юл/상대경로).read_text())
        if not мәгълүмат.get('passed') or мәгълүмат.get('kernel_sha256') != төш_Хәш:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[исем] = {'passed': True, 'report': 상대경로}
    чек_исем = json.loads((раслау_юл/'naming/report.json').read_text())
    if not чек_исем['passed'] or not чек_исем['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for Yul, 기대값 in чек_исем['c_source_sha256'].items():
        if Хәш_файл(экранга_җибәрү_тамыр/Yul) != 기대값: raise SystemExit('명명 검사 Артка_VALUE 바뀐 C чыганак: '+Yul)
    자바검사 = json.loads((раслау_юл/'jvm/report.json').read_text())
    직접화면 = json.loads((раслау_юл/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('Татарча 직접 화면 үтәргә_команда 시험 필요')
    чек_байт_VALUE = json.loads((раслау_юл/'naming/direct-bytecode.json').read_text())
    if not чек_байт_VALUE['passed'] or чек_байт_VALUE['jar_sha256'] != Хәш_файл(экранга_җибәрү_тамыр/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 Татарча 라이브러리의 직접 호출 바이트코드 раслау 필요')
    чек_ачыклык = json.loads((раслау_юл/'resolution/report.json').read_text())
    чек_үлчәмен_үзгәртү = json.loads((раслау_юл/'resize/report.json').read_text())
    갱신검사 = json.loads((раслау_юл/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != төш_Хәш:
        raise SystemExit('현재 커널의 부분 яңарту 시험 필요')
    for Yul, 기대값 in 갱신검사['source_sha256'].items():
        if Хәш_файл(экранга_җибәрү_тамыр/Yul) != 기대값: raise SystemExit('부분 яңарту 시험 Артка_VALUE 바뀐 чыганак: '+Yul)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('Татарча 직접 가닥과 эшләтү кертү_балл 시험 필요')
    예제검사 = json.loads((раслау_юл/'examples/report.json').read_text())
    if sorted(чек_үлчәмен_үзгәртү['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 үлчәмен_үзгәртү 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('Татарча Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(чек_ачыклык['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 фактик_мәгълүмат 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != Хәш_файл(экранга_җибәрү_тамыр/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 Артка_VALUE 라이브러리가 바뀌었습니다.')
    for исем in ('한국어통신시험','한국어예외시험'):
        if not any(кертү_VALUE['name']==исем and кертү_VALUE.get('openjdk_output_equal') for кертү_VALUE in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+исем)
    예외들 = sorted(Yul.stem for Yul in (экранга_җибәрү_тамыр/'한국어자바/Татарча/자체').glob('*예외.java'))
    예외기록 = (раслау_юл/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for исем in 예외들:
        if '\n'+исем+'\n' not in 예외기록: raise SystemExit('예외 булдыру·잡기·설명 시험 필요: '+исем)
    명세 = json.loads((экранга_җибәрү_тамыр/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != Хәш_файл(экранга_җибәрү_тамыр/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 IMAGE_VALUE Хәш_файл 불일치')
    with zipfile.ZipFile(str(экранга_җибәрү_тамыр/'dist/jkoros-native-rpi4-boot.zip')) as пакет:
        if hashlib.sha256(пакет.read('kernel8.img')).hexdigest() != төш_Хәш:
            raise SystemExit('부팅 ZIP төш_VALUE 불일치')
        부팅설정 = пакет.read('config.txt')
        for исем, үлчәмен_үзгәртү in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+исем+'='+str(үлчәмен_үзгәртү) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Caylaw 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(экранга_җибәрү_тамыр/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(экранга_җибәрү_тамыр/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if Хәш_файл(복사본) != төш_Хәш: raise SystemExit('SD IMAGE_VALUE төш_VALUE 불일치')
        экземпляр_Параметрлар = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(экранга_җибәрү_тамыр/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(экземпляр_Параметрлар)])
        if экземпляр_Параметрлар.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Caylaw 불일치')
    LOG_юл = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': төш_Хәш,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(чек_ачыклык['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {исем:Хәш_файл(экранга_җибәрү_тамыр/'dist'/исем) for исем in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (раслау_юл/'native-runtime-summary.json').write_text(json.dumps(LOG_юл,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 LOG_юл, Татарча 예외',len(예외들),'класс_Билгеләмә, SD IMAGE_VALUE·ZIP 일치')

if __name__ == '__main__': эшләтү()
