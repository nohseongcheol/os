#!/usr/bin/env python3
"""bieżący_towar 커널과 rzeczywisty_dane testy·배포물이 일치할 때에만 통합 walidować 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

Project_korzeń = Path(__file__).resolve().parents[1]

def skrót_Plik(ścieżka_2):
    계산 = hashlib.sha256()
    with ścieżka_2.open('rb') as nazwa_pliku:
        for dane in iter(lambda: nazwa_pliku.read(1048576), b''): 계산.update(dane)
    return 계산.hexdigest()

def Uruchom_2():
    walidacja_ścieżka = Project_korzeń/'build/verification'
    jądro_skrót = skrót_Plik(Project_korzeń/'build/kernel8.img')
    기록들 = {}
    for Nazwa in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        ścieżka_względna = 'report.json' if Nazwa == 'boot' else Nazwa+'/report.json'
        dane = json.loads((walidacja_ścieżka/ścieżka_względna).read_text())
        if not dane.get('passed') or dane.get('kernel_sha256') != jądro_skrót:
            raise SystemExit('bieżący_towar 커널에 대한 성공 기록이 필요합니다: '+ścieżka_względna)
        기록들[Nazwa] = {'passed': True, 'report': ścieżka_względna}
    czek_nazwa = json.loads((walidacja_ścieżka/'naming/report.json').read_text())
    if not czek_nazwa['passed'] or not czek_nazwa['c_semantic_checked']: raise SystemExit('C 선언을 포함한 명명 검사 필요')
    for ścieżka_2, 기대값 in czek_nazwa['c_source_sha256'].items():
        if skrót_Plik(Project_korzeń/ścieżka_2) != 기대값: raise SystemExit('명명 검사 BACK_WARTOŚĆ 바뀐 C plik_źródłowy: '+ścieżka_2)
    자바검사 = json.loads((walidacja_ścieżka/'jvm/report.json').read_text())
    직접화면 = json.loads((walidacja_ścieżka/'swing/report.json').read_text())
    if not 직접화면.get('direct_korean_gui'): raise SystemExit('polski 직접 화면 Wykonaj_polecenie testy 필요')
    czek_bajt_WARTOŚĆ = json.loads((walidacja_ścieżka/'naming/direct-bytecode.json').read_text())
    if not czek_bajt_WARTOŚĆ['passed'] or czek_bajt_WARTOŚĆ['jar_sha256'] != skrót_Plik(Project_korzeń/'dist/jkoros-native-korean.jar'):
        raise SystemExit('bieżący_towar polski 라이브러리의 직접 호출 바이트코드 확인 필요')
    czek_rozdzielczość = json.loads((walidacja_ścieżka/'resolution/report.json').read_text())
    czek_zmienić_rozmiar = json.loads((walidacja_ścieżka/'resize/report.json').read_text())
    갱신검사 = json.loads((walidacja_ścieżka/'redraw/report.json').read_text())
    if not 갱신검사['passed'] or 갱신검사['kernel_sha256'] != jądro_skrót:
        raise SystemExit('bieżący_towar 커널의 부분 odświeżyć testy 필요')
    for ścieżka_2, 기대값 in 갱신검사['source_sha256'].items():
        if skrót_Plik(Project_korzeń/ścieżka_2) != 기대값: raise SystemExit('부분 odświeżyć testy BACK_WARTOŚĆ 바뀐 plik_źródłowy: '+ścieżka_2)
    if not 자바검사.get('direct_korean_thread_and_entry'):
        raise SystemExit('polski 직접 가닥과 Uruchom_2 punkt_wejścia testy 필요')
    예제검사 = json.loads((walidacja_ścieżka/'examples/report.json').read_text())
    if sorted(czek_zmienić_rozmiar['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 모서리 Rozmiar 조절 testy 필요')
    if not 예제검사.get('swing_example_korean_input_button_label_and_close') or 예제검사['examples_executed'] != 13:
        raise SystemExit('polski Swing 창을 포함한 예제 13개 testy 필요')
    if sorted(czek_rozdzielczość['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 rzeczywisty_dane 화면 testy 필요')
    if 자바검사['korean_library_sha256'] != skrót_Plik(Project_korzeń/'dist/jkoros-native-korean.jar'):
        raise SystemExit('자바 testy BACK_WARTOŚĆ 라이브러리가 바뀌었습니다.')
    for Nazwa in ('한국어통신시험','한국어예외시험'):
        if not any(wpis_WARTOŚĆ['name']==Nazwa and wpis_WARTOŚĆ.get('openjdk_output_equal') for wpis_WARTOŚĆ in 자바검사['tests']):
            raise SystemExit('OpenJDK 대조 testy 필요: '+Nazwa)
    wyjątek_Lista = sorted(ścieżka_2.stem for ścieżka_2 in (Project_korzeń/'한국어자바/polski/własny').glob('*wyjątek.java'))
    wyjątek_LOG = (walidacja_ścieżka/'jvm/한국어예외시험.log').read_text().replace('\r\n','\n')
    for Nazwa in wyjątek_Lista:
        if '\n'+Nazwa+'\n' not in wyjątek_LOG: raise SystemExit('wyjątek generować·잡기·설명 testy 필요: '+Nazwa)
    명세 = json.loads((Project_korzeń/'dist/manifest.json').read_text())
    if 명세['image_sha256'] != skrót_Plik(Project_korzeń/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('dystrybucja_WARTOŚĆ OBRAZ_WARTOŚĆ skrót_Plik 불일치')
    with zipfile.ZipFile(str(Project_korzeń/'dist/jkoros-native-rpi4-boot.zip')) as pakiet:
        if hashlib.sha256(pakiet.read('kernel8.img')).hexdigest() != jądro_skrót:
            raise SystemExit('rozruch_maszyny ZIP jądro_WARTOŚĆ 불일치')
        부팅설정 = pakiet.read('config.txt')
        for Nazwa, Rozmiar in zip(('width', 'height'), 명세['framebuffer_resolution']):
            if 'framebuffer_'+Nazwa+'='+str(Rozmiar) not in 부팅설정.decode().splitlines():
                raise SystemExit('rozruch_maszyny ZIP 화면 Ustawienia 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(Project_korzeń/'build')) as 임시:
        복사본 = Path(임시)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(Project_korzeń/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(복사본)])
        if skrót_Plik(복사본) != jądro_skrót: raise SystemExit('SD OBRAZ_WARTOŚĆ jądro_WARTOŚĆ 불일치')
        kopiować_Ustawienia = Path(임시)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(Project_korzeń/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(kopiować_Ustawienia)])
        if kopiować_Ustawienia.read_bytes() != 부팅설정: raise SystemExit('SD 영상과 ZIP 화면 Ustawienia 불일치')
    LOG_zapis = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': jądro_skrót,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': 기록들, 'naming_report': 'naming/report.json',
            'korean_exception_classes': wyjątek_Lista, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': 예제검사['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(czek_rozdzielczość['resolutions']),
            'sd_framebuffer_resolution': 명세['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Nazwa:skrót_Plik(Project_korzeń/'dist'/Nazwa) for Nazwa in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (walidacja_ścieżka/'native-runtime-summary.json').write_text(json.dumps(LOG_zapis,ensure_ascii=False,indent=2)+'\n')
    print('PASS: bieżący_towar 커널의',len(기록들),'개 통합 testy LOG_zapis, polski wyjątek',len(wyjątek_Lista),'Klasa_Definicja, SD OBRAZ_WARTOŚĆ·ZIP 일치')

if __name__ == '__main__': Uruchom_2()
