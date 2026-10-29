#!/usr/bin/env python3
"""dữLiệuThựcTế ring 3 ELF/Chủ UDP 왕복/bảoVệGiáTrị lỗi/giáTrịThờiGian giáTrịGiớiHạn/잘못된 ELF를 검증한다."""
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

vịTrí = Path(__file__).resolve().parents[1]


class MáyẢo:
    def __init__(self, đườngDẫn, giáTrịLoại='elf', giáTrịMạng=True, môiGiớiLưuTrữ=None):
        self.giáTrịTạm = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        giáTrịThưMục = Path(self.giáTrịTạm.name)
        self.bảnGhiNhậtKý = bytearray()
        self.giáTrịNốiTiếp = socket.socket(socket.AF_UNIX)
        self.giáTrịBộGiámSát = socket.socket(socket.AF_UNIX)
        đườngDẫnNốiTiếp, đườngDẫnBộGiámSát = giáTrịThưMục / 'serial.sock', giáTrịThưMục / 'monitor.sock'
        lệnh = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(đườngDẫnNốiTiếp) + ',server,nowait',
                '-monitor', 'unix:' + str(đườngDẫnBộGiámSát) + ',server,nowait']
        lệnh += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if giáTrịMạng else ['-net', 'none']
        lệnh += ['-kernel', str(đườngDẫn)] if giáTrịLoại == 'elf' else ['-cdrom', str(đườngDẫn), '-boot', 'd']
        if môiGiớiLưuTrữ is not None:
            lệnh += ['-drive', 'file=' + str(môiGiớiLưuTrữ) + ',format=raw,if=ide,index=0']
        self.giáTrịTiếnTrình = subprocess.Popen(lệnh, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            phầnKết = time.monotonic() + 10
            while not (đườngDẫnNốiTiếp.exists() and đườngDẫnBộGiámSát.exists()):
                if self.giáTrịTiếnTrình.poll() is not None:
                    raise AssertionError(self.giáTrịTiếnTrình.stderr.read().decode())
                if time.monotonic() > phầnKết: raise AssertionError('QEMU chạy giáTrịThờiGian 초과')
                time.sleep(0.03)
            self.giáTrịNốiTiếp.connect(str(đườngDẫnNốiTiếp))
            self.giáTrịBộGiámSát.connect(str(đườngDẫnBộGiámSát))
            self.giáTrịNốiTiếp.setblocking(False)
            self.giáTrịBộGiámSát.sendall(b'cont\n')
            self.chờTrạngThái('jkoros> ')
        except BaseException:
            self.đóng()
            raise

    def chờTrạngThái(self, giáTrịCụmTừ, chạy=0, giáTrịGiớiHạn=15):
        phầnKết = time.monotonic() + giáTrịGiớiHạn
        while time.monotonic() < phầnKết:
            if giáTrịCụmTừ.encode() in self.bảnGhiNhậtKý[chạy:]:
                return self.bảnGhiNhậtKý[chạy:].decode('utf-8', 'replace')
            đọc, _, _ = select.select([self.giáTrịNốiTiếp], [], [], 0.1)
            if đọc:
                DữLiệu = self.giáTrịNốiTiếp.recv(65536)
                if not DữLiệu: break
                self.bảnGhiNhậtKý.extend(DữLiệu)
            if self.giáTrịTiếnTrình.poll() is not None: break
        raise AssertionError('chờGiáTrị giáTrịSựThấtBại: ' + giáTrịCụmTừ + '\n' + self.bảnGhiNhậtKý.decode('utf-8', 'replace'))

    def lệnh(self, ChuỗiKýTự, kỳVọng):
        chạy = len(self.bảnGhiNhậtKý)
        self.giáTrịNốiTiếp.sendall((ChuỗiKýTự + '\n').encode())
        kếtQuả = self.chờTrạngThái('jkoros> ', chạy)
        for giáTrịCụmTừ in kỳVọng:
            assert giáTrịCụmTừ in kếtQuả, (ChuỗiKýTự, giáTrịCụmTừ, kếtQuả)
        assert 'PANIC' not in kếtQuả, kếtQuả
        return kếtQuả

    def đóng(self):
        self.giáTrịNốiTiếp.close()
        self.giáTrịBộGiámSát.close()
        if self.giáTrịTiếnTrình.poll() is None:
            self.giáTrịTiếnTrình.terminate()
            try: self.giáTrịTiếnTrình.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.giáTrịTiếnTrình.kill()
                self.giáTrịTiếnTrình.wait()
        self.giáTrịTiếnTrình.communicate()
        self.giáTrịTạm.cleanup()


def nhânĐượcBảoVệ(giáTrịThưMục):
    danhSáchCácTrườngHợp = {
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
    danhSáchCácMục = ['hello=' + str(vịTrí / 'build/apps/hello.elf')]
    for tên, giáTrịNộiDung in danhSáchCácTrườngHợp.items():
        mãNguồn = giáTrịThưMục / (tên + '.s')
        mãNguồn.write_text('.code32\n.text\n.globl _start\n_start:\n' + giáTrịNộiDung +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(giáTrịThưMục / (tên + '.o')), str(mãNguồn)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(vịTrí.parent / 'compiler/bốTríLiênKếtNgườiDùng.ld'),
                        '-o', str(giáTrịThưMục / (tên + '.elf')), str(giáTrịThưMục / (tên + '.o'))], check=True)
        danhSáchCácMục.append(tên + '=' + str(giáTrịThưMục / (tên + '.elf')))
    làBìnhThường = bytearray((vịTrí / 'build/apps/hello.elf').read_bytes())
    danhSáchCácBiếnThể = {}
    kếtQuảKhôngHợpLệ = bytearray(làBìnhThường); kếtQuảKhôngHợpLệ[0] = 0; danhSáchCácBiếnThể['badelf'] = kếtQuảKhôngHợpLệ
    kếtQuảKhôngHợpLệ = bytearray(làBìnhThường); struct.pack_into('<I', kếtQuảKhôngHợpLệ, 24, 0x00100000); danhSáchCácBiếnThể['badentry'] = kếtQuảKhôngHợpLệ
    kếtQuảKhôngHợpLệ = bytearray(làBìnhThường); struct.pack_into('<I', kếtQuảKhôngHợpLệ, 28, 0x7fffffff); danhSáchCácBiếnThể['badtable'] = kếtQuảKhôngHợpLệ
    kếtQuảKhôngHợpLệ = bytearray(làBìnhThường); Bảng = struct.unpack_from('<I', kếtQuảKhôngHợpLệ, 28)[0]
    struct.pack_into('<I', kếtQuảKhôngHợpLệ, Bảng + 20, 0x7fffffff); danhSáchCácBiếnThể['badsize'] = kếtQuảKhôngHợpLệ
    for tên, DữLiệu in danhSáchCácBiếnThể.items():
        Tệp = giáTrịThưMục / (tên + '.elf'); Tệp.write_bytes(DữLiệu)
        danhSáchCácMục.append(tên + '=' + str(Tệp))
    subprocess.run([sys.executable, str(vịTrí / 'CôngCụ/GóiTệpThựcThi.py'), '-o', str(giáTrịThưMục / 'apps.bin')] + danhSáchCácMục, check=True)
    mãNguồn = giáTrịThưMục / 'apps.s'
    mãNguồn.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(giáTrịThưMục / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(giáTrịThưMục / 'apps.o'), str(mãNguồn)], check=True)
    giáTrịNhân = giáTrịThưMục / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(vịTrí / 'KhởiĐộng/BốTríLiênKết.ld'), '-o', str(giáTrịNhân),
                    str(vịTrí / 'build/boot.o'), str(vịTrí / 'build/java.o'), str(vịTrí / 'build/user.o'), str(giáTrịThưMục / 'apps.o')], check=True)
    return giáTrịNhân


def thựcThiLệnh():
    kếtQuả = {}
    giáTrịMáyChủ = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    giáTrịMáyChủ.bind(('127.0.0.1', 0))
    giáTrịMáyChủ.settimeout(0.1)
    giáTrịCổng = giáTrịMáyChủ.getsockname()[1]
    phầnMụcĐãNhận = []
    chươngTrìnhRa = threading.Event()
    def lờiĐápVọngLại():
        while not chươngTrìnhRa.is_set():
            try: DữLiệu, giáTrịĐốiTác = giáTrịMáyChủ.recvfrom(4096)
            except socket.timeout: continue
            phầnMụcĐãNhận.append(DữLiệu)
            if DữLiệu != b'drop-me': giáTrịMáyChủ.sendto(DữLiệu, giáTrịĐốiTác)
    giáTrịBộLàmViệc = threading.Thread(target=lờiĐápVọngLại, daemon=True)
    giáTrịBộLàmViệc.start()
    try:
        for giáTrịLoại in ('elf', 'iso'):
            máy = MáyẢo(vịTrí / ('build/kernel.elf' if giáTrịLoại == 'elf' else 'build/kernel.iso'), giáTrịLoại)
            try:
                máy.lệnh('apps', ['hello', 'udp', 'netcheck', 'stress'])
                máy.lệnh('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                máy.lệnh('run missing', ['Exit: -2'])
                máy.lệnh('net', ['NET RTL8139'])
                máy.lệnh('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for giáTrịNộiDung in ('hello-network', 'odd', 'even', 'repeat-123'):
                    máy.lệnh('run udp 10.0.2.2 {} {}'.format(giáTrịCổng, giáTrịNộiDung), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert giáTrịNộiDung.encode() in phầnMụcĐãNhận, 'Chủ 서버에서 자료를 받지 못함'
                máy.lệnh('run stress {}'.format(giáTrịCổng), ['UDP STRESS PASS', 'Exit: 0'])
                máy.lệnh('run udp 10.0.2.2 {} drop-me'.format(giáTrịCổng), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                máy.lệnh('run hello recovered', ['arg: recovered', 'Exit: 0'])
                kếtQuả[giáTrịLoại] = máy.bảnGhiNhậtKý.decode('utf-8', 'replace')
                print('PASS: {} NgườiDùng ELF/ring 3/cácĐốiSố/UDP Chủ 왕복/giáTrịThờiGian 초과/vỏLệnh 복귀'.format(giáTrịLoại), flush=True)
            finally:
                try: máy.lệnh('net', [])
                except Exception: pass
                (vịTrí / 'build/사용자통신-last.log').write_bytes(máy.bảnGhiNhậtKý)
                máy.đóng()
        máy = MáyẢo(vịTrí / 'build/kernel.elf', giáTrịMạng=False)
        try:
            máy.lệnh('net', ['NET unavailable'])
            máy.lệnh('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            máy.lệnh('run hello', ['USER MODE ring 3', 'Exit: 0'])
            kếtQuả['no_nic'] = máy.bảnGhiNhậtKý.decode()
        finally: máy.đóng()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as giáTrịTạm:
            máy = MáyẢo(nhânĐượcBảoVệ(Path(giáTrịTạm)), giáTrịMạng=False)
            try:
                for tên, giáTrịTrạngThái in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    máy.lệnh('run ' + tên, ['Exit: ' + str(giáTrịTrạngThái)])
                    máy.lệnh('run hello', ['USER MODE ring 3', 'Exit: 0'])
                kếtQuả['protection'] = máy.bảnGhiNhậtKý.decode()
                print('PASS: NgườiDùng dữLiệuBộNhớ/cổngPhầnCứng 격리, 잘못된 conTrỏ/ELF, CPU ngoạiLệ, 무한 giáTrịLầnLặp giáTrịGiớiHạn', flush=True)
            finally:
                (vịTrí / 'build/ThửSựBảoVệ-last.log').write_bytes(máy.bảnGhiNhậtKý)
                máy.đóng()
    finally:
        chươngTrìnhRa.set()
        giáTrịBộLàmViệc.join(timeout=2)
        giáTrịMáyChủ.close()
    kếtQuả['host_udp_received'] = [{'length': len(DữLiệu), 'sha256': hashlib.sha256(DữLiệu).hexdigest()} for DữLiệu in phầnMụcĐãNhận]
    (vịTrí / 'build/thửMạngNgườiDùng.json').write_text(json.dumps(kếtQuả, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    thựcThiLệnh()
