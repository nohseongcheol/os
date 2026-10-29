#!/usr/bin/env python3
"""pašreizējais_krājums 커널과 faktisks_dati 시험·배포물이 일치할 때에만 통합 validēt 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

Project_sakne = Path(__file__).resolve().parents[1]

def jaukšana_Fails(CEĻŠ):
    계산 = hashlib.sha256()
    with CEĻŠ.open('rb') as Fails:
        for dati in iter(lambda: Fails.read(1048576), b''): 계산.update(dati)
    return 계산.hexdigest()

def Palaist():
    validācija_ceļš = Project_sakne/'build/verification'
    kodols_jaukšana = jaukšana_Fails(Project_sakne/'build/kernel8.img')
    기록들 = {}
    for Nosaukums in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        relatīvais_ceļš = 'report.json' if Nosaukums == 'boot' else Nosaukums+'/report.json'
        dati = json.loads((validācija_ceļš/relatīvais_ceļš).read_text())
        if not dati.get('passed') or dati.get('kernel_sha256') != kodols_jaukšana:
            raise SystemExit('pašreizējais_krājums 커널에 대한 성공 기록이 필요합니다: '+relatīvais_ceļš)
        기록들[Nosaukums] = {'passed': True, 'report': relatīvais_ceļš}
    čeks_nosaukums = json.loads((validācija_ceļš/'naming/report.json').read_text())
    if not čeks_nosaukums['passed'] or not čeks_nosaukums['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for CEĻŠ, 기대값 in čeks_nosaukums['c_source_sha256'].items():
        if jaukšana_Fails(Project_sakne/CEĻŠ) != 기대값: raise SystemExit('명명 검사 ATPAKAĻ_VALUE 바뀐 C AVOTS: '+CEĻŠ)
    자바검사 = json.loads((validācija_ceļš/'jvm/report.json').read_text())
    직접화면 = json.loads((validācija_ceļš/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('Latviešu 직접 화면 Izpildīt_komanda 시험 필요')
    čeks_byte_VALUE = json.loads((validācija_ceļš/'naming/direct-bytecode.json').read_text())
    if not čeks_byte_VALUE['passed'] or čeks_byte_VALUE['jar_sha256'] != jaukšana_Fails(Project_sakne/'dist/jkoros-native-korean.jar'):
        raise SystemExit('pašreizējais_krājums Latviešu 라이브러리의 직접 호출 바이트코드 verificēt 필요')
    čeks_izšķirtspēja = json.loads((validācija_ceļš/'resolution/report.json').read_text())
    čeks_mainīt_izmērus = json.loads((validācija_ceļš/'resize/report.json').read_text())
    갱신검사 = json.loads((validācija_ceļš/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != kodols_jaukšana:
        raise SystemExit('pašreizējais_krājums 커널의 부분 atsvaidzināt 시험 필요')
    for CEĻŠ, 기대값 in 갱신검사['source_sha256'].items():
        if jaukšana_Fails(Project_sakne/CEĻŠ) != 기대값: raise SystemExit('부분 atsvaidzināt 시험 ATPAKAĻ_VALUE 바뀐 AVOTS: '+CEĻŠ)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('Latviešu 직접 가닥과 Palaist ieejas_punkts 시험 필요')
    예제검사 = json.loads((validācija_ceļš/'examples/report.json').read_text())
    if sorted(čeks_mainīt_izmērus['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Izmērs 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('Latviešu Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(čeks_izšķirtspēja['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 faktisks_dati 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != jaukšana_Fails(Project_sakne/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 ATPAKAĻ_VALUE 라이브러리가 바뀌었습니다.')
    for Nosaukums in ('한국어통신시험','한국어예외시험'):
        if not any(ievade_VALUE['name']==Nosaukums and ievade_VALUE.get('openjdk_output_equal') for ievade_VALUE in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Nosaukums)
    izņēmums_Saraksts = sorted(CEĻŠ.stem for CEĻŠ in (Project_sakne/'한국어자바/Latviešu/savs').glob('*izņēmums.java'))
    izņēmums_LOG = (validācija_ceļš/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Nosaukums in izņēmums_Saraksts:
        if '\n'+Nosaukums+'\n' not in izņēmums_LOG: raise SystemExit('izņēmums ģenerēt·잡기·설명 시험 필요: '+Nosaukums)
    명세 = json.loads((Project_sakne/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != jaukšana_Fails(Project_sakne/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('sadale_VALUE IMAGE_VALUE jaukšana_Fails 불일치')
    with zipfile.ZipFile(str(Project_sakne/'dist/jkoros-native-rpi4-boot.zip')) as saistīt:
        if hashlib.sha256(saistīt.read('kernel8.img')).hexdigest() != kodols_jaukšana:
            raise SystemExit('부팅 ZIP kodols_VALUE 불일치')
        부팅설정 = saistīt.read('config.txt')
        for Nosaukums, Izmērs in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Nosaukums+'='+str(Izmērs) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Uzstādījumi 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(Project_sakne/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(Project_sakne/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if jaukšana_Fails(복사본) != kodols_jaukšana: raise SystemExit('SD IMAGE_VALUE kodols_VALUE 불일치')
        kopēt_Iestatījumi = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(Project_sakne/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(kopēt_Iestatījumi)])
        if kopēt_Iestatījumi.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Uzstādījumi 불일치')
    LOG_RECORD = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': kodols_jaukšana,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': izņēmums_Saraksts, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(čeks_izšķirtspēja['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Nosaukums:jaukšana_Fails(Project_sakne/'dist'/Nosaukums) for Nosaukums in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (validācija_ceļš/'native-runtime-summary.json').write_text(json.dumps(LOG_RECORD,ensure_ascii=False,indent=2)+'\n')
    print('PASS: pašreizējais_krājums 커널의',len(기록들),'개 통합 시험 LOG_RECORD, Latviešu izņēmums',len(izņēmums_Saraksts),'klase_definīcija, SD IMAGE_VALUE·ZIP 일치')

if __name__ == '__main__': Palaist()
