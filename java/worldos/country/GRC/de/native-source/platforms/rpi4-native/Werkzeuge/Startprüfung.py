#!/usr/bin/env python3
"""tatsächlichDaten raspi4b Startvorgang, UART Eingabewert, 재실행, framebuffer 픽셀을 검사한다."""
import hashlib
import json
from pathlib import Path
import selectors
import re
import socket
import subprocess
import tempfile
import time
from befehlAusführen import projektWurzel, befehl


def ausführenVorgang():
    ausgabe = projektWurzel / 'build/verification'
    ausgabe.mkdir(parents=True, exist_ok=True)
    ablaufprotokoll = bytearray()
    validierungBericht = {'passed': False, 'machine': 'raspi4b', 'physical_board_tested': False,
              'firmware_boot_tested': False, 'linux_loaded': False}
    with tempfile.TemporaryDirectory(prefix='jkoros-native-') as arbeitendPfad:
        qMPPfad = Path(arbeitendPfad) / 'qmp.sock'
        befehlArgumente = befehl() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                           '-qmp', 'unix:{},server=on,wait=off'.format(qMPPfad),
                           '-vnc', 'unix:{}'.format(Path(arbeitendPfad) / 'vnc.sock')]
        validierungBericht['command'] = befehlArgumente
        prozess = subprocess.Popen(befehlArgumente, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        auswähler = selectors.DefaultSelector()
        auswähler.register(prozess.stdout, selectors.EVENT_READ)
        def bisEmpfangen(markierung, versatzwertWert=0, ausführungZeitüberschreitung=45):
            fristZeit = time.monotonic() + ausführungZeitüberschreitung
            while markierung not in ablaufprotokoll[versatzwertWert:]:
                if time.monotonic() > fristZeit:
                    raise AssertionError('UART timeout: ' + repr(markierung))
                for gedrücktWert, _ in auswähler.select(0.2):
                    datenBlock = gedrücktWert.fileobj.read(4096)
                    if datenBlock:
                        ablaufprotokoll.extend(datenBlock)
                if re.search(rb'(?:^|\n)(?:PANIC:|FAIL |EXCEPTION )', ablaufprotokoll):
                    raise AssertionError('kernel failure')
                if prozess.poll() is not None:
                    raise AssertionError('QEMU exited: {}'.format(prozess.returncode))
        try:
            bisEmpfangen(b'jkoros-native> ')
            markierungen = [b'JAVA AOT PASS', b'C++ POSIX-KOR PASS', b'TASK PASS', b'FRAMEBUFFER PASS',
                       b'ELF64 REJECT PASS', b'EL0 C++ PASS', b'USER PROTECTION PASS', b'EL0 UDP LOOPBACK PASS',
                       '안녕하세요 · 日本語 · العربية · 😀'.encode('utf-8'), b'NATIVE READY']
            for markierung in markierungen:
                assert markierung in ablaufprotokoll, markierung
            # GTK 없는 aktuellElementeintrag 호스트에서도 VNC로 tatsächlichDaten GUI를 볼 Zahl 있어야 한다.
            with socket.socket(socket.AF_UNIX) as bildschirmAnfragestelle:
                bildschirmAnfragestelle.settimeout(5); bildschirmAnfragestelle.connect(str(Path(arbeitendPfad) / 'vnc.sock'))
                def exaktWert(größe):
                    ergebnis = b''
                    while len(ergebnis) < größe:
                        fragmentWert = bildschirmAnfragestelle.recv(größe - len(ergebnis))
                        if not fragmentWert: raise AssertionError('VNC disconnected')
                        ergebnis += fragmentWert
                    return ergebnis
                assert exaktWert(12) == b'RFB 003.008\n'
                bildschirmAnfragestelle.sendall(b'RFB 003.008\n')
                assert 1 in exaktWert(exaktWert(1)[0]); bildschirmAnfragestelle.sendall(b'\x01')
                assert exaktWert(4) == b'\x00\x00\x00\x00'; bildschirmAnfragestelle.sendall(b'\x01')
                dienstanbieterWert = exaktWert(24)
                assert int.from_bytes(dienstanbieterWert[:2], 'big') == 640 and int.from_bytes(dienstanbieterWert[2:4], 'big') == 480
                exaktWert(int.from_bytes(dienstanbieterWert[20:24], 'big'))
            # 여러 번 호출해 descriptor 누수, 종료한 task의 재생성도 검증한다.
            for befehlByte, markierung in [(b'c', b'C++ POSIX-KOR PASS')] * 20 + [(b't', b'TASK PASS')] * 3 + [
                    (b'e', b'ELF DEMO PASS')] * 20 + [(b'n', b'EL0 UDP LOOPBACK PASS')] * 12 + [
                    (b'u', b'USER PROTECTION PASS'),
                    (b'f', 'Prüfungen.txt'.encode('utf-8')), (b'i', b'Java subset + MicroPython; no full OpenJDK/CPython/Swing.')]:
                versatzwertWert = len(ablaufprotokoll)
                prozess.stdin.write(befehlByte + b'\n')
                prozess.stdin.flush()
                bisEmpfangen(b'jkoros-native> ', versatzwertWert)
                assert markierung in ablaufprotokoll[versatzwertWert:], markierung
            def befehlshülle(zeile, erwartet):
                versatzwertWert = len(ablaufprotokoll)
                prozess.stdin.write(zeile.encode('utf-8') + b'\n'); prozess.stdin.flush()
                bisEmpfangen(b'jkoros-native> ', versatzwertWert)
                rückmeldung = bytes(ablaufprotokoll[versatzwertWert:])
                for Text in erwartet:
                    assert Text.encode('utf-8') in rückmeldung, (zeile, Text, rückmeldung)
                return rückmeldung
            def eintreten(zeile, eingabeaufforderung):
                versatzwertWert = len(ablaufprotokoll)
                prozess.stdin.write(zeile.encode('utf-8') + b'\n'); prozess.stdin.flush()
                bisEmpfangen(eingabeaufforderung, versatzwertWert)
                return bytes(ablaufprotokoll[versatzwertWert:])
            def bearbeitenWert(Name, inhaltswertWert, abbrechenVorgangVorgang=False):
                eintreten('edit ' + Name, b'edit> ')
                for zeile in inhaltswertWert.splitlines(): eintreten(zeile, b'edit> ')
                if abbrechenVorgangVorgang:
                    versatzwertWert = len(ablaufprotokoll)
                    prozess.stdin.write(b'\x03'); prozess.stdin.flush()
                    bisEmpfangen(b'jkoros-native> ', versatzwertWert)
                    assert b'EDIT CANCELLED' in ablaufprotokoll[versatzwertWert:]
                else:
                    assert b'SAVED' in eintreten('.', b'jkoros-native> ')
            def hochladenDateien(Name, Daten):
                assert len(Daten) <= 16384
                eintreten('load ' + Name, b'hex> ')
                for ordnungszahlIndex in range(0, len(Daten), 64): eintreten(Daten[ordnungszahlIndex:ordnungszahlIndex+64].hex(), b'hex> ')
                assert b'LOADED' in eintreten('.', b'jkoros-native> ')
            def herunterladen(Name):
                rückmeldung = befehlshülle('hex ' + Name, ['HEX BEGIN', 'HEX END'])
                istGleich = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', rückmeldung, re.S)
                Daten = bytes.fromhex(''.join(istGleich.group(2).decode('ascii').split()))
                assert len(Daten) == int(istGleich.group(1)); return Daten
            befehlshülle('javac -version', ['subset compiler; not OpenJDK', 'exit 0'])
            befehlshülle('java -version', ['not OpenJDK', 'exit 0'])
            befehlshülle('javac Hello.java', ['Compiled: Hello.class', 'exit 0'])
            befehlshülle('java Hello "한글 argumente 😀"', ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 argumente 😀', 'exit 0'])
            befehlshülle('python --version', ['MicroPython 1.24.1', 'exit 0'])
            befehlshülle('python hello.py', ['squares: [0, 1, 4, 9, 16, 25]', '한글 Datei', 'exit 0'])
            befehlshülle('cat python.txt', ['한글 Datei'])
            # The guest-produced .class must also pass the independent OpenJDK verifier.
            javaKlasse = ausgabe / 'Hello.class'; javaKlasse.write_bytes(herunterladen('Hello.class'))
            erwartet = subprocess.check_output(['java', '-Xverify:all', '-cp', str(ausgabe), 'Hello', '한글 argumente 😀']).decode('utf-8')
            assert erwartet.splitlines() == ['안녕하세요 · 日本語 · العربية · 😀', 'square=49', '한글 argumente 😀'], erwartet
            bearbeitenWert('Gruß.java', 'public class Gruß { public static void main(String[] args) { int Wert = 7; System.out.println("한글=" + Wert); } }')
            befehlshülle('javac Gruß.java', ['Compiled: Gruß.class', 'exit 0'])
            befehlshülle('java Gruß', ['한글=7', 'exit 0'])
            (ausgabe / 'Gruß.class').write_bytes(herunterladen('Gruß.class'))
            assert subprocess.check_output(['java', '-Xverify:all', '-cp', str(ausgabe), 'Gruß']).decode().strip() == '한글=7'
            bearbeitenWert('Hello.java', 'broken', abbrechenVorgangVorgang=True)
            befehlshülle('javac Hello.java', ['Compiled:', 'exit 0'])
            bearbeitenWert('Broken.java', 'public class Broken { public static void main(String[] a) { int x = ; } }')
            befehlshülle('javac Broken.java', ['javac error:', 'exit 1'])
            hochladenDateien('Broken.java', b'public class Broken { /*\xc0\xaf*/ }')
            befehlshülle('javac Broken.java', ['invalid UTF-8', 'exit 1'])
            befehlshülle('rm Broken.java', [])
            importiert = ausgabe / 'Imported.java'
            importiert.write_text('public class Imported { public static void main(String[] a) { int[] v = new int[3]; v[1] = 81; System.out.println("HOST CLASS 한글 😀"); System.out.println(v[1]); } }', encoding='utf-8')
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', str(importiert)])
            hochladenDateien('Imported.class', (ausgabe / 'Imported.class').read_bytes())
            befehlshülle('java Imported', ['HOST CLASS 한글 😀', '81', 'exit 0'])
            befehlshülle('rm Imported.class', [])
            bearbeitenWert('Loop.java', 'public class Loop { public static void main(String[] a) { while (true) {} } }')
            befehlshülle('javac Loop.java', ['Compiled:', 'exit 0'])
            rückmeldung = befehlshülle('java Loop', ['exit '])
            assert b'instruction limit' in rückmeldung or b'exit -1004' in rückmeldung
            befehlshülle('rm Loop.java', []); befehlshülle('rm Loop.class', [])
            # CPython-independent Python runtime: Unicode, big integers, closures/classes,
            # GC roots, file imports, exceptions and UDP queues are exercised in the guest.
            pythonPrüfpunkte = """import gc, jkoros
assert len('한글😀') == 3
assert 2**100 == 1267650600228229401496703205376
class Counter:
    def __init__(self, n): self.n = n
    def value(self): return self.n + 1
keep = Counter(41)
for i in range(300):
    garbage = [str(j) for j in range(80)]
    gc.collect()
assert keep.value() == 42
try:
    1 // 0
except ZeroDivisionError:
    print('PY EXCEPTION OK')
a = jkoros.udp_open(9401)
b = jkoros.udp_open(9402)
assert jkoros.udp_send(a, 9402, b'udp-python') == 10
assert jkoros.udp_recv(b) == (b'udp-python', 9401)
try:
    jkoros.udp_recv(b)
except OSError as e:
    assert e.args[0] == 11
jkoros.udp_close(a)
jkoros.udp_close(b)
print('PY GC UNICODE MPZ CLASS UDP OK')
"""
            bearbeitenWert('checks.py', pythonPrüfpunkte)
            befehlshülle('python checks.py', ['PY EXCEPTION OK', 'PY GC UNICODE MPZ CLASS UDP OK', 'exit 0'])
            befehlshülle('rm checks.py', [])
            bearbeitenWert('helper.py', 'value = 321')
            befehlshülle("python -c 'import helper; print(helper.value)'", ['321', 'exit 0'])
            befehlshülle('rm helper.py', [])
            befehlshülle("python -c 'print(1 // 0)'", ['ZeroDivisionError', 'exit 1'])
            befehlshülle("python -c 'while True: pass'", ['exit -1004'])
            for ordnungszahlIndex in range(4):
                befehlshülle('python hello.py', ['한글 Datei', 'exit 0'])
                befehlshülle('java Hello', ['square=49', 'exit 0'])
            # Import a normal SDK-built ELF, run it through the same MMU/ABI checks,
            # and reject a malformed file without losing the console.
            hochladenDateien('app.elf', (projektWurzel / 'build/user/demo.elf').read_bytes())
            assert herunterladen('app.elf') == (projektWurzel / 'build/user/demo.elf').read_bytes()
            befehlshülle('run app.elf', ['EL0 C++', 'exit 0'])
            hochladenDateien('app.elf', b'not an ELF')
            befehlshülle('run app.elf', ['exit -8'])
            befehlshülle('rm app.elf', [])
            befehlshülle('run cpp', ['ELF DEMO PASS'])
            # Java framebuffer uses the same EL0 SVC boundary as C++/Python.
            zeichnungPfad = ausgabe / 'java-framebuffer'; zeichnungPfad.mkdir(exist_ok=True)
            subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(projektWurzel / 'dist/jkoros-native-korean.jar'), '-d', str(zeichnungPfad), str(projektWurzel / 'Prüfungen/Java/bildschirmPrüfung.java')])
            hochladenDateien('bildschirmPrüfung.class', (zeichnungPfad / 'bildschirmPrüfung.class').read_bytes())
            befehlshülle('java bildschirmPrüfung', ['Bildschirm beschneiden wertZurückweisen', 'JAVA FRAMEBUFFER PASS', 'exit 0'])
            befehlshülle('rm bildschirmPrüfung.class', [])
            with socket.socket(socket.AF_UNIX) as anfragestelle:
                anfragestelle.settimeout(10)
                anfragestelle.connect(str(qMPPfad))
                with anfragestelle.makefile('rwb') as datenstromWert:
                    Gruß = json.loads(datenstromWert.readline())
                    def attrappeSteuerungVerbindung(aufgabeAusführen, weitergeleitetArgument=None):
                        netzwerkNachricht = {'execute': aufgabeAusführen}
                        if weitergeleitetArgument: netzwerkNachricht['arguments'] = weitergeleitetArgument
                        datenstromWert.write((json.dumps(netzwerkNachricht) + '\n').encode())
                        datenstromWert.flush()
                        while True:
                            antwort = json.loads(datenstromWert.readline())
                            if 'error' in antwort: raise AssertionError(antwort)
                            if 'return' in antwort: return antwort['return']
                    attrappeSteuerungVerbindung('qmp_capabilities')
                    bildschirmaufnahme = ausgabe / 'framebuffer.ppm'
                    attrappeSteuerungVerbindung('screendump', {'filename': str(bildschirmaufnahme), 'format': 'ppm'})
                    def beispielEinträge(pfad, punkte):
                        with pfad.open('rb') as bildpunktDatei:
                            assert bildpunktDatei.readline().strip() == b'P6'
                            assert bildpunktDatei.readline().strip() == b'640 480'
                            assert bildpunktDatei.readline().strip() == b'255'
                            bildpunktDaten = bildpunktDatei.read()
                        assert len(bildpunktDaten) == 640 * 480 * 3
                        return [list(bildpunktDaten[(senkrechteKoordinateKoordinate * 640 + waagerechteKoordinateKoordinate) * 3:(senkrechteKoordinateKoordinate * 640 + waagerechteKoordinateKoordinate) * 3 + 3]) for waagerechteKoordinateKoordinate, senkrechteKoordinateKoordinate in punkte]
                    assert beispielEinträge(bildschirmaufnahme, [(405, 405)]) == [[86, 52, 18]], 'Java framebuffer SVC did not draw'
                    assert beispielEinträge(bildschirmaufnahme, [(475, 315)]) == [[80, 192, 64]], 'EL0 graphics syscall did not draw'
                    def senden(gedrücktWert, markierung):
                        versatzwertWert = len(ablaufprotokoll)
                        prozess.stdin.write(gedrücktWert); prozess.stdin.flush()
                        bisEmpfangen(markierung, versatzwertWert)
                    senden(b'gui\n', b'GUI READY:')
                    ersterGUI = ausgabe / 'gui-programs.ppm'
                    attrappeSteuerungVerbindung('screendump', {'filename': str(ersterGUI), 'format': 'ppm'})
                    attrappeSteuerungVerbindung('screendump', {'filename': str(ausgabe / 'gui-programs.png'), 'format': 'png'})
                    assert beispielEinträge(ersterGUI, [(70, 120), (70, 180), (56, 40)]) == [[64, 160, 208], [200, 208, 216], [255, 255, 255]]
                    senden(b'\r', b'GUI ACTION 0 RESULT 0')
                    senden(b'\t', b'GUI FOCUS 1')
                    senden(b'\r', b'GUI ACTION 1 RESULT 0')
                    zweiterGUI = ausgabe / 'gui-network.ppm'
                    attrappeSteuerungVerbindung('screendump', {'filename': str(zweiterGUI), 'format': 'ppm'})
                    attrappeSteuerungVerbindung('screendump', {'filename': str(ausgabe / 'gui-network.png'), 'format': 'png'})
                    assert beispielEinträge(zweiterGUI, [(70, 120), (70, 180)]) == [[200, 208, 216], [64, 160, 208]]
                    senden(b'\t', b'GUI FOCUS 2')
                    senden(b'\r', b'GUI ACTION 2 RESULT 0')
                    senden(b'\t', b'GUI FOCUS 3')
                    senden(b'\r', b'GUI ACTION 3 RESULT 0')
                    attrappeSteuerungVerbindung('screendump', {'filename': str(ausgabe / 'gui-python.png'), 'format': 'png'})
                    senden(b'q', b'jkoros-native> ')
                    validierungBericht['qemu'] = Gruß['QMP']['version']
                    attrappeSteuerungVerbindung('quit')
            prozess.wait(timeout=10)
            # framebuffer 응답뿐 아니라 tatsächlichDaten scanout 픽셀도 확인한다.
            with bildschirmaufnahme.open('rb') as dateiEintrag:
                assert dateiEintrag.readline().strip() == b'P6'
                abmessungenWert = dateiEintrag.readline().strip()
                assert abmessungenWert == b'640 480', abmessungenWert
                assert dateiEintrag.readline().strip() == b'255'
                bildpunkteListe = dateiEintrag.read()
            assert len(bildpunkteListe) == 640 * 480 * 3
            def bildpunkt(waagerechteKoordinateKoordinate, senkrechteKoordinateKoordinate): return list(bildpunkteListe[(senkrechteKoordinateKoordinate * 640 + waagerechteKoordinateKoordinate) * 3:(senkrechteKoordinateKoordinate * 640 + waagerechteKoordinateKoordinate) * 3 + 3])
            beispielEinträge = {'background': bildpunkt(5, 5), 'panel': bildpunkt(45, 85), 'tile': bildpunkt(65, 115)}
            assert beispielEinträge == {'background': [24, 32, 48], 'panel': [226, 232, 239], 'tile': [80, 176, 144]}, beispielEinträge
            validierungBericht.update(passed=True, checks=['Java arithmetic/arrays/UTF-16/64-bit references/EL1',
                'UTF-8 Korean/Japanese/Arabic/emoji UART', 'C++ direct RAM file API (21 runs)',
                'cooperative independent stacks (4 runs)', 'line shell/UTF-8/quotes/edit/cancel/hex upload/download',
                'guest Java compiler/JVM and OpenJDK two-way class verification',
                'Korean Java framebuffer library bounds and actual scanout pixels',
                'Korean Java identifiers, UTF-8 validation, malformed source and bounded execution',
                'MicroPython GC/classes/Unicode/MPZ/imports/exceptions/files/UDP and timeout recovery',
                'load and run custom ELF with malformed image rejection', 'RGB32 framebuffer pixels',
                'ELF64 rejection fixtures: 22', 'EL0 C++ constructors/RAII/FP/files/heap/pointer validation',
                'kernel/text/MMIO/guard/NX/privileged instruction protection', 'timer terminates EL0 infinite loop',
                'repeated EL0 program exit closes leaked descriptors', 'UDP loopback payload/peer/reply/truncation/queue/zero datagram/errors/cleanup',
                'GUI focus/keyboard activation/C++/UDP/Java/MicroPython launch/exit and framebuffer pixels'],
                vnc='RFB 3.8 / 640x480 / UART input',
                framebuffer=beispielEinträge, kernel_sha256=hashlib.sha256((projektWurzel / 'build/kernel8.img').read_bytes()).hexdigest())
            print('PASS: raspi4b native Java + shell + guest Java tools + MicroPython + ELF64/C++ + UDP loopback + GUI')
        finally:
            if prozess.poll() is None:
                prozess.terminate()
                try: prozess.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    prozess.kill(); prozess.wait(timeout=5)
            auswähler.close()
            prozess.stdin.close(); prozess.stdout.close()
            (ausgabe / 'serial.log').write_bytes(ablaufprotokoll)
            (ausgabe / 'report.json').write_text(json.dumps(validierungBericht, indent=2) + '\n')


if __name__ == '__main__':
    ausführenVorgang()
