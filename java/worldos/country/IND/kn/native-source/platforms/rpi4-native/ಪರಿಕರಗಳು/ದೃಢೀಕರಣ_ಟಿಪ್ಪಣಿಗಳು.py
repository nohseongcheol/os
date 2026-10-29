#!/usr/bin/env python3
"""현재 커널과 ನಿಜವಾದ_ಡೇಟಾ 시험·배포물이 일치할 때에만 통합 ಸಕ್ರಮೀಕರಿಸು 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

ಬಿಂಬಿಸು_ಮೂಲ = Path(__file__).resolve().parents[1]

def ಹ್ಯಾಶ್_ಫೈಲ್(ಮಾರ್ಗ):
    계산 = hashlib.sha256()
    with ಮಾರ್ಗ.open('rb') as ಕಡತ:
        for ಡೇಟಾ in iter(lambda: ಕಡತ.read(1048576), b''): 계산.update(ಡೇಟಾ)
    return 계산.hexdigest()

def ಚಲಾಯಿಸು_2():
    ದೃಢೀಕರಣ_ಹಾದಿ = ಬಿಂಬಿಸು_ಮೂಲ/'build/verification'
    ಕರ್ನಲ್_ಹ್ಯಾಶ್ = ಹ್ಯಾಶ್_ಫೈಲ್(ಬಿಂಬಿಸು_ಮೂಲ/'build/kernel8.img')
    기록들 = {}
    for ಹೆಸರು in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if ಹೆಸರು == 'boot' else ಹೆಸರು+'/report.json'
        ಡೇಟಾ = json.loads((ದೃಢೀಕರಣ_ಹಾದಿ/상대경로).read_text())
        if not ಡೇಟಾ.get('passed') or ಡೇಟಾ.get('kernel_sha256') != ಕರ್ನಲ್_ಹ್ಯಾಶ್:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[ಹೆಸರು] = {'passed': True, 'report': 상대경로}
    ಚೆಕ್_ಹೆಸರು = json.loads((ದೃಢೀಕರಣ_ಹಾದಿ/'naming/report.json').read_text())
    if not ಚೆಕ್_ಹೆಸರು['passed'] or not ಚೆಕ್_ಹೆಸರು['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for ಮಾರ್ಗ, 기대값 in ಚೆಕ್_ಹೆಸರು['c_source_sha256'].items():
        if ಹ್ಯಾಶ್_ಫೈಲ್(ಬಿಂಬಿಸು_ಮೂಲ/ಮಾರ್ಗ) != 기대값: raise SystemExit('명명 검사 ಹಿಂದೆ_ಮೌಲ್ಯ 바뀐 C ಮೂಲ: '+ಮಾರ್ಗ)
    자바검사 = json.loads((ದೃಢೀಕರಣ_ಹಾದಿ/'jvm/report.json').read_text())
    직접화면 = json.loads((ದೃಢೀಕರಣ_ಹಾದಿ/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('ಕನ್ನಡ 직접 화면 ಪೂರೈಸು_ಆದೇಶ 시험 필요')
    ಚೆಕ್_ಬೈಟ್_ಮೌಲ್ಯ = json.loads((ದೃಢೀಕರಣ_ಹಾದಿ/'naming/direct-bytecode.json').read_text())
    if not ಚೆಕ್_ಬೈಟ್_ಮೌಲ್ಯ['passed'] or ಚೆಕ್_ಬೈಟ್_ಮೌಲ್ಯ['jar_sha256'] != ಹ್ಯಾಶ್_ಫೈಲ್(ಬಿಂಬಿಸು_ಮೂಲ/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 ಕನ್ನಡ 라이브러리의 직접 호출 바이트코드 ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು 필요')
    ಚೆಕ್_ರಿಸೊಲ್ಯೂಶನ್ = json.loads((ದೃಢೀಕರಣ_ಹಾದಿ/'resolution/report.json').read_text())
    ಚೆಕ್_ಗಾತ್ರಿಸು = json.loads((ದೃಢೀಕರಣ_ಹಾದಿ/'resize/report.json').read_text())
    갱신검사 = json.loads((ದೃಢೀಕರಣ_ಹಾದಿ/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != ಕರ್ನಲ್_ಹ್ಯಾಶ್:
        raise SystemExit('현재 커널의 부분 ತಾಜಾಮಾಡು 시험 필요')
    for ಮಾರ್ಗ, 기대값 in 갱신검사['source_sha256'].items():
        if ಹ್ಯಾಶ್_ಫೈಲ್(ಬಿಂಬಿಸು_ಮೂಲ/ಮಾರ್ಗ) != 기대값: raise SystemExit('부분 ತಾಜಾಮಾಡು 시험 ಹಿಂದೆ_ಮೌಲ್ಯ 바뀐 ಮೂಲ: '+ಮಾರ್ಗ)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('ಕನ್ನಡ 직접 가닥과 ಚಲಾಯಿಸು_2 ನಮೂದು_ಬಿಂದು 시험 필요')
    예제검사 = json.loads((ದೃಢೀಕರಣ_ಹಾದಿ/'examples/report.json').read_text())
    if sorted(ಚೆಕ್_ಗಾತ್ರಿಸು['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 ಗಾತ್ರ 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('ಕನ್ನಡ Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(ಚೆಕ್_ರಿಸೊಲ್ಯೂಶನ್['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 ನಿಜವಾದ_ಡೇಟಾ 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != ಹ್ಯಾಶ್_ಫೈಲ್(ಬಿಂಬಿಸು_ಮೂಲ/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 ಹಿಂದೆ_ಮೌಲ್ಯ 라이브러리가 바뀌었습니다.')
    for ಹೆಸರು in ('한국어통신시험','한국어예외시험'):
        if not any(ನಮೂದು_ಮೌಲ್ಯ['name']==ಹೆಸರು and ನಮೂದು_ಮೌಲ್ಯ.get('openjdk_output_equal') for ನಮೂದು_ಮೌಲ್ಯ in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+ಹೆಸರು)
    ವಿನಾಯಿತಿ_ಪಟ್ಟಿ = sorted(ಮಾರ್ಗ.stem for ಮಾರ್ಗ in (ಬಿಂಬಿಸು_ಮೂಲ/'한국어자바/ಕನ್ನಡ/자체').glob('*ವಿನಾಯಿತಿ.java'))
    ವಿನಾಯಿತಿ_ಲಾಗ್ = (ದೃಢೀಕರಣ_ಹಾದಿ/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for ಹೆಸರು in ವಿನಾಯಿತಿ_ಪಟ್ಟಿ:
        if '\n'+ಹೆಸರು+'\n' not in ವಿನಾಯಿತಿ_ಲಾಗ್: raise SystemExit('ವಿನಾಯಿತಿ ರಚಿಸಿ·잡기·설명 시험 필요: '+ಹೆಸರು)
    명세 = json.loads((ಬಿಂಬಿಸು_ಮೂಲ/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != ಹ್ಯಾಶ್_ಫೈಲ್(ಬಿಂಬಿಸು_ಮೂಲ/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 ಇಮೇಜ್_ಮೌಲ್ಯ ಹ್ಯಾಶ್_ಫೈಲ್ 불일치')
    with zipfile.ZipFile(str(ಬಿಂಬಿಸು_ಮೂಲ/'dist/jkoros-native-rpi4-boot.zip')) as ಬಂಡಲ್:
        if hashlib.sha256(ಬಂಡಲ್.read('kernel8.img')).hexdigest() != ಕರ್ನಲ್_ಹ್ಯಾಶ್:
            raise SystemExit('부팅 ZIP ಕರ್ನಲ್_ಮೌಲ್ಯ 불일치')
        부팅설정 = ಬಂಡಲ್.read('config.txt')
        for ಹೆಸರು, ಗಾತ್ರ in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+ಹೆಸರು+'='+str(ಗಾತ್ರ) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 ಸಿದ್ಧತೆಗಳು 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(ಬಿಂಬಿಸು_ಮೂಲ/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(ಬಿಂಬಿಸು_ಮೂಲ/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if ಹ್ಯಾಶ್_ಫೈಲ್(복사본) != ಕರ್ನಲ್_ಹ್ಯಾಶ್: raise SystemExit('SD ಇಮೇಜ್_ಮೌಲ್ಯ ಕರ್ನಲ್_ಮೌಲ್ಯ 불일치')
        ನಕಲಿಸು_ಸೆಟ್ಟಿಂಗ್ಸ್ = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(ಬಿಂಬಿಸು_ಮೂಲ/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(ನಕಲಿಸು_ಸೆಟ್ಟಿಂಗ್ಸ್)])
        if ನಕಲಿಸು_ಸೆಟ್ಟಿಂಗ್ಸ್.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 ಸಿದ್ಧತೆಗಳು 불일치')
    ಲಾಗ್_ದಾಖಲೆ = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': ಕರ್ನಲ್_ಹ್ಯಾಶ್,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': ವಿನಾಯಿತಿ_ಪಟ್ಟಿ, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(ಚೆಕ್_ರಿಸೊಲ್ಯೂಶನ್['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {ಹೆಸರು:ಹ್ಯಾಶ್_ಫೈಲ್(ಬಿಂಬಿಸು_ಮೂಲ/'dist'/ಹೆಸರು) for ಹೆಸರು in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (ದೃಢೀಕರಣ_ಹಾದಿ/'native-runtime-summary.json').write_text(json.dumps(ಲಾಗ್_ದಾಖಲೆ,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 ಲಾಗ್_ದಾಖಲೆ, ಕನ್ನಡ ವಿನಾಯಿತಿ',len(ವಿನಾಯಿತಿ_ಪಟ್ಟಿ),'ವರ್ಗ_ವಿವರಣೆ, SD ಇಮೇಜ್_ಮೌಲ್ಯ·ZIP 일치')

if __name__ == '__main__': ಚಲಾಯಿಸು_2()
