#!/usr/bin/env python3
"""현재 커널과 nyakuri_amakurushingiro 시험·배포물이 일치할 때에만 통합 kwemeza 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

기준 = Path(__file__).resolve().parents[1]

def hashi_dosiye(Inzira):
    계산 = hashlib.sha256()
    with Inzira.open('rb') as Idosiye:
        for amakurushingiro in iter(lambda: Idosiye.read(1048576), b''): 계산.update(amakurushingiro)
    return 계산.hexdigest()

def ihuriro():
    iyemeza_inzira = 기준/'build/verification'
    intima_hashi = hashi_dosiye(기준/'build/kernel8.img')
    기록들 = {}
    for Izina in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Izina == 'boot' else Izina+'/report.json'
        amakurushingiro = json.loads((iyemeza_inzira/상대경로).read_text())
        if not amakurushingiro.get('passed') or amakurushingiro.get('kernel_sha256') != intima_hashi:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Izina] = {'passed': True, 'report': 상대경로}
    sheki_izina = json.loads((iyemeza_inzira/'naming/report.json').read_text())
    if not sheki_izina['passed'] or not sheki_izina['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for Inzira, 기대값 in sheki_izina['c_source_sha256'].items():
        if hashi_dosiye(기준/Inzira) != 기대값: raise SystemExit('명명 검사 Ikibanza_agaciro 바뀐 C Inkomoko: '+Inzira)
    자바검사 = json.loads((iyemeza_inzira/'jvm/report.json').read_text())
    직접화면 = json.loads((iyemeza_inzira/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('Ikinyarwanda 직접 화면 gukora_ibwiriza 시험 필요')
    sheki_bayiti_agaciro = json.loads((iyemeza_inzira/'naming/direct-bytecode.json').read_text())
    if not sheki_bayiti_agaciro['passed'] or sheki_bayiti_agaciro['jar_sha256'] != hashi_dosiye(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 Ikinyarwanda 라이브러리의 직접 호출 바이트코드 gusuzuma 필요')
    sheki_ibonerana = json.loads((iyemeza_inzira/'resolution/report.json').read_text())
    sheki_ingano = json.loads((iyemeza_inzira/'resize/report.json').read_text())
    갱신검사 = json.loads((iyemeza_inzira/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != intima_hashi:
        raise SystemExit('현재 커널의 부분 kugaruraho 시험 필요')
    for Inzira, 기대값 in 갱신검사['source_sha256'].items():
        if hashi_dosiye(기준/Inzira) != 기대값: raise SystemExit('부분 kugaruraho 시험 Ikibanza_agaciro 바뀐 Inkomoko: '+Inzira)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('Ikinyarwanda 직접 가닥과 ihuriro icyinjizwa_inota 시험 필요')
    예제검사 = json.loads((iyemeza_inzira/'examples/report.json').read_text())
    if sorted(sheki_ingano['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Ingano 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('Ikinyarwanda Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(sheki_ibonerana['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 nyakuri_amakurushingiro 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != hashi_dosiye(기준/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 Ikibanza_agaciro 라이브러리가 바뀌었습니다.')
    for Izina in ('한국어통신시험','한국어예외시험'):
        if not any(icyinjizwa_agaciro['name']==Izina and icyinjizwa_agaciro.get('openjdk_output_equal') for icyinjizwa_agaciro in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Izina)
    예외들 = sorted(Inzira.stem for Inzira in (기준/'한국어자바/Ikinyarwanda/자체').glob('*예외.java'))
    예외기록 = (iyemeza_inzira/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Izina in 예외들:
        if '\n'+Izina+'\n' not in 예외기록: raise SystemExit('예외 생성·잡기·설명 시험 필요: '+Izina)
    명세 = json.loads((기준/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != hashi_dosiye(기준/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 ishusho_agaciro hashi_dosiye 불일치')
    with zipfile.ZipFile(str(기준/'dist/jkoros-native-rpi4-boot.zip')) as ipaki:
        if hashlib.sha256(ipaki.read('kernel8.img')).hexdigest() != intima_hashi:
            raise SystemExit('부팅 ZIP intima_agaciro 불일치')
        부팅설정 = ipaki.read('config.txt')
        for Izina, Ingano in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Izina+'='+str(Ingano) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Amagenamiterere 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(기준/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if hashi_dosiye(복사본) != intima_hashi: raise SystemExit('SD ishusho_agaciro intima_agaciro 불일치')
        kopi_Amagenamiterere = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(기준/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(kopi_Amagenamiterere)])
        if kopi_Amagenamiterere.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Amagenamiterere 불일치')
    kubika_umurongo = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': intima_hashi,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': 예외들, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(sheki_ibonerana['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Izina:hashi_dosiye(기준/'dist'/Izina) for Izina in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (iyemeza_inzira/'native-runtime-summary.json').write_text(json.dumps(kubika_umurongo,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 kubika_umurongo, Ikinyarwanda 예외',len(예외들),'icyiciro_Igisobanuro, SD ishusho_agaciro·ZIP 일치')

if __name__ == '__main__': ihuriro()
