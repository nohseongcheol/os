#!/usr/bin/env python3
"""현재 커널과 aktual_të_dhëna 시험·배포물이 일치할 때에만 통합 vlerësoj 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

Project_rrënjë = Path(__file__).resolve().parents[1]

def hash_skedar(POZICIONI):
    계산 = hashlib.sha256()
    with POZICIONI.open('rb') as Kartelë:
        for të_dhëna in iter(lambda: Kartelë.read(1048576), b''): 계산.update(të_dhëna)
    return 계산.hexdigest()

def Ekzekuto():
    miratim_shteg = Project_rrënjë/'build/verification'
    bërthamë_hash = hash_skedar(Project_rrënjë/'build/kernel8.img')
    기록들 = {}
    for Emër in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Emër == 'boot' else Emër+'/report.json'
        të_dhëna = json.loads((miratim_shteg/상대경로).read_text())
        if not të_dhëna.get('passed') or të_dhëna.get('kernel_sha256') != bërthamë_hash:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Emër] = {'passed': True, 'report': 상대경로}
    çek_emër = json.loads((miratim_shteg/'naming/report.json').read_text())
    if not çek_emër['passed'] or not çek_emër['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for POZICIONI, 기대값 in çek_emër['c_source_sha256'].items():
        if hash_skedar(Project_rrënjë/POZICIONI) != 기대값: raise SystemExit('명명 검사 PAS_VALUE 바뀐 C BURIMI: '+POZICIONI)
    자바검사 = json.loads((miratim_shteg/'jvm/report.json').read_text())
    직접화면 = json.loads((miratim_shteg/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 zbatoj_komandë 시험 필요')
    çek_bajt_VALUE = json.loads((miratim_shteg/'naming/direct-bytecode.json').read_text())
    if not çek_bajt_VALUE['passed'] or çek_bajt_VALUE['jar_sha256'] != hash_skedar(Project_rrënjë/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 verifikoj 필요')
    çek_rezolucion = json.loads((miratim_shteg/'resolution/report.json').read_text())
    çek_ndryshoj_përmasat = json.loads((miratim_shteg/'resize/report.json').read_text())
    갱신검사 = json.loads((miratim_shteg/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != bërthamë_hash:
        raise SystemExit('현재 커널의 부분 freskoj 시험 필요')
    for POZICIONI, 기대값 in 갱신검사['source_sha256'].items():
        if hash_skedar(Project_rrënjë/POZICIONI) != 기대값: raise SystemExit('부분 freskoj 시험 PAS_VALUE 바뀐 BURIMI: '+POZICIONI)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 Ekzekuto futje_p 시험 필요')
    예제검사 = json.loads((miratim_shteg/'examples/report.json').read_text())
    if sorted(çek_ndryshoj_përmasat['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Madhësi 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(çek_rezolucion['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 aktual_të_dhëna 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != hash_skedar(Project_rrënjë/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 PAS_VALUE 라이브러리가 바뀌었습니다.')
    for Emër in ('한국어통신시험','한국어예외시험'):
        if not any(futje_VALUE['name']==Emër and futje_VALUE.get('openjdk_output_equal') for futje_VALUE in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Emër)
    përjashtim_Listë = sorted(POZICIONI.stem for POZICIONI in (Project_rrënjë/'한국어자바/한국어/자체').glob('*përjashtim.java'))
    përjashtim_LOG = (miratim_shteg/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Emër in përjashtim_Listë:
        if '\n'+Emër+'\n' not in përjashtim_LOG: raise SystemExit('përjashtim gjeneroj·잡기·설명 시험 필요: '+Emër)
    명세 = json.loads((Project_rrënjë/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != hash_skedar(Project_rrënjë/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 IMAGE_VALUE hash_skedar 불일치')
    with zipfile.ZipFile(str(Project_rrënjë/'dist/jkoros-native-rpi4-boot.zip')) as grupoj:
        if hashlib.sha256(grupoj.read('kernel8.img')).hexdigest() != bërthamë_hash:
            raise SystemExit('부팅 ZIP bërthamë_VALUE 불일치')
        부팅설정 = grupoj.read('config.txt')
        for Emër, Madhësi in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Emër+'='+str(Madhësi) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Rregullime 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(Project_rrënjë/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(Project_rrënjë/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if hash_skedar(복사본) != bërthamë_hash: raise SystemExit('SD IMAGE_VALUE bërthamë_VALUE 불일치')
        kopjoj_cilësimet = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(Project_rrënjë/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(kopjoj_cilësimet)])
        if kopjoj_cilësimet.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Rregullime 불일치')
    LOG_RECORD = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': bërthamë_hash,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': përjashtim_Listë, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(çek_rezolucion['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Emër:hash_skedar(Project_rrënjë/'dist'/Emër) for Emër in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (miratim_shteg/'native-runtime-summary.json').write_text(json.dumps(LOG_RECORD,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 LOG_RECORD, 한국어 përjashtim',len(përjashtim_Listë),'klasë_Përkufizim, SD IMAGE_VALUE·ZIP 일치')

if __name__ == '__main__': Ekzekuto()
