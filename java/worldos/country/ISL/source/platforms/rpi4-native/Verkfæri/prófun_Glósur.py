#!/usr/bin/env python3
"""현재 커널과 raun_gögn 시험·배포물이 일치할 때에만 통합 staðfesta 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

verk_rót = Path(__file__).resolve().parents[1]

def tæting_skrá(SLÓÐ):
    계산 = hashlib.sha256()
    with SLÓÐ.open('rb') as Skrá:
        for gögn in iter(lambda: Skrá.read(1048576), b''): 계산.update(gögn)
    return 계산.hexdigest()

def Keyra_2():
    prófun_slóð = verk_rót/'build/verification'
    kjarni_tæting = tæting_skrá(verk_rót/'build/kernel8.img')
    기록들 = {}
    for Heiti in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Heiti == 'boot' else Heiti+'/report.json'
        gögn = json.loads((prófun_slóð/상대경로).read_text())
        if not gögn.get('passed') or gögn.get('kernel_sha256') != kjarni_tæting:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Heiti] = {'passed': True, 'report': 상대경로}
    athuga_heiti = json.loads((prófun_slóð/'naming/report.json').read_text())
    if not athuga_heiti['passed'] or not athuga_heiti['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for SLÓÐ, 기대값 in athuga_heiti['c_source_sha256'].items():
        if tæting_skrá(verk_rót/SLÓÐ) != 기대값: raise SystemExit('명명 검사 TIL_BAKA_VALUE 바뀐 C Uppruni: '+SLÓÐ)
    자바검사 = json.loads((prófun_slóð/'jvm/report.json').read_text())
    직접화면 = json.loads((prófun_slóð/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('Íslenska 직접 화면 keyra_skipun 시험 필요')
    athuga_bæti_VALUE = json.loads((prófun_slóð/'naming/direct-bytecode.json').read_text())
    if not athuga_bæti_VALUE['passed'] or athuga_bæti_VALUE['jar_sha256'] != tæting_skrá(verk_rót/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 Íslenska 라이브러리의 직접 호출 바이트코드 sannprófa 필요')
    athuga_upplausn = json.loads((prófun_slóð/'resolution/report.json').read_text())
    athuga_breyta_stærð = json.loads((prófun_slóð/'resize/report.json').read_text())
    갱신검사 = json.loads((prófun_slóð/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != kjarni_tæting:
        raise SystemExit('현재 커널의 부분 uppfæra 시험 필요')
    for SLÓÐ, 기대값 in 갱신검사['source_sha256'].items():
        if tæting_skrá(verk_rót/SLÓÐ) != 기대값: raise SystemExit('부분 uppfæra 시험 TIL_BAKA_VALUE 바뀐 Uppruni: '+SLÓÐ)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('Íslenska 직접 가닥과 Keyra_2 færsla_P 시험 필요')
    예제검사 = json.loads((prófun_slóð/'examples/report.json').read_text())
    if sorted(athuga_breyta_stærð['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Stærð 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('Íslenska Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(athuga_upplausn['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 raun_gögn 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != tæting_skrá(verk_rót/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 TIL_BAKA_VALUE 라이브러리가 바뀌었습니다.')
    for Heiti in ('한국어통신시험','한국어예외시험'):
        if not any(færsla_VALUE['name']==Heiti and færsla_VALUE.get('openjdk_output_equal') for færsla_VALUE in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Heiti)
    undantekning_Listi = sorted(SLÓÐ.stem for SLÓÐ in (verk_rót/'한국어자바/Íslenska/eigin').glob('*undantekning.java'))
    undantekning_LOG = (prófun_slóð/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Heiti in undantekning_Listi:
        if '\n'+Heiti+'\n' not in undantekning_LOG: raise SystemExit('undantekning skapa·잡기·설명 시험 필요: '+Heiti)
    명세 = json.loads((verk_rót/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != tæting_skrá(verk_rót/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('dreifing_VALUE mynd_VALUE tæting_skrá 불일치')
    with zipfile.ZipFile(str(verk_rót/'dist/jkoros-native-rpi4-boot.zip')) as búnt:
        if hashlib.sha256(búnt.read('kernel8.img')).hexdigest() != kjarni_tæting:
            raise SystemExit('부팅 ZIP kjarni_VALUE 불일치')
        부팅설정 = búnt.read('config.txt')
        for Heiti, Stærð in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Heiti+'='+str(Stærð) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Stillingar 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(verk_rót/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(verk_rót/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if tæting_skrá(복사본) != kjarni_tæting: raise SystemExit('SD mynd_VALUE kjarni_VALUE 불일치')
        afrita_Stillingar = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(verk_rót/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(afrita_Stillingar)])
        if afrita_Stillingar.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Stillingar 불일치')
    LOG_lína = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': kjarni_tæting,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': undantekning_Listi, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(athuga_upplausn['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Heiti:tæting_skrá(verk_rót/'dist'/Heiti) for Heiti in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (prófun_slóð/'native-runtime-summary.json').write_text(json.dumps(LOG_lína,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 LOG_lína, Íslenska undantekning',len(undantekning_Listi),'klasi_Skilgreining, SD mynd_VALUE·ZIP 일치')

if __name__ == '__main__': Keyra_2()
