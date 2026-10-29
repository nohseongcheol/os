#!/usr/bin/env python3
"""현재 커널과 kgonthe_data 시험·배포물이 일치할 때에만 통합 kgonthiša_5fb2b747 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

기준 = Path(__file__).resolve().parents[1]

def haše_faele(Tsejana):
    계산 = hashlib.sha256()
    with Tsejana.open('rb') as Faele:
        for data in iter(lambda: Faele.read(1048576), b''): 계산.update(data)
    return 계산.hexdigest()

def Diriša():
    tiišetšo_tsela = 기준/'build/verification'
    khenele_haše = haše_faele(기준/'build/kernel8.img')
    기록들 = {}
    for Leina in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Leina == 'boot' else Leina+'/report.json'
        data = json.loads((tiišetšo_tsela/상대경로).read_text())
        if not data.get('passed') or data.get('kernel_sha256') != khenele_haše:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Leina] = {'passed': True, 'report': 상대경로}
    lekola_leina = json.loads((tiišetšo_tsela/'naming/report.json').read_text())
    if not lekola_leina['passed'] or not lekola_leina['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for Tsejana, 기대값 in lekola_leina['c_source_sha256'].items():
        if haše_faele(기준/Tsejana) != 기대값: raise SystemExit('명명 검사 Morago_boleng 바뀐 C mohlodi: '+Tsejana)
    자바검사 = json.loads((tiišetšo_tsela/'jvm/report.json').read_text())
    직접화면 = json.loads((tiišetšo_tsela/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 phethagatša_taelo 시험 필요')
    lekola_paete_boleng = json.loads((tiišetšo_tsela/'naming/direct-bytecode.json').read_text())
    if not lekola_paete_boleng['passed'] or lekola_paete_boleng['jar_sha256'] != haše_faele(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 kgonthiša 필요')
    lekola_sephetho = json.loads((tiišetšo_tsela/'resolution/report.json').read_text())
    lekola_bogolo = json.loads((tiišetšo_tsela/'resize/report.json').read_text())
    갱신검사 = json.loads((tiišetšo_tsela/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != khenele_haše:
        raise SystemExit('현재 커널의 부분 mpshafatša 시험 필요')
    for Tsejana, 기대값 in 갱신검사['source_sha256'].items():
        if haše_faele(기준/Tsejana) != 기대값: raise SystemExit('부분 mpshafatša 시험 Morago_boleng 바뀐 mohlodi: '+Tsejana)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 Diriša go_tsenya_tshedimošo_ntlha 시험 필요')
    예제검사 = json.loads((tiišetšo_tsela/'examples/report.json').read_text())
    if sorted(lekola_bogolo['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Bogolo 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(lekola_sephetho['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 kgonthe_data 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != haše_faele(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 Morago_boleng 라이브러리가 바뀌었습니다.')
    for Leina in ('한국어통신시험','한국어예외시험'):
        if not any(go_tsenya_tshedimošo_boleng['name']==Leina and go_tsenya_tshedimošo_boleng.get('openjdk_output_equal') for go_tsenya_tshedimošo_boleng in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Leina)
    예외들 = sorted(Tsejana.stem for Tsejana in (기준/'한국어자바/한국어/자체').glob('*예외.java'))
    예외기록 = (tiišetšo_tsela/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Leina in 예외들:
        if '\n'+Leina+'\n' not in 예외기록: raise SystemExit('예외 생성·잡기·설명 시험 필요: '+Leina)
    명세 = json.loads((기준/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != haše_faele(기준/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 seswantšho_boleng haše_faele 불일치')
    with zipfile.ZipFile(str(기준/'dist/jkoros-native-rpi4-boot.zip')) as sehlopha:
        if hashlib.sha256(sehlopha.read('kernel8.img')).hexdigest() != khenele_haše:
            raise SystemExit('부팅 ZIP khenele_boleng 불일치')
        부팅설정 = sehlopha.read('config.txt')
        for Leina, Bogolo in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Leina+'='+str(Bogolo) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Dipeakanyo 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(기준/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if haše_faele(복사본) != khenele_haše: raise SystemExit('SD seswantšho_boleng khenele_boleng 불일치')
        kopiša_Dipeakanyo = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(kopiša_Dipeakanyo)])
        if kopiša_Dipeakanyo.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Dipeakanyo 불일치')
    pego_rei = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': khenele_haše,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(lekola_sephetho['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Leina:haše_faele(기준/'dist'/Leina) for Leina in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (tiišetšo_tsela/'native-runtime-summary.json').write_text(json.dumps(pego_rei,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 pego_rei, 한국어 예외',len(예외들),'legoro_Tlhaloso, SD seswantšho_boleng·ZIP 일치')

if __name__ == '__main__': Diriša()
