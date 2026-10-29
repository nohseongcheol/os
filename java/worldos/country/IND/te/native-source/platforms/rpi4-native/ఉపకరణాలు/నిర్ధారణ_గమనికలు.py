#!/usr/bin/env python3
"""현재 커널과 వాస్తవ_డేటా 시험·배포물이 일치할 때에만 통합 నిర్థారీకరించు 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

ప్రొజెక్ట్_మూలం = Path(__file__).resolve().parents[1]

def హాష్_ఫైలు(పాత్):
    계산 = hashlib.sha256()
    with పాత్.open('rb') as దస్త్రం:
        for డేటా in iter(lambda: దస్త్రం.read(1048576), b''): 계산.update(డేటా)
    return 계산.hexdigest()

def నడుపుము():
    నిర్ధారణ_పథం = ప్రొజెక్ట్_మూలం/'build/verification'
    కెర్నల్_హాష్ = హాష్_ఫైలు(ప్రొజెక్ట్_మూలం/'build/kernel8.img')
    기록들 = {}
    for పేరు in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if పేరు == 'boot' else పేరు+'/report.json'
        డేటా = json.loads((నిర్ధారణ_పథం/상대경로).read_text())
        if not డేటా.get('passed') or డేటా.get('kernel_sha256') != కెర్నల్_హాష్:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[పేరు] = {'passed': True, 'report': 상대경로}
    తనిఖీ_పేరు = json.loads((నిర్ధారణ_పథం/'naming/report.json').read_text())
    if not తనిఖీ_పేరు['passed'] or not తనిఖీ_పేరు['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for పాత్, 기대값 in తనిఖీ_పేరు['c_source_sha256'].items():
        if హాష్_ఫైలు(ప్రొజెక్ట్_మూలం/పాత్) != 기대값: raise SystemExit('명명 검사 వెనుకకు_మూల్యం 바뀐 C వనరు: '+పాత్)
    자바검사 = json.loads((నిర్ధారణ_పథం/'jvm/report.json').read_text())
    직접화면 = json.loads((నిర్ధారణ_పథం/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 అమలు_చేయి_ఆదేశం 시험 필요')
    తనిఖీ_బైట్_మూల్యం = json.loads((నిర్ధారణ_పథం/'naming/direct-bytecode.json').read_text())
    if not తనిఖీ_బైట్_మూల్యం['passed'] or తనిఖీ_బైట్_మూల్యం['jar_sha256'] != హాష్_ఫైలు(ప్రొజెక్ట్_మూలం/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 సరిచూడు 필요')
    తనిఖీ_స్పష్టత = json.loads((నిర్ధారణ_పథం/'resolution/report.json').read_text())
    తనిఖీ_పరిమాణం_మార్చు = json.loads((నిర్ధారణ_పథం/'resize/report.json').read_text())
    갱신검사 = json.loads((నిర్ధారణ_పథం/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != కెర్నల్_హాష్:
        raise SystemExit('현재 커널의 부분 పునశ్చరించు 시험 필요')
    for పాత్, 기대값 in 갱신검사['source_sha256'].items():
        if హాష్_ఫైలు(ప్రొజెక్ట్_మూలం/పాత్) != 기대값: raise SystemExit('부분 పునశ్చరించు 시험 వెనుకకు_మూల్యం 바뀐 వనరు: '+పాత్)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 నడుపుము ప్రవేశం_పాయింట్ 시험 필요')
    예제검사 = json.loads((నిర్ధారణ_పథం/'examples/report.json').read_text())
    if sorted(తనిఖీ_పరిమాణం_మార్చు['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 పరిమాణం 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(తనిఖీ_స్పష్టత['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 వాస్తవ_డేటా 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != హాష్_ఫైలు(ప్రొజెక్ట్_మూలం/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 వెనుకకు_మూల్యం 라이브러리가 바뀌었습니다.')
    for పేరు in ('한국어통신시험','한국어예외시험'):
        if not any(ప్రవేశం_మూల్యం['name']==పేరు and ప్రవేశం_మూల్యం.get('openjdk_output_equal') for ప్రవేశం_మూల్యం in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+పేరు)
    మినహాయింపు_జాబితా = sorted(పాత్.stem for పాత్ in (ప్రొజెక్ట్_మూలం/'한국어자바/한국어/자체').glob('*మినహాయింపు.java'))
    మినహాయింపు_లాగ్ = (నిర్ధారణ_పథం/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for పేరు in మినహాయింపు_జాబితా:
        if '\n'+పేరు+'\n' not in మినహాయింపు_లాగ్: raise SystemExit('మినహాయింపు రూపొందించు·잡기·설명 시험 필요: '+పేరు)
    명세 = json.loads((ప్రొజెక్ట్_మూలం/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != హాష్_ఫైలు(ప్రొజెక్ట్_మూలం/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 చిత్రం_మూల్యం హాష్_ఫైలు 불일치')
    with zipfile.ZipFile(str(ప్రొజెక్ట్_మూలం/'dist/jkoros-native-rpi4-boot.zip')) as బండిల్:
        if hashlib.sha256(బండిల్.read('kernel8.img')).hexdigest() != కెర్నల్_హాష్:
            raise SystemExit('부팅 ZIP కెర్నల్_మూల్యం 불일치')
        부팅설정 = బండిల్.read('config.txt')
        for పేరు, పరిమాణం in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+పేరు+'='+str(పరిమాణం) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 అమరికలు 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(ప్రొజెక్ట్_మూలం/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(ప్రొజెక్ట్_మూలం/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if హాష్_ఫైలు(복사본) != కెర్నల్_హాష్: raise SystemExit('SD చిత్రం_మూల్యం కెర్నల్_మూల్యం 불일치')
        కాపీ_సెట్టింగ్_లు = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(ప్రొజెక్ట్_మూలం/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(కాపీ_సెట్టింగ్_లు)])
        if కాపీ_సెట్టింగ్_లు.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 అమరికలు 불일치')
    లాగ్_వరుస = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': కెర్నల్_హాష్,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': మినహాయింపు_జాబితా, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(తనిఖీ_స్పష్టత['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {పేరు:హాష్_ఫైలు(ప్రొజెక్ట్_మూలం/'dist'/పేరు) for పేరు in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (నిర్ధారణ_పథం/'native-runtime-summary.json').write_text(json.dumps(లాగ్_వరుస,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 లాగ్_వరుస, 한국어 మినహాయింపు',len(మినహాయింపు_జాబితా),'తరగతి_నిర్వచనం, SD చిత్రం_మూల్యం·ZIP 일치')

if __name__ == '__main__': నడుపుము()
