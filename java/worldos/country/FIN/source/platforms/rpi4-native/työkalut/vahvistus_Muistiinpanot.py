#!/usr/bin/env python3
"""nykyinen_kohde 커널과 todellinen_data testit·배포물이 일치할 때에만 통합 vahvista 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

aloite_juuri = Path(__file__).resolve().parents[1]

def hajautusarvo_Tiedosto(polku_2):
    계산 = hashlib.sha256()
    with polku_2.open('rb') as tiedoston_nimi:
        for data in iter(lambda: tiedoston_nimi.read(1048576), b''): 계산.update(data)
    return 계산.hexdigest()

def Suorita_2():
    vahvistus_polku = aloite_juuri/'build/verification'
    ydin_hajautusarvo = hajautusarvo_Tiedosto(aloite_juuri/'build/kernel8.img')
    기록들 = {}
    for Nimi in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        suhteellinen_polku = 'report.json' if Nimi == 'boot' else Nimi+'/report.json'
        data = json.loads((vahvistus_polku/suhteellinen_polku).read_text())
        if not data.get('passed') or data.get('kernel_sha256') != ydin_hajautusarvo:
            raise SystemExit('nykyinen_kohde 커널에 대한 성공 기록이 필요합니다: '+suhteellinen_polku)
        기록들[Nimi] = {'passed': True, 'report': suhteellinen_polku}
    sekki_nimi = json.loads((vahvistus_polku/'naming/report.json').read_text())
    if not sekki_nimi['passed'] or not sekki_nimi['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for polku_2, 기대값 in sekki_nimi['c_source_sha256'].items():
        if hajautusarvo_Tiedosto(aloite_juuri/polku_2) != 기대값: raise SystemExit('명명 검사 BACK_ARVO 바뀐 C lähdetiedosto: '+polku_2)
    자바검사 = json.loads((vahvistus_polku/'jvm/report.json').read_text())
    직접화면 = json.loads((vahvistus_polku/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('suomi 직접 화면 Suorita_komento testit 필요')
    sekki_tavu_ARVO = json.loads((vahvistus_polku/'naming/direct-bytecode.json').read_text())
    if not sekki_tavu_ARVO['passed'] or sekki_tavu_ARVO['jar_sha256'] != hajautusarvo_Tiedosto(aloite_juuri/'dist/jkoros-native-korean.jar'):
        raise SystemExit('nykyinen_kohde suomi 라이브러리의 직접 호출 바이트코드 tarkistaa 필요')
    sekki_tarkkuus = json.loads((vahvistus_polku/'resolution/report.json').read_text())
    sekki_muuttaa_kokoa = json.loads((vahvistus_polku/'resize/report.json').read_text())
    갱신검사 = json.loads((vahvistus_polku/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != ydin_hajautusarvo:
        raise SystemExit('nykyinen_kohde 커널의 부분 päivittää testit 필요')
    for polku_2, 기대값 in 갱신검사['source_sha256'].items():
        if hajautusarvo_Tiedosto(aloite_juuri/polku_2) != 기대값: raise SystemExit('부분 päivittää testit BACK_ARVO 바뀐 lähdetiedosto: '+polku_2)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('suomi 직접 가닥과 Suorita_2 aloituskohta testit 필요')
    예제검사 = json.loads((vahvistus_polku/'examples/report.json').read_text())
    if sorted(sekki_muuttaa_kokoa['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Koko 조절 testit 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('suomi Swing 창을 포함한 예제 13개 testit 필요')
    if sorted(sekki_tarkkuus['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 todellinen_data 화면 testit 필요')
    if 자바검사['korean_library_sha256'] != hajautusarvo_Tiedosto(aloite_juuri/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 testit BACK_ARVO 라이브러리가 바뀌었습니다.')
    for Nimi in ('한국어통신시험','한국어예외시험'):
        if not any(merkintä_ARVO_962f286b['name']==Nimi and merkintä_ARVO_962f286b.get('openjdk_output_equal') for merkintä_ARVO_962f286b in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 testit 필요: '+Nimi)
    poikkeus_luettelo = sorted(polku_2.stem for polku_2 in (aloite_juuri/'한국어자바/suomi/oma').glob('*poikkeus.java'))
    poikkeus_LOG = (vahvistus_polku/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Nimi in poikkeus_luettelo:
        if '\n'+Nimi+'\n' not in poikkeus_LOG: raise SystemExit('poikkeus generoida·잡기·설명 testit 필요: '+Nimi)
    määritys = json.loads((aloite_juuri/'dist/manifest.json').read_text())
    if määritys['image_sha256'] != hajautusarvo_Tiedosto(aloite_juuri/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('jakelu_ARVO KUVA_ARVO hajautusarvo_Tiedosto 불일치')
    with zipfile.ZipFile(str(aloite_juuri/'dist/jkoros-native-rpi4-boot.zip')) as nippu:
        if hashlib.sha256(nippu.read('kernel8.img')).hexdigest() != ydin_hajautusarvo:
            raise SystemExit('koneen_käynnistys ZIP ydin_ARVO 불일치')
        부팅설정 = nippu.read('config.txt')
        for Nimi, Koko in zip(('width', 'height'), määritys['framebuffer_resolution']):
            if 'framebuffer_'+Nimi+'='+str(Koko) not in 부팅설정.decode().splitlines():
                raise SystemExit('koneen_käynnistys ZIP 화면 Asetukset 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(aloite_juuri/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(aloite_juuri/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if hajautusarvo_Tiedosto(복사본) != ydin_hajautusarvo: raise SystemExit('SD KUVA_ARVO ydin_ARVO 불일치')
        kopioida_Asetukset = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(aloite_juuri/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(kopioida_Asetukset)])
        if kopioida_Asetukset.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Asetukset 불일치')
    LOG_TIETUE = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': ydin_hajautusarvo,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': poikkeus_luettelo, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(sekki_tarkkuus['resolutions']),
            'sd_framebuffer_resolution': määritys['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Nimi:hajautusarvo_Tiedosto(aloite_juuri/'dist'/Nimi) for Nimi in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (vahvistus_polku/'native-runtime-summary.json').write_text(json.dumps(LOG_TIETUE,ensure_ascii=False,indent=2)+'\n')
    print('PASS: nykyinen_kohde 커널의',len(기록들),'개 통합 testit LOG_TIETUE, suomi poikkeus',len(poikkeus_luettelo),'Luokka_Määritelmä, SD KUVA_ARVO·ZIP 일치')

if __name__ == '__main__': Suorita_2()
