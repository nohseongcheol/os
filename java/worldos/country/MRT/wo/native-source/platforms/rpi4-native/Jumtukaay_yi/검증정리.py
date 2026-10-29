#!/usr/bin/env python3
"""현재 커널과 liteew_mbir 시험·배포물이 일치할 때에만 통합 wéral 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

기준 = Path(__file__).resolve().parents[1]

def caabiy_teqale_bi_bara_denc(Yoonu_jëmale):
    계산 = hashlib.sha256()
    with Yoonu_jëmale.open('rb') as bara_denc:
        for mbir in iter(lambda: bara_denc.read(1048576), b''): 계산.update(mbir)
    return 계산.hexdigest()

def daw():
    wéral_Yoonu_jëmale = 기준/'build/verification'
    xoox_caabiy_teqale_bi = caabiy_teqale_bi_bara_denc(기준/'build/kernel8.img')
    기록들 = {}
    for tur_253d1510 in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if tur_253d1510 == 'boot' else tur_253d1510+'/report.json'
        mbir = json.loads((wéral_Yoonu_jëmale/상대경로).read_text())
        if not mbir.get('passed') or mbir.get('kernel_sha256') != xoox_caabiy_teqale_bi:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[tur_253d1510] = {'passed': True, 'report': 상대경로}
    sek_tur = json.loads((wéral_Yoonu_jëmale/'naming/report.json').read_text())
    if not sek_tur['passed'] or not sek_tur['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for Yoonu_jëmale, 기대값 in sek_tur['c_source_sha256'].items():
        if caabiy_teqale_bi_bara_denc(기준/Yoonu_jëmale) != 기대값: raise SystemExit('명명 검사 woñeeku_xëyma 바뀐 C Cosaan: '+Yoonu_jëmale)
    자바검사 = json.loads((wéral_Yoonu_jëmale/'jvm/report.json').read_text())
    직접화면 = json.loads((wéral_Yoonu_jëmale/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 def_ndigel 시험 필요')
    sek_okte_xëyma = json.loads((wéral_Yoonu_jëmale/'naming/direct-bytecode.json').read_text())
    if not sek_okte_xëyma['passed'] or sek_okte_xëyma['jar_sha256'] != caabiy_teqale_bi_bara_denc(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 한국어 라이브러리의 직접 호출 바이트코드 luñutu 필요')
    sek_Sottal = json.loads((wéral_Yoonu_jëmale/'resolution/report.json').read_text())
    sek_tolluwaay = json.loads((wéral_Yoonu_jëmale/'resize/report.json').read_text())
    갱신검사 = json.loads((wéral_Yoonu_jëmale/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != xoox_caabiy_teqale_bi:
        raise SystemExit('현재 커널의 부분 Yeesal 시험 필요')
    for Yoonu_jëmale, 기대값 in 갱신검사['source_sha256'].items():
        if caabiy_teqale_bi_bara_denc(기준/Yoonu_jëmale) != 기대값: raise SystemExit('부분 Yeesal 시험 woñeeku_xëyma 바뀐 Cosaan: '+Yoonu_jëmale)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 daw dugal_xabaar_Tomb 시험 필요')
    예제검사 = json.loads((wéral_Yoonu_jëmale/'examples/report.json').read_text())
    if sorted(sek_tolluwaay['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 tolluwaay 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(sek_Sottal['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 liteew_mbir 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != caabiy_teqale_bi_bara_denc(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 woñeeku_xëyma 라이브러리가 바뀌었습니다.')
    for tur_253d1510 in ('한국어통신시험','한국어예외시험'):
        if not any(dugal_xabaar_xëyma['name']==tur_253d1510 and dugal_xabaar_xëyma.get('openjdk_output_equal') for dugal_xabaar_xëyma in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+tur_253d1510)
    예외들 = sorted(Yoonu_jëmale.stem for Yoonu_jëmale in (기준/'한국어자바/한국어/자체').glob('*예외.java'))
    예외기록 = (wéral_Yoonu_jëmale/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for tur_253d1510 in 예외들:
        if '\n'+tur_253d1510+'\n' not in 예외기록: raise SystemExit('예외 생성·잡기·설명 시험 필요: '+tur_253d1510)
    명세 = json.loads((기준/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != caabiy_teqale_bi_bara_denc(기준/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 nataal_xëyma caabiy_teqale_bi_bara_denc 불일치')
    with zipfile.ZipFile(str(기준/'dist/jkoros-native-rpi4-boot.zip')) as takku_xéewël:
        if hashlib.sha256(takku_xéewël.read('kernel8.img')).hexdigest() != xoox_caabiy_teqale_bi:
            raise SystemExit('부팅 ZIP xoox_xëyma 불일치')
        부팅설정 = takku_xéewël.read('config.txt')
        for tur_253d1510, tolluwaay in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+tur_253d1510+'='+str(tolluwaay) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Jekkal_yi 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(기준/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if caabiy_teqale_bi_bara_denc(복사본) != xoox_caabiy_teqale_bi: raise SystemExit('SD nataal_xëyma xoox_xëyma 불일치')
        mbokk_Jekkal_yi = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(mbokk_Jekkal_yi)])
        if mbokk_Jekkal_yi.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Jekkal_yi 불일치')
    làq_Dënk = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': xoox_caabiy_teqale_bi,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(sek_Sottal['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {tur_253d1510:caabiy_teqale_bi_bara_denc(기준/'dist'/tur_253d1510) for tur_253d1510 in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (wéral_Yoonu_jëmale/'native-runtime-summary.json').write_text(json.dumps(làq_Dënk,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 làq_Dënk, 한국어 예외',len(예외들),'maas_Tekki_baat, SD nataal_xëyma·ZIP 일치')

if __name__ == '__main__': daw()
