#!/usr/bin/env python3
"""현재 커널과 ដែលពិត_ទិន្នន័យ 시험·배포물이 일치할 때에만 통합 ធ្វើអោយមានសុពលភាព 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

បញ្ចាំង_ឬស = Path(__file__).resolve().parents[1]

def ហាស_ឯកសារ(ផ្លូវ):
    계산 = hashlib.sha256()
    with ផ្លូវ.open('rb') as ឯកសារ:
        for ទិន្នន័យ in iter(lambda: ឯកសារ.read(1048576), b''): 계산.update(ទិន្នន័យ)
    return 계산.hexdigest()

def រត់():
    សុពលភាព_ផ្លូវ = បញ្ចាំង_ឬស/'build/verification'
    ខឺណេល_ហាស = ហាស_ឯកសារ(បញ្ចាំង_ឬស/'build/kernel8.img')
    기록들 = {}
    for ឈ្មោះ in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if ឈ្មោះ == 'boot' else ឈ្មោះ+'/report.json'
        ទិន្នន័យ = json.loads((សុពលភាព_ផ្លូវ/상대경로).read_text())
        if not ទិន្នន័យ.get('passed') or ទិន្នន័យ.get('kernel_sha256') != ខឺណេល_ហាស:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[ឈ្មោះ] = {'passed': True, 'report': 상대경로}
    ត្រួតពិនិត្យ_ឈ្មោះ = json.loads((សុពលភាព_ផ្លូវ/'naming/report.json').read_text())
    if not ត្រួតពិនិត្យ_ឈ្មោះ['passed'] or not ត្រួតពិនិត្យ_ឈ្មោះ['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for ផ្លូវ, 기대값 in ត្រួតពិនិត្យ_ឈ្មោះ['c_source_sha256'].items():
        if ហាស_ឯកសារ(បញ្ចាំង_ឬស/ផ្លូវ) != 기대값: raise SystemExit('명명 검사 ការថយ_តំលៃ 바뀐 C ប្រភព: '+ផ្លូវ)
    자바검사 = json.loads((សុពលភាព_ផ្លូវ/'jvm/report.json').read_text())
    직접화면 = json.loads((សុពលភាព_ផ្លូវ/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 អនុវត្ត_ពាក្យបញ្ជា 시험 필요')
    ត្រួតពិនិត្យ_បៃ_តំលៃ = json.loads((សុពលភាព_ផ្លូវ/'naming/direct-bytecode.json').read_text())
    if not ត្រួតពិនិត្យ_បៃ_តំលៃ['passed'] or ត្រួតពិនិត្យ_បៃ_តំលៃ['jar_sha256'] != ហាស_ឯកសារ(បញ្ចាំង_ឬស/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 ផ្ទៀងផ្ទាត់ 필요')
    ត្រួតពិនិត្យ_គុណភាព_បង្ហាញ = json.loads((សុពលភាព_ផ្លូវ/'resolution/report.json').read_text())
    ត្រួតពិនិត្យ_ដាក់ទំហំ = json.loads((សុពលភាព_ផ្លូវ/'resize/report.json').read_text())
    갱신검사 = json.loads((សុពលភាព_ផ្លូវ/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != ខឺណេល_ហាស:
        raise SystemExit('현재 커널의 부분 ផ្ទុក_ឡើង_វិញ 시험 필요')
    for ផ្លូវ, 기대값 in 갱신검사['source_sha256'].items():
        if ហាស_ឯកសារ(បញ្ចាំង_ឬស/ផ្លូវ) != 기대값: raise SystemExit('부분 ផ្ទុក_ឡើង_វិញ 시험 ការថយ_តំលៃ 바뀐 ប្រភព: '+ផ្លូវ)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 រត់ ការបញ្ចូល_ចំនុច 시험 필요')
    예제검사 = json.loads((សុពលភាព_ផ្លូវ/'examples/report.json').read_text())
    if sorted(ត្រួតពិនិត្យ_ដាក់ទំហំ['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 ដាក់ទំហំ 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(ត្រួតពិនិត្យ_គុណភាព_បង្ហាញ['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 ដែលពិត_ទិន្នន័យ 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != ហាស_ឯកសារ(បញ្ចាំង_ឬស/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 ការថយ_តំលៃ 라이브러리가 바뀌었습니다.')
    for ឈ្មោះ in ('한국어통신시험','한국어예외시험'):
        if not any(ការបញ្ចូល_តំលៃ['name']==ឈ្មោះ and ការបញ្ចូល_តំលៃ.get('openjdk_output_equal') for ការបញ្ចូល_តំលៃ in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+ឈ្មោះ)
    ការលើកលែង_បញ្ជី = sorted(ផ្លូវ.stem for ផ្លូវ in (បញ្ចាំង_ឬស/'한국어자바/한국어/자체').glob('*ការលើកលែង.java'))
    ការលើកលែង_កំណត់_ហេតុ = (សុពលភាព_ផ្លូវ/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for ឈ្មោះ in ការលើកលែង_បញ្ជី:
        if '\n'+ឈ្មោះ+'\n' not in ការលើកលែង_កំណត់_ហេតុ: raise SystemExit('ការលើកលែង បង្កើត·잡기·설명 시험 필요: '+ឈ្មោះ)
    명세 = json.loads((បញ្ចាំង_ឬស/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != ហាស_ឯកសារ(បញ្ចាំង_ឬស/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 រូបថត_តំលៃ ហាស_ឯកសារ 불일치')
    with zipfile.ZipFile(str(បញ្ចាំង_ឬស/'dist/jkoros-native-rpi4-boot.zip')) as បាច់:
        if hashlib.sha256(បាច់.read('kernel8.img')).hexdigest() != ខឺណេល_ហាស:
            raise SystemExit('부팅 ZIP ខឺណេល_តំលៃ 불일치')
        부팅설정 = បាច់.read('config.txt')
        for ឈ្មោះ, ដាក់ទំហំ in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+ឈ្មោះ+'='+str(ដាក់ទំហំ) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 ការកំណត់ 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(បញ្ចាំង_ឬស/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(បញ្ចាំង_ឬស/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if ហាស_ឯកសារ(복사본) != ខឺណេល_ហាស: raise SystemExit('SD រូបថត_តំលៃ ខឺណេល_តំលៃ 불일치')
        ចំលង_ការកំណត់ = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(បញ្ចាំង_ឬស/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(ចំលង_ការកំណត់)])
        if ចំលង_ការកំណត់.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 ការកំណត់ 불일치')
    កំណត់_ហេតុ_ថត = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': ខឺណេល_ហាស,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': ការលើកលែង_បញ្ជី, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(ត្រួតពិនិត្យ_គុណភាព_បង្ហាញ['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {ឈ្មោះ:ហាស_ឯកសារ(បញ្ចាំង_ឬស/'dist'/ឈ្មោះ) for ឈ្មោះ in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (សុពលភាព_ផ្លូវ/'native-runtime-summary.json').write_text(json.dumps(កំណត់_ហេតុ_ថត,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 កំណត់_ហេតុ_ថត, 한국어 ការលើកលែង',len(ការលើកលែង_បញ្ជី),'ថ្នាក់_និយមន័យ, SD រូបថត_តំលៃ·ZIP 일치')

if __name__ == '__main__': រត់()
