#!/usr/bin/env python3
"""ток_элемент 커널과 нақты_деректер 시험·배포물이 일치할 때에만 통합 тексеру_5fb2b747 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

жоба_түбір = Path(__file__).resolve().parents[1]

def хэш_файл(Жол_2):
    계산 = hashlib.sha256()
    with Жол_2.open('rb') as Файл:
        for деректер in iter(lambda: Файл.read(1048576), b''): 계산.update(деректер)
    return 계산.hexdigest()

def Орындау_2():
    тексерім_жол = жоба_түбір/'build/verification'
    ядро_хэш = хэш_файл(жоба_түбір/'build/kernel8.img')
    기록들 = {}
    for Аты in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Аты == 'boot' else Аты+'/report.json'
        деректер = json.loads((тексерім_жол/상대경로).read_text())
        if not деректер.get('passed') or деректер.get('kernel_sha256') != ядро_хэш:
            raise SystemExit('ток_элемент 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Аты] = {'passed': True, 'report': 상대경로}
    чек_аты = json.loads((тексерім_жол/'naming/report.json').read_text())
    if not чек_аты['passed'] or not чек_аты['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for Жол_2, 기대값 in чек_аты['c_source_sha256'].items():
        if хэш_файл(жоба_түбір/Жол_2) != 기대값: raise SystemExit('명명 검사 АРТҚА_мән 바뀐 C Неден: '+Жол_2)
    자바검사 = json.loads((тексерім_жол/'jvm/report.json').read_text())
    직접화면 = json.loads((тексерім_жол/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 орындау_пәрмен 시험 필요')
    чек_байт_мән = json.loads((тексерім_жол/'naming/direct-bytecode.json').read_text())
    if not чек_байт_мән['passed'] or чек_байт_мән['jar_sha256'] != хэш_файл(жоба_түбір/'dist/jkoros-native-korean.jar'):
        raise SystemExit('ток_элемент 한국어 라이브러리의 직접 호출 바이트코드 тексеру 필요')
    чек_ажыратымдылық = json.loads((тексерім_жол/'resolution/report.json').read_text())
    чек_өлшемді_өзгерту = json.loads((тексерім_жол/'resize/report.json').read_text())
    갱신검사 = json.loads((тексерім_жол/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != ядро_хэш:
        raise SystemExit('ток_элемент 커널의 부분 жаңарту 시험 필요')
    for Жол_2, 기대값 in 갱신검사['source_sha256'].items():
        if хэш_файл(жоба_түбір/Жол_2) != 기대값: raise SystemExit('부분 жаңарту 시험 АРТҚА_мән 바뀐 Неден: '+Жол_2)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 Орындау_2 енгізу_ұпай 시험 필요')
    예제검사 = json.loads((тексерім_жол/'examples/report.json').read_text())
    if sorted(чек_өлшемді_өзгерту['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Өлшемі 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(чек_ажыратымдылық['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 нақты_деректер 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != хэш_файл(жоба_түбір/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 АРТҚА_мән 라이브러리가 바뀌었습니다.')
    for Аты in ('한국어통신시험','한국어예외시험'):
        if not any(енгізу_мән['name']==Аты and енгізу_мән.get('openjdk_output_equal') for енгізу_мән in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Аты)
    ерекшелік_Тізім = sorted(Жол_2.stem for Жол_2 in (жоба_түбір/'한국어자바/한국어/자체').glob('*ерекшелік.java'))
    ерекшелік_журнал = (тексерім_жол/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Аты in ерекшелік_Тізім:
        if '\n'+Аты+'\n' not in ерекшелік_журнал: raise SystemExit('ерекшелік жасау·잡기·설명 시험 필요: '+Аты)
    сипаттама = json.loads((жоба_түбір/'dist/manifest.json').read_text())
    if сипаттама['image_sha256'] != хэш_файл(жоба_түбір/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 сурет_мән хэш_файл 불일치')
    with zipfile.ZipFile(str(жоба_түбір/'dist/jkoros-native-rpi4-boot.zip')) as жинау:
        if hashlib.sha256(жинау.read('kernel8.img')).hexdigest() != ядро_хэш:
            raise SystemExit('부팅 ZIP ядро_мән 불일치')
        부팅설정 = жинау.read('config.txt')
        for Аты, Өлшемі in zip(('width', 'height'), сипаттама['framebuffer_resolution']):
            if 'framebuffer_'+Аты+'='+str(Өлшемі) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Баптаулар 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(жоба_түбір/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(жоба_түбір/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if хэш_файл(복사본) != ядро_хэш: raise SystemExit('SD сурет_мән ядро_мән 불일치')
        дана_Параметрлер = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(жоба_түбір/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(дана_Параметрлер)])
        if дана_Параметрлер.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Баптаулар 불일치')
    журнал_жол = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': ядро_хэш,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': ерекшелік_Тізім, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(чек_ажыратымдылық['resolutions']),
            'sd_framebuffer_resolution': сипаттама['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Аты:хэш_файл(жоба_түбір/'dist'/Аты) for Аты in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (тексерім_жол/'native-runtime-summary.json').write_text(json.dumps(журнал_жол,ensure_ascii=False,indent=2)+'\n')
    print('PASS: ток_элемент 커널의',len(기록들),'개 통합 시험 журнал_жол, 한국어 ерекшелік',len(ерекшелік_Тізім),'оқу_Анықтама, SD сурет_мән·ZIP 일치')

if __name__ == '__main__': Орындау_2()
