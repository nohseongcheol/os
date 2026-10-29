#!/usr/bin/env python3
"""현재 커널과 ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 시험·배포물이 일치할 때에만 통합 ᎪᎯᏳᏙᏗ 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

기준 = Path(__file__).resolve().parents[1]

def 해시(ᎠᏍᏓᏩᏛᏍᏗ):
    계산 = hashlib.sha256()
    with ᎠᏍᏓᏩᏛᏍᏗ.open('rb') as ᎠᏍᏆᏂᎪᏙᏗ:
        for ᎦᏟᏌᏅᎯ in iter(lambda: ᎠᏍᏆᏂᎪᏙᏗ.read(1048576), b''): 계산.update(ᎦᏟᏌᏅᎯ)
    return 계산.hexdigest()

def ᎠᎢᏎᏍᏗ():
    ᎤᏙᎯᏳᏒᎢ_ᎠᏍᏓᏩᏛᏍᏗ = 기준/'build/verification'
    커널해시 = 해시(기준/'build/kernel8.img')
    기록들 = {}
    for ᏚᏙᎥᎢ in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if ᏚᏙᎥᎢ == 'boot' else ᏚᏙᎥᎢ+'/report.json'
        ᎦᏟᏌᏅᎯ = json.loads((ᎤᏙᎯᏳᏒᎢ_ᎠᏍᏓᏩᏛᏍᏗ/상대경로).read_text())
        if not ᎦᏟᏌᏅᎯ.get('passed') or ᎦᏟᏌᏅᎯ.get('kernel_sha256') != 커널해시:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[ᏚᏙᎥᎢ] = {'passed': True, 'report': 상대경로}
    ᎪᎯᏳᏔᏅ_ᏚᏙᎥᎢ = json.loads((ᎤᏙᎯᏳᏒᎢ_ᎠᏍᏓᏩᏛᏍᏗ/'naming/report.json').read_text())
    if not ᎪᎯᏳᏔᏅ_ᏚᏙᎥᎢ['passed'] or not ᎪᎯᏳᏔᏅ_ᏚᏙᎥᎢ['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for ᎠᏍᏓᏩᏛᏍᏗ, 기대값 in ᎪᎯᏳᏔᏅ_ᏚᏙᎥᎢ['c_source_sha256'].items():
        if 해시(기준/ᎠᏍᏓᏩᏛᏍᏗ) != 기대값: raise SystemExit('명명 검사 ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ 바뀐 C ᎦᏟᏌᏅᎯ_0201f362: '+ᎠᏍᏓᏩᏛᏍᏗ)
    자바검사 = json.loads((ᎤᏙᎯᏳᏒᎢ_ᎠᏍᏓᏩᏛᏍᏗ/'jvm/report.json').read_text())
    직접화면 = json.loads((ᎤᏙᎯᏳᏒᎢ_ᎠᏍᏓᏩᏛᏍᏗ/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ 시험 필요')
    ᎪᎯᏳᏔᏅ_byte_ᏧᎬᏩᎶᏗᏯ = json.loads((ᎤᏙᎯᏳᏒᎢ_ᎠᏍᏓᏩᏛᏍᏗ/'naming/direct-bytecode.json').read_text())
    if not ᎪᎯᏳᏔᏅ_byte_ᏧᎬᏩᎶᏗᏯ['passed'] or ᎪᎯᏳᏔᏅ_byte_ᏧᎬᏩᎶᏗᏯ['jar_sha256'] != 해시(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 ᎰᎯᏳᏓ 필요')
    ᎪᎯᏳᏔᏅ_ᏫᏓᏤᎸ_ᎤᏓᏴᎳᏛ = json.loads((ᎤᏙᎯᏳᏒᎢ_ᎠᏍᏓᏩᏛᏍᏗ/'resolution/report.json').read_text())
    ᎪᎯᏳᏔᏅ_ᎢᎩᏓ = json.loads((ᎤᏙᎯᏳᏒᎢ_ᎠᏍᏓᏩᏛᏍᏗ/'resize/report.json').read_text())
    갱신검사 = json.loads((ᎤᏙᎯᏳᏒᎢ_ᎠᏍᏓᏩᏛᏍᏗ/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != 커널해시:
        raise SystemExit('현재 커널의 부분 ᎯᏤᎲᏍᏓ 시험 필요')
    for ᎠᏍᏓᏩᏛᏍᏗ, 기대값 in 갱신검사['source_sha256'].items():
        if 해시(기준/ᎠᏍᏓᏩᏛᏍᏗ) != 기대값: raise SystemExit('부분 ᎯᏤᎲᏍᏓ 시험 ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ 바뀐 ᎦᏟᏌᏅᎯ_0201f362: '+ᎠᏍᏓᏩᏛᏍᏗ)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 ᎠᎢᏎᏍᏗ Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ 시험 필요')
    예제검사 = json.loads((ᎤᏙᎯᏳᏒᎢ_ᎠᏍᏓᏩᏛᏍᏗ/'examples/report.json').read_text())
    if sorted(ᎪᎯᏳᏔᏅ_ᎢᎩᏓ['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 ᎢᎩᏓ 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(ᎪᎯᏳᏔᏅ_ᏫᏓᏤᎸ_ᎤᏓᏴᎳᏛ['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != 해시(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ 라이브러리가 바뀌었습니다.')
    for ᏚᏙᎥᎢ in ('한국어통신시험','한국어예외시험'):
        if not any(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ['name']==ᏚᏙᎥᎢ and Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.get('openjdk_output_equal') for Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+ᏚᏙᎥᎢ)
    예외들 = sorted(ᎠᏍᏓᏩᏛᏍᏗ.stem for ᎠᏍᏓᏩᏛᏍᏗ in (기준/'한국어자바/한국어/자체').glob('*예외.java'))
    예외기록 = (ᎤᏙᎯᏳᏒᎢ_ᎠᏍᏓᏩᏛᏍᏗ/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for ᏚᏙᎥᎢ in 예외들:
        if '\n'+ᏚᏙᎥᎢ+'\n' not in 예외기록: raise SystemExit('예외 생성·잡기·설명 시험 필요: '+ᏚᏙᎥᎢ)
    명세 = json.loads((기준/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != 해시(기준/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 ᎤᏓᏴᎳᏛ_ᏧᎬᏩᎶᏗᏯ 해시 불일치')
    with zipfile.ZipFile(str(기준/'dist/jkoros-native-rpi4-boot.zip')) as ᎦᏇᏅᎯ:
        if hashlib.sha256(ᎦᏇᏅᎯ.read('kernel8.img')).hexdigest() != 커널해시:
            raise SystemExit('부팅 ZIP kernel_ᏧᎬᏩᎶᏗᏯ 불일치')
        부팅설정 = ᎦᏇᏅᎯ.read('config.txt')
        for ᏚᏙᎥᎢ, ᎢᎩᏓ in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+ᏚᏙᎥᎢ+'='+str(ᎢᎩᏓ) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 ᏕᎦᎧᎲᎢ 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(기준/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if 해시(복사본) != 커널해시: raise SystemExit('SD ᎤᏓᏴᎳᏛ_ᏧᎬᏩᎶᏗᏯ kernel_ᏧᎬᏩᎶᏗᏯ 불일치')
        ᏗᏟᎶᏍᏔᏅᎯ_ᏕᎦᎧᎲᎢ = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(ᏗᏟᎶᏍᏔᏅᎯ_ᏕᎦᎧᎲᎢ)])
        if ᏗᏟᎶᏍᏔᏅᎯ_ᏕᎦᎧᎲᎢ.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 ᏕᎦᎧᎲᎢ 불일치')
    ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': 커널해시,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(ᎪᎯᏳᏔᏅ_ᏫᏓᏤᎸ_ᎤᏓᏴᎳᏛ['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {ᏚᏙᎥᎢ:해시(기준/'dist'/ᏚᏙᎥᎢ) for ᏚᏙᎥᎢ in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (ᎤᏙᎯᏳᏒᎢ_ᎠᏍᏓᏩᏛᏍᏗ/'native-runtime-summary.json').write_text(json.dumps(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ, 한국어 예외',len(예외들),'종, SD ᎤᏓᏴᎳᏛ_ᏧᎬᏩᎶᏗᏯ·ZIP 일치')

if __name__ == '__main__': ᎠᎢᏎᏍᏗ()
