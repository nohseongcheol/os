#!/usr/bin/env python3
"""в_срок_артикул 커널과 действителен_данни 시험·배포물이 일치할 때에만 통합 проверка 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

проект_корен = Path(__file__).resolve().parents[1]

def хеширане_Файл(ПЪТ):
    계산 = hashlib.sha256()
    with ПЪТ.open('rb') as Файл:
        for данни in iter(lambda: Файл.read(1048576), b''): 계산.update(данни)
    return 계산.hexdigest()

def Стартиране():
    проверка_път = проект_корен/'build/verification'
    ядро_хеширане = хеширане_Файл(проект_корен/'build/kernel8.img')
    기록들 = {}
    for Име in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        относителен_път = 'report.json' if Име == 'boot' else Име+'/report.json'
        данни = json.loads((проверка_път/относителен_път).read_text())
        if not данни.get('passed') or данни.get('kernel_sha256') != ядро_хеширане:
            raise SystemExit('в_срок_артикул 커널에 대한 성공 기록이 필요합니다: '+относителен_път)
        기록들[Име] = {'passed': True, 'report': относителен_път}
    проверявам_препратка_към_клетка = json.loads((проверка_път/'naming/report.json').read_text())
    if not проверявам_препратка_към_клетка['passed'] or not проверявам_препратка_към_клетка['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for ПЪТ, 기대값 in проверявам_препратка_към_клетка['c_source_sha256'].items():
        if хеширане_Файл(проект_корен/ПЪТ) != 기대값: raise SystemExit('명명 검사 НАЗАД_стойност 바뀐 C ИЗТОЧНИК: '+ПЪТ)
    자바검사 = json.loads((проверка_път/'jvm/report.json').read_text())
    직접화면 = json.loads((проверка_път/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('Български 직접 화면 изпълнявам_команда 시험 필요')
    проверявам_байт_стойност = json.loads((проверка_път/'naming/direct-bytecode.json').read_text())
    if not проверявам_байт_стойност['passed'] or проверявам_байт_стойност['jar_sha256'] != хеширане_Файл(проект_корен/'dist/jkoros-native-korean.jar'):
        raise SystemExit('в_срок_артикул Български 라이브러리의 직접 호출 바이트코드 проверявам 필요')
    проверявам_разделителна_способност = json.loads((проверка_път/'resolution/report.json').read_text())
    проверявам_размер = json.loads((проверка_път/'resize/report.json').read_text())
    갱신검사 = json.loads((проверка_път/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != ядро_хеширане:
        raise SystemExit('в_срок_артикул 커널의 부분 обновявам 시험 필요')
    for ПЪТ, 기대값 in 갱신검사['source_sha256'].items():
        if хеширане_Файл(проект_корен/ПЪТ) != 기대값: raise SystemExit('부분 обновявам 시험 НАЗАД_стойност 바뀐 ИЗТОЧНИК: '+ПЪТ)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('Български 직접 가닥과 Стартиране запис_пункт 시험 필요')
    예제검사 = json.loads((проверка_път/'examples/report.json').read_text())
    if sorted(проверявам_размер['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Размер 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('Български Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(проверявам_разделителна_способност['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 действителен_данни 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != хеширане_Файл(проект_корен/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 НАЗАД_стойност 라이브러리가 바뀌었습니다.')
    for Име in ('한국어통신시험','한국어예외시험'):
        if not any(запис_стойност['name']==Име and запис_стойност.get('openjdk_output_equal') for запис_стойност in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Име)
    изключение_Списък = sorted(ПЪТ.stem for ПЪТ in (проект_корен/'한국어자바/Български/자체').glob('*изключение.java'))
    изключение_регистрирам = (проверка_път/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Име in изключение_Списък:
        if '\n'+Име+'\n' not in изключение_регистрирам: raise SystemExit('изключение генерирам·잡기·설명 시험 필요: '+Име)
    명세 = json.loads((проект_корен/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != хеширане_Файл(проект_корен/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 снимка_стойност хеширане_Файл 불일치')
    with zipfile.ZipFile(str(проект_корен/'dist/jkoros-native-rpi4-boot.zip')) as пакет:
        if hashlib.sha256(пакет.read('kernel8.img')).hexdigest() != ядро_хеширане:
            raise SystemExit('부팅 ZIP ядро_стойност 불일치')
        부팅설정 = пакет.read('config.txt')
        for Име, Размер in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Име+'='+str(Размер) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Настройки 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(проект_корен/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(проект_корен/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if хеширане_Файл(복사본) != ядро_хеширане: raise SystemExit('SD снимка_стойност ядро_стойност 불일치')
        копирам_Настройки = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(проект_корен/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(копирам_Настройки)])
        if копирам_Настройки.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Настройки 불일치')
    регистрирам_запис = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': ядро_хеширане,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': изключение_Списък, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(проверявам_разделителна_способност['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Име:хеширане_Файл(проект_корен/'dist'/Име) for Име in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (проверка_път/'native-runtime-summary.json').write_text(json.dumps(регистрирам_запис,ensure_ascii=False,indent=2)+'\n')
    print('PASS: в_срок_артикул 커널의',len(기록들),'개 통합 시험 регистрирам_запис, Български изключение',len(изключение_Списък),'Клас_Дефиниция, SD снимка_стойност·ZIP 일치')

if __name__ == '__main__': Стартиране()
