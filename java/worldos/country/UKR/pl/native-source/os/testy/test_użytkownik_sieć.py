#!/usr/bin/env python3
"""rzeczywisty_dane ring 3 ELF/host UDP 왕복/chronić_WARTOŚĆ błąd/wartość_czasu 제한/잘못된 ELF를 검증한다."""
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

pozycja = Path(__file__).resolve().parents[1]


class maszyna_wirtualna:
    def __init__(self, ścieżka_2, Rodzaj_WARTOŚĆ='elf', sieć_WARTOŚĆ=True, Pamięć_nośnik=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        Katalog_WARTOŚĆ = Path(self.임시.name)
        self.LOG_zapis = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.monitor_WARTOŚĆ = socket.socket(socket.AF_UNIX)
        직렬경로, monitor_ścieżka = Katalog_WARTOŚĆ / 'serial.sock', Katalog_WARTOŚĆ / 'monitor.sock'
        polecenie = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitor_ścieżka) + ',server,nowait']
        polecenie += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if sieć_WARTOŚĆ else ['-net', 'none']
        polecenie += ['-kernel', str(ścieżka_2)] if Rodzaj_WARTOŚĆ == 'elf' else ['-cdrom', str(ścieżka_2), '-boot', 'd']
        if Pamięć_nośnik is not None:
            polecenie += ['-drive', 'file=' + str(Pamięć_nośnik) + ',format=raw,if=ide,index=0']
        self.Proces_WARTOŚĆ = subprocess.Popen(polecenie, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and monitor_ścieżka.exists()):
                if self.Proces_WARTOŚĆ.poll() is not None:
                    raise AssertionError(self.Proces_WARTOŚĆ.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Uruchom_2 wartość_czasu 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.monitor_WARTOŚĆ.connect(str(monitor_ścieżka))
            self.직렬.setblocking(False)
            self.monitor_WARTOŚĆ.sendall(b'cont\n')
            self.stan_oczekiwania('jkoros> ')
        except BaseException:
            self.Zamknięte()
            raise

    def stan_oczekiwania(self, 문구, Uruchom_2=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_zapis[Uruchom_2:]:
                return self.LOG_zapis[Uruchom_2:].decode('utf-8', 'replace')
            Odczyt, _, _ = select.select([self.직렬], [], [], 0.1)
            if Odczyt:
                dane = self.직렬.recv(65536)
                if not dane: break
                self.LOG_zapis.extend(dane)
            if self.Proces_WARTOŚĆ.poll() is not None: break
        raise AssertionError('chwileczkę_WARTOŚĆ awaria_WARTOŚĆ: ' + 문구 + '\n' + self.LOG_zapis.decode('utf-8', 'replace'))

    def polecenie(self, ciąg_WARTOŚĆ, 기대):
        Uruchom_2 = len(self.LOG_zapis)
        self.직렬.sendall((ciąg_WARTOŚĆ + '\n').encode())
        WYNIK = self.stan_oczekiwania('jkoros> ', Uruchom_2)
        for 문구 in 기대:
            assert 문구 in WYNIK, (ciąg_WARTOŚĆ, 문구, WYNIK)
        assert 'PANIC' not in WYNIK, WYNIK
        return WYNIK

    def Zamknięte(self):
        self.직렬.close()
        self.monitor_WARTOŚĆ.close()
        if self.Proces_WARTOŚĆ.poll() is None:
            self.Proces_WARTOŚĆ.terminate()
            try: self.Proces_WARTOŚĆ.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Proces_WARTOŚĆ.kill()
                self.Proces_WARTOŚĆ.wait()
        self.Proces_WARTOŚĆ.communicate()
        self.임시.cleanup()


def 보호커널(Katalog_WARTOŚĆ):
    사례들 = {
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
    항목들 = ['hello=' + str(pozycja / 'build/apps/hello.elf')]
    for Nazwa, treść_WARTOŚĆ_cb0f2404 in 사례들.items():
        plik_źródłowy = Katalog_WARTOŚĆ / (Nazwa + '.s')
        plik_źródłowy.write_text('.code32\n.text\n.globl _start\n_start:\n' + treść_WARTOŚĆ_cb0f2404 +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(Katalog_WARTOŚĆ / (Nazwa + '.o')), str(plik_źródłowy)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(pozycja.parent / 'compiler/użytkownik_Link_Układ.ld'),
                        '-o', str(Katalog_WARTOŚĆ / (Nazwa + '.elf')), str(Katalog_WARTOŚĆ / (Nazwa + '.o'))], check=True)
        항목들.append(Nazwa + '=' + str(Katalog_WARTOŚĆ / (Nazwa + '.elf')))
    systemy_informacyjne_zwykła = bytearray((pozycja / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    nieważny_KR = bytearray(systemy_informacyjne_zwykła); nieważny_KR[0] = 0; 변형들['badelf'] = nieważny_KR
    nieważny_KR = bytearray(systemy_informacyjne_zwykła); struct.pack_into('<I', nieważny_KR, 24, 0x00100000); 변형들['badentry'] = nieważny_KR
    nieważny_KR = bytearray(systemy_informacyjne_zwykła); struct.pack_into('<I', nieważny_KR, 28, 0x7fffffff); 변형들['badtable'] = nieważny_KR
    nieważny_KR = bytearray(systemy_informacyjne_zwykła); WYSZUKAJ_tabela = struct.unpack_from('<I', nieważny_KR, 28)[0]
    struct.pack_into('<I', nieważny_KR, WYSZUKAJ_tabela + 20, 0x7fffffff); 변형들['badsize'] = nieważny_KR
    for Nazwa, dane in 변형들.items():
        nazwa_pliku = Katalog_WARTOŚĆ / (Nazwa + '.elf'); nazwa_pliku.write_bytes(dane)
        항목들.append(Nazwa + '=' + str(nazwa_pliku))
    subprocess.run([sys.executable, str(pozycja / 'narzędzia/BIND_uczestnik.py'), '-o', str(Katalog_WARTOŚĆ / 'apps.bin')] + 항목들, check=True)
    plik_źródłowy = Katalog_WARTOŚĆ / 'apps.s'
    plik_źródłowy.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(Katalog_WARTOŚĆ / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(Katalog_WARTOŚĆ / 'apps.o'), str(plik_źródłowy)], check=True)
    jądro_WARTOŚĆ = Katalog_WARTOŚĆ / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(pozycja / 'rozruch_maszyny/układ_konsolidacji.ld'), '-o', str(jądro_WARTOŚĆ),
                    str(pozycja / 'build/boot.o'), str(pozycja / 'build/java.o'), str(pozycja / 'build/user.o'), str(Katalog_WARTOŚĆ / 'apps.o')], check=True)
    return jądro_WARTOŚĆ


def Wykonaj_polecenie():
    WYNIK = {}
    serwer_WARTOŚĆ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serwer_WARTOŚĆ.bind(('127.0.0.1', 0))
    serwer_WARTOŚĆ.settimeout(0.1)
    port_WARTOŚĆ = serwer_WARTOŚĆ.getsockname()[1]
    KWOTA_WYKUP_towar = []
    wyjść_program = threading.Event()
    def echo_odpowiedź():
        while not wyjść_program.is_set():
            try: dane, węzeł_równorzędny_WARTOŚĆ = serwer_WARTOŚĆ.recvfrom(4096)
            except socket.timeout: continue
            KWOTA_WYKUP_towar.append(dane)
            if dane != b'drop-me': serwer_WARTOŚĆ.sendto(dane, węzeł_równorzędny_WARTOŚĆ)
    pracownik_WARTOŚĆ = threading.Thread(target=echo_odpowiedź, daemon=True)
    pracownik_WARTOŚĆ.start()
    try:
        for Rodzaj_WARTOŚĆ in ('elf', 'iso'):
            maszyna = maszyna_wirtualna(pozycja / ('build/kernel.elf' if Rodzaj_WARTOŚĆ == 'elf' else 'build/kernel.iso'), Rodzaj_WARTOŚĆ)
            try:
                maszyna.polecenie('apps', ['hello', 'udp', 'netcheck', 'stress'])
                maszyna.polecenie('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                maszyna.polecenie('run missing', ['Exit: -2'])
                maszyna.polecenie('net', ['NET RTL8139'])
                maszyna.polecenie('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for treść_WARTOŚĆ_cb0f2404 in ('hello-network', 'odd', 'even', 'repeat-123'):
                    maszyna.polecenie('run udp 10.0.2.2 {} {}'.format(port_WARTOŚĆ, treść_WARTOŚĆ_cb0f2404), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert treść_WARTOŚĆ_cb0f2404.encode() in KWOTA_WYKUP_towar, 'host 서버에서 자료를 받지 못함'
                maszyna.polecenie('run stress {}'.format(port_WARTOŚĆ), ['UDP STRESS PASS', 'Exit: 0'])
                maszyna.polecenie('run udp 10.0.2.2 {} drop-me'.format(port_WARTOŚĆ), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                maszyna.polecenie('run hello recovered', ['arg: recovered', 'Exit: 0'])
                WYNIK[Rodzaj_WARTOŚĆ] = maszyna.LOG_zapis.decode('utf-8', 'replace')
                print('PASS: {} przestrzeń_użytkownika ELF/ring 3/argumenty/UDP host 왕복/wartość_czasu 초과/powłoka 복귀'.format(Rodzaj_WARTOŚĆ), flush=True)
            finally:
                try: maszyna.polecenie('net', [])
                except Exception: pass
                (pozycja / 'build/사용자통신-last.log').write_bytes(maszyna.LOG_zapis)
                maszyna.Zamknięte()
        maszyna = maszyna_wirtualna(pozycja / 'build/kernel.elf', sieć_WARTOŚĆ=False)
        try:
            maszyna.polecenie('net', ['NET unavailable'])
            maszyna.polecenie('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            maszyna.polecenie('run hello', ['USER MODE ring 3', 'Exit: 0'])
            WYNIK['no_nic'] = maszyna.LOG_zapis.decode()
        finally: maszyna.Zamknięte()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            maszyna = maszyna_wirtualna(보호커널(Path(임시)), sieć_WARTOŚĆ=False)
            try:
                for Nazwa, Stan_WARTOŚĆ in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    maszyna.polecenie('run ' + Nazwa, ['Exit: ' + str(Stan_WARTOŚĆ)])
                    maszyna.polecenie('run hello', ['USER MODE ring 3', 'Exit: 0'])
                WYNIK['protection'] = maszyna.LOG_zapis.decode()
                print('PASS: przestrzeń_użytkownika Pamięć_dane/sprzęt_port 격리, 잘못된 wskaźnik/ELF, CPU wyjątek, 무한 iteracja_WARTOŚĆ 제한', flush=True)
            finally:
                (pozycja / 'build/Ochrona_test-last.log').write_bytes(maszyna.LOG_zapis)
                maszyna.Zamknięte()
    finally:
        wyjść_program.set()
        pracownik_WARTOŚĆ.join(timeout=2)
        serwer_WARTOŚĆ.close()
    WYNIK['host_udp_received'] = [{'length': len(dane), 'sha256': hashlib.sha256(dane).hexdigest()} for dane in KWOTA_WYKUP_towar]
    (pozycja / 'build/test_użytkownik_sieć.json').write_text(json.dumps(WYNIK, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Wykonaj_polecenie()
