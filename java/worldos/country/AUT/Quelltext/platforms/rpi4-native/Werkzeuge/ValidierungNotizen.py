#!/usr/bin/env python3
"""aktuellElementeintrag 커널과 tatsächlichDaten Prüfungen·배포물이 일치할 때에만 통합 validieren 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

projektWurzel = Path(__file__).resolve().parents[1]

def prüfsummeDatei(pfad):
    berechnung = hashlib.sha256()
    with pfad.open('rb') as Datei:
        for Daten in iter(lambda: Datei.read(1048576), b''): berechnung.update(Daten)
    return berechnung.hexdigest()

def ausführenVorgang():
    validierungPfad = projektWurzel/'build/verification'
    betriebskernPrüfsumme = prüfsummeDatei(projektWurzel/'build/kernel8.img')
    protokolldateiAufzeichnungen = {}
    for Name in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        relativPfad = 'report.json' if Name == 'boot' else Name+'/report.json'
        Daten = json.loads((validierungPfad/relativPfad).read_text())
        if not Daten.get('passed') or Daten.get('kernel_sha256') != betriebskernPrüfsumme:
            raise SystemExit('aktuellElementeintrag 커널에 대한 erfolgWert 기록이 필요합니다: '+relativPfad)
        protokolldateiAufzeichnungen[Name] = {'passed': True, 'report': relativPfad}
    namePrüfen = json.loads((validierungPfad/'naming/report.json').read_text())
    if not namePrüfen['passed'] or not namePrüfen['c_semantic_checked']: raise SystemExit('C 선언을 포함한 benennung Prüfpunkte benötigtWert')
    for pfad, erwartetWert in namePrüfen['c_source_sha256'].items():
        if prüfsummeDatei(projektWurzel/pfad) != erwartetWert: raise SystemExit('benennung Prüfpunkte rückseiteWert 바뀐 C Quelltext: '+pfad)
    javaPrüfen = json.loads((validierungPfad/'jvm/report.json').read_text())
    DirektBildschirm = json.loads((validierungPfad/'swing/report.json').read_text())
    if not DirektBildschirm.get('direct_korean_gui'): raise SystemExit('Deutsch 직접 Bildschirm befehlAusführen Prüfungen benötigtWert')
    byteWertPrüfen = json.loads((validierungPfad/'naming/direct-bytecode.json').read_text())
    if not byteWertPrüfen['passed'] or byteWertPrüfen['jar_sha256'] != prüfsummeDatei(projektWurzel/'dist/jkoros-native-korean.jar'):
        raise SystemExit('aktuellElementeintrag Deutsch 라이브러리의 직접 aufrufen bytecode überprüfen benötigtWert')
    auflösungPrüfen = json.loads((validierungPfad/'resolution/report.json').read_text())
    größePrüfen = json.loads((validierungPfad/'resize/report.json').read_text())
    fürAktualisierungenPrüfen = json.loads((validierungPfad/'redraw/report.json').read_text())
    if not fürAktualisierungenPrüfen['passed'] or fürAktualisierungenPrüfen['kernel_sha256'] != betriebskernPrüfsumme:
        raise SystemExit('aktuellElementeintrag 커널의 unterteilWert auffrischen Prüfungen benötigtWert')
    for pfad, erwartetWert in fürAktualisierungenPrüfen['source_sha256'].items():
        if prüfsummeDatei(projektWurzel/pfad) != erwartetWert: raise SystemExit('unterteilWert auffrischen Prüfungen rückseiteWert 바뀐 Quelltext: '+pfad)
    if not javaPrüfen.get('direct_korean_thread_and_entry'):
        raise SystemExit('Deutsch 직접 가닥과 ausführenVorgang eintragPunkt Prüfungen benötigtWert')
    beispielPrüfen = json.loads((validierungPfad/'examples/report.json').read_text())
    if sorted(größePrüfen['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 eckeWert größe 조절 Prüfungen benötigtWert')
    if not beispielPrüfen.get('swing_example_korean_input_button_label_and_close') or beispielPrüfen['examples_executed'] != 13:
        raise SystemExit('Deutsch Swing 창을 포함한 Beispiele 13개 Prüfungen benötigtWert')
    if sorted(auflösungPrüfen['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 tatsächlichDaten Bildschirm Prüfungen benötigtWert')
    if javaPrüfen['korean_library_sha256'] != prüfsummeDatei(projektWurzel/'dist/jkoros-native-korean.jar'):
        raise SystemExit('Java Prüfungen rückseiteWert 라이브러리가 바뀌었습니다.')
    for Name in ('koreanischNetzbetriebPrüfung','koreanischAusnahmenPrüfung'):
        if not any(eintragWert['name']==Name and eintragWert.get('openjdk_output_equal') for eintragWert in javaPrüfen['tests']):
            raise SystemExit('OpenJDK 대조 Prüfungen benötigtWert: '+Name)
    ausnahmeListe = sorted(pfad.stem for pfad in (projektWurzel/'DeutschJava/Deutsch/eigen').glob('*ausnahme.java'))
    ausnahmeProtokolldatei = (validierungPfad/'jvm/koreanischAusnahmenPrüfung.log').read_text().replace('\r\n','\n')
    for Name in ausnahmeListe:
        if '\n'+Name+'\n' not in ausnahmeProtokolldatei: raise SystemExit('ausnahme generieren·잡기·beschreibung Prüfungen benötigtWert: '+Name)
    vorgabe = json.loads((projektWurzel/'dist/manifest.json').read_text())
    if vorgabe['image_sha256'] != prüfsummeDatei(projektWurzel/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('verteilungWert abbildWert prüfsummeDatei 불일치')
    with zipfile.ZipFile(str(projektWurzel/'dist/jkoros-native-rpi4-boot.zip')) as Paket:
        if hashlib.sha256(Paket.read('kernel8.img')).hexdigest() != betriebskernPrüfsumme:
            raise SystemExit('Startvorgang ZIP betriebskernWert 불일치')
        startvorgangEinstellungen = Paket.read('config.txt')
        for Name, größe in zip(('width', 'height'), vorgabe['framebuffer_resolution']):
            if 'framebuffer_'+Name+'='+str(größe) not in startvorgangEinstellungen.decode().splitlines():
                raise SystemExit('Startvorgang ZIP Bildschirm einstellungen 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(projektWurzel/'build')) as vorläufigWert:
        kopiertWert = Path(vorläufigWert)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(projektWurzel/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(kopiertWert)])
        if prüfsummeDatei(kopiertWert) != betriebskernPrüfsumme: raise SystemExit('SD abbildWert betriebskernWert 불일치')
        einstellungenKopieren = Path(vorläufigWert)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(projektWurzel/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(einstellungenKopieren)])
        if einstellungenKopieren.read_bytes() != startvorgangEinstellungen: raise SystemExit('SD 영상과 ZIP Bildschirm einstellungen 불일치')
    protokolldateiAufzeichnung = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': betriebskernPrüfsumme,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': protokolldateiAufzeichnungen, 'naming_report': 'naming/report.json',
            'korean_exception_classes': ausnahmeListe, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': beispielPrüfen['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(auflösungPrüfen['resolutions']),
            'sd_framebuffer_resolution': vorgabe['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {Name:prüfsummeDatei(projektWurzel/'dist'/Name) for Name in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (validierungPfad/'native-runtime-summary.json').write_text(json.dumps(protokolldateiAufzeichnung,ensure_ascii=False,indent=2)+'\n')
    print('PASS: aktuellElementeintrag 커널의',len(protokolldateiAufzeichnungen),'개 통합 Prüfungen protokolldateiAufzeichnung, Deutsch ausnahme',len(ausnahmeListe),'klasseDefinition, SD abbildWert·ZIP istGleich')

if __name__ == '__main__': ausführenVorgang()
