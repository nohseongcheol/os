#!/usr/bin/env python3
"""fiili_veri ring 3 ELF/konak UDP 왕복/korumak_değer hata/zaman_değeri 제한/잘못된 ELF를 검증한다."""
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

konum = Path(__file__).resolve().parents[1]


class VM:
    def __init__(self, yol, Tip_değer='elf', ağ_değer=True, Depolama_Orta=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        dizin_değer = Path(self.임시.name)
        self.LOG_KAYIT = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.izlemek_değer = socket.socket(socket.AF_UNIX)
        직렬경로, izlemek_yol = dizin_değer / 'serial.sock', dizin_değer / 'monitor.sock'
        komut = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(izlemek_yol) + ',server,nowait']
        komut += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if ağ_değer else ['-net', 'none']
        komut += ['-kernel', str(yol)] if Tip_değer == 'elf' else ['-cdrom', str(yol), '-boot', 'd']
        if Depolama_Orta is not None:
            komut += ['-drive', 'file=' + str(Depolama_Orta) + ',format=raw,if=ide,index=0']
        self.işlem_değer = subprocess.Popen(komut, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and izlemek_yol.exists()):
                if self.işlem_değer.poll() is not None:
                    raise AssertionError(self.işlem_değer.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU çalıştır zaman_değeri 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.izlemek_değer.connect(str(izlemek_yol))
            self.직렬.setblocking(False)
            self.izlemek_değer.sendall(b'cont\n')
            self.bekleme_durumu('jkoros> ')
        except BaseException:
            self.Kapat()
            raise

    def bekleme_durumu(self, 문구, çalıştır=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_KAYIT[çalıştır:]:
                return self.LOG_KAYIT[çalıştır:].decode('utf-8', 'replace')
            Okuma, _, _ = select.select([self.직렬], [], [], 0.1)
            if Okuma:
                veri = self.직렬.recv(65536)
                if not veri: break
                self.LOG_KAYIT.extend(veri)
            if self.işlem_değer.poll() is not None: break
        raise AssertionError('bekle_değer hata_değer: ' + 문구 + '\n' + self.LOG_KAYIT.decode('utf-8', 'replace'))

    def komut(self, dize_değer, 기대):
        çalıştır = len(self.LOG_KAYIT)
        self.직렬.sendall((dize_değer + '\n').encode())
        sonuç = self.bekleme_durumu('jkoros> ', çalıştır)
        for 문구 in 기대:
            assert 문구 in sonuç, (dize_değer, 문구, sonuç)
        assert 'PANIC' not in sonuç, sonuç
        return sonuç

    def Kapat(self):
        self.직렬.close()
        self.izlemek_değer.close()
        if self.işlem_değer.poll() is None:
            self.işlem_değer.terminate()
            try: self.işlem_değer.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.işlem_değer.kill()
                self.işlem_değer.wait()
        self.işlem_değer.communicate()
        self.임시.cleanup()


def 보호커널(dizin_değer):
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
    항목들 = ['hello=' + str(konum / 'build/apps/hello.elf')]
    for İsim, içerik_değer in 사례들.items():
        kaynakKod = dizin_değer / (İsim + '.s')
        kaynakKod.write_text('.code32\n.text\n.globl _start\n_start:\n' + içerik_değer +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(dizin_değer / (İsim + '.o')), str(kaynakKod)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(konum.parent / 'compiler/kullanıcı_köprü_Düzen.ld'),
                        '-o', str(dizin_değer / (İsim + '.elf')), str(dizin_değer / (İsim + '.o'))], check=True)
        항목들.append(İsim + '=' + str(dizin_değer / (İsim + '.elf')))
    bilgi_teknolojisi_normal = bytearray((konum / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    geçersiz_KR = bytearray(bilgi_teknolojisi_normal); geçersiz_KR[0] = 0; 변형들['badelf'] = geçersiz_KR
    geçersiz_KR = bytearray(bilgi_teknolojisi_normal); struct.pack_into('<I', geçersiz_KR, 24, 0x00100000); 변형들['badentry'] = geçersiz_KR
    geçersiz_KR = bytearray(bilgi_teknolojisi_normal); struct.pack_into('<I', geçersiz_KR, 28, 0x7fffffff); 변형들['badtable'] = geçersiz_KR
    geçersiz_KR = bytearray(bilgi_teknolojisi_normal); arama_tablosu = struct.unpack_from('<I', geçersiz_KR, 28)[0]
    struct.pack_into('<I', geçersiz_KR, arama_tablosu + 20, 0x7fffffff); 변형들['badsize'] = geçersiz_KR
    for İsim, veri in 변형들.items():
        dosya = dizin_değer / (İsim + '.elf'); dosya.write_bytes(veri)
        항목들.append(İsim + '=' + str(dosya))
    subprocess.run([sys.executable, str(konum / 'araçlar/BIND_uç_nokta.py'), '-o', str(dizin_değer / 'apps.bin')] + 항목들, check=True)
    kaynakKod = dizin_değer / 'apps.s'
    kaynakKod.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(dizin_değer / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(dizin_değer / 'apps.o'), str(kaynakKod)], check=True)
    çekirdek_değer = dizin_değer / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(konum / 'makine_başlatma/bağlama_düzeni.ld'), '-o', str(çekirdek_değer),
                    str(konum / 'build/boot.o'), str(konum / 'build/java.o'), str(konum / 'build/user.o'), str(dizin_değer / 'apps.o')], check=True)
    return çekirdek_değer


def yürütmek_komut():
    sonuç = {}
    sunucu_değer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sunucu_değer.bind(('127.0.0.1', 0))
    sunucu_değer.settimeout(0.1)
    taşımak_değer = sunucu_değer.getsockname()[1]
    GETİRİ_öğe = []
    Çıkış_program = threading.Event()
    def yankı_yanıt():
        while not Çıkış_program.is_set():
            try: veri, eş_değer = sunucu_değer.recvfrom(4096)
            except socket.timeout: continue
            GETİRİ_öğe.append(veri)
            if veri != b'drop-me': sunucu_değer.sendto(veri, eş_değer)
    çalışan_değer = threading.Thread(target=yankı_yanıt, daemon=True)
    çalışan_değer.start()
    try:
        for Tip_değer in ('elf', 'iso'):
            makine = VM(konum / ('build/kernel.elf' if Tip_değer == 'elf' else 'build/kernel.iso'), Tip_değer)
            try:
                makine.komut('apps', ['hello', 'udp', 'netcheck', 'stress'])
                makine.komut('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                makine.komut('run missing', ['Exit: -2'])
                makine.komut('net', ['NET RTL8139'])
                makine.komut('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for içerik_değer in ('hello-network', 'odd', 'even', 'repeat-123'):
                    makine.komut('run udp 10.0.2.2 {} {}'.format(taşımak_değer, içerik_değer), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert içerik_değer.encode() in GETİRİ_öğe, 'konak 서버에서 자료를 받지 못함'
                makine.komut('run stress {}'.format(taşımak_değer), ['UDP STRESS PASS', 'Exit: 0'])
                makine.komut('run udp 10.0.2.2 {} drop-me'.format(taşımak_değer), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                makine.komut('run hello recovered', ['arg: recovered', 'Exit: 0'])
                sonuç[Tip_değer] = makine.LOG_KAYIT.decode('utf-8', 'replace')
                print('PASS: {} kullanıcı_alanı ELF/ring 3/bağımsız_değişkenler/UDP konak 왕복/zaman_değeri 초과/kabuk 복귀'.format(Tip_değer), flush=True)
            finally:
                try: makine.komut('net', [])
                except Exception: pass
                (konum / 'build/사용자통신-last.log').write_bytes(makine.LOG_KAYIT)
                makine.Kapat()
        makine = VM(konum / 'build/kernel.elf', ağ_değer=False)
        try:
            makine.komut('net', ['NET unavailable'])
            makine.komut('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            makine.komut('run hello', ['USER MODE ring 3', 'Exit: 0'])
            sonuç['no_nic'] = makine.LOG_KAYIT.decode()
        finally: makine.Kapat()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            makine = VM(보호커널(Path(임시)), ağ_değer=False)
            try:
                for İsim, Durum_değer in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    makine.komut('run ' + İsim, ['Exit: ' + str(Durum_değer)])
                    makine.komut('run hello', ['USER MODE ring 3', 'Exit: 0'])
                sonuç['protection'] = makine.LOG_KAYIT.decode()
                print('PASS: kullanıcı_alanı Bellek_veri/donanım_taşımak 격리, 잘못된 işaretçi/ELF, CPU özel_durum, 무한 öğe_değer_58902391 제한', flush=True)
            finally:
                (konum / 'build/Koruma_test-last.log').write_bytes(makine.LOG_KAYIT)
                makine.Kapat()
    finally:
        Çıkış_program.set()
        çalışan_değer.join(timeout=2)
        sunucu_değer.close()
    sonuç['host_udp_received'] = [{'length': len(veri), 'sha256': hashlib.sha256(veri).hexdigest()} for veri in GETİRİ_öğe]
    (konum / 'build/test_kullanıcı_ağ.json').write_text(json.dumps(sonuç, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    yürütmek_komut()
