#!/usr/bin/env python3
"""phầnMụcHiệnTại 커널과 dữLiệuThựcTế KiểmThử·배포물이 일치할 때에만 통합 thẩmĐịnh 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

gốcCâyDựÁn = Path(__file__).resolve().parents[1]

def tệpMãBăm(đườngDẫn):
    phépTính = hashlib.sha256()
    with đườngDẫn.open('rb') as Tệp:
        for DữLiệu in iter(lambda: Tệp.read(1048576), b''): phépTính.update(DữLiệu)
    return phépTính.hexdigest()

def chạy():
    đườngDẫnViệcThẩmĐịnh = gốcCâyDựÁn/'build/verification'
    mãBămNhân = tệpMãBăm(gốcCâyDựÁn/'build/kernel8.img')
    cácBảnGhiNhậtKý = {}
    for tên in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        đườngDẫnTươngĐối = 'report.json' if tên == 'boot' else tên+'/report.json'
        DữLiệu = json.loads((đườngDẫnViệcThẩmĐịnh/đườngDẫnTươngĐối).read_text())
        if not DữLiệu.get('passed') or DữLiệu.get('kernel_sha256') != mãBămNhân:
            raise SystemExit('phầnMụcHiệnTại 커널에 대한 giáTrịThànhCông 기록이 필요합니다: '+đườngDẫnTươngĐối)
        cácBảnGhiNhậtKý[tên] = {'passed': True, 'report': đườngDẫnTươngĐối}
    kiểmTraTên = json.loads((đườngDẫnViệcThẩmĐịnh/'naming/report.json').read_text())
    if not kiểmTraTên['passed'] or not kiểmTraTên['c_semantic_checked']: raise SystemExit('C 선언을 포함한 cáchĐặtTên CácPhépKiểmTra giáTrịCầnĐến')
    for đườngDẫn, giáTrịDựKiến in kiểmTraTên['c_source_sha256'].items():
        if tệpMãBăm(gốcCâyDựÁn/đườngDẫn) != giáTrịDựKiến: raise SystemExit('cáchĐặtTên CácPhépKiểmTra giáTrịLùi 바뀐 C mãNguồn: '+đườngDẫn)
    kiểmTraJava = json.loads((đườngDẫnViệcThẩmĐịnh/'jvm/report.json').read_text())
    MànHìnhTrựcTiếp = json.loads((đườngDẫnViệcThẩmĐịnh/'swing/report.json').read_text())
    if not MànHìnhTrựcTiếp.get('direct_korean_gui'): raise SystemExit('tiếngViệt 직접 MànHình thựcThiLệnh KiểmThử giáTrịCầnĐến')
    kiểmTraGiáTrịByte = json.loads((đườngDẫnViệcThẩmĐịnh/'naming/direct-bytecode.json').read_text())
    if not kiểmTraGiáTrịByte['passed'] or kiểmTraGiáTrịByte['jar_sha256'] != tệpMãBăm(gốcCâyDựÁn/'dist/jkoros-native-korean.jar'):
        raise SystemExit('phầnMụcHiệnTại tiếngViệt 라이브러리의 직접 gọiThựcHiện mãByte xácMinh giáTrịCầnĐến')
    kiểmTraĐộPhânGiải = json.loads((đườngDẫnViệcThẩmĐịnh/'resolution/report.json').read_text())
    kiểmTraCỡ = json.loads((đườngDẫnViệcThẩmĐịnh/'resize/report.json').read_text())
    kiểmTraCácCậpNhậtCho = json.loads((đườngDẫnViệcThẩmĐịnh/'redraw/report.json').read_text())
    if not kiểmTraCácCậpNhậtCho['passed'] or kiểmTraCácCậpNhậtCho['kernel_sha256'] != mãBămNhân:
        raise SystemExit('phầnMụcHiệnTại 커널의 giáTrịPhầnCon làmMới KiểmThử giáTrịCầnĐến')
    for đườngDẫn, giáTrịDựKiến in kiểmTraCácCậpNhậtCho['source_sha256'].items():
        if tệpMãBăm(gốcCâyDựÁn/đườngDẫn) != giáTrịDựKiến: raise SystemExit('giáTrịPhầnCon làmMới KiểmThử giáTrịLùi 바뀐 mãNguồn: '+đườngDẫn)
    if not kiểmTraJava.get('direct_korean_thread_and_entry'):
        raise SystemExit('tiếngViệt 직접 가닥과 chạy điểmMục KiểmThử giáTrịCầnĐến')
    kiểmTraVíDụ = json.loads((đườngDẫnViệcThẩmĐịnh/'examples/report.json').read_text())
    if sorted(kiểmTraCỡ['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 giáTrịGóc cỡ 조절 KiểmThử giáTrịCầnĐến')
    if not kiểmTraVíDụ.get('swing_example_korean_input_button_label_and_close') or kiểmTraVíDụ['examples_executed'] != 13:
        raise SystemExit('tiếngViệt Swing 창을 포함한 VíDụ 13개 KiểmThử giáTrịCầnĐến')
    if sorted(kiểmTraĐộPhânGiải['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 dữLiệuThựcTế MànHình KiểmThử giáTrịCầnĐến')
    if kiểmTraJava['korean_library_sha256'] != tệpMãBăm(gốcCâyDựÁn/'dist/jkoros-native-korean.jar'):
        raise SystemExit('Java KiểmThử giáTrịLùi 라이브러리가 바뀌었습니다.')
    for tên in ('thửKếtNốiMạngTiếngHàn','thửCácNgoạiLệTiếngHàn'):
        if not any(giáTrịMục['name']==tên and giáTrịMục.get('openjdk_output_equal') for giáTrịMục in kiểmTraJava['tests']):
            raise SystemExit('OpenJDK 대조 KiểmThử giáTrịCầnĐến: '+tên)
    danhSáchNgoạiLệ = sorted(đườngDẫn.stem for đườngDẫn in (gốcCâyDựÁn/'JavaTiếngViệt/tiếngViệt/tựThân').glob('*ngoạiLệ.java'))
    nhậtKýNgoạiLệ = (đườngDẫnViệcThẩmĐịnh/'jvm/thửCácNgoạiLệTiếngHàn.log').read_text().replace('\r\n','\n')
    for tên in danhSáchNgoạiLệ:
        if '\n'+tên+'\n' not in nhậtKýNgoạiLệ: raise SystemExit('ngoạiLệ sinh·잡기·môTả KiểmThử giáTrịCầnĐến: '+tên)
    đặcTả = json.loads((gốcCâyDựÁn/'dist/manifest.json').read_text())
    if đặcTả['image_sha256'] != tệpMãBăm(gốcCâyDựÁn/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('giáTrịBảnPhânPhối giáTrịẢnh tệpMãBăm 불일치')
    with zipfile.ZipFile(str(gốcCâyDựÁn/'dist/jkoros-native-rpi4-boot.zip')) as GóiGộp:
        if hashlib.sha256(GóiGộp.read('kernel8.img')).hexdigest() != mãBămNhân:
            raise SystemExit('KhởiĐộng ZIP giáTrịNhân 불일치')
        cácThiếtLậpKhởiĐộng = GóiGộp.read('config.txt')
        for tên, cỡ in zip(('width', 'height'), đặcTả['framebuffer_resolution']):
            if 'framebuffer_'+tên+'='+str(cỡ) not in cácThiếtLậpKhởiĐộng.decode().splitlines():
                raise SystemExit('KhởiĐộng ZIP MànHình cácThiếtLập 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(gốcCâyDựÁn/'build')) as giáTrịTạm:
        giáTrịĐãSaoChép = Path(giáTrịTạm)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(gốcCâyDựÁn/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(giáTrịĐãSaoChép)])
        if tệpMãBăm(giáTrịĐãSaoChép) != mãBămNhân: raise SystemExit('SD giáTrịẢnh giáTrịNhân 불일치')
        saoChépCácThiếtLập = Path(giáTrịTạm)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(gốcCâyDựÁn/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(saoChépCácThiếtLập)])
        if saoChépCácThiếtLập.read_bytes() != cácThiếtLậpKhởiĐộng: raise SystemExit('SD 영상과 ZIP MànHình cácThiếtLập 불일치')
    bảnGhiNhậtKý = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': mãBămNhân,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': cácBảnGhiNhậtKý, 'naming_report': 'naming/report.json',
            'korean_exception_classes': danhSáchNgoạiLệ, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': kiểmTraVíDụ['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(kiểmTraĐộPhânGiải['resolutions']),
            'sd_framebuffer_resolution': đặcTả['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {tên:tệpMãBăm(gốcCâyDựÁn/'dist'/tên) for tên in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (đườngDẫnViệcThẩmĐịnh/'native-runtime-summary.json').write_text(json.dumps(bảnGhiNhậtKý,ensure_ascii=False,indent=2)+'\n')
    print('PASS: phầnMụcHiệnTại 커널의',len(cácBảnGhiNhậtKý),'개 통합 KiểmThử bảnGhiNhậtKý, tiếngViệt ngoạiLệ',len(danhSáchNgoạiLệ),'địnhNghĩaLớp, SD giáTrịẢnh·ZIP làBằng')

if __name__ == '__main__': chạy()
