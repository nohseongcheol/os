#!/usr/bin/env python3
"""ga_jaana_selwana 커널과 tota_tshedimosetso 시험·배포물이 일치할 때에만 통합 netefatsa_5fb2b747 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

기준 = Path(__file__).resolve().parents[1]

def heše_faele(tsela):
    계산 = hashlib.sha256()
    with tsela.open('rb') as faele:
        for tshedimosetso in iter(lambda: faele.read(1048576), b''): 계산.update(tshedimosetso)
    return 계산.hexdigest()

def dirisa():
    netefatso_tsela = 기준/'build/verification'
    Khenele_heše = heše_faele(기준/'build/kernel8.img')
    기록들 = {}
    for leina in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if leina == 'boot' else leina+'/report.json'
        tshedimosetso = json.loads((netefatso_tsela/상대경로).read_text())
        if not tshedimosetso.get('passed') or tshedimosetso.get('kernel_sha256') != Khenele_heše:
            raise SystemExit('ga_jaana_selwana 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[leina] = {'passed': True, 'report': 상대경로}
    tlhola_leina = json.loads((netefatso_tsela/'naming/report.json').read_text())
    if not tlhola_leina['passed'] or not tlhola_leina['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for tsela, 기대값 in tlhola_leina['c_source_sha256'].items():
        if heše_faele(기준/tsela) != 기대값: raise SystemExit('명명 검사 Morago_Boleng 바뀐 C Motswedi: '+tsela)
    자바검사 = json.loads((netefatso_tsela/'jvm/report.json').read_text())
    직접화면 = json.loads((netefatso_tsela/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 diragatsa_Taelo 시험 필요')
    tlhola_baete_Boleng = json.loads((netefatso_tsela/'naming/direct-bytecode.json').read_text())
    if not tlhola_baete_Boleng['passed'] or tlhola_baete_Boleng['jar_sha256'] != heše_faele(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('ga_jaana_selwana 한국어 라이브러리의 직접 호출 바이트코드 netefatsa 필요')
    tlhola_resolušene = json.loads((netefatso_tsela/'resolution/report.json').read_text())
    tlhola_lekanya = json.loads((netefatso_tsela/'resize/report.json').read_text())
    갱신검사 = json.loads((netefatso_tsela/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != Khenele_heše:
        raise SystemExit('ga_jaana_selwana 커널의 부분 Tsosolosa 시험 필요')
    for tsela, 기대값 in 갱신검사['source_sha256'].items():
        if heše_faele(기준/tsela) != 기대값: raise SystemExit('부분 Tsosolosa 시험 Morago_Boleng 바뀐 Motswedi: '+tsela)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 dirisa tsenyo_ntlha 시험 필요')
    예제검사 = json.loads((netefatso_tsela/'examples/report.json').read_text())
    if sorted(tlhola_lekanya['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 lekanya 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(tlhola_resolušene['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 tota_tshedimosetso 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != heše_faele(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 Morago_Boleng 라이브러리가 바뀌었습니다.')
    for leina in ('한국어통신시험','한국어예외시험'):
        if not any(tsenyo_Boleng['name']==leina and tsenyo_Boleng.get('openjdk_output_equal') for tsenyo_Boleng in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+leina)
    예외들 = sorted(tsela.stem for tsela in (기준/'한국어자바/한국어/자체').glob('*예외.java'))
    예외기록 = (netefatso_tsela/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for leina in 예외들:
        if '\n'+leina+'\n' not in 예외기록: raise SystemExit('예외 생성·잡기·설명 시험 필요: '+leina)
    명세 = json.loads((기준/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != heše_faele(기준/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 Setshwantsho_Boleng heše_faele 불일치')
    with zipfile.ZipFile(str(기준/'dist/jkoros-native-rpi4-boot.zip')) as ngatanngwe:
        if hashlib.sha256(ngatanngwe.read('kernel8.img')).hexdigest() != Khenele_heše:
            raise SystemExit('부팅 ZIP Khenele_Boleng 불일치')
        부팅설정 = ngatanngwe.read('config.txt')
        for leina, lekanya in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+leina+'='+str(lekanya) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Diseting 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(기준/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if heše_faele(복사본) != Khenele_heše: raise SystemExit('SD Setshwantsho_Boleng Khenele_Boleng 불일치')
        leloko_Diseting = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(leloko_Diseting)])
        if leloko_Diseting.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Diseting 불일치')
    rekota_mola = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': Khenele_heše,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(tlhola_resolušene['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {leina:heše_faele(기준/'dist'/leina) for leina in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (netefatso_tsela/'native-runtime-summary.json').write_text(json.dumps(rekota_mola,ensure_ascii=False,indent=2)+'\n')
    print('PASS: ga_jaana_selwana 커널의',len(기록들),'개 통합 시험 rekota_mola, 한국어 예외',len(예외들),'mofuta_Tlhaloso, SD Setshwantsho_Boleng·ZIP 일치')

if __name__ == '__main__': dirisa()
