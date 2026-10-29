#!/usr/bin/env python3
"""현재 커널과 ਅਸਲ_ਸਮੱਗਰੀ 시험·배포물이 일치할 때에만 통합 ਪ੍ਰਮਾਣਿਤ 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

ਪ੍ਰੋਜੈਕਟ_ਰੂਟ = Path(__file__).resolve().parents[1]

def ਹੈਸ਼_ਲਿਖਤ_ਪੱਤਰ(ਮਾਰਗ):
    계산 = hashlib.sha256()
    with ਮਾਰਗ.open('rb') as ਫਾਇਲ:
        for ਸਮੱਗਰੀ in iter(lambda: ਫਾਇਲ.read(1048576), b''): 계산.update(ਸਮੱਗਰੀ)
    return 계산.hexdigest()

def ਚਲਾਓ_2():
    ਮਾਨਤਾ_ਰਸਤਾ = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/verification'
    ਪੱਕੇ_ਹੋਣਾ_ਹੈਸ਼ = ਹੈਸ਼_ਲਿਖਤ_ਪੱਤਰ(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/kernel8.img')
    기록들 = {}
    for ਨਾਂ in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if ਨਾਂ == 'boot' else ਨਾਂ+'/report.json'
        ਸਮੱਗਰੀ = json.loads((ਮਾਨਤਾ_ਰਸਤਾ/상대경로).read_text())
        if not ਸਮੱਗਰੀ.get('passed') or ਸਮੱਗਰੀ.get('kernel_sha256') != ਪੱਕੇ_ਹੋਣਾ_ਹੈਸ਼:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[ਨਾਂ] = {'passed': True, 'report': 상대경로}
    ਚੈਕ_ਕਰੋ_ਨਾਮ = json.loads((ਮਾਨਤਾ_ਰਸਤਾ/'naming/report.json').read_text())
    if not ਚੈਕ_ਕਰੋ_ਨਾਮ['passed'] or not ਚੈਕ_ਕਰੋ_ਨਾਮ['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for ਮਾਰਗ, 기대값 in ਚੈਕ_ਕਰੋ_ਨਾਮ['c_source_sha256'].items():
        if ਹੈਸ਼_ਲਿਖਤ_ਪੱਤਰ(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/ਮਾਰਗ) != 기대값: raise SystemExit('명명 검사 ਪਿਛਲਾ_ਕੀਮਤ 바뀐 C ਸਰੋਤ: '+ਮਾਰਗ)
    자바검사 = json.loads((ਮਾਨਤਾ_ਰਸਤਾ/'jvm/report.json').read_text())
    직접화면 = json.loads((ਮਾਨਤਾ_ਰਸਤਾ/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('ਪੰਜਾਬੀ 직접 화면 ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ 시험 필요')
    ਚੈਕ_ਕਰੋ_ਬਾਈਟ_ਕੀਮਤ = json.loads((ਮਾਨਤਾ_ਰਸਤਾ/'naming/direct-bytecode.json').read_text())
    if not ਚੈਕ_ਕਰੋ_ਬਾਈਟ_ਕੀਮਤ['passed'] or ਚੈਕ_ਕਰੋ_ਬਾਈਟ_ਕੀਮਤ['jar_sha256'] != ਹੈਸ਼_ਲਿਖਤ_ਪੱਤਰ(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 ਪੰਜਾਬੀ 라이브러리의 직접 호출 바이트코드 ਤਸਦੀਕ 필요')
    ਚੈਕ_ਕਰੋ_ਰੂਪਾਂਤਰ = json.loads((ਮਾਨਤਾ_ਰਸਤਾ/'resolution/report.json').read_text())
    ਚੈਕ_ਕਰੋ_ਆਕਾਰ = json.loads((ਮਾਨਤਾ_ਰਸਤਾ/'resize/report.json').read_text())
    갱신검사 = json.loads((ਮਾਨਤਾ_ਰਸਤਾ/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != ਪੱਕੇ_ਹੋਣਾ_ਹੈਸ਼:
        raise SystemExit('현재 커널의 부분 ਤਾਜ਼ਾ_ਕਰੋ 시험 필요')
    for ਮਾਰਗ, 기대값 in 갱신검사['source_sha256'].items():
        if ਹੈਸ਼_ਲਿਖਤ_ਪੱਤਰ(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/ਮਾਰਗ) != 기대값: raise SystemExit('부분 ਤਾਜ਼ਾ_ਕਰੋ 시험 ਪਿਛਲਾ_ਕੀਮਤ 바뀐 ਸਰੋਤ: '+ਮਾਰਗ)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('ਪੰਜਾਬੀ 직접 가닥과 ਚਲਾਓ_2 ਦਾਖਲਾ_ਪੌਇੰਟ 시험 필요')
    예제검사 = json.loads((ਮਾਨਤਾ_ਰਸਤਾ/'examples/report.json').read_text())
    if sorted(ਚੈਕ_ਕਰੋ_ਆਕਾਰ['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 ਆਕਾਰ 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('ਪੰਜਾਬੀ Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(ਚੈਕ_ਕਰੋ_ਰੂਪਾਂਤਰ['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 ਅਸਲ_ਸਮੱਗਰੀ 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != ਹੈਸ਼_ਲਿਖਤ_ਪੱਤਰ(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 ਪਿਛਲਾ_ਕੀਮਤ 라이브러리가 바뀌었습니다.')
    for ਨਾਂ in ('한국어통신시험','한국어예외시험'):
        if not any(ਦਾਖਲਾ_ਕੀਮਤ['name']==ਨਾਂ and ਦਾਖਲਾ_ਕੀਮਤ.get('openjdk_output_equal') for ਦਾਖਲਾ_ਕੀਮਤ in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+ਨਾਂ)
    예외들 = sorted(ਮਾਰਗ.stem for ਮਾਰਗ in (ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'한국어자바/ਪੰਜਾਬੀ/자체').glob('*예외.java'))
    예외기록 = (ਮਾਨਤਾ_ਰਸਤਾ/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for ਨਾਂ in 예외들:
        if '\n'+ਨਾਂ+'\n' not in 예외기록: raise SystemExit('예외 ਜਨਰੇਟ_ਕਰੋ·잡기·설명 시험 필요: '+ਨਾਂ)
    명세 = json.loads((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != ਹੈਸ਼_ਲਿਖਤ_ਪੱਤਰ(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 ਤਸਵੀਰ_ਕੀਮਤ ਹੈਸ਼_ਲਿਖਤ_ਪੱਤਰ 불일치')
    with zipfile.ZipFile(str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'dist/jkoros-native-rpi4-boot.zip')) as ਬੰਡਲ:
        if hashlib.sha256(ਬੰਡਲ.read('kernel8.img')).hexdigest() != ਪੱਕੇ_ਹੋਣਾ_ਹੈਸ਼:
            raise SystemExit('부팅 ZIP ਪੱਕੇ_ਹੋਣਾ_ਕੀਮਤ 불일치')
        부팅설정 = ਬੰਡਲ.read('config.txt')
        for ਨਾਂ, ਆਕਾਰ in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+ਨਾਂ+'='+str(ਆਕਾਰ) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 ਸੈਟਿੰਗ 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if ਹੈਸ਼_ਲਿਖਤ_ਪੱਤਰ(복사본) != ਪੱਕੇ_ਹੋਣਾ_ਹੈਸ਼: raise SystemExit('SD ਤਸਵੀਰ_ਕੀਮਤ ਪੱਕੇ_ਹੋਣਾ_ਕੀਮਤ 불일치')
        ਇਨਸਟੈਂਸ_ਸੈਟਿੰਗਾਂ = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(ਇਨਸਟੈਂਸ_ਸੈਟਿੰਗਾਂ)])
        if ਇਨਸਟੈਂਸ_ਸੈਟਿੰਗਾਂ.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 ਸੈਟਿੰਗ 불일치')
    ਲੌਗ_ਕਤਾਰ = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': ਪੱਕੇ_ਹੋਣਾ_ਹੈਸ਼,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(ਚੈਕ_ਕਰੋ_ਰੂਪਾਂਤਰ['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {ਨਾਂ:ਹੈਸ਼_ਲਿਖਤ_ਪੱਤਰ(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'dist'/ਨਾਂ) for ਨਾਂ in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (ਮਾਨਤਾ_ਰਸਤਾ/'native-runtime-summary.json').write_text(json.dumps(ਲੌਗ_ਕਤਾਰ,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 ਲੌਗ_ਕਤਾਰ, ਪੰਜਾਬੀ 예외',len(예외들),'ਸ੍ਰੇਣੀ_ਪਰਿਭਾਸ਼ਾ, SD ਤਸਵੀਰ_ਕੀਮਤ·ZIP 일치')

if __name__ == '__main__': ਚਲਾਓ_2()
