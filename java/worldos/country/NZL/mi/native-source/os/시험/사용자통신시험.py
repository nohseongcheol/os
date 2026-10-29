#!/usr/bin/env python3
"""tūturu_raraunga ring 3 ELF/taurima UDP 왕복/pare_uara Pōhēhē/TIME_uara 제한/잘못된 ELF를 검증한다."""
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

tūranga = Path(__file__).resolve().parents[1]


class mariko_mīhini:
    def __init__(self, ara, 종류='elf', whatunga_uara=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        whaiaronga_uara = Path(self.임시.name)
        self.LOG_RECORD = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.kaupane_uara = socket.socket(socket.AF_UNIX)
        직렬경로, kaupane_ara = whaiaronga_uara / 'serial.sock', whaiaronga_uara / 'monitor.sock'
        tono = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(kaupane_ara) + ',server,nowait']
        tono += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if whatunga_uara else ['-net', 'none']
        tono += ['-kernel', str(ara)] if 종류 == 'elf' else ['-cdrom', str(ara), '-boot', 'd']
        if 저장매체 is not None:
            tono += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Hātepe_uara = subprocess.Popen(tono, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and kaupane_ara.exists()):
                if self.Hātepe_uara.poll() is not None:
                    raise AssertionError(self.Hātepe_uara.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU whakahaere TIME_uara 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.kaupane_uara.connect(str(kaupane_ara))
            self.직렬.setblocking(False)
            self.kaupane_uara.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.Kati()
            raise

    def 기다림(self, 문구, whakahaere=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_RECORD[whakahaere:]:
                return self.LOG_RECORD[whakahaere:].decode('utf-8', 'replace')
            Pānuitia, _, _ = select.select([self.직렬], [], [], 0.1)
            if Pānuitia:
                raraunga = self.직렬.recv(65536)
                if not raraunga: break
                self.LOG_RECORD.extend(raraunga)
            if self.Hātepe_uara.poll() is not None: break
        raise AssertionError('대기 rahunga_uara: ' + 문구 + '\n' + self.LOG_RECORD.decode('utf-8', 'replace'))

    def tono(self, aho_uara, 기대):
        whakahaere = len(self.LOG_RECORD)
        self.직렬.sendall((aho_uara + '\n').encode())
        mēhua = self.기다림('jkoros> ', whakahaere)
        for 문구 in 기대:
            assert 문구 in mēhua, (aho_uara, 문구, mēhua)
        assert 'PANIC' not in mēhua, mēhua
        return mēhua

    def Kati(self):
        self.직렬.close()
        self.kaupane_uara.close()
        if self.Hātepe_uara.poll() is None:
            self.Hātepe_uara.terminate()
            try: self.Hātepe_uara.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Hātepe_uara.kill()
                self.Hātepe_uara.wait()
        self.Hātepe_uara.communicate()
        self.임시.cleanup()


def 보호커널(whaiaronga_uara):
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
    항목들 = ['hello=' + str(tūranga / 'build/apps/hello.elf')]
    for Ingoa, Ihirangi_uara in 사례들.items():
        pūtake = whaiaronga_uara / (Ingoa + '.s')
        pūtake.write_text('.code32\n.text\n.globl _start\n_start:\n' + Ihirangi_uara +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(whaiaronga_uara / (Ingoa + '.o')), str(pūtake)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(tūranga.parent / 'compiler/kaiwhakamahi_Hono_Tahora.ld'),
                        '-o', str(whaiaronga_uara / (Ingoa + '.elf')), str(whaiaronga_uara / (Ingoa + '.o'))], check=True)
        항목들.append(Ingoa + '=' + str(whaiaronga_uara / (Ingoa + '.elf')))
    정상 = bytearray((tūranga / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    muhu_mēhua = bytearray(정상); muhu_mēhua[0] = 0; 변형들['badelf'] = muhu_mēhua
    muhu_mēhua = bytearray(정상); struct.pack_into('<I', muhu_mēhua, 24, 0x00100000); 변형들['badentry'] = muhu_mēhua
    muhu_mēhua = bytearray(정상); struct.pack_into('<I', muhu_mēhua, 28, 0x7fffffff); 변형들['badtable'] = muhu_mēhua
    muhu_mēhua = bytearray(정상); Rapu_ripanga = struct.unpack_from('<I', muhu_mēhua, 28)[0]
    struct.pack_into('<I', muhu_mēhua, Rapu_ripanga + 20, 0x7fffffff); 변형들['badsize'] = muhu_mēhua
    for Ingoa, raraunga in 변형들.items():
        Kōnae = whaiaronga_uara / (Ingoa + '.elf'); Kōnae.write_bytes(raraunga)
        항목들.append(Ingoa + '=' + str(Kōnae))
    subprocess.run([sys.executable, str(tūranga / 'Ngā_Utauta/묶기.py'), '-o', str(whaiaronga_uara / 'apps.bin')] + 항목들, check=True)
    pūtake = whaiaronga_uara / 'apps.s'
    pūtake.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(whaiaronga_uara / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(whaiaronga_uara / 'apps.o'), str(pūtake)], check=True)
    kākano_uara_0611a8a8 = whaiaronga_uara / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(tūranga / '부팅/Hono_Tahora.ld'), '-o', str(kākano_uara_0611a8a8),
                    str(tūranga / 'build/boot.o'), str(tūranga / 'build/java.o'), str(tūranga / 'build/user.o'), str(whaiaronga_uara / 'apps.o')], check=True)
    return kākano_uara_0611a8a8


def kawe_tono():
    mēhua = {}
    tūmau_uara = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tūmau_uara.bind(('127.0.0.1', 0))
    tūmau_uara.settimeout(0.1)
    kawe_uara = tūmau_uara.getsockname()[1]
    RECEIVED_tuemi = []
    Putaatu_kaupapa = threading.Event()
    def 되보내기():
        while not Putaatu_kaupapa.is_set():
            try: raraunga, hoa_uara = tūmau_uara.recvfrom(4096)
            except socket.timeout: continue
            RECEIVED_tuemi.append(raraunga)
            if raraunga != b'drop-me': tūmau_uara.sendto(raraunga, hoa_uara)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            mīhini = mariko_mīhini(tūranga / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                mīhini.tono('apps', ['hello', 'udp', 'netcheck', 'stress'])
                mīhini.tono('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                mīhini.tono('run missing', ['Exit: -2'])
                mīhini.tono('net', ['NET RTL8139'])
                mīhini.tono('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Ihirangi_uara in ('hello-network', 'odd', 'even', 'repeat-123'):
                    mīhini.tono('run udp 10.0.2.2 {} {}'.format(kawe_uara, Ihirangi_uara), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Ihirangi_uara.encode() in RECEIVED_tuemi, 'taurima 서버에서 자료를 받지 못함'
                mīhini.tono('run stress {}'.format(kawe_uara), ['UDP STRESS PASS', 'Exit: 0'])
                mīhini.tono('run udp 10.0.2.2 {} drop-me'.format(kawe_uara), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                mīhini.tono('run hello recovered', ['arg: recovered', 'Exit: 0'])
                mēhua[종류] = mīhini.LOG_RECORD.decode('utf-8', 'replace')
                print('PASS: {} kaiwhakamahi ELF/ring 3/인수/UDP taurima 왕복/TIME_uara 초과/anga 복귀'.format(종류), flush=True)
            finally:
                try: mīhini.tono('net', [])
                except Exception: pass
                (tūranga / 'build/사용자통신-last.log').write_bytes(mīhini.LOG_RECORD)
                mīhini.Kati()
        mīhini = mariko_mīhini(tūranga / 'build/kernel.elf', whatunga_uara=False)
        try:
            mīhini.tono('net', ['NET unavailable'])
            mīhini.tono('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            mīhini.tono('run hello', ['USER MODE ring 3', 'Exit: 0'])
            mēhua['no_nic'] = mīhini.LOG_RECORD.decode()
        finally: mīhini.Kati()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            mīhini = mariko_mīhini(보호커널(Path(임시)), whatunga_uara=False)
            try:
                for Ingoa, tūnga_uara in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    mīhini.tono('run ' + Ingoa, ['Exit: ' + str(tūnga_uara)])
                    mīhini.tono('run hello', ['USER MODE ring 3', 'Exit: 0'])
                mēhua['protection'] = mīhini.LOG_RECORD.decode()
                print('PASS: kaiwhakamahi Pūmahara_raraunga/포트 격리, 잘못된 atatohu/ELF, CPU 예외, 무한 whitiauau_uara 제한', flush=True)
            finally:
                (tūranga / 'build/보호시험-last.log').write_bytes(mīhini.LOG_RECORD)
                mīhini.Kati()
    finally:
        Putaatu_kaupapa.set()
        일꾼.join(timeout=2)
        tūmau_uara.close()
    mēhua['host_udp_received'] = [{'length': len(raraunga), 'sha256': hashlib.sha256(raraunga).hexdigest()} for raraunga in RECEIVED_tuemi]
    (tūranga / 'build/사용자통신시험.json').write_text(json.dumps(mēhua, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    kawe_tono()
