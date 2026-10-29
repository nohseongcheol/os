#!/usr/bin/env python3
"""aktual_data ring 3 ELF/host UDP 왕복/amankan_VALUE galat/TIME_VALUE 제한/잘못된 ELF를 검증한다."""
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

posisi = Path(__file__).resolve().parents[1]


class mesin_virtual:
    def __init__(self, jalur, 종류='elf', jaringan_VALUE=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        Direktori_VALUE = Path(self.임시.name)
        self.LOG_baris = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.pantau_VALUE = socket.socket(socket.AF_UNIX)
        직렬경로, pantau_jalur = Direktori_VALUE / 'serial.sock', Direktori_VALUE / 'monitor.sock'
        perintah = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(pantau_jalur) + ',server,nowait']
        perintah += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if jaringan_VALUE else ['-net', 'none']
        perintah += ['-kernel', str(jalur)] if 종류 == 'elf' else ['-cdrom', str(jalur), '-boot', 'd']
        if 저장매체 is not None:
            perintah += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Proses_VALUE = subprocess.Popen(perintah, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and pantau_jalur.exists()):
                if self.Proses_VALUE.poll() is not None:
                    raise AssertionError(self.Proses_VALUE.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU jalankan TIME_VALUE 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.pantau_VALUE.connect(str(pantau_jalur))
            self.직렬.setblocking(False)
            self.pantau_VALUE.sendall(b'cont\n')
            self.tunggu_Status('jkoros> ')
        except BaseException:
            self.Tutup()
            raise

    def tunggu_Status(self, 문구, jalankan=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_baris[jalankan:]:
                return self.LOG_baris[jalankan:].decode('utf-8', 'replace')
            Baca, _, _ = select.select([self.직렬], [], [], 0.1)
            if Baca:
                data = self.직렬.recv(65536)
                if not data: break
                self.LOG_baris.extend(data)
            if self.Proses_VALUE.poll() is not None: break
        raise AssertionError('tunggu_VALUE kegagalan_VALUE: ' + 문구 + '\n' + self.LOG_baris.decode('utf-8', 'replace'))

    def perintah(self, string_VALUE, 기대):
        jalankan = len(self.LOG_baris)
        self.직렬.sendall((string_VALUE + '\n').encode())
        hasil = self.tunggu_Status('jkoros> ', jalankan)
        for 문구 in 기대:
            assert 문구 in hasil, (string_VALUE, 문구, hasil)
        assert 'PANIC' not in hasil, hasil
        return hasil

    def Tutup(self):
        self.직렬.close()
        self.pantau_VALUE.close()
        if self.Proses_VALUE.poll() is None:
            self.Proses_VALUE.terminate()
            try: self.Proses_VALUE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Proses_VALUE.kill()
                self.Proses_VALUE.wait()
        self.Proses_VALUE.communicate()
        self.임시.cleanup()


def 보호커널(Direktori_VALUE):
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
    항목들 = ['hello=' + str(posisi / 'build/apps/hello.elf')]
    for Nama_2, Isi_VALUE in 사례들.items():
        kodeSumber = Direktori_VALUE / (Nama_2 + '.s')
        kodeSumber.write_text('.code32\n.text\n.globl _start\n_start:\n' + Isi_VALUE +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(Direktori_VALUE / (Nama_2 + '.o')), str(kodeSumber)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(posisi.parent / 'compiler/pengguna_link_Navigasi.ld'),
                        '-o', str(Direktori_VALUE / (Nama_2 + '.elf')), str(Direktori_VALUE / (Nama_2 + '.o'))], check=True)
        항목들.append(Nama_2 + '=' + str(Direktori_VALUE / (Nama_2 + '.elf')))
    정상 = bytearray((posisi / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    tidak_sahih_KR = bytearray(정상); tidak_sahih_KR[0] = 0; 변형들['badelf'] = tidak_sahih_KR
    tidak_sahih_KR = bytearray(정상); struct.pack_into('<I', tidak_sahih_KR, 24, 0x00100000); 변형들['badentry'] = tidak_sahih_KR
    tidak_sahih_KR = bytearray(정상); struct.pack_into('<I', tidak_sahih_KR, 28, 0x7fffffff); 변형들['badtable'] = tidak_sahih_KR
    tidak_sahih_KR = bytearray(정상); LOOKUP_tabel = struct.unpack_from('<I', tidak_sahih_KR, 28)[0]
    struct.pack_into('<I', tidak_sahih_KR, LOOKUP_tabel + 20, 0x7fffffff); 변형들['badsize'] = tidak_sahih_KR
    for Nama_2, data in 변형들.items():
        berkas = Direktori_VALUE / (Nama_2 + '.elf'); berkas.write_bytes(data)
        항목들.append(Nama_2 + '=' + str(berkas))
    subprocess.run([sys.executable, str(posisi / 'alat/ikat_peserta.py'), '-o', str(Direktori_VALUE / 'apps.bin')] + 항목들, check=True)
    kodeSumber = Direktori_VALUE / 'apps.s'
    kodeSumber.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(Direktori_VALUE / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(Direktori_VALUE / 'apps.o'), str(kodeSumber)], check=True)
    kernel_VALUE = Direktori_VALUE / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(posisi / 'awal_mesin/tata_letak_penautan.ld'), '-o', str(kernel_VALUE),
                    str(posisi / 'build/boot.o'), str(posisi / 'build/java.o'), str(posisi / 'build/user.o'), str(Direktori_VALUE / 'apps.o')], check=True)
    return kernel_VALUE


def Jalankan_perintah():
    hasil = {}
    server_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_VALUE.bind(('127.0.0.1', 0))
    server_VALUE.settimeout(0.1)
    port_VALUE = server_VALUE.getsockname()[1]
    RECEIVED_item = []
    Keluar_apl = threading.Event()
    def echo_balas():
        while not Keluar_apl.is_set():
            try: data, serekan_VALUE = server_VALUE.recvfrom(4096)
            except socket.timeout: continue
            RECEIVED_item.append(data)
            if data != b'drop-me': server_VALUE.sendto(data, serekan_VALUE)
    일꾼 = threading.Thread(target=echo_balas, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            mesin = mesin_virtual(posisi / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                mesin.perintah('apps', ['hello', 'udp', 'netcheck', 'stress'])
                mesin.perintah('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                mesin.perintah('run missing', ['Exit: -2'])
                mesin.perintah('net', ['NET RTL8139'])
                mesin.perintah('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Isi_VALUE in ('hello-network', 'odd', 'even', 'repeat-123'):
                    mesin.perintah('run udp 10.0.2.2 {} {}'.format(port_VALUE, Isi_VALUE), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Isi_VALUE.encode() in RECEIVED_item, 'host 서버에서 자료를 받지 못함'
                mesin.perintah('run stress {}'.format(port_VALUE), ['UDP STRESS PASS', 'Exit: 0'])
                mesin.perintah('run udp 10.0.2.2 {} drop-me'.format(port_VALUE), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                mesin.perintah('run hello recovered', ['arg: recovered', 'Exit: 0'])
                hasil[종류] = mesin.LOG_baris.decode('utf-8', 'replace')
                print('PASS: {} ruang_pengguna ELF/ring 3/argumen/UDP host 왕복/TIME_VALUE 초과/shell 복귀'.format(종류), flush=True)
            finally:
                try: mesin.perintah('net', [])
                except Exception: pass
                (posisi / 'build/사용자통신-last.log').write_bytes(mesin.LOG_baris)
                mesin.Tutup()
        mesin = mesin_virtual(posisi / 'build/kernel.elf', jaringan_VALUE=False)
        try:
            mesin.perintah('net', ['NET unavailable'])
            mesin.perintah('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            mesin.perintah('run hello', ['USER MODE ring 3', 'Exit: 0'])
            hasil['no_nic'] = mesin.LOG_baris.decode()
        finally: mesin.Tutup()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            mesin = mesin_virtual(보호커널(Path(임시)), jaringan_VALUE=False)
            try:
                for Nama_2, Status_VALUE in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    mesin.perintah('run ' + Nama_2, ['Exit: ' + str(Status_VALUE)])
                    mesin.perintah('run hello', ['USER MODE ring 3', 'Exit: 0'])
                hasil['protection'] = mesin.LOG_baris.decode()
                print('PASS: ruang_pengguna Memori_data/포트 격리, 잘못된 pointer/ELF, CPU pengecualian, 무한 sprint_VALUE 제한', flush=True)
            finally:
                (posisi / 'build/보호시험-last.log').write_bytes(mesin.LOG_baris)
                mesin.Tutup()
    finally:
        Keluar_apl.set()
        일꾼.join(timeout=2)
        server_VALUE.close()
    hasil['host_udp_received'] = [{'length': len(data), 'sha256': hashlib.sha256(data).hexdigest()} for data in RECEIVED_item]
    (posisi / 'build/사용자통신시험.json').write_text(json.dumps(hasil, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Jalankan_perintah()
