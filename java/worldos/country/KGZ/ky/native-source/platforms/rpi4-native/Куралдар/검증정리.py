#!/usr/bin/env python3
"""현재 커널과 актуалдуу_берилмелер 시험·배포물이 일치할 때에만 통합 жарактуулугун_текшерүү 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

기준 = Path(__file__).resolve().parents[1]

def хэш_файл(ЖОЛ):
    계산 = hashlib.sha256()
    with ЖОЛ.open('rb') as Файл:
        for берилмелер in iter(lambda: Файл.read(1048576), b''): 계산.update(берилмелер)
    return 계산.hexdigest()

def Жүргүзүү():
    ырастоо_жол = 기준/'build/verification'
    өзөк_хэш = хэш_файл(기준/'build/kernel8.img')
    기록들 = {}
    for Аты in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Аты == 'boot' else Аты+'/report.json'
        берилмелер = json.loads((ырастоо_жол/상대경로).read_text())
        if not берилмелер.get('passed') or берилмелер.get('kernel_sha256') != өзөк_хэш:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Аты] = {'passed': True, 'report': 상대경로}
    чек_аты = json.loads((ырастоо_жол/'naming/report.json').read_text())
    if not чек_аты['passed'] or not чек_аты['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for ЖОЛ, 기대값 in чек_аты['c_source_sha256'].items():
        if хэш_файл(기준/ЖОЛ) != 기대값: raise SystemExit('명명 검사 Артка_маани 바뀐 C Булак: '+ЖОЛ)
    자바검사 = json.loads((ырастоо_жол/'jvm/report.json').read_text())
    직접화면 = json.loads((ырастоо_жол/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 аткаруу_буйрук 시험 필요')
    чек_байт_маани = json.loads((ырастоо_жол/'naming/direct-bytecode.json').read_text())
    if not чек_байт_маани['passed'] or чек_байт_маани['jar_sha256'] != хэш_файл(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 тууралыгын_аныктоо 필요')
    чек_чечим = json.loads((ырастоо_жол/'resolution/report.json').read_text())
    чек_көлөм = json.loads((ырастоо_жол/'resize/report.json').read_text())
    갱신검사 = json.loads((ырастоо_жол/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != өзөк_хэш:
        raise SystemExit('현재 커널의 부분 жаңылоо 시험 필요')
    for ЖОЛ, 기대값 in 갱신검사['source_sha256'].items():
        if хэш_файл(기준/ЖОЛ) != 기대값: raise SystemExit('부분 жаңылоо 시험 Артка_маани 바뀐 Булак: '+ЖОЛ)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 Жүргүзүү киргизме_жазуу_упай 시험 필요')
    예제검사 = json.loads((ырастоо_жол/'examples/report.json').read_text())
    if sorted(чек_көлөм['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Өлчөмү 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(чек_чечим['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 актуалдуу_берилмелер 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != хэш_файл(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 Артка_маани 라이브러리가 바뀌었습니다.')
    for Аты in ('한국어통신시험','한국어예외시험'):
        if not any(киргизме_жазуу_маани['name']==Аты and киргизме_жазуу_маани.get('openjdk_output_equal') for киргизме_жазуу_маани in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Аты)
    예외들 = sorted(ЖОЛ.stem for ЖОЛ in (기준/'한국어자바/한국어/자체').glob('*예외.java'))
    예외기록 = (ырастоо_жол/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Аты in 예외들:
        if '\n'+Аты+'\n' not in 예외기록: raise SystemExit('예외 생성·잡기·설명 시험 필요: '+Аты)
    명세 = json.loads((기준/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != хэш_файл(기준/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 сүрөт_маани хэш_файл 불일치')
    with zipfile.ZipFile(str(기준/'dist/jkoros-native-rpi4-boot.zip')) as пакет:
        if hashlib.sha256(пакет.read('kernel8.img')).hexdigest() != өзөк_хэш:
            raise SystemExit('부팅 ZIP өзөк_маани 불일치')
        부팅설정 = пакет.read('config.txt')
        for Аты, Өлчөмү in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Аты+'='+str(Өлчөмү) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Орнотуулар 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(기준/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if хэш_файл(복사본) != өзөк_хэш: raise SystemExit('SD сүрөт_маани өзөк_маани 불일치')
        даана_Орнотуулар = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(даана_Орнотуулар)])
        if даана_Орнотуулар.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Орнотуулар 불일치')
    жазуу_катар = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': өзөк_хэш,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(чек_чечим['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Аты:хэш_файл(기준/'dist'/Аты) for Аты in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (ырастоо_жол/'native-runtime-summary.json').write_text(json.dumps(жазуу_катар,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 жазуу_катар, 한국어 예외',len(예외들),'класс_Аныктама, SD сүрөт_маани·ZIP 일치')

if __name__ == '__main__': Жүргүзүү()
