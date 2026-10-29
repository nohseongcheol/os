#!/usr/bin/env python3
"""현재 커널과 benetako_datuak 시험·배포물이 일치할 때에만 통합 baliozkotu 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

Project_erro = Path(__file__).resolve().parents[1]

def hash_fitxategi(Bide_izena):
    계산 = hashlib.sha256()
    with Bide_izena.open('rb') as Fitxategia:
        for datuak in iter(lambda: Fitxategia.read(1048576), b''): 계산.update(datuak)
    return 계산.hexdigest()

def Exekutatu_2():
    balidazio_bide_izen = Project_erro/'build/verification'
    nukleo_hash = hash_fitxategi(Project_erro/'build/kernel8.img')
    기록들 = {}
    for Izena in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        상대경로 = 'report.json' if Izena == 'boot' else Izena+'/report.json'
        datuak = json.loads((balidazio_bide_izen/상대경로).read_text())
        if not datuak.get('passed') or datuak.get('kernel_sha256') != nukleo_hash:
            raise SystemExit('현재 커널에 대한 성공 기록이 필요합니다: '+상대경로)
        기록들[Izena] = {'passed': True, 'report': 상대경로}
    txeke_izen = json.loads((balidazio_bide_izen/'naming/report.json').read_text())
    if not txeke_izen['passed'] or not txeke_izen['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for Bide_izena, 기대값 in txeke_izen['c_source_sha256'].items():
        if hash_fitxategi(Project_erro/Bide_izena) != 기대값: raise SystemExit('명명 검사 ATZERA_balio 바뀐 C ITURBURUA: '+Bide_izena)
    자바검사 = json.loads((balidazio_bide_izen/'jvm/report.json').read_text())
    직접화면 = json.loads((balidazio_bide_izen/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('Euskara 직접 화면 exekutatu_komando 시험 필요')
    txeke_byte_balio = json.loads((balidazio_bide_izen/'naming/direct-bytecode.json').read_text())
    if not txeke_byte_balio['passed'] or txeke_byte_balio['jar_sha256'] != hash_fitxategi(Project_erro/'dist/jkoros-native-korean.jar'):
        raise SystemExit('현재 Euskara 라이브러리의 직접 호출 바이트코드 egiaztatu 필요')
    txeke_bereizmen = json.loads((balidazio_bide_izen/'resolution/report.json').read_text())
    크기검사 = json.loads((balidazio_bide_izen/'resize/report.json').read_text())
    갱신검사 = json.loads((balidazio_bide_izen/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != nukleo_hash:
        raise SystemExit('현재 커널의 부분 freskatu 시험 필요')
    for Bide_izena, 기대값 in 갱신검사['source_sha256'].items():
        if hash_fitxategi(Project_erro/Bide_izena) != 기대값: raise SystemExit('부분 freskatu 시험 ATZERA_balio 바뀐 ITURBURUA: '+Bide_izena)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('Euskara 직접 가닥과 Exekutatu_2 sarrera_p 시험 필요')
    예제검사 = json.loads((balidazio_bide_izen/'examples/report.json').read_text())
    if sorted(크기검사['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Tamaina 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('Euskara Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(txeke_bereizmen['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 benetako_datuak 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != hash_fitxategi(Project_erro/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 ATZERA_balio 라이브러리가 바뀌었습니다.')
    for Izena in ('한국어통신시험','한국어예외시험'):
        if not any(sarrera_balio['name']==Izena and sarrera_balio.get('openjdk_output_equal') for sarrera_balio in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Izena)
    salbuespen_Zerrenda = sorted(Bide_izena.stem for Bide_izena in (Project_erro/'한국어자바/Euskara/자체').glob('*salbuespen.java'))
    salbuespen_LOG = (balidazio_bide_izen/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Izena in salbuespen_Zerrenda:
        if '\n'+Izena+'\n' not in salbuespen_LOG: raise SystemExit('salbuespen sortu·잡기·설명 시험 필요: '+Izena)
    명세 = json.loads((Project_erro/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != hash_fitxategi(Project_erro/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 irudi_balio hash_fitxategi 불일치')
    with zipfile.ZipFile(str(Project_erro/'dist/jkoros-native-rpi4-boot.zip')) as multzo:
        if hashlib.sha256(multzo.read('kernel8.img')).hexdigest() != nukleo_hash:
            raise SystemExit('부팅 ZIP nukleo_balio 불일치')
        부팅설정 = multzo.read('config.txt')
        for Izena, Tamaina in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Izena+'='+str(Tamaina) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Ezarpenak 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(Project_erro/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(Project_erro/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if hash_fitxategi(복사본) != nukleo_hash: raise SystemExit('SD irudi_balio nukleo_balio 불일치')
        kopiatu_Ezarpenak = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(Project_erro/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(kopiatu_Ezarpenak)])
        if kopiatu_Ezarpenak.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Ezarpenak 불일치')
    LOG_marka = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': nukleo_hash,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': salbuespen_Zerrenda, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(txeke_bereizmen['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Izena:hash_fitxategi(Project_erro/'dist'/Izena) for Izena in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (balidazio_bide_izen/'native-runtime-summary.json').write_text(json.dumps(LOG_marka,ensure_ascii=False,indent=2)+'\n')
    print('PASS: 현재 커널의',len(기록들),'개 통합 시험 LOG_marka, Euskara salbuespen',len(salbuespen_Zerrenda),'Gela_Definizioa, SD irudi_balio·ZIP 일치')

if __name__ == '__main__': Exekutatu_2()
