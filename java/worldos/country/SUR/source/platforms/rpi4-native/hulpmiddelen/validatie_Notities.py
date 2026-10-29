#!/usr/bin/env python3
"""actueel_item 커널과 werkelijk_gegevens tests·배포물이 일치할 때에만 통합 valideren 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

Taken_wortel = Path(__file__).resolve().parents[1]

def hash_Bestand(pad):
    계산 = hashlib.sha256()
    with pad.open('rb') as bestand:
        for gegevens in iter(lambda: bestand.read(1048576), b''): 계산.update(gegevens)
    return 계산.hexdigest()

def starten():
    validatie_pad = Taken_wortel/'build/verification'
    kernel_hash = hash_Bestand(Taken_wortel/'build/kernel8.img')
    기록들 = {}
    for Naam in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        relatief_pad = 'report.json' if Naam == 'boot' else Naam+'/report.json'
        gegevens = json.loads((validatie_pad/relatief_pad).read_text())
        if not gegevens.get('passed') or gegevens.get('kernel_sha256') != kernel_hash:
            raise SystemExit('actueel_item 커널에 대한 성공 기록이 필요합니다: '+relatief_pad)
        기록들[Naam] = {'passed': True, 'report': relatief_pad}
    cheque_naam = json.loads((validatie_pad/'naming/report.json').read_text())
    if not cheque_naam['passed'] or not cheque_naam['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for pad, 기대값 in cheque_naam['c_source_sha256'].items():
        if hash_Bestand(Taken_wortel/pad) != 기대값: raise SystemExit('명명 검사 BACK_WAARDE 바뀐 C broncode: '+pad)
    자바검사 = json.loads((validatie_pad/'jvm/report.json').read_text())
    직접화면 = json.loads((validatie_pad/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('Nederlands 직접 scherm Uitvoeren_opdracht tests 필요')
    cheque_byte_WAARDE = json.loads((validatie_pad/'naming/direct-bytecode.json').read_text())
    if not cheque_byte_WAARDE['passed'] or cheque_byte_WAARDE['jar_sha256'] != hash_Bestand(Taken_wortel/'dist/jkoros-native-korean.jar'):
        raise SystemExit('actueel_item Nederlands 라이브러리의 직접 호출 바이트코드 bevestigen 필요')
    cheque_resolutie = json.loads((validatie_pad/'resolution/report.json').read_text())
    cheque_formaat_wijzigen = json.loads((validatie_pad/'resize/report.json').read_text())
    갱신검사 = json.loads((validatie_pad/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != kernel_hash:
        raise SystemExit('actueel_item 커널의 부분 vernieuwen tests 필요')
    for pad, 기대값 in 갱신검사['source_sha256'].items():
        if hash_Bestand(Taken_wortel/pad) != 기대값: raise SystemExit('부분 vernieuwen tests BACK_WAARDE 바뀐 broncode: '+pad)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('Nederlands 직접 가닥과 starten beginpunt tests 필요')
    예제검사 = json.loads((validatie_pad/'examples/report.json').read_text())
    if sorted(cheque_formaat_wijzigen['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Grootte 조절 tests 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('Nederlands Swing 창을 포함한 예제 13개 tests 필요')
    if sorted(cheque_resolutie['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 werkelijk_gegevens scherm tests 필요')
    if 자바검사['korean_library_sha256'] != hash_Bestand(Taken_wortel/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 tests BACK_WAARDE 라이브러리가 바뀌었습니다.')
    for Naam in ('한국어통신시험','한국어예외시험'):
        if not any(invoer_WAARDE_962f286b['name']==Naam and invoer_WAARDE_962f286b.get('openjdk_output_equal') for invoer_WAARDE_962f286b in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 tests 필요: '+Naam)
    uitzondering_Lijst = sorted(pad.stem for pad in (Taken_wortel/'한국어자바/Nederlands/Eigen').glob('*uitzondering.java'))
    uitzondering_LOG = (validatie_pad/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Naam in uitzondering_Lijst:
        if '\n'+Naam+'\n' not in uitzondering_LOG: raise SystemExit('uitzondering genereren·잡기·설명 tests 필요: '+Naam)
    specificatie = json.loads((Taken_wortel/'dist/manifest.json').read_text())
    if specificatie['image_sha256'] != hash_Bestand(Taken_wortel/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('distributie_WAARDE kopie_WAARDE hash_Bestand 불일치')
    with zipfile.ZipFile(str(Taken_wortel/'dist/jkoros-native-rpi4-boot.zip')) as bundel:
        if hashlib.sha256(bundel.read('kernel8.img')).hexdigest() != kernel_hash:
            raise SystemExit('machineopstart ZIP kernel_WAARDE 불일치')
        부팅설정 = bundel.read('config.txt')
        for Naam, Grootte in zip(('width', 'height'), specificatie['framebuffer_resolution']):
            if 'framebuffer_'+Naam+'='+str(Grootte) not in 부팅설정.decode().splitlines():
                raise SystemExit('machineopstart ZIP scherm Instellingen 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(Taken_wortel/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(Taken_wortel/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if hash_Bestand(복사본) != kernel_hash: raise SystemExit('SD kopie_WAARDE kernel_WAARDE 불일치')
        kopiëren_Instellingen = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(Taken_wortel/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(kopiëren_Instellingen)])
        if kopiëren_Instellingen.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP scherm Instellingen 불일치')
    LOG_RECORD = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': kernel_hash,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': uitzondering_Lijst, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(cheque_resolutie['resolutions']),
            'sd_framebuffer_resolution': specificatie['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Naam:hash_Bestand(Taken_wortel/'dist'/Naam) for Naam in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (validatie_pad/'native-runtime-summary.json').write_text(json.dumps(LOG_RECORD,ensure_ascii=False,indent=2)+'\n')
    print('PASS: actueel_item 커널의',len(기록들),'개 통합 tests LOG_RECORD, Nederlands uitzondering',len(uitzondering_Lijst),'les_Definitie, SD kopie_WAARDE·ZIP 일치')

if __name__ == '__main__': starten()
