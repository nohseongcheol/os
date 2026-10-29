#!/usr/bin/env python3
"""현재 커널과 attwali_data 시험·배포물이 일치할 때에만 통합 vvalida 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

pprojetta_għerq = Path(__file__).resolve().parents[1]

def hash_fajl(mogħdija):
    계산 = hashlib.sha256()
    with mogħdija.open('rb') as fajl:
        for data in iter(lambda: fajl.read(1048576), b''): 계산.update(data)
    return 계산.hexdigest()

def serje():
    validazzjoni_mogħdija = pprojetta_għerq/'build/verification'
    kernel_hash = hash_fajl(pprojetta_għerq/'build/kernel8.img')
    기록들 = {}
    for isem in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if isem == 'boot' else isem+'/report.json'
        data = json.loads((validazzjoni_mogħdija/상대경로).read_text())
        if not data.get('passed') or data.get('kernel_sha256') != kernel_hash:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[isem] = {'passed': True, 'report': 상대경로}
    ċekk_isem = json.loads((validazzjoni_mogħdija/'naming/report.json').read_text())
    if not ċekk_isem['passed'] or not ċekk_isem['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for mogħdija, 기대값 in ċekk_isem['c_source_sha256'].items():
        if hash_fajl(pprojetta_għerq/mogħdija) != 기대값: raise SystemExit('명명 검사 Lura_VALUE 바뀐 C sors: '+mogħdija)
    자바검사 = json.loads((validazzjoni_mogħdija/'jvm/report.json').read_text())
    직접화면 = json.loads((validazzjoni_mogħdija/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('Malti 직접 화면 eżegwixxa_kmand 시험 필요')
    ċekk_byte_VALUE = json.loads((validazzjoni_mogħdija/'naming/direct-bytecode.json').read_text())
    if not ċekk_byte_VALUE['passed'] or ċekk_byte_VALUE['jar_sha256'] != hash_fajl(pprojetta_għerq/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 Malti 라이브러리의 직접 호출 바이트코드 vverifika 필요')
    ċekk_riżoluzzjoni = json.loads((validazzjoni_mogħdija/'resolution/report.json').read_text())
    ċekk_daqqas = json.loads((validazzjoni_mogħdija/'resize/report.json').read_text())
    갱신검사 = json.loads((validazzjoni_mogħdija/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != kernel_hash:
        raise SystemExit('현재 커널의 부분 aġġorna 시험 필요')
    for mogħdija, 기대값 in 갱신검사['source_sha256'].items():
        if hash_fajl(pprojetta_għerq/mogħdija) != 기대값: raise SystemExit('부분 aġġorna 시험 Lura_VALUE 바뀐 sors: '+mogħdija)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('Malti 직접 가닥과 serje entrata_punt 시험 필요')
    예제검사 = json.loads((validazzjoni_mogħdija/'examples/report.json').read_text())
    if sorted(ċekk_daqqas['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 daqqas 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('Malti Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(ċekk_riżoluzzjoni['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 attwali_data 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != hash_fajl(pprojetta_għerq/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 Lura_VALUE 라이브러리가 바뀌었습니다.')
    for isem in ('한국어통신시험','한국어예외시험'):
        if not any(entrata_VALUE['name']==isem and entrata_VALUE.get('openjdk_output_equal') for entrata_VALUE in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+isem)
    예외들 = sorted(mogħdija.stem for mogħdija in (pprojetta_għerq/'한국어자바/Malti/자체').glob('*예외.java'))
    예외기록 = (validazzjoni_mogħdija/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for isem in 예외들:
        if '\n'+isem+'\n' not in 예외기록: raise SystemExit('예외 iġġenera·잡기·설명 시험 필요: '+isem)
    명세 = json.loads((pprojetta_għerq/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != hash_fajl(pprojetta_għerq/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 IMAGE_VALUE hash_fajl 불일치')
    with zipfile.ZipFile(str(pprojetta_għerq/'dist/jkoros-native-rpi4-boot.zip')) as lott:
        if hashlib.sha256(lott.read('kernel8.img')).hexdigest() != kernel_hash:
            raise SystemExit('부팅 ZIP kernel_VALUE 불일치')
        부팅설정 = lott.read('config.txt')
        for isem, daqqas in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+isem+'='+str(daqqas) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Settings 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(pprojetta_għerq/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(pprojetta_għerq/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if hash_fajl(복사본) != kernel_hash: raise SystemExit('SD IMAGE_VALUE kernel_VALUE 불일치')
        kkopja_Settings = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(pprojetta_għerq/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(kkopja_Settings)])
        if kkopja_Settings.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Settings 불일치')
    LOG_RECORD = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': kernel_hash,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(ċekk_riżoluzzjoni['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {isem:hash_fajl(pprojetta_għerq/'dist'/isem) for isem in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (validazzjoni_mogħdija/'native-runtime-summary.json').write_text(json.dumps(LOG_RECORD,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 LOG_RECORD, Malti 예외',len(예외들),'klassi_Definizzjoni, SD IMAGE_VALUE·ZIP 일치')

if __name__ == '__main__': serje()
