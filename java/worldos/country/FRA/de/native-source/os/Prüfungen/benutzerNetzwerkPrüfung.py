#!/usr/bin/env python3
"""tatsächlichDaten ring 3 ELF/Wirtssystem UDP 왕복/wertSchützen fehler/zeitWert grenzwertWert/잘못된 ELF를 검증한다."""
import json
import hashlib
from pathlib import Path
import select
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import time

position = Path(__file__).resolve().parents[1]


class VirtuelleMaschine:
    def __init__(self, pfad, artWert='elf', netzwerkWert=True, speichergerätMittelgroß=None):
        self.vorläufigWert = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        verzeichnisWert = Path(self.vorläufigWert.name)
        self.protokolldateiAufzeichnung = bytearray()
        self.seriellWert = socket.socket(socket.AF_UNIX)
        self.überwacherWert = socket.socket(socket.AF_UNIX)
        seriellPfad, überwacherPfad = verzeichnisWert / 'serial.sock', verzeichnisWert / 'monitor.sock'
        befehl = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(seriellPfad) + ',server,nowait',
                '-monitor', 'unix:' + str(überwacherPfad) + ',server,nowait']
        befehl += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if netzwerkWert else ['-net', 'none']
        befehl += ['-kernel', str(pfad)] if artWert == 'elf' else ['-cdrom', str(pfad), '-boot', 'd']
        if speichergerätMittelgroß is not None:
            befehl += ['-drive', 'file=' + str(speichergerätMittelgroß) + ',format=raw,if=ide,index=0']
        self.prozessWert = subprocess.Popen(befehl, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            endung = time.monotonic() + 10
            while not (seriellPfad.exists() and überwacherPfad.exists()):
                if self.prozessWert.poll() is not None:
                    raise AssertionError(self.prozessWert.stderr.read().decode())
                if time.monotonic() > endung: raise AssertionError('QEMU ausführenVorgang zeitWert 초과')
                time.sleep(0.03)
            self.seriellWert.connect(str(seriellPfad))
            self.überwacherWert.connect(str(überwacherPfad))
            self.seriellWert.setblocking(False)
            self.überwacherWert.sendall(b'cont\n')
            self.statuswertWarten('jkoros> ')
        except BaseException:
            self.schließen()
            raise

    def statuswertWarten(self, wortgruppeWert, ausführenVorgang=0, grenzwertWert=15):
        endung = time.monotonic() + grenzwertWert
        while time.monotonic() < endung:
            if wortgruppeWert.encode() in self.protokolldateiAufzeichnung[ausführenVorgang:]:
                return self.protokolldateiAufzeichnung[ausführenVorgang:].decode('utf-8', 'replace')
            lesen, _, _ = select.select([self.seriellWert], [], [], 0.1)
            if lesen:
                Daten = self.seriellWert.recv(65536)
                if not Daten: break
                self.protokolldateiAufzeichnung.extend(Daten)
            if self.prozessWert.poll() is not None: break
        raise AssertionError('wertWarten fehlschlagWert: ' + wortgruppeWert + '\n' + self.protokolldateiAufzeichnung.decode('utf-8', 'replace'))

    def befehl(self, Zeichenkette, erwartung):
        ausführenVorgang = len(self.protokolldateiAufzeichnung)
        self.seriellWert.sendall((Zeichenkette + '\n').encode())
        ergebnis = self.statuswertWarten('jkoros> ', ausführenVorgang)
        for wortgruppeWert in erwartung:
            assert wortgruppeWert in ergebnis, (Zeichenkette, wortgruppeWert, ergebnis)
        assert 'PANIC' not in ergebnis, ergebnis
        return ergebnis

    def schließen(self):
        self.seriellWert.close()
        self.überwacherWert.close()
        if self.prozessWert.poll() is None:
            self.prozessWert.terminate()
            try: self.prozessWert.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.prozessWert.kill()
                self.prozessWert.wait()
        self.prozessWert.communicate()
        self.vorläufigWert.cleanup()


def geschütztBetriebskern(verzeichnisWert):
    falllisteListe = {
        'badmem': 'movl $7, 0x00100000',
        'badport': 'movw $0x3f8, %dx\noutb %al, %dx',
        'spin': '1: jmp 1b',
        'badptr': 'movl $1,%eax\nmovl $0x00100000,%ebx\nint $0x80\ncmpl $-14,%eax\njne fail\n'
                  'movl $999,%eax\nint $0x80\ncmpl $-38,%eax\njne fail\n'
                  'xorl %ebx,%ebx\nxorl %eax,%eax\nint $0x80\nfail: movl $1,%ebx\nxorl %eax,%eax\nint $0x80',
        'fault': 'ud2',
        'badfile': '''
            movl $20,%eax
            movl $0x00100000,%ebx
            movl $empty,%ecx
            int $0x80
            cmpl $-14,%eax
            jne fail
            movl $20,%eax
            movl $name,%ebx
            movl $0x00100000,%ecx
            int $0x80
            cmpl $-14,%eax
            jne fail
            movl $21,%eax
            movl $name,%ebx
            movl $negative,%ecx
            xorl %edx,%edx
            int $0x80
            cmpl $-14,%eax
            jne fail
            movl $21,%eax
            movl $name,%ebx
            movl $empty,%ecx
            movl $1,%edx
            int $0x80
            cmpl $-22,%eax
            jne fail
            movl $20,%eax
            movl $empty,%ebx
            movl $empty,%ecx
            int $0x80
            cmpl $-22,%eax
            jne fail
            xorl %eax,%eax
            xorl %ebx,%ebx
            int $0x80
        fail:
            xorl %eax,%eax
            movl $1,%ebx
            int $0x80
        .balign 4
        name: .long 1,88
        empty: .long 0
        negative: .long -1
        ''',
    }
    einträgeListe = ['hello=' + str(position / 'build/apps/hello.elf')]
    for Name, inhaltswertWert in falllisteListe.items():
        Quelltext = verzeichnisWert / (Name + '.s')
        Quelltext.write_text('.code32\n.text\n.globl _start\n_start:\n' + inhaltswertWert +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(verzeichnisWert / (Name + '.o')), str(Quelltext)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(position.parent / 'compiler/benutzerBindenAnordnung.ld'),
                        '-o', str(verzeichnisWert / (Name + '.elf')), str(verzeichnisWert / (Name + '.o'))], check=True)
        einträgeListe.append(Name + '=' + str(verzeichnisWert / (Name + '.elf')))
    istNormal = bytearray((position / 'build/apps/hello.elf').read_bytes())
    variantenListe = {}
    ungültigErgebnis = bytearray(istNormal); ungültigErgebnis[0] = 0; variantenListe['badelf'] = ungültigErgebnis
    ungültigErgebnis = bytearray(istNormal); struct.pack_into('<I', ungültigErgebnis, 24, 0x00100000); variantenListe['badentry'] = ungültigErgebnis
    ungültigErgebnis = bytearray(istNormal); struct.pack_into('<I', ungültigErgebnis, 28, 0x7fffffff); variantenListe['badtable'] = ungültigErgebnis
    ungültigErgebnis = bytearray(istNormal); Tabelle = struct.unpack_from('<I', ungültigErgebnis, 28)[0]
    struct.pack_into('<I', ungültigErgebnis, Tabelle + 20, 0x7fffffff); variantenListe['badsize'] = ungültigErgebnis
    for Name, Daten in variantenListe.items():
        Datei = verzeichnisWert / (Name + '.elf'); Datei.write_bytes(Daten)
        einträgeListe.append(Name + '=' + str(Datei))
    subprocess.run([sys.executable, str(position / 'Werkzeuge/AusführbündelPacken.py'), '-o', str(verzeichnisWert / 'apps.bin')] + einträgeListe, check=True)
    Quelltext = verzeichnisWert / 'apps.s'
    Quelltext.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(verzeichnisWert / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(verzeichnisWert / 'apps.o'), str(Quelltext)], check=True)
    betriebskernWert = verzeichnisWert / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(position / 'Startvorgang/Bindungsanordnung.ld'), '-o', str(betriebskernWert),
                    str(position / 'build/boot.o'), str(position / 'build/java.o'), str(position / 'build/user.o'), str(verzeichnisWert / 'apps.o')], check=True)
    return betriebskernWert


def befehlAusführen():
    ergebnis = {}
    dienstanbieterWert = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dienstanbieterWert.bind(('127.0.0.1', 0))
    dienstanbieterWert.settimeout(0.1)
    portWert = dienstanbieterWert.getsockname()[1]
    empfangenWertElementeintrag = []
    verlassenProzessProgramm = threading.Event()
    def wiedergebenAntwort():
        while not verlassenProzessProgramm.is_set():
            try: Daten, gegenstelleWert = dienstanbieterWert.recvfrom(4096)
            except socket.timeout: continue
            empfangenWertElementeintrag.append(Daten)
            if Daten != b'drop-me': dienstanbieterWert.sendto(Daten, gegenstelleWert)
    hintergrundarbeiterWert = threading.Thread(target=wiedergebenAntwort, daemon=True)
    hintergrundarbeiterWert.start()
    try:
        for artWert in ('elf', 'iso'):
            maschine = VirtuelleMaschine(position / ('build/kernel.elf' if artWert == 'elf' else 'build/kernel.iso'), artWert)
            try:
                maschine.befehl('apps', ['hello', 'udp', 'netcheck', 'stress'])
                maschine.befehl('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                maschine.befehl('run missing', ['Exit: -2'])
                maschine.befehl('net', ['NET RTL8139'])
                maschine.befehl('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for inhaltswertWert in ('hello-network', 'odd', 'even', 'repeat-123'):
                    maschine.befehl('run udp 10.0.2.2 {} {}'.format(portWert, inhaltswertWert), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert inhaltswertWert.encode() in empfangenWertElementeintrag, 'Wirtssystem 서버에서 자료를 받지 못함'
                maschine.befehl('run stress {}'.format(portWert), ['UDP STRESS PASS', 'Exit: 0'])
                maschine.befehl('run udp 10.0.2.2 {} drop-me'.format(portWert), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                maschine.befehl('run hello recovered', ['arg: recovered', 'Exit: 0'])
                ergebnis[artWert] = maschine.protokolldateiAufzeichnung.decode('utf-8', 'replace')
                print('PASS: {} Benutzer ELF/ring 3/argumente/UDP Wirtssystem 왕복/zeitWert 초과/befehlshülle 복귀'.format(artWert), flush=True)
            finally:
                try: maschine.befehl('net', [])
                except Exception: pass
                (position / 'build/사용자통신-last.log').write_bytes(maschine.protokolldateiAufzeichnung)
                maschine.schließen()
        maschine = VirtuelleMaschine(position / 'build/kernel.elf', netzwerkWert=False)
        try:
            maschine.befehl('net', ['NET unavailable'])
            maschine.befehl('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            maschine.befehl('run hello', ['USER MODE ring 3', 'Exit: 0'])
            ergebnis['no_nic'] = maschine.protokolldateiAufzeichnung.decode()
        finally: maschine.schließen()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as vorläufigWert:
            maschine = VirtuelleMaschine(geschütztBetriebskern(Path(vorläufigWert)), netzwerkWert=False)
            try:
                for Name, statuswertWert in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    maschine.befehl('run ' + Name, ['Exit: ' + str(statuswertWert)])
                    maschine.befehl('run hello', ['USER MODE ring 3', 'Exit: 0'])
                ergebnis['protection'] = maschine.protokolldateiAufzeichnung.decode()
                print('PASS: Benutzer speicherDaten/hardwarePort 격리, 잘못된 zeiger/ELF, CPU ausnahme, 무한 wiederholungsschrittWert grenzwertWert', flush=True)
            finally:
                (position / 'build/SchutzPrüfung-last.log').write_bytes(maschine.protokolldateiAufzeichnung)
                maschine.schließen()
    finally:
        verlassenProzessProgramm.set()
        hintergrundarbeiterWert.join(timeout=2)
        dienstanbieterWert.close()
    ergebnis['host_udp_received'] = [{'length': len(Daten), 'sha256': hashlib.sha256(Daten).hexdigest()} for Daten in empfangenWertElementeintrag]
    (position / 'build/benutzerNetzwerkPrüfung.json').write_text(json.dumps(ergebnis, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    befehlAusführen()
