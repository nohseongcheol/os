#!/usr/bin/env python3
"""текущий_товар 커널과 фактический_данные испытания·배포물이 일치할 때에만 통합 проверить 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

задача_корень = Path(__file__).resolve().parents[1]

def хэш_файл(путь):
    계산 = hashlib.sha256()
    with путь.open('rb') as файл:
        for данные in iter(lambda: файл.read(1048576), b''): 계산.update(данные)
    return 계산.hexdigest()

def запустить():
    проверка_путь = задача_корень/'build/verification'
    ядро_хэш = хэш_файл(задача_корень/'build/kernel8.img')
    기록들 = {}
    for Название in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        относительный_путь = 'report.json' if Название == 'boot' else Название+'/report.json'
        данные = json.loads((проверка_путь/относительный_путь).read_text())
        if not данные.get('passed') or данные.get('kernel_sha256') != ядро_хэш:
            raise SystemExit('текущий_товар 커널에 대한 성공 기록이 필요합니다: '+относительный_путь)
        기록들[Название] = {'passed': True, 'report': относительный_путь}
    чек_имя = json.loads((проверка_путь/'naming/report.json').read_text())
    if not чек_имя['passed'] or not чек_имя['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for путь, 기대값 in чек_имя['c_source_sha256'].items():
        if хэш_файл(задача_корень/путь) != 기대값: raise SystemExit('명명 검사 BACK_ЗНАЧЕН 바뀐 C исходныйКод: '+путь)
    자바검사 = json.loads((проверка_путь/'jvm/report.json').read_text())
    직접화면 = json.loads((проверка_путь/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('русский 직접 экран 실행 испытания 필요')
    чек_байт_ЗНАЧЕН = json.loads((проверка_путь/'naming/direct-bytecode.json').read_text())
    if not чек_байт_ЗНАЧЕН['passed'] or чек_байт_ЗНАЧЕН['jar_sha256'] != хэш_файл(задача_корень/'dist/jkoros-native-korean.jar'):
        raise SystemExit('текущий_товар русский 라이브러리의 직접 호출 바이트코드 проверять 필요')
    чек_разрешение = json.loads((проверка_путь/'resolution/report.json').read_text())
    чек_изменить_размер = json.loads((проверка_путь/'resize/report.json').read_text())
    갱신검사 = json.loads((проверка_путь/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != ядро_хэш:
        raise SystemExit('текущий_товар 커널의 부분 обновить испытания 필요')
    for путь, 기대값 in 갱신검사['source_sha256'].items():
        if хэш_файл(задача_корень/путь) != 기대값: raise SystemExit('부분 обновить испытания BACK_ЗНАЧЕН 바뀐 исходныйКод: '+путь)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('русский 직접 가닥과 запустить точка_входа испытания 필요')
    예제검사 = json.loads((проверка_путь/'examples/report.json').read_text())
    if sorted(чек_изменить_размер['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Размер 조절 испытания 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('русский Swing 창을 포함한 예제 13개 испытания 필요')
    if sorted(чек_разрешение['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 фактический_данные экран испытания 필요')
    if 자바검사['korean_library_sha256'] != хэш_файл(задача_корень/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 испытания BACK_ЗНАЧЕН 라이브러리가 바뀌었습니다.')
    for Название in ('한국어통신시험','한국어예외시험'):
        if not any(ввод_ЗНАЧЕН['name']==Название and ввод_ЗНАЧЕН.get('openjdk_output_equal') for ввод_ЗНАЧЕН in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 испытания 필요: '+Название)
    исключение_Список = sorted(путь.stem for путь in (задача_корень/'한국어자바/русский/свой').glob('*исключение.java'))
    исключение_LOG = (проверка_путь/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Название in исключение_Список:
        if '\n'+Название+'\n' not in исключение_LOG: raise SystemExit('исключение генерировать·잡기·описание испытания 필요: '+Название)
    спецификация = json.loads((задача_корень/'dist/manifest.json').read_text())
    if спецификация['image_sha256'] != хэш_файл(задача_корень/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('распределение_ЗНАЧЕН фото_ЗНАЧЕН хэш_файл 불일치')
    with zipfile.ZipFile(str(задача_корень/'dist/jkoros-native-rpi4-boot.zip')) as пакет:
        if hashlib.sha256(пакет.read('kernel8.img')).hexdigest() != ядро_хэш:
            raise SystemExit('запуск_машины ZIP ядро_ЗНАЧЕН 불일치')
        부팅설정 = пакет.read('config.txt')
        for Название, Размер in zip(('width', 'height'), спецификация['framebuffer_resolution']):
            if 'framebuffer_'+Название+'='+str(Размер) not in 부팅설정.decode().splitlines():
                raise SystemExit('запуск_машины ZIP экран Настройки 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(задача_корень/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(задача_корень/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if хэш_файл(복사본) != ядро_хэш: raise SystemExit('SD фото_ЗНАЧЕН ядро_ЗНАЧЕН 불일치')
        экземпляр_Настройки = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(задача_корень/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(экземпляр_Настройки)])
        if экземпляр_Настройки.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP экран Настройки 불일치')
    LOG_ЗАПИСЬ = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': ядро_хэш,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': исключение_Список, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(чек_разрешение['resolutions']),
            'sd_framebuffer_resolution': спецификация['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Название:хэш_файл(задача_корень/'dist'/Название) for Название in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (проверка_путь/'native-runtime-summary.json').write_text(json.dumps(LOG_ЗАПИСЬ,ensure_ascii=False,indent=2)+'\n')
    print('PASS: текущий_товар 커널의',len(기록들),'개 통합 испытания LOG_ЗАПИСЬ, русский исключение',len(исключение_Список),'Класс_Определение, SD фото_ЗНАЧЕН·ZIP 일치')

if __name__ == '__main__': запустить()
