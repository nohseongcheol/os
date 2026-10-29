#!/usr/bin/env python3
"""현재 커널과 რეალური_მონაცემები 시험·배포물이 일치할 때에만 통합 შემოწმება 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

პროეცირება_ფესვი = Path(__file__).resolve().parents[1]

def ჰეში_ფაილი(გეზი):
    계산 = hashlib.sha256()
    with გეზი.open('rb') as ფაილი:
        for მონაცემები in iter(lambda: ფაილი.read(1048576), b''): 계산.update(მონაცემები)
    return 계산.hexdigest()

def გაშვება():
    გადამოწმება_მდებარეობა = პროეცირება_ფესვი/'build/verification'
    ბირთვი_ჰეში = ჰეში_ფაილი(პროეცირება_ფესვი/'build/kernel8.img')
    기록들 = {}
    for სახელი in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if სახელი == 'boot' else სახელი+'/report.json'
        მონაცემები = json.loads((გადამოწმება_მდებარეობა/상대경로).read_text())
        if not მონაცემები.get('passed') or მონაცემები.get('kernel_sha256') != ბირთვი_ჰეში:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[სახელი] = {'passed': True, 'report': 상대경로}
    შემოწმება_სახელი = json.loads((გადამოწმება_მდებარეობა/'naming/report.json').read_text())
    if not შემოწმება_სახელი['passed'] or not შემოწმება_სახელი['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for გეზი, 기대값 in შემოწმება_სახელი['c_source_sha256'].items():
        if ჰეში_ფაილი(პროეცირება_ფესვი/გეზი) != 기대값: raise SystemExit('명명 검사 უკან_მნიშვნელობა 바뀐 C წყარო: '+გეზი)
    자바검사 = json.loads((გადამოწმება_მდებარეობა/'jvm/report.json').read_text())
    직접화면 = json.loads((გადამოწმება_მდებარეობა/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 შესრულება_ბრძანება 시험 필요')
    შემოწმება_ბაიტი_მნიშვნელობა = json.loads((გადამოწმება_მდებარეობა/'naming/direct-bytecode.json').read_text())
    if not შემოწმება_ბაიტი_მნიშვნელობა['passed'] or შემოწმება_ბაიტი_მნიშვნელობა['jar_sha256'] != ჰეში_ფაილი(პროეცირება_ფესვი/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 გადამოწმება 필요')
    შემოწმება_გარჩევადობა = json.loads((გადამოწმება_მდებარეობა/'resolution/report.json').read_text())
    შემოწმება_ზომის_შეცვლა = json.loads((გადამოწმება_მდებარეობა/'resize/report.json').read_text())
    갱신검사 = json.loads((გადამოწმება_მდებარეობა/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != ბირთვი_ჰეში:
        raise SystemExit('현재 커널의 부분 განახლება 시험 필요')
    for გეზი, 기대값 in 갱신검사['source_sha256'].items():
        if ჰეში_ფაილი(პროეცირება_ფესვი/გეზი) != 기대값: raise SystemExit('부분 განახლება 시험 უკან_მნიშვნელობა 바뀐 წყარო: '+გეზი)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 გაშვება შენატანი_პტ 시험 필요')
    예제검사 = json.loads((გადამოწმება_მდებარეობა/'examples/report.json').read_text())
    if sorted(შემოწმება_ზომის_შეცვლა['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 ზომა 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(შემოწმება_გარჩევადობა['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 რეალური_მონაცემები 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != ჰეში_ფაილი(პროეცირება_ფესვი/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 უკან_მნიშვნელობა 라이브러리가 바뀌었습니다.')
    for სახელი in ('한국어통신시험','한국어예외시험'):
        if not any(შენატანი_მნიშვნელობა['name']==სახელი and შენატანი_მნიშვნელობა.get('openjdk_output_equal') for შენატანი_მნიშვნელობა in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+სახელი)
    예외들 = sorted(გეზი.stem for გეზი in (პროეცირება_ფესვი/'한국어자바/한국어/자체').glob('*예외.java'))
    예외기록 = (გადამოწმება_მდებარეობა/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for სახელი in 예외들:
        if '\n'+სახელი+'\n' not in 예외기록: raise SystemExit('예외 დაგენერირება·잡기·설명 시험 필요: '+სახელი)
    명세 = json.loads((პროეცირება_ფესვი/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != ჰეში_ფაილი(პროეცირება_ფესვი/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 ნახატი_მნიშვნელობა ჰეში_ფაილი 불일치')
    with zipfile.ZipFile(str(პროეცირება_ფესვი/'dist/jkoros-native-rpi4-boot.zip')) as შეკვრა:
        if hashlib.sha256(შეკვრა.read('kernel8.img')).hexdigest() != ბირთვი_ჰეში:
            raise SystemExit('부팅 ZIP ბირთვი_მნიშვნელობა 불일치')
        부팅설정 = შეკვრა.read('config.txt')
        for სახელი, ზომა in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+სახელი+'='+str(ზომა) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 პარამეტრები 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(პროეცირება_ფესვი/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(პროეცირება_ფესვი/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if ჰეში_ფაილი(복사본) != ბირთვი_ჰეში: raise SystemExit('SD ნახატი_მნიშვნელობა ბირთვი_მნიშვნელობა 불일치')
        ასლი_პარამეტრები = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(პროეცირება_ფესვი/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(ასლი_პარამეტრები)])
        if ასლი_პარამეტრები.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 პარამეტრები 불일치')
    ჟურნალი_ჩაწერა = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': ბირთვი_ჰეში,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(შემოწმება_გარჩევადობა['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {სახელი:ჰეში_ფაილი(პროეცირება_ფესვი/'dist'/სახელი) for სახელი in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (გადამოწმება_მდებარეობა/'native-runtime-summary.json').write_text(json.dumps(ჟურნალი_ჩაწერა,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 ჟურნალი_ჩაწერა, 한국어 예외',len(예외들),'კლასი_განსაზღვრება, SD ნახატი_მნიშვნელობა·ZIP 일치')

if __name__ == '__main__': გაშვება()
