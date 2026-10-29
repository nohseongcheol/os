#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 seriellWert/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

position = Path(__file__).resolve().parents[1]


def abwarten(Prüfpunkte, beschreibung, grenzwertWert=15):
    endung = time.monotonic() + grenzwertWert
    while time.monotonic() < endung:
        ergebnis = Prüfpunkte()
        if ergebnis:
            return ergebnis
        time.sleep(0.05)
    raise AssertionError('zeitWert 초과: ' + beschreibung)


def Prüfungen(artWert):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as vorläufigWert:
        vorläufigWert = Path(vorläufigWert)
        seriellPfad = vorläufigWert / 'serial.sock'
        überwacherPfad = vorläufigWert / 'monitor.sock'
        befehl = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(seriellPfad) + ',server,nowait',
                '-monitor', 'unix:' + str(überwacherPfad) + ',server,nowait']
        befehl += ['-kernel', str(position / 'build/kernel.elf')] if artWert == 'elf' else [
            '-cdrom', str(position / 'build/kernel.iso'), '-boot', 'd']
        # seriellWert 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        befehl += ['-S']
        prozessWert = subprocess.Popen(befehl, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        seriellWert = socket.socket(socket.AF_UNIX)
        überwacherWert = socket.socket(socket.AF_UNIX)
        protokolldateiAufzeichnung = bytearray()
        try:
            def netzbuchseVorbereiten():
                if prozessWert.poll() is not None:
                    raise AssertionError(prozessWert.stderr.read().decode('utf-8', 'replace'))
                return seriellPfad.exists() and überwacherPfad.exists()
            abwarten(netzbuchseVorbereiten, 'QEMU netzbuchseWert')
            seriellWert.connect(str(seriellPfad))
            überwacherWert.connect(str(überwacherPfad))
            seriellWert.setblocking(False)
            überwacherWert.sendall(b'cont\n')

            def Kopfdateien(Zeichenkette, ausführenVorgang=0):
                lesen, _, _ = select.select([seriellWert], [], [], 0.1)
                if lesen:
                    Daten = seriellWert.recv(65536)
                    if not Daten:
                        raise AssertionError('seriellWert verbinden verlassenProzessProgramm')
                    protokolldateiAufzeichnung.extend(Daten)
                if prozessWert.poll() is not None:
                    raise AssertionError('QEMU 비정상 verlassenProzessProgramm: ' + str(prozessWert.returncode))
                return Zeichenkette.encode('utf-8') in protokolldateiAufzeichnung[ausführenVorgang:]

            def befehlePrüfung(Eingabewert, erwartung):
                ausführenVorgang = len(protokolldateiAufzeichnung)
                seriellWert.sendall(Eingabewert.encode('ascii'))
                abwarten(lambda: Kopfdateien(erwartung, ausführenVorgang), erwartung)
                abwarten(lambda: Kopfdateien('jkoros> ', ausführenVorgang), 'befehl danachStatuswert 프롬프트')

            abwarten(lambda: Kopfdateien('READY'), artWert + ' Startvorgang')
            assert b'JAVA SELFTEST PASS' in protokolldateiAufzeichnung
            assert 'Java 기계어 betriebskernWert ausführenVorgang'.encode() in protokolldateiAufzeichnung
            befehlePrüfung('info\r\n', 'embedded subset JVM / polling kernel')
            befehlePrüfung('help\n', 'free N | echo TEXT')
            befehlePrüfung('mem\n', ' / 8 (각 4096바이트)')
            befehlePrüfung('echo natix\bve\n', 'native\r\n')
            for Nummer in range(8):
                befehlePrüfung('alloc\n', 'abschnittWert Nummer: ' + str(Nummer))
            befehlePrüfung('alloc\n', 'abschnittWert Nummer: -1')
            befehlePrüfung('free 3\n', '반환됨')
            befehlePrüfung('free 3\n', '할당되지 않은 abschnittWert')
            befehlePrüfung('free 99\n', '사용법: free 0..7')
            befehlePrüfung('alloc\n', 'abschnittWert Nummer: 3')
            befehlePrüfung('free 0\n', '반환됨')
            befehlePrüfung('test\n', 'JAVA SELFTEST PASS')
            befehlePrüfung('unknown\n', '알 Zahl 없는 명령입니다')
            befehlePrüfung('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            ausführenVorgang = len(protokolldateiAufzeichnung)
            for tasteWert in ('i', 'n', 'f', 'o', 'ret'):
                überwacherWert.sendall(('sendkey ' + tasteWert + ' 30\n').encode())
                time.sleep(0.09)
            abwarten(lambda: Kopfdateien('embedded subset JVM / polling kernel', ausführenVorgang), 'PS/2 info Eingabewert')
            befehlePrüfung('echo ' + 'a' * 150 + '\n', 'a' * 123)
            seriellWert.sendall(b'halt\n')
            abwarten(lambda: Kopfdateien('HALTED'), 'anhaltenAusführung befehl')
            assert b'PANIC' not in protokolldateiAufzeichnung and b'SELFTEST FAIL' not in protokolldateiAufzeichnung
            print('PASS: {} Startvorgang, Java eigen Prüfungen, seriellWert befehl, PS/2 Eingabewert, speichergerätZuteilen/zurückkehrenErgebnis, anhaltenAusführung'.format(artWert))
            return protokolldateiAufzeichnung.decode('utf-8', 'replace')
        finally:
            seriellWert.close()
            überwacherWert.close()
            prozessWert.terminate()
            try:
                prozessWert.wait(timeout=3)
            except subprocess.TimeoutExpired:
                prozessWert.kill()
                prozessWert.wait()


if __name__ == '__main__':
    ergebnis = {artWert: Prüfungen(artWert) for artWert in ('elf', 'iso')}
    (position / 'build/Startprüfung.json').write_text(json.dumps(ergebnis, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
