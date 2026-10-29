#!/usr/bin/env python3
"""sebenar_data ring 3 ELF/hos UDP 왕복/lindung_VALUE RALAT/nilai_masa 제한/잘못된 ELF를 검증한다."""
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

Kedudukan = Path(__file__).resolve().parents[1]


class mesin_maya:
    def __init__(self, LALUAN, 종류='elf', rangkaian_VALUE=True, Storan_medium=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        direktori_VALUE = Path(self.임시.name)
        self.LOG_baris = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.pantau_VALUE = socket.socket(socket.AF_UNIX)
        직렬경로, pantau_laluan = direktori_VALUE / 'serial.sock', direktori_VALUE / 'monitor.sock'
        Perintah = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(pantau_laluan) + ',server,nowait']
        Perintah += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if rangkaian_VALUE else ['-net', 'none']
        Perintah += ['-kernel', str(LALUAN)] if 종류 == 'elf' else ['-cdrom', str(LALUAN), '-boot', 'd']
        if Storan_medium is not None:
            Perintah += ['-drive', 'file=' + str(Storan_medium) + ',format=raw,if=ide,index=0']
        self.Proses_VALUE = subprocess.Popen(Perintah, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and pantau_laluan.exists()):
                if self.Proses_VALUE.poll() is not None:
                    raise AssertionError(self.Proses_VALUE.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Jalan nilai_masa 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.pantau_VALUE.connect(str(pantau_laluan))
            self.직렬.setblocking(False)
            self.pantau_VALUE.sendall(b'cont\n')
            self.keadaan_tunggu('jkoros> ')
        except BaseException:
            self.Tutup()
            raise

    def keadaan_tunggu(self, 문구, Jalan=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_baris[Jalan:]:
                return self.LOG_baris[Jalan:].decode('utf-8', 'replace')
            Baca, _, _ = select.select([self.직렬], [], [], 0.1)
            if Baca:
                data = self.직렬.recv(65536)
                if not data: break
                self.LOG_baris.extend(data)
            if self.Proses_VALUE.poll() is not None: break
        raise AssertionError('tunggu_VALUE kegagalan_VALUE: ' + 문구 + '\n' + self.LOG_baris.decode('utf-8', 'replace'))

    def Perintah(self, rentetan_VALUE, 기대):
        Jalan = len(self.LOG_baris)
        self.직렬.sendall((rentetan_VALUE + '\n').encode())
        ukuran = self.keadaan_tunggu('jkoros> ', Jalan)
        for 문구 in 기대:
            assert 문구 in ukuran, (rentetan_VALUE, 문구, ukuran)
        assert 'PANIC' not in ukuran, ukuran
        return ukuran

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


def 보호커널(direktori_VALUE):
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
    항목들 = ['hello=' + str(Kedudukan / 'build/apps/hello.elf')]
    for Nama, Kandungan_VALUE in 사례들.items():
        SUMBER = direktori_VALUE / (Nama + '.s')
        SUMBER.write_text('.code32\n.text\n.globl _start\n_start:\n' + Kandungan_VALUE +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(direktori_VALUE / (Nama + '.o')), str(SUMBER)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Kedudukan.parent / 'compiler/pengguna_paut_Navigasi.ld'),
                        '-o', str(direktori_VALUE / (Nama + '.elf')), str(direktori_VALUE / (Nama + '.o'))], check=True)
        항목들.append(Nama + '=' + str(direktori_VALUE / (Nama + '.elf')))
    정상 = bytearray((Kedudukan / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    tak_sah_ukuran = bytearray(정상); tak_sah_ukuran[0] = 0; 변형들['badelf'] = tak_sah_ukuran
    tak_sah_ukuran = bytearray(정상); struct.pack_into('<I', tak_sah_ukuran, 24, 0x00100000); 변형들['badentry'] = tak_sah_ukuran
    tak_sah_ukuran = bytearray(정상); struct.pack_into('<I', tak_sah_ukuran, 28, 0x7fffffff); 변형들['badtable'] = tak_sah_ukuran
    tak_sah_ukuran = bytearray(정상); Carian_jadual = struct.unpack_from('<I', tak_sah_ukuran, 28)[0]
    struct.pack_into('<I', tak_sah_ukuran, Carian_jadual + 20, 0x7fffffff); 변형들['badsize'] = tak_sah_ukuran
    for Nama, data in 변형들.items():
        Fail = direktori_VALUE / (Nama + '.elf'); Fail.write_bytes(data)
        항목들.append(Nama + '=' + str(Fail))
    subprocess.run([sys.executable, str(Kedudukan / 'alat/ikat_peserta.py'), '-o', str(direktori_VALUE / 'apps.bin')] + 항목들, check=True)
    SUMBER = direktori_VALUE / 'apps.s'
    SUMBER.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(direktori_VALUE / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(direktori_VALUE / 'apps.o'), str(SUMBER)], check=True)
    kernel_VALUE = direktori_VALUE / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Kedudukan / 'permulaan_mesin/susun_atur_pautan.ld'), '-o', str(kernel_VALUE),
                    str(Kedudukan / 'build/boot.o'), str(Kedudukan / 'build/java.o'), str(Kedudukan / 'build/user.o'), str(direktori_VALUE / 'apps.o')], check=True)
    return kernel_VALUE


def laksanakan_perintah():
    ukuran = {}
    pelayan_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    pelayan_VALUE.bind(('127.0.0.1', 0))
    pelayan_VALUE.settimeout(0.1)
    port_VALUE = pelayan_VALUE.getsockname()[1]
    RECEIVED_item = []
    Keluar_aplikasi = threading.Event()
    def 되보내기():
        while not Keluar_aplikasi.is_set():
            try: data, rakan_VALUE = pelayan_VALUE.recvfrom(4096)
            except socket.timeout: continue
            RECEIVED_item.append(data)
            if data != b'drop-me': pelayan_VALUE.sendto(data, rakan_VALUE)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            mesin = mesin_maya(Kedudukan / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                mesin.Perintah('apps', ['hello', 'udp', 'netcheck', 'stress'])
                mesin.Perintah('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                mesin.Perintah('run missing', ['Exit: -2'])
                mesin.Perintah('net', ['NET RTL8139'])
                mesin.Perintah('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Kandungan_VALUE in ('hello-network', 'odd', 'even', 'repeat-123'):
                    mesin.Perintah('run udp 10.0.2.2 {} {}'.format(port_VALUE, Kandungan_VALUE), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Kandungan_VALUE.encode() in RECEIVED_item, 'hos 서버에서 자료를 받지 못함'
                mesin.Perintah('run stress {}'.format(port_VALUE), ['UDP STRESS PASS', 'Exit: 0'])
                mesin.Perintah('run udp 10.0.2.2 {} drop-me'.format(port_VALUE), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                mesin.Perintah('run hello recovered', ['arg: recovered', 'Exit: 0'])
                ukuran[종류] = mesin.LOG_baris.decode('utf-8', 'replace')
                print('PASS: {} ruang_pengguna ELF/ring 3/인수/UDP hos 왕복/nilai_masa 초과/cangkerang 복귀'.format(종류), flush=True)
            finally:
                try: mesin.Perintah('net', [])
                except Exception: pass
                (Kedudukan / 'build/사용자통신-last.log').write_bytes(mesin.LOG_baris)
                mesin.Tutup()
        mesin = mesin_maya(Kedudukan / 'build/kernel.elf', rangkaian_VALUE=False)
        try:
            mesin.Perintah('net', ['NET unavailable'])
            mesin.Perintah('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            mesin.Perintah('run hello', ['USER MODE ring 3', 'Exit: 0'])
            ukuran['no_nic'] = mesin.LOG_baris.decode()
        finally: mesin.Tutup()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            mesin = mesin_maya(보호커널(Path(임시)), rangkaian_VALUE=False)
            try:
                for Nama, status_VALUE in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    mesin.Perintah('run ' + Nama, ['Exit: ' + str(status_VALUE)])
                    mesin.Perintah('run hello', ['USER MODE ring 3', 'Exit: 0'])
                ukuran['protection'] = mesin.LOG_baris.decode()
                print('PASS: ruang_pengguna Memori_data/포트 격리, 잘못된 penuding/ELF, CPU pengecualian, 무한 lelaran_VALUE 제한', flush=True)
            finally:
                (Kedudukan / 'build/Perlindungan_ujian-last.log').write_bytes(mesin.LOG_baris)
                mesin.Tutup()
    finally:
        Keluar_aplikasi.set()
        일꾼.join(timeout=2)
        pelayan_VALUE.close()
    ukuran['host_udp_received'] = [{'length': len(data), 'sha256': hashlib.sha256(data).hexdigest()} for data in RECEIVED_item]
    (Kedudukan / 'build/ujian_pengguna_rangkaian.json').write_text(json.dumps(ukuran, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    laksanakan_perintah()
