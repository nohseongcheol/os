#!/usr/bin/env python3
"""OpenJDK와 eigen ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from befehlAusführen import projektWurzel


def ausführenVorgang():
    ausgabe = projektWurzel / 'build/verification/jvm'
    klassePfad = ausgabe / 'classes'; klassePfad.mkdir(parents=True, exist_ok=True)
    javaBündel = projektWurzel / 'dist/jkoros-native-korean.jar'
    Quelltextliste = sorted((projektWurzel / 'Prüfungen/Java').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(javaBündel), '-d', str(klassePfad)] + [str(zeichenketteDaten) for zeichenketteDaten in Quelltextliste])
    listePrüfung = [('objektePrüfung', ['hintergrundWert', 'verzweigungWert', 'kannBerechnen']), ('ausnahmenPrüfung', []), ('SammlungPrüfung', []),
             ('ausführungsfädenPrüfung', ['zählerWert', 'AufgabeAktion', 'ausführungsfadenWert']), ('hangulPrüfung', []), ('netzbetriebPrüfung', []), ('koreanischNetzbetriebPrüfung', []), ('koreanischAusnahmenPrüfung', []), ('hangulQuelltext', []), ('grenzstellenPrüfung', []), ('validieren.bündelPrüfung', []), ('EintragVerträglichkeitPrüfung', [])]
    validierungBericht = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((projektWurzel / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(javaBündel.read_bytes()).hexdigest(), 'tests': []}
    try:
        for Name, einschlüsse in listePrüfung:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as vorläufigPfad:
                erwartet = subprocess.check_output(['java', '-Xverify:all', '-cp', str(klassePfad) + ':' + str(javaBündel), Name], cwd=vorläufigPfad, timeout=15).decode('utf-8')
            befehlArgumente = ['python3', str(projektWurzel / 'Werkzeuge/dateiAusführen.py'), str(klassePfad / (Name.replace('.', '/') + '.class'))]
            if '.' in Name: befehlArgumente += ['--class-name', Name]
            for einbinden in einschlüsse: befehlArgumente += ['--include', str(klassePfad / (einbinden + '.class'))]
            if Name == 'hangulQuelltext': befehlArgumente[2] = str(projektWurzel / 'Prüfungen/Java/hangulQuelltext.java')
            abgeschlossenGesamtmenge = subprocess.run(befehlArgumente, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            tatsächlichErgebnis = abgeschlossenGesamtmenge.stdout.decode('utf-8').replace('\r\n', '\n')
            (ausgabe / (Name + '.log')).write_text(tatsächlichErgebnis, encoding='utf-8')
            istGleich = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", tatsächlichErgebnis, re.S)
            assert abgeschlossenGesamtmenge.returncode == 0 and istGleich, (Name, tatsächlichErgebnis)
            ergebnis = next(zeichenketteDaten for zeichenketteDaten in istGleich.groups() if zeichenketteDaten is not None) + '\n'
            assert ergebnis == erwartet, (Name, erwartet, ergebnis)
            validierungBericht['tests'].append({'name': Name, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', Name, flush=True)
        # eigen JVM에 직접 연결한 Deutsch ausführungsfadenWert/진입점은 OpenJDK용 래퍼가 아니다.
        abgeschlossenGesamtmenge = subprocess.run(['python3', str(projektWurzel/'Werkzeuge/dateiAusführen.py'), str(klassePfad/'koreanischAusführungsfädenPrüfung.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        ergebnis = abgeschlossenGesamtmenge.stdout.decode('utf-8').replace('\r\n', '\n')
        (ausgabe/'koreanischAusführungsfädenPrüfung.log').write_text(ergebnis)
        assert abgeschlossenGesamtmenge.returncode == 0 and 'Deutsch 직접 ausführungsfadenWert durchgangWert\n' in ergebnis and '\nexit 0\n' in ergebnis, ergebnis
        validierungBericht['direct_korean_thread_and_entry'] = True
        print('PASS: Deutsch 직접 ausführungsfadenWert·aufgabeAusführen·ausführenVorgang eintragPunkt', flush=True)
        gültig = (klassePfad / 'objektePrüfung.class').read_bytes()
        fallPrüfung = [('판거부', gültig[:6] + b'\x00\x35' + gültig[8:], 'supported class versions'),
                 ('잘린클래스', gültig[:24], 'truncated class file')]
        validierungBericht['rejection_tests'] = []
        for Name, nutzdatenDaten, mitteilungText in fallPrüfung:
            datenPrüfung = ausgabe / (Name + '.class'); datenPrüfung.write_bytes(nutzdatenDaten)
            abgeschlossenGesamtmenge = subprocess.run(['python3', str(projektWurzel / 'Werkzeuge/dateiAusführen.py'), str(datenPrüfung)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            Text = abgeschlossenGesamtmenge.stdout.decode('utf-8').replace('\r\n', '\n')
            (ausgabe / (Name + '.log')).write_text(Text, encoding='utf-8')
            assert abgeschlossenGesamtmenge.returncode == 1 and mitteilungText in Text and 'exit 1\n' in Text, (Name, Text)
            validierungBericht['rejection_tests'].append({'name': Name, 'passed': True})
            print('PASS (rejected):', Name, flush=True)
        validierungBericht['passed'] = True
    finally:
        (ausgabe / 'report.json').write_text(json.dumps(validierungBericht, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ausführenVorgang()
