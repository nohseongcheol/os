#!/usr/bin/env python3
"""PyPI physischHardware 배포와 부정 Eingabewert·RAM 되돌림을 eigen 커널에서 검사한다."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import selectors
import shutil
import socket
import subprocess
import time
import zipfile
from bündelWeitergeben import bündelAblage, entpacken
from befehlAusführen import projektWurzel


def radPrüfung(Name, dateiEinträge, vertragWert='Root-Is-Purelib: true\n', abhängigkeiten=''):
    Daten = io.BytesIO()
    with zipfile.ZipFile(Daten, 'w', zipfile.ZIP_DEFLATED) as Paket:
        Paket.writestr(Name + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + vertragWert)
        Paket.writestr(Name + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + Name + '\nVersion: 1.0\n' + abhängigkeiten)
        for pfad, inhaltswertWert in dateiEinträge.items():
            Paket.writestr(pfad, inhaltswertWert)
    return Daten.getvalue()


def wirtssystemPrüfen():
    istNormal = radPrüfung('jkoros-fixture', {'mod.py': 'Wert=42\n'})
    assert entpacken('jkoros_fixture-1.0-py3-none-any.whl', istNormal, 'jkoros-fixture', '1.0') == {'mod.py': 'Wert=42\n'.encode()}
    for Daten in (
            radPrüfung('jkoros-fixture', {'../escape.py': ''}),
            radPrüfung('jkoros-fixture', {'/abs.py': ''}),
            radPrüfung('jkoros-fixture', {'big.py': 'x' * 16385}),
            radPrüfung('jkoros-fixture', {'mod.so': ''}),
            radPrüfung('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            radPrüfung('jkoros-fixture', {'mod.py': ''}, abhängigkeiten='Requires-Dist: requests\n')):
        try:
            entpacken('jkoros_fixture-1.0-py3-none-any.whl', Daten, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel pfad·größe·C erweiterungWert·abhängigkeiten wertZurückweisen')


def leerwertPortNummer():
    with socket.socket() as netzbuchseWert:
        netzbuchseWert.bind(('127.0.0.1', 0))
        return netzbuchseWert.getsockname()[1]


def ausführenVorgang():
    Strukturanalysierer = argparse.ArgumentParser(description=__doc__)
    Strukturanalysierer.add_argument('--host-only', action='store_true')
    argumente = Strukturanalysierer.parse_args()
    wirtssystemPrüfen()
    if argumente.host_only:
        return
    ergebnisPfad = projektWurzel/'build/verification/pip'
    ergebnisPfad.mkdir(parents=True, exist_ok=True)
    speichergerätPfad = ergebnisPfad/'cache'
    speichergerätPfad.mkdir(exist_ok=True)
    # tatsächlichDaten PyPI verteilungWert Datei. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    bündelAblage(projektWurzel/'build/pip-cache').vorbereiten('micropython-bisect==3.3.3')
    for endstückWert in ('.archive', '.json'):
        shutil.copyfile(str(projektWurzel/'build/pip-cache'/('micropython-bisect==3.3.3'+endstückWert)), str(speichergerätPfad/('micropython-bisect==3.3.3'+endstückWert)))
    hardwareProtokolldatei = json.loads((speichergerätPfad/'micropython-bisect==3.3.3.json').read_text())
    assert hardwareProtokolldatei['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for Name, dateiEinträge in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .berechnung import werteHinzufügen\n', '검증꾸러미/berechnung.py': 'def werteHinzufügen(ersterOperand,zweiterOperand):\n return ersterOperand+zweiterOperand\n'}),
            ('jkoros-space', {'space%d.py' % Zahl: 'Wert=1\n' for Zahl in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        Daten = radPrüfung(Name, dateiEinträge)
        (speichergerätPfad/(Name+'==1.0.archive')).write_bytes(Daten)
        (speichergerätPfad/(Name+'==1.0.json')).write_text(json.dumps({'name': Name, 'version': '1.0',
            'filename': Name.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(Daten).hexdigest()}))
    validieren = {'passed': False, 'kernel_sha256': hashlib.sha256((projektWurzel/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': hardwareProtokolldatei, 'checks': []}
    portNummer = leerwertPortNummer()
    prozess = subprocess.Popen(['python3', str(projektWurzel/'Werkzeuge/befehlAusführen.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(portNummer), '--pip-cache', str(speichergerätPfad), '--ftp-port', str(leerwertPortNummer())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    Auswähler = selectors.DefaultSelector()
    Auswähler.register(prozess.stdout, selectors.EVENT_READ)
    ablaufprotokoll = bytearray()
    def abwarten(wertAnzeigen=b'jkoros-native> '):
        inhaltswertWert = bytearray()
        endung = time.monotonic()+120
        while wertAnzeigen not in inhaltswertWert:
            if time.monotonic() > endung or prozess.poll() is not None:
                raise AssertionError('게스트 antwort fehlendMethode: '+inhaltswertWert.decode('utf-8','replace'))
            for eintragWert, _ in Auswähler.select(.1):
                fragmentWert = eintragWert.fileobj.read(4096)
                inhaltswertWert.extend(fragmentWert)
                ablaufprotokoll.extend(fragmentWert)
        return inhaltswertWert.decode('utf-8', 'replace').replace('\r\n','\n')
    def befehlshülle(befehl, wertAnzeigen=b'jkoros-native> '):
        prozess.stdin.write(befehl.encode()+b'\n')
        prozess.stdin.flush()
        return abwarten(wertAnzeigen)
    def befehlAusführen(befehl, erwartetWerte, statuswertWert=0):
        inhaltswertWert = befehlshülle(befehl)
        assert erwartetWerte in inhaltswertWert and '\nexit '+str(statuswertWert)+'\n' in inhaltswertWert, inhaltswertWert
        validieren['checks'].append(befehl)
        return inhaltswertWert
    def hochladenDateien(Name, Daten):
        befehlshülle('load '+Name, b'hex> ')
        for positionIndex in range(0, len(Daten), 64):
            befehlshülle(Daten[positionIndex:positionIndex+64].hex(), b'hex> ')
        assert 'LOADED' in befehlshülle('.')
    try:
        abwarten()
        befehlAusführen('pip --help', 'MicroPython quelltextBaum 설치기')
        hochladenDateien('오류시험.py', (projektWurzel/'Prüfungen/Python/KoreanischFehlerPrüfung.py').read_bytes())
        befehlAusführen('python 오류시험.py', 'Deutsch Datei ausnahme überprüfen')
        befehlAusführen('pip install micropython-bisect==3.3.3 --port '+str(portNummer), 'wertEinrichten istFertig: micropython-bisect 3.3.3')
        befehlAusführen('python -c \'from bisect import insort as 순서대로넣기; Wert=[1,5]; 순서대로넣기(Wert,3); print(Wert)\'', '[1, 3, 5]')
        befehlAusführen('python -m pip list', 'micropython-bisect 3.3.3')
        befehlAusführen('pip install micropython-bisect==3.3.3 --port '+str(portNummer), '이미 설치됨:')
        befehlAusführen('pip install jkoros-fixture==1.0 --port '+str(portNummer), 'wertEinrichten istFertig: jkoros-fixture')
        befehlAusführen('python -c \'from 검증꾸러미 import werteHinzufügen; print(werteHinzufügen(20,22))\'', '\n42\n')
        befehlAusführen('pip install jkoros-syntax==1.0 --port '+str(portNummer), 'Paket fehler:', 1)
        befehlAusführen('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 fehler 보존")\'', '구문 fehler 보존')
        hochladenDateien('공간시험.py', (projektWurzel/'Prüfungen/Python/BündelNamensraumPrüfung.py').read_bytes())
        befehlAusführen('python 공간시험.py '+str(portNummer), 'Paket adresseGebiet 부족 zurückkehrenBrücke überprüfen')
        befehlAusführen('pip uninstall jkoros-fixture', 'eintragEntfernen istFertig: jkoros-fixture')
        befehlAusführen('pip uninstall micropython-bisect', 'eintragEntfernen istFertig: micropython-bisect')
        befehlAusführen('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("eintragEntfernen überprüfen")\'', 'eintragEntfernen überprüfen')
        validieren['passed'] = True
        print('PASS: PyPI physischHardware wertEinrichten·import·befehlAusführen, Deutsch ausnahme, 패키지 verzeichnisWert, fehlschlagWert zurückkehrenBrücke, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 verlassenProzessProgramm 키로 QEMU를 끝내면 실행기의 wertWeitergeben 문맥도 정리된다.
            prozess.stdin.write(b'\x01x')
            prozess.stdin.flush()
            prozess.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            prozess.terminate()
            try:
                prozess.wait(timeout=8)
            except subprocess.TimeoutExpired:
                prozess.kill()
                prozess.wait()
        if prozess.poll() is None:
            prozess.kill()
            prozess.wait()
        Auswähler.close()
        prozess.stdin.close()
        prozess.stdout.close()
        (ergebnisPfad/'serial.log').write_bytes(ablaufprotokoll)
        (ergebnisPfad/'report.json').write_text(json.dumps(validieren, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    ausführenVorgang()
