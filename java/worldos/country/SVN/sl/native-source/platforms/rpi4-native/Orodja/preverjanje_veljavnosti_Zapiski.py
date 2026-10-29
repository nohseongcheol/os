#!/usr/bin/env python3
"""sprotno_element 커널과 dejanski_podatki 시험·배포물이 일치할 때에만 통합 preveriti_veljavnost 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

pobuda_koren = Path(__file__).resolve().parents[1]

def zgoščena_vrednost_Datoteka(POT):
    계산 = hashlib.sha256()
    with POT.open('rb') as Datoteka:
        for podatki in iter(lambda: Datoteka.read(1048576), b''): 계산.update(podatki)
    return 계산.hexdigest()

def Zaženi():
    preverjanje_veljavnosti_pot = pobuda_koren/'build/verification'
    jedro_zgoščena_vrednost = zgoščena_vrednost_Datoteka(pobuda_koren/'build/kernel8.img')
    기록들 = {}
    for Ime in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        relativna_pot = 'report.json' if Ime == 'boot' else Ime+'/report.json'
        podatki = json.loads((preverjanje_veljavnosti_pot/relativna_pot).read_text())
        if not podatki.get('passed') or podatki.get('kernel_sha256') != jedro_zgoščena_vrednost:
            raise SystemExit('sprotno_element 커널에 대한 성공 기록이 필요합니다: '+relativna_pot)
        기록들[Ime] = {'passed': True, 'report': relativna_pot}
    preveriti_ime = json.loads((preverjanje_veljavnosti_pot/'naming/report.json').read_text())
    if not preveriti_ime['passed'] or not preveriti_ime['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for POT, 기대값 in preveriti_ime['c_source_sha256'].items():
        if zgoščena_vrednost_Datoteka(pobuda_koren/POT) != 기대값: raise SystemExit('명명 검사 ZAJ_VALUE 바뀐 C VIR: '+POT)
    자바검사 = json.loads((preverjanje_veljavnosti_pot/'jvm/report.json').read_text())
    직접화면 = json.loads((preverjanje_veljavnosti_pot/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('slovenščina 직접 화면 Izvedi_ukaz 시험 필요')
    preveriti_bajt_VALUE = json.loads((preverjanje_veljavnosti_pot/'naming/direct-bytecode.json').read_text())
    if not preveriti_bajt_VALUE['passed'] or preveriti_bajt_VALUE['jar_sha256'] != zgoščena_vrednost_Datoteka(pobuda_koren/'dist/jkoros-native-korean.jar'):
        raise SystemExit('sprotno_element slovenščina 라이브러리의 직접 호출 바이트코드 확인 필요')
    preveriti_ločljivost = json.loads((preverjanje_veljavnosti_pot/'resolution/report.json').read_text())
    preveriti_spremeniti_velikost = json.loads((preverjanje_veljavnosti_pot/'resize/report.json').read_text())
    갱신검사 = json.loads((preverjanje_veljavnosti_pot/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != jedro_zgoščena_vrednost:
        raise SystemExit('sprotno_element 커널의 부분 osvežiti 시험 필요')
    for POT, 기대값 in 갱신검사['source_sha256'].items():
        if zgoščena_vrednost_Datoteka(pobuda_koren/POT) != 기대값: raise SystemExit('부분 osvežiti 시험 ZAJ_VALUE 바뀐 VIR: '+POT)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('slovenščina 직접 가닥과 Zaženi vnos_p 시험 필요')
    예제검사 = json.loads((preverjanje_veljavnosti_pot/'examples/report.json').read_text())
    if sorted(preveriti_spremeniti_velikost['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Velikost 조절 시험 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('slovenščina Swing 창을 포함한 예제 13개 시험 필요')
    if sorted(preveriti_ločljivost['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 dejanski_podatki 화면 시험 필요')
    if 자바검사['korean_library_sha256'] != zgoščena_vrednost_Datoteka(pobuda_koren/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 시험 ZAJ_VALUE 라이브러리가 바뀌었습니다.')
    for Ime in ('한국어통신시험','한국어예외시험'):
        if not any(vnos_VALUE['name']==Ime and vnos_VALUE.get('openjdk_output_equal') for vnos_VALUE in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 시험 필요: '+Ime)
    izjema_Seznam = sorted(POT.stem for POT in (pobuda_koren/'한국어자바/slovenščina/lastno').glob('*izjema.java'))
    izjema_LOG = (preverjanje_veljavnosti_pot/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Ime in izjema_Seznam:
        if '\n'+Ime+'\n' not in izjema_LOG: raise SystemExit('izjema ustvariti·잡기·설명 시험 필요: '+Ime)
    명세 = json.loads((pobuda_koren/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != zgoščena_vrednost_Datoteka(pobuda_koren/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('배포 IMAGE_VALUE zgoščena_vrednost_Datoteka 불일치')
    with zipfile.ZipFile(str(pobuda_koren/'dist/jkoros-native-rpi4-boot.zip')) as sveženj:
        if hashlib.sha256(sveženj.read('kernel8.img')).hexdigest() != jedro_zgoščena_vrednost:
            raise SystemExit('부팅 ZIP jedro_VALUE 불일치')
        부팅설정 = sveženj.read('config.txt')
        for Ime, Velikost in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Ime+'='+str(Velikost) not in 부팅설정.decode().splitlines():
                raise SystemExit('부팅 ZIP 화면 Nastavitve 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(pobuda_koren/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(pobuda_koren/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if zgoščena_vrednost_Datoteka(복사본) != jedro_zgoščena_vrednost: raise SystemExit('SD IMAGE_VALUE jedro_VALUE 불일치')
        kopirati_Nastavitve = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(pobuda_koren/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(kopirati_Nastavitve)])
        if kopirati_Nastavitve.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Nastavitve 불일치')
    LOG_zapis = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': jedro_zgoščena_vrednost,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': izjema_Seznam, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(preveriti_ločljivost['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Ime:zgoščena_vrednost_Datoteka(pobuda_koren/'dist'/Ime) for Ime in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (preverjanje_veljavnosti_pot/'native-runtime-summary.json').write_text(json.dumps(LOG_zapis,ensure_ascii=False,indent=2)+'\n')
    print('PASS: sprotno_element 커널의',len(기록들),'개 통합 시험 LOG_zapis, slovenščina izjema',len(izjema_Seznam),'Razred_definicija, SD IMAGE_VALUE·ZIP 일치')

if __name__ == '__main__': Zaženi()
