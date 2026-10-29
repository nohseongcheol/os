#!/usr/bin/env python3
"""чинний_елемент 커널과 фактично_дані випробування·배포물이 일치할 때에만 통합 затвердити 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

Дії_корінь = Path(__file__).resolve().parents[1]

def геш_код_Файл(шлях):
    계산 = hashlib.sha256()
    with шлях.open('rb') as файл:
        for дані in iter(lambda: файл.read(1048576), b''): 계산.update(дані)
    return 계산.hexdigest()

def запустити():
    перевірка_шлях = Дії_корінь/'build/verification'
    ядро_геш_код = геш_код_Файл(Дії_корінь/'build/kernel8.img')
    기록들 = {}
    for Назва in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        відносний_шлях = 'report.json' if Назва == 'boot' else Назва+'/report.json'
        дані = json.loads((перевірка_шлях/відносний_шлях).read_text())
        if not дані.get('passed') or дані.get('kernel_sha256') != ядро_геш_код:
            raise SystemExit('чинний_елемент 커널에 대한 성공 기록이 필요합니다: '+відносний_шлях)
        기록들[Назва] = {'passed': True, 'report': відносний_шлях}
    перевіряти_ім_я = json.loads((перевірка_шлях/'naming/report.json').read_text())
    if not перевіряти_ім_я['passed'] or not перевіряти_ім_я['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for шлях, 기대값 in перевіряти_ім_я['c_source_sha256'].items():
        if геш_код_Файл(Дії_корінь/шлях) != 기대값: raise SystemExit('명명 검사 НАЗАД_значення 바뀐 C вихіднийКод: '+шлях)
    자바검사 = json.loads((перевірка_шлях/'jvm/report.json').read_text())
    직접화면 = json.loads((перевірка_шлях/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('українська 직접 화면 Виконати_команда випробування 필요')
    перевіряти_байт_значення = json.loads((перевірка_шлях/'naming/direct-bytecode.json').read_text())
    if not перевіряти_байт_значення['passed'] or перевіряти_байт_значення['jar_sha256'] != геш_код_Файл(Дії_корінь/'dist/jkoros-native-korean.jar'):
        raise SystemExit('чинний_елемент українська 라이브러리의 직접 호출 바이트코드 перевіряти 필요')
    перевіряти_роздільна_здатність = json.loads((перевірка_шлях/'resolution/report.json').read_text())
    перевіряти_змінювати_розмір = json.loads((перевірка_шлях/'resize/report.json').read_text())
    갱신검사 = json.loads((перевірка_шлях/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != ядро_геш_код:
        raise SystemExit('чинний_елемент 커널의 부분 оновлювати випробування 필요')
    for шлях, 기대값 in 갱신검사['source_sha256'].items():
        if геш_код_Файл(Дії_корінь/шлях) != 기대값: raise SystemExit('부분 оновлювати випробування НАЗАД_значення 바뀐 вихіднийКод: '+шлях)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('українська 직접 가닥과 запустити запис_бал випробування 필요')
    예제검사 = json.loads((перевірка_шлях/'examples/report.json').read_text())
    if sorted(перевіряти_змінювати_розмір['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Розмір 조절 випробування 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('українська Swing 창을 포함한 예제 13개 випробування 필요')
    if sorted(перевіряти_роздільна_здатність['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 фактично_дані 화면 випробування 필요')
    if 자바검사['korean_library_sha256'] != геш_код_Файл(Дії_корінь/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 випробування НАЗАД_значення 라이브러리가 바뀌었습니다.')
    for Назва in ('한국어통신시험','한국어예외시험'):
        if not any(запис_значення_962f286b['name']==Назва and запис_значення_962f286b.get('openjdk_output_equal') for запис_значення_962f286b in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 випробування 필요: '+Назва)
    виняток_список = sorted(шлях.stem for шлях in (Дії_корінь/'한국어자바/українська/своє').glob('*виняток.java'))
    виняток_журнал = (перевірка_шлях/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Назва in виняток_список:
        if '\n'+Назва+'\n' not in виняток_журнал: raise SystemExit('виняток генерувати·잡기·설명 випробування 필요: '+Назва)
    명세 = json.loads((Дії_корінь/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != геш_код_Файл(Дії_корінь/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 фото_значення геш_код_Файл 불일치')
    with zipfile.ZipFile(str(Дії_корінь/'dist/jkoros-native-rpi4-boot.zip')) as набір:
        if hashlib.sha256(набір.read('kernel8.img')).hexdigest() != ядро_геш_код:
            raise SystemExit('запуск_машини ZIP ядро_значення 불일치')
        부팅설정 = набір.read('config.txt')
        for Назва, Розмір in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Назва+'='+str(Розмір) not in 부팅설정.decode().splitlines():
                raise SystemExit('запуск_машини ZIP 화면 Налаштування 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(Дії_корінь/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(Дії_корінь/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if геш_код_Файл(복사본) != ядро_геш_код: raise SystemExit('SD фото_значення ядро_значення 불일치')
        екземпляр_Настройки = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(Дії_корінь/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(екземпляр_Настройки)])
        if екземпляр_Настройки.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Налаштування 불일치')
    журнал_запис = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': ядро_геш_код,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': виняток_список, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(перевіряти_роздільна_здатність['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Назва:геш_код_Файл(Дії_корінь/'dist'/Назва) for Назва in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (перевірка_шлях/'native-runtime-summary.json').write_text(json.dumps(журнал_запис,ensure_ascii=False,indent=2)+'\n')
    print('PASS: чинний_елемент 커널의',len(기록들),'개 통합 випробування журнал_запис, українська виняток',len(виняток_список),'Клас_Визначення, SD фото_значення·ZIP 일치')

if __name__ == '__main__': запустити()
