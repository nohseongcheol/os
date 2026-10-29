#!/usr/bin/env python3
"""현재 커널과 реален_податоци 시험·배포물이 일치할 때에만 통합 потврди 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

Project_корен = Path(__file__).resolve().parents[1]

def хаш_датотека(ПАТЕКА):
    계산 = hashlib.sha256()
    with ПАТЕКА.open('rb') as Датотека:
        for податоци in iter(lambda: Датотека.read(1048576), b''): 계산.update(податоци)
    return 계산.hexdigest()

def Изврши_2():
    проверка_патека = Project_корен/'build/verification'
    јадро_хаш = хаш_датотека(Project_корен/'build/kernel8.img')
    기록들 = {}
    for Име in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Име == 'boot' else Име+'/report.json'
        податоци = json.loads((проверка_патека/상대경로).read_text())
        if not податоци.get('passed') or податоци.get('kernel_sha256') != јадро_хаш:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Име] = {'passed': True, 'report': 상대경로}
    провери_име = json.loads((проверка_патека/'naming/report.json').read_text())
    if not провери_име['passed'] or not провери_име['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for ПАТЕКА, 기대값 in провери_име['c_source_sha256'].items():
        if хаш_датотека(Project_корен/ПАТЕКА) != 기대값: raise SystemExit('명명 검사 Назад_VALUE 바뀐 C ИЗВОР: '+ПАТЕКА)
    자바검사 = json.loads((проверка_патека/'jvm/report.json').read_text())
    직접화면 = json.loads((проверка_патека/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('Македонски 직접 화면 Изврши_наредба 시험 필요')
    провери_бајт_VALUE = json.loads((проверка_патека/'naming/direct-bytecode.json').read_text())
    if not провери_бајт_VALUE['passed'] or провери_бајт_VALUE['jar_sha256'] != хаш_датотека(Project_корен/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 Македонски 라이브러리의 직접 호출 바이트코드 провери 필요')
    провери_резолуција = json.loads((проверка_патека/'resolution/report.json').read_text())
    провери_големина = json.loads((проверка_патека/'resize/report.json').read_text())
    갱신검사 = json.loads((проверка_патека/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != јадро_хаш:
        raise SystemExit('현재 커널의 부분 освежи 시험 필요')
    for ПАТЕКА, 기대값 in 갱신검사['source_sha256'].items():
        if хаш_датотека(Project_корен/ПАТЕКА) != 기대값: raise SystemExit('부분 освежи 시험 Назад_VALUE 바뀐 ИЗВОР: '+ПАТЕКА)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('Македонски 직접 가닥과 Изврши_2 внес_поен 시험 필요')
    예제검사 = json.loads((проверка_патека/'examples/report.json').read_text())
    if sorted(провери_големина['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Големина 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('Македонски Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(провери_резолуција['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 реален_податоци 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != хаш_датотека(Project_корен/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 Назад_VALUE 라이브러리가 바뀌었습니다.')
    for Име in ('한국어통신시험','한국어예외시험'):
        if not any(внес_VALUE['name']==Име and внес_VALUE.get('openjdk_output_equal') for внес_VALUE in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Име)
    исклучок_Список = sorted(ПАТЕКА.stem for ПАТЕКА in (Project_корен/'한국어자바/Македонски/자체').glob('*исклучок.java'))
    исклучок_LOG = (проверка_патека/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Име in исклучок_Список:
        if '\n'+Име+'\n' not in исклучок_LOG: raise SystemExit('исклучок генерира·잡기·설명 시험 필요: '+Име)
    명세 = json.loads((Project_корен/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != хаш_датотека(Project_корен/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 IMAGE_VALUE хаш_датотека 불일치')
    with zipfile.ZipFile(str(Project_корен/'dist/jkoros-native-rpi4-boot.zip')) as пакет:
        if hashlib.sha256(пакет.read('kernel8.img')).hexdigest() != јадро_хаш:
            raise SystemExit('부팅 ZIP јадро_VALUE 불일치')
        부팅설정 = пакет.read('config.txt')
        for Име, Големина in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Име+'='+str(Големина) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Подесувања 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(Project_корен/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(Project_корен/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if хаш_датотека(복사본) != јадро_хаш: raise SystemExit('SD IMAGE_VALUE јадро_VALUE 불일치')
        копирај_Параметри = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(Project_корен/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(копирај_Параметри)])
        if копирај_Параметри.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Подесувања 불일치')
    LOG_ред = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': јадро_хаш,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': исклучок_Список, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(провери_резолуција['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Име:хаш_датотека(Project_корен/'dist'/Име) for Име in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (проверка_патека/'native-runtime-summary.json').write_text(json.dumps(LOG_ред,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 LOG_ред, Македонски исклучок',len(исклучок_Список),'класа_Дефиниција, SD IMAGE_VALUE·ZIP 일치')

if __name__ == '__main__': Изврши_2()
