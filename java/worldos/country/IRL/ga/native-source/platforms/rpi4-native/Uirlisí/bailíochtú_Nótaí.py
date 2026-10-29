#!/usr/bin/env python3
"""현재 커널과 iarbhír_sonraí 시험·배포물이 일치할 때에만 통합 bailíochtaigh 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

teilgean_fréamh = Path(__file__).resolve().parents[1]

def hais_comhad(CONAIR):
    계산 = hashlib.sha256()
    with CONAIR.open('rb') as Comhad:
        for sonraí in iter(lambda: Comhad.read(1048576), b''): 계산.update(sonraí)
    return 계산.hexdigest()

def Rith_2():
    bailíochtú_cosán = teilgean_fréamh/'build/verification'
    eithne_hais = hais_comhad(teilgean_fréamh/'build/kernel8.img')
    기록들 = {}
    for Ainm in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Ainm == 'boot' else Ainm+'/report.json'
        sonraí = json.loads((bailíochtú_cosán/상대경로).read_text())
        if not sonraí.get('passed') or sonraí.get('kernel_sha256') != eithne_hais:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Ainm] = {'passed': True, 'report': 상대경로}
    seic_ainm = json.loads((bailíochtú_cosán/'naming/report.json').read_text())
    if not seic_ainm['passed'] or not seic_ainm['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for CONAIR, 기대값 in seic_ainm['c_source_sha256'].items():
        if hais_comhad(teilgean_fréamh/CONAIR) != 기대값: raise SystemExit('명명 검사 Siar_VALUE 바뀐 C FOINSE: '+CONAIR)
    자바검사 = json.loads((bailíochtú_cosán/'jvm/report.json').read_text())
    직접화면 = json.loads((bailíochtú_cosán/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('Gaeilge 직접 화면 Rith_ordú 시험 필요')
    seic_beart_VALUE = json.loads((bailíochtú_cosán/'naming/direct-bytecode.json').read_text())
    if not seic_beart_VALUE['passed'] or seic_beart_VALUE['jar_sha256'] != hais_comhad(teilgean_fréamh/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 Gaeilge 라이브러리의 직접 호출 바이트코드 fíoraigh 필요')
    seic_taifeach = json.loads((bailíochtú_cosán/'resolution/report.json').read_text())
    seic_socraigh_méid = json.loads((bailíochtú_cosán/'resize/report.json').read_text())
    갱신검사 = json.loads((bailíochtú_cosán/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != eithne_hais:
        raise SystemExit('현재 커널의 부분 athnuaigh 시험 필요')
    for CONAIR, 기대값 in 갱신검사['source_sha256'].items():
        if hais_comhad(teilgean_fréamh/CONAIR) != 기대값: raise SystemExit('부분 athnuaigh 시험 Siar_VALUE 바뀐 FOINSE: '+CONAIR)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('Gaeilge 직접 가닥과 Rith_2 iontráil_pointe 시험 필요')
    예제검사 = json.loads((bailíochtú_cosán/'examples/report.json').read_text())
    if sorted(seic_socraigh_méid['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Méid 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('Gaeilge Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(seic_taifeach['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 iarbhír_sonraí 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != hais_comhad(teilgean_fréamh/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 Siar_VALUE 라이브러리가 바뀌었습니다.')
    for Ainm in ('한국어통신시험','한국어예외시험'):
        if not any(iontráil_VALUE['name']==Ainm and iontráil_VALUE.get('openjdk_output_equal') for iontráil_VALUE in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Ainm)
    eisceacht_Liosta = sorted(CONAIR.stem for CONAIR in (teilgean_fréamh/'한국어자바/Gaeilge/자체').glob('*eisceacht.java'))
    eisceacht_LOG = (bailíochtú_cosán/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Ainm in eisceacht_Liosta:
        if '\n'+Ainm+'\n' not in eisceacht_LOG: raise SystemExit('eisceacht giniúint·잡기·설명 시험 필요: '+Ainm)
    명세 = json.loads((teilgean_fréamh/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != hais_comhad(teilgean_fréamh/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 IMAGE_VALUE hais_comhad 불일치')
    with zipfile.ZipFile(str(teilgean_fréamh/'dist/jkoros-native-rpi4-boot.zip')) as beart:
        if hashlib.sha256(beart.read('kernel8.img')).hexdigest() != eithne_hais:
            raise SystemExit('부팅 ZIP eithne_VALUE 불일치')
        부팅설정 = beart.read('config.txt')
        for Ainm, Méid in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Ainm+'='+str(Méid) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Socruithe 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(teilgean_fréamh/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(teilgean_fréamh/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if hais_comhad(복사본) != eithne_hais: raise SystemExit('SD IMAGE_VALUE eithne_VALUE 불일치')
        ásc_Socruithe = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(teilgean_fréamh/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(ásc_Socruithe)])
        if ásc_Socruithe.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Socruithe 불일치')
    LOG_ró = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': eithne_hais,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': eisceacht_Liosta, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(seic_taifeach['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Ainm:hais_comhad(teilgean_fréamh/'dist'/Ainm) for Ainm in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (bailíochtú_cosán/'native-runtime-summary.json').write_text(json.dumps(LOG_ró,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 LOG_ró, Gaeilge eisceacht',len(eisceacht_Liosta),'aicme_Sainmhíniú, SD IMAGE_VALUE·ZIP 일치')

if __name__ == '__main__': Rith_2()
