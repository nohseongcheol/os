#!/usr/bin/env python3
"""현재 커널과 વાસ્તવિક_ડેટા 시험·배포물이 일치할 때에만 통합 માન્ય_કરો 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

પ્રોજેક્ટ_રૂટ = Path(__file__).resolve().parents[1]

def હૅશ_ફાઇલ(પથ):
    계산 = hashlib.sha256()
    with પથ.open('rb') as ફાઈલ:
        for ડેટા in iter(lambda: ફાઈલ.read(1048576), b''): 계산.update(ડેટા)
    return 계산.hexdigest()

def ચલાવો_2():
    માન્યતા_પાથ = પ્રોજેક્ટ_રૂટ/'build/verification'
    કર્નેલ_હૅશ = હૅશ_ફાઇલ(પ્રોજેક્ટ_રૂટ/'build/kernel8.img')
    기록들 = {}
    for નામ in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if નામ == 'boot' else નામ+'/report.json'
        ડેટા = json.loads((માન્યતા_પાથ/상대경로).read_text())
        if not ડેટા.get('passed') or ડેટા.get('kernel_sha256') != કર્નેલ_હૅશ:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[નામ] = {'passed': True, 'report': 상대경로}
    તપાસો_નામ = json.loads((માન્યતા_પાથ/'naming/report.json').read_text())
    if not તપાસો_નામ['passed'] or not તપાસો_નામ['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for પથ, 기대값 in તપાસો_નામ['c_source_sha256'].items():
        if હૅશ_ફાઇલ(પ્રોજેક્ટ_રૂટ/પથ) != 기대값: raise SystemExit('명명 검사 બેક_મૂલ્ય 바뀐 C સ્રોત: '+પથ)
    자바검사 = json.loads((માન્યતા_પાથ/'jvm/report.json').read_text())
    직접화면 = json.loads((માન્યતા_પાથ/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('ગુજરાતી 직접 화면 અમલ_કરો_આદેશ 시험 필요')
    તપાસો_બાઇટ_મૂલ્ય = json.loads((માન્યતા_પાથ/'naming/direct-bytecode.json').read_text())
    if not તપાસો_બાઇટ_મૂલ્ય['passed'] or તપાસો_બાઇટ_મૂલ્ય['jar_sha256'] != હૅશ_ફાઇલ(પ્રોજેક્ટ_રૂટ/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 ગુજરાતી 라이브러리의 직접 호출 바이트코드 ચકાસવું 필요')
    તપાસો_રિઝોલ્યૂશન = json.loads((માન્યતા_પાથ/'resolution/report.json').read_text())
    તપાસો_આકાર = json.loads((માન્યતા_પાથ/'resize/report.json').read_text())
    갱신검사 = json.loads((માન્યતા_પાથ/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != કર્નેલ_હૅશ:
        raise SystemExit('현재 커널의 부분 તાજું_કરો 시험 필요')
    for પથ, 기대값 in 갱신검사['source_sha256'].items():
        if હૅશ_ફાઇલ(પ્રોજેક્ટ_રૂટ/પથ) != 기대값: raise SystemExit('부분 તાજું_કરો 시험 બેક_મૂલ્ય 바뀐 સ્રોત: '+પથ)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('ગુજરાતી 직접 가닥과 ચલાવો_2 પ્રવેશ_બિંદુ 시험 필요')
    예제검사 = json.loads((માન્યતા_પાથ/'examples/report.json').read_text())
    if sorted(તપાસો_આકાર['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 માપ 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('ગુજરાતી Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(તપાસો_રિઝોલ્યૂશન['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 વાસ્તવિક_ડેટા 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != હૅશ_ફાઇલ(પ્રોજેક્ટ_રૂટ/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 બેક_મૂલ્ય 라이브러리가 바뀌었습니다.')
    for નામ in ('한국어통신시험','한국어예외시험'):
        if not any(પ્રવેશ_મૂલ્ય['name']==નામ and પ્રવેશ_મૂલ્ય.get('openjdk_output_equal') for પ્રવેશ_મૂલ્ય in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+નામ)
    예외들 = sorted(પથ.stem for પથ in (પ્રોજેક્ટ_રૂટ/'한국어자바/ગુજરાતી/자체').glob('*예외.java'))
    예외기록 = (માન્યતા_પાથ/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for નામ in 예외들:
        if '\n'+નામ+'\n' not in 예외기록: raise SystemExit('예외 જનરેટ_કરો·잡기·설명 시험 필요: '+નામ)
    명세 = json.loads((પ્રોજેક્ટ_રૂટ/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != હૅશ_ફાઇલ(પ્રોજેક્ટ_રૂટ/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 છબી_મૂલ્ય હૅશ_ફાઇલ 불일치')
    with zipfile.ZipFile(str(પ્રોજેક્ટ_રૂટ/'dist/jkoros-native-rpi4-boot.zip')) as બન્ડલ:
        if hashlib.sha256(બન્ડલ.read('kernel8.img')).hexdigest() != કર્નેલ_હૅશ:
            raise SystemExit('부팅 ZIP કર્નેલ_મૂલ્ય 불일치')
        부팅설정 = બન્ડલ.read('config.txt')
        for નામ, માપ in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+નામ+'='+str(માપ) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 સુયોજના 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(પ્રોજેક્ટ_રૂટ/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(પ્રોજેક્ટ_રૂટ/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if હૅશ_ફાઇલ(복사본) != કર્નેલ_હૅશ: raise SystemExit('SD છબી_મૂલ્ય કર્નેલ_મૂલ્ય 불일치')
        ઉદાહરણ_સેટિંગ્સ = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(પ્રોજેક્ટ_રૂટ/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(ઉદાહરણ_સેટિંગ્સ)])
        if ઉદાહરણ_સેટિંગ્સ.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 સુયોજના 불일치')
    લૉગ_પંક્તિ = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': કર્નેલ_હૅશ,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(તપાસો_રિઝોલ્યૂશન['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {નામ:હૅશ_ફાઇલ(પ્રોજેક્ટ_રૂટ/'dist'/નામ) for નામ in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (માન્યતા_પાથ/'native-runtime-summary.json').write_text(json.dumps(લૉગ_પંક્તિ,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 લૉગ_પંક્તિ, ગુજરાતી 예외',len(예외들),'વર્ગ_વ્યાખ્યા, SD છબી_મૂલ્ય·ZIP 일치')

if __name__ == '__main__': ચલાવો_2()
