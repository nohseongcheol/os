#!/usr/bin/env python3
"""현재 커널과 ପ୍ରକୃତ_ଡାଟା 시험·배포물이 일치할 때에만 통합 ବୈଧକରଣ 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ = Path(__file__).resolve().parents[1]

def ହାସ୍_ଫାଇଲ୍(ପଥ):
    계산 = hashlib.sha256()
    with ପଥ.open('rb') as ଫାଇଲ:
        for ଡାଟା in iter(lambda: ଫାଇଲ.read(1048576), b''): 계산.update(ଡାଟା)
    return 계산.hexdigest()

def ଚଳାନ୍ତୁ():
    ବୈଧକରଣ_ପଥ = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/verification'
    କେନ୍ଦ୍ରିକ_ହାସ୍ = ହାସ୍_ଫାଇଲ୍(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/kernel8.img')
    기록들 = {}
    for ନାମ in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if ନାମ == 'boot' else ନାମ+'/report.json'
        ଡାଟା = json.loads((ବୈଧକରଣ_ପଥ/상대경로).read_text())
        if not ଡାଟା.get('passed') or ଡାଟା.get('kernel_sha256') != କେନ୍ଦ୍ରିକ_ହାସ୍:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[ନାମ] = {'passed': True, 'report': 상대경로}
    ପରୀକ୍ଷିତ_ନାମ = json.loads((ବୈଧକରଣ_ପଥ/'naming/report.json').read_text())
    if not ପରୀକ୍ଷିତ_ନାମ['passed'] or not ପରୀକ୍ଷିତ_ନାମ['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for ପଥ, 기대값 in ପରୀକ୍ଷିତ_ନାମ['c_source_sha256'].items():
        if ହାସ୍_ଫାଇଲ୍(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/ପଥ) != 기대값: raise SystemExit('명명 검사 ପଛ_ମୂଲ୍ୟ 바뀐 C ଉତ୍ସ: '+ପଥ)
    자바검사 = json.loads((ବୈଧକରଣ_ପଥ/'jvm/report.json').read_text())
    직접화면 = json.loads((ବୈଧକରଣ_ପଥ/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ 시험 필요')
    ପରୀକ୍ଷିତ_ବାଇଟ୍_ମୂଲ୍ୟ = json.loads((ବୈଧକରଣ_ପଥ/'naming/direct-bytecode.json').read_text())
    if not ପରୀକ୍ଷିତ_ବାଇଟ୍_ମୂଲ୍ୟ['passed'] or ପରୀକ୍ଷିତ_ବାଇଟ୍_ମୂଲ୍ୟ['jar_sha256'] != ହାସ୍_ଫାଇଲ୍(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 ଯାଞ୍ଚ୍_କରିବା 필요')
    ପରୀକ୍ଷିତ_ସ୍ପଷ୍ଟତା = json.loads((ବୈଧକରଣ_ପଥ/'resolution/report.json').read_text())
    ପରୀକ୍ଷିତ_ଅକାର = json.loads((ବୈଧକରଣ_ପଥ/'resize/report.json').read_text())
    갱신검사 = json.loads((ବୈଧକରଣ_ପଥ/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != କେନ୍ଦ୍ରିକ_ହାସ୍:
        raise SystemExit('현재 커널의 부분 ସତେଜ_କରନ୍ତୁ 시험 필요')
    for ପଥ, 기대값 in 갱신검사['source_sha256'].items():
        if ହାସ୍_ଫାଇଲ୍(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/ପଥ) != 기대값: raise SystemExit('부분 ସତେଜ_କରନ୍ତୁ 시험 ପଛ_ମୂଲ୍ୟ 바뀐 ଉତ୍ସ: '+ପଥ)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 ଚଳାନ୍ତୁ ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍ 시험 필요')
    예제검사 = json.loads((ବୈଧକରଣ_ପଥ/'examples/report.json').read_text())
    if sorted(ପରୀକ୍ଷିତ_ଅକାର['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 ଆକାର 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(ପରୀକ୍ଷିତ_ସ୍ପଷ୍ଟତା['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 ପ୍ରକୃତ_ଡାଟା 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != ହାସ୍_ଫାଇଲ୍(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 ପଛ_ମୂଲ୍ୟ 라이브러리가 바뀌었습니다.')
    for ନାମ in ('한국어통신시험','한국어예외시험'):
        if not any(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ['name']==ନାମ and ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.get('openjdk_output_equal') for ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+ନାମ)
    ବ୍ୟତିକ୍ରମ_ତାଲିକା = sorted(ପଥ.stem for ପଥ in (ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'한국어자바/한국어/자체').glob('*ବ୍ୟତିକ୍ରମ.java'))
    ବ୍ୟତିକ୍ରମ_ଲଗ୍ = (ବୈଧକରଣ_ପଥ/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for ନାମ in ବ୍ୟତିକ୍ରମ_ତାଲିକା:
        if '\n'+ନାମ+'\n' not in ବ୍ୟତିକ୍ରମ_ଲଗ୍: raise SystemExit('ବ୍ୟତିକ୍ରମ ସୃଷ୍ଟି_କରିବା·잡기·설명 시험 필요: '+ନାମ)
    명세 = json.loads((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != ହାସ୍_ଫାଇଲ୍(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 ଚିତ୍ର_ମୂଲ୍ୟ ହାସ୍_ଫାଇଲ୍ 불일치')
    with zipfile.ZipFile(str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'dist/jkoros-native-rpi4-boot.zip')) as ବଣ୍ଡଲ୍:
        if hashlib.sha256(ବଣ୍ଡଲ୍.read('kernel8.img')).hexdigest() != କେନ୍ଦ୍ରିକ_ହାସ୍:
            raise SystemExit('부팅 ZIP କେନ୍ଦ୍ରିକ_ମୂଲ୍ୟ 불일치')
        부팅설정 = ବଣ୍ଡଲ୍.read('config.txt')
        for ନାମ, ଆକାର in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+ନାମ+'='+str(ଆକାର) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 ବିନ୍ଯାସ 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if ହାସ୍_ଫାଇଲ୍(복사본) != କେନ୍ଦ୍ରିକ_ହାସ୍: raise SystemExit('SD ଚିତ୍ର_ମୂଲ୍ୟ କେନ୍ଦ୍ରିକ_ମୂଲ୍ୟ 불일치')
        କପି_ସେଟିଂସ୍ = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(କପି_ସେଟିଂସ୍)])
        if କପି_ସେଟିଂସ୍.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 ବିନ୍ଯାସ 불일치')
    ଲଗ୍_ଧାଡ଼ି = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': କେନ୍ଦ୍ରିକ_ହାସ୍,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': ବ୍ୟତିକ୍ରମ_ତାଲିକା, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(ପରୀକ୍ଷିତ_ସ୍ପଷ୍ଟତା['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {ନାମ:ହାସ୍_ଫାଇଲ୍(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'dist'/ନାମ) for ନାମ in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (ବୈଧକରଣ_ପଥ/'native-runtime-summary.json').write_text(json.dumps(ଲଗ୍_ଧାଡ଼ି,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 ଲଗ୍_ଧାଡ଼ି, 한국어 ବ୍ୟତିକ୍ରମ',len(ବ୍ୟତିକ୍ରମ_ତାଲିକା),'ଶ୍ରେଣୀ_ବ୍ୟାଖ୍ୟା, SD ଚିତ୍ର_ମୂଲ୍ୟ·ZIP 일치')

if __name__ == '__main__': ଚଳାନ୍ତୁ()
