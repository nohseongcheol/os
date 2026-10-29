#!/usr/bin/env python3
"""trenutno_stavka 커널과 stvaran_podaci 시험·배포물이 일치할 때에만 통합 ovjeriti 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

projicirati_koijen = Path(__file__).resolve().parents[1]

def raspršivanje_fajl(Putanja):
    계산 = hashlib.sha256()
    with Putanja.open('rb') as Fajl:
        for podaci in iter(lambda: Fajl.read(1048576), b''): 계산.update(podaci)
    return 계산.hexdigest()

def Pokreni():
    provjera_put = projicirati_koijen/'build/verification'
    jezgro_raspršivanje = raspršivanje_fajl(projicirati_koijen/'build/kernel8.img')
    기록들 = {}
    for Naziv in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Naziv == 'boot' else Naziv+'/report.json'
        podaci = json.loads((provjera_put/상대경로).read_text())
        if not podaci.get('passed') or podaci.get('kernel_sha256') != jezgro_raspršivanje:
            raise SystemExit('trenutno_stavka 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Naziv] = {'passed': True, 'report': 상대경로}
    ček_naziv = json.loads((provjera_put/'naming/report.json').read_text())
    if not ček_naziv['passed'] or not ček_naziv['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for Putanja, 기대값 in ček_naziv['c_source_sha256'].items():
        if raspršivanje_fajl(projicirati_koijen/Putanja) != 기대값: raise SystemExit('명명 검사 ZAD_VALUE 바뀐 C IZVOR: '+Putanja)
    자바검사 = json.loads((provjera_put/'jvm/report.json').read_text())
    직접화면 = json.loads((provjera_put/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('한국어 직접 화면 Izvrši_komanda 시험 필요')
    ček_bajt_VALUE = json.loads((provjera_put/'naming/direct-bytecode.json').read_text())
    if not ček_bajt_VALUE['passed'] or ček_bajt_VALUE['jar_sha256'] != raspršivanje_fajl(projicirati_koijen/'dist/jkoros-native-korean.jar'):
        raise SystemExit('trenutno_stavka 한국어 라이브러리의 직접 호출 바이트코드 potvrditi 필요')
    ček_rezolucija = json.loads((provjera_put/'resolution/report.json').read_text())
    ček_podesiti_veličinu = json.loads((provjera_put/'resize/report.json').read_text())
    갱신검사 = json.loads((provjera_put/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != jezgro_raspršivanje:
        raise SystemExit('trenutno_stavka 커널의 부분 osvježiti 시험 필요')
    for Putanja, 기대값 in 갱신검사['source_sha256'].items():
        if raspršivanje_fajl(projicirati_koijen/Putanja) != 기대값: raise SystemExit('부분 osvježiti 시험 ZAD_VALUE 바뀐 IZVOR: '+Putanja)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('한국어 직접 가닥과 Pokreni unos_p 시험 필요')
    예제검사 = json.loads((provjera_put/'examples/report.json').read_text())
    if sorted(ček_podesiti_veličinu['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Veličina 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('한국어 Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(ček_rezolucija['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 stvaran_podaci 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != raspršivanje_fajl(projicirati_koijen/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 ZAD_VALUE 라이브러리가 바뀌었습니다.')
    for Naziv in ('한국어통신시험','한국어예외시험'):
        if not any(unos_VALUE['name']==Naziv and unos_VALUE.get('openjdk_output_equal') for unos_VALUE in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Naziv)
    izuzetak_spisak = sorted(Putanja.stem for Putanja in (projicirati_koijen/'한국어자바/한국어/자체').glob('*izuzetak.java'))
    izuzetak_LOG = (provjera_put/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Naziv in izuzetak_spisak:
        if '\n'+Naziv+'\n' not in izuzetak_LOG: raise SystemExit('izuzetak generirati·잡기·설명 시험 필요: '+Naziv)
    명세 = json.loads((projicirati_koijen/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != raspršivanje_fajl(projicirati_koijen/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 IMAGE_VALUE raspršivanje_fajl 불일치')
    with zipfile.ZipFile(str(projicirati_koijen/'dist/jkoros-native-rpi4-boot.zip')) as paket:
        if hashlib.sha256(paket.read('kernel8.img')).hexdigest() != jezgro_raspršivanje:
            raise SystemExit('부팅 ZIP jezgro_VALUE 불일치')
        부팅설정 = paket.read('config.txt')
        for Naziv, Veličina in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Naziv+'='+str(Veličina) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Postavke 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(projicirati_koijen/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(projicirati_koijen/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if raspršivanje_fajl(복사본) != jezgro_raspršivanje: raise SystemExit('SD IMAGE_VALUE jezgro_VALUE 불일치')
        instanca_Postavke = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(projicirati_koijen/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(instanca_Postavke)])
        if instanca_Postavke.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Postavke 불일치')
    LOG_red = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': jezgro_raspršivanje,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': izuzetak_spisak, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(ček_rezolucija['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Naziv:raspršivanje_fajl(projicirati_koijen/'dist'/Naziv) for Naziv in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (provjera_put/'native-runtime-summary.json').write_text(json.dumps(LOG_red,ensure_ascii=False,indent=2)+'\n')
    print('PASS: trenutno_stavka 커널의',len(기록들),'개 통합 시험 LOG_red, 한국어 izuzetak',len(izuzetak_spisak),'klasa_Definicija, SD IMAGE_VALUE·ZIP 일치')

if __name__ == '__main__': Pokreni()
