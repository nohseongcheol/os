#!/usr/bin/env python3
"""актуелно_ставка 커널과 стваран_подаци 시험·배포물이 일치할 때에만 통합 потврдити_5fb2b747 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

пројектовати_корен = Path(__file__).resolve().parents[1]

def хеш_фајл(ПУТАЊА):
    계산 = hashlib.sha256()
    with ПУТАЊА.open('rb') as Датотека:
        for подаци in iter(lambda: Датотека.read(1048576), b''): 계산.update(подаци)
    return 계산.hexdigest()

def Покрени():
    провјера_пут = пројектовати_корен/'build/verification'
    језгро_хеш = хеш_фајл(пројектовати_корен/'build/kernel8.img')
    기록들 = {}
    for Назив in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Назив == 'boot' else Назив+'/report.json'
        подаци = json.loads((провјера_пут/상대경로).read_text())
        if not подаци.get('passed') or подаци.get('kernel_sha256') != језгро_хеш:
            raise SystemExit('актуелно_ставка 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Назив] = {'passed': True, 'report': 상대경로}
    чек_име = json.loads((провјера_пут/'naming/report.json').read_text())
    if not чек_име['passed'] or not чек_име['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for ПУТАЊА, 기대값 in чек_име['c_source_sha256'].items():
        if хеш_фајл(пројектовати_корен/ПУТАЊА) != 기대값: raise SystemExit('명명 검사 НАЗАД_вриједност 바뀐 C ИЗВОР: '+ПУТАЊА)
    자바검사 = json.loads((провјера_пут/'jvm/report.json').read_text())
    직접화면 = json.loads((провјера_пут/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 Изврши_команда 시험 필요')
    чек_бајт_вриједност = json.loads((провјера_пут/'naming/direct-bytecode.json').read_text())
    if not чек_бајт_вриједност['passed'] or чек_бајт_вриједност['jar_sha256'] != хеш_фајл(пројектовати_корен/'dist/jkoros-native-korean.jar'):
        raise SystemExit('актуелно_ставка 한국어 라이브러리의 직접 호출 바이트코드 потврдити 필요')
    чек_резолуција = json.loads((провјера_пут/'resolution/report.json').read_text())
    чек_подесити_величину = json.loads((провјера_пут/'resize/report.json').read_text())
    갱신검사 = json.loads((провјера_пут/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != језгро_хеш:
        raise SystemExit('актуелно_ставка 커널의 부분 освежити 시험 필요')
    for ПУТАЊА, 기대값 in 갱신검사['source_sha256'].items():
        if хеш_фајл(пројектовати_корен/ПУТАЊА) != 기대값: raise SystemExit('부분 освежити 시험 НАЗАД_вриједност 바뀐 ИЗВОР: '+ПУТАЊА)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 Покрени унос_поен 시험 필요')
    예제검사 = json.loads((провјера_пут/'examples/report.json').read_text())
    if sorted(чек_подесити_величину['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Величина 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(чек_резолуција['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 стваран_подаци 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != хеш_фајл(пројектовати_корен/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 НАЗАД_вриједност 라이브러리가 바뀌었습니다.')
    for Назив in ('한국어통신시험','한국어예외시험'):
        if not any(унос_вриједност['name']==Назив and унос_вриједност.get('openjdk_output_equal') for унос_вриједност in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Назив)
    изузетак_Листа = sorted(ПУТАЊА.stem for ПУТАЊА in (пројектовати_корен/'한국어자바/한국어/자체').glob('*изузетак.java'))
    изузетак_евиденција = (провјера_пут/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Назив in изузетак_Листа:
        if '\n'+Назив+'\n' not in изузетак_евиденција: raise SystemExit('изузетак генерисати·잡기·설명 시험 필요: '+Назив)
    명세 = json.loads((пројектовати_корен/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != хеш_фајл(пројектовати_корен/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 слика_вриједност хеш_фајл 불일치')
    with zipfile.ZipFile(str(пројектовати_корен/'dist/jkoros-native-rpi4-boot.zip')) as пакет:
        if hashlib.sha256(пакет.read('kernel8.img')).hexdigest() != језгро_хеш:
            raise SystemExit('부팅 ZIP језгро_вриједност 불일치')
        부팅설정 = пакет.read('config.txt')
        for Назив, Величина in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Назив+'='+str(Величина) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Поставке 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(пројектовати_корен/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(пројектовати_корен/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if хеш_фајл(복사본) != језгро_хеш: raise SystemExit('SD слика_вриједност језгро_вриједност 불일치')
        инстанца_Поставке = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(пројектовати_корен/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(инстанца_Поставке)])
        if инстанца_Поставке.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Поставке 불일치')
    евиденција_ред = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': језгро_хеш,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': изузетак_Листа, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(чек_резолуција['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Назив:хеш_фајл(пројектовати_корен/'dist'/Назив) for Назив in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (провјера_пут/'native-runtime-summary.json').write_text(json.dumps(евиденција_ред,ensure_ascii=False,indent=2)+'\n')
    print('PASS: актуелно_ставка 커널의',len(기록들),'개 통합 시험 евиденција_ред, 한국어 изузетак',len(изузетак_Листа),'класа_Дефиниција, SD слика_вриједност·ZIP 일치')

if __name__ == '__main__': Покрени()
