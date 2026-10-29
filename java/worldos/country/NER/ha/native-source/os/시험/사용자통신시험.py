#!/usr/bin/env python3
"""Na_hakika_Tarin_bayani ring 3 ELF/sauka UDP 왕복/Kare_Daraja Kuskure/lokaci_Daraja 제한/잘못된 ELF를 검증한다."""
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

위치 = Path(__file__).resolve().parents[1]


class Mai_alaka_da_aikin_na_ura_na_boye_na_ura_mai_kwakwalwa:
    def __init__(self, Hanyar_shiga, 종류='elf', Hanyar_sadarwa_Daraja=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        ma_ajiya_Daraja = Path(self.임시.name)
        self.logu_naɗa = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.Allon_kwamfuta_Daraja = socket.socket(socket.AF_UNIX)
        직렬경로, Allon_kwamfuta_Hanyar_shiga = ma_ajiya_Daraja / 'serial.sock', ma_ajiya_Daraja / 'monitor.sock'
        Umarni = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(Allon_kwamfuta_Hanyar_shiga) + ',server,nowait']
        Umarni += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Hanyar_sadarwa_Daraja else ['-net', 'none']
        Umarni += ['-kernel', str(Hanyar_shiga)] if 종류 == 'elf' else ['-cdrom', str(Hanyar_shiga), '-boot', 'd']
        if 저장매체 is not None:
            Umarni += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.haryar_aikin_na_ura_Daraja = subprocess.Popen(Umarni, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and Allon_kwamfuta_Hanyar_shiga.exists()):
                if self.haryar_aikin_na_ura_Daraja.poll() is not None:
                    raise AssertionError(self.haryar_aikin_na_ura_Daraja.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Tafiyar_da lokaci_Daraja 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.Allon_kwamfuta_Daraja.connect(str(Allon_kwamfuta_Hanyar_shiga))
            self.직렬.setblocking(False)
            self.Allon_kwamfuta_Daraja.sendall(b'cont\n')
            self.jira_Matsayi('jkoros> ')
        except BaseException:
            self.Rufe()
            raise

    def jira_Matsayi(self, 문구, Tafiyar_da=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.logu_naɗa[Tafiyar_da:]:
                return self.logu_naɗa[Tafiyar_da:].decode('utf-8', 'replace')
            Yi_Karatu, _, _ = select.select([self.직렬], [], [], 0.1)
            if Yi_Karatu:
                Tarin_bayani = self.직렬.recv(65536)
                if not Tarin_bayani: break
                self.logu_naɗa.extend(Tarin_bayani)
            if self.haryar_aikin_na_ura_Daraja.poll() is not None: break
        raise AssertionError('jira_Daraja Kasa_aiki_Daraja: ' + 문구 + '\n' + self.logu_naɗa.decode('utf-8', 'replace'))

    def Umarni(self, Zare_Daraja, 기대):
        Tafiyar_da = len(self.logu_naɗa)
        self.직렬.sendall((Zare_Daraja + '\n').encode())
        결과 = self.jira_Matsayi('jkoros> ', Tafiyar_da)
        for 문구 in 기대:
            assert 문구 in 결과, (Zare_Daraja, 문구, 결과)
        assert 'PANIC' not in 결과, 결과
        return 결과

    def Rufe(self):
        self.직렬.close()
        self.Allon_kwamfuta_Daraja.close()
        if self.haryar_aikin_na_ura_Daraja.poll() is None:
            self.haryar_aikin_na_ura_Daraja.terminate()
            try: self.haryar_aikin_na_ura_Daraja.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.haryar_aikin_na_ura_Daraja.kill()
                self.haryar_aikin_na_ura_Daraja.wait()
        self.haryar_aikin_na_ura_Daraja.communicate()
        self.임시.cleanup()


def 보호커널(ma_ajiya_Daraja):
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
    항목들 = ['hello=' + str(위치 / 'build/apps/hello.elf')]
    for Suna, kunshiya_Daraja in 사례들.items():
        tushe = ma_ajiya_Daraja / (Suna + '.s')
        tushe.write_text('.code32\n.text\n.globl _start\n_start:\n' + kunshiya_Daraja +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(ma_ajiya_Daraja / (Suna + '.o')), str(tushe)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치.parent / 'compiler/Mai_anfani_da_kwamfuta_Kafa_Zagaye.ld'),
                        '-o', str(ma_ajiya_Daraja / (Suna + '.elf')), str(ma_ajiya_Daraja / (Suna + '.o'))], check=True)
        항목들.append(Suna + '=' + str(ma_ajiya_Daraja / (Suna + '.elf')))
    정상 = bytearray((위치 / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    잘못 = bytearray(정상); 잘못[0] = 0; 변형들['badelf'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 24, 0x00100000); 변형들['badentry'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 28, 0x7fffffff); 변형들['badtable'] = 잘못
    잘못 = bytearray(정상); 표 = struct.unpack_from('<I', 잘못, 28)[0]
    struct.pack_into('<I', 잘못, 표 + 20, 0x7fffffff); 변형들['badsize'] = 잘못
    for Suna, Tarin_bayani in 변형들.items():
        Fayil = ma_ajiya_Daraja / (Suna + '.elf'); Fayil.write_bytes(Tarin_bayani)
        항목들.append(Suna + '=' + str(Fayil))
    subprocess.run([sys.executable, str(위치 / 'Kaya/묶기.py'), '-o', str(ma_ajiya_Daraja / 'apps.bin')] + 항목들, check=True)
    tushe = ma_ajiya_Daraja / 'apps.s'
    tushe.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(ma_ajiya_Daraja / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(ma_ajiya_Daraja / 'apps.o'), str(tushe)], check=True)
    Kwara_Daraja = ma_ajiya_Daraja / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/Kafa_Zagaye.ld'), '-o', str(Kwara_Daraja),
                    str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(위치 / 'build/user.o'), str(ma_ajiya_Daraja / 'apps.o')], check=True)
    return Kwara_Daraja


def gudanar_Umarni():
    결과 = {}
    Saba_Daraja = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    Saba_Daraja.bind(('127.0.0.1', 0))
    Saba_Daraja.settimeout(0.1)
    fot_Daraja = Saba_Daraja.getsockname()[1]
    받은것 = []
    Mafita_Shiri = threading.Event()
    def 되보내기():
        while not Mafita_Shiri.is_set():
            try: Tarin_bayani, Fiya_Daraja = Saba_Daraja.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(Tarin_bayani)
            if Tarin_bayani != b'drop-me': Saba_Daraja.sendto(Tarin_bayani, Fiya_Daraja)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            na_ura_mai_kwakwalwa = Mai_alaka_da_aikin_na_ura_na_boye_na_ura_mai_kwakwalwa(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                na_ura_mai_kwakwalwa.Umarni('apps', ['hello', 'udp', 'netcheck', 'stress'])
                na_ura_mai_kwakwalwa.Umarni('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                na_ura_mai_kwakwalwa.Umarni('run missing', ['Exit: -2'])
                na_ura_mai_kwakwalwa.Umarni('net', ['NET RTL8139'])
                na_ura_mai_kwakwalwa.Umarni('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for kunshiya_Daraja in ('hello-network', 'odd', 'even', 'repeat-123'):
                    na_ura_mai_kwakwalwa.Umarni('run udp 10.0.2.2 {} {}'.format(fot_Daraja, kunshiya_Daraja), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert kunshiya_Daraja.encode() in 받은것, 'sauka 서버에서 자료를 받지 못함'
                na_ura_mai_kwakwalwa.Umarni('run stress {}'.format(fot_Daraja), ['UDP STRESS PASS', 'Exit: 0'])
                na_ura_mai_kwakwalwa.Umarni('run udp 10.0.2.2 {} drop-me'.format(fot_Daraja), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                na_ura_mai_kwakwalwa.Umarni('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = na_ura_mai_kwakwalwa.logu_naɗa.decode('utf-8', 'replace')
                print('PASS: {} Mai_anfani_da_kwamfuta ELF/ring 3/인수/UDP sauka 왕복/lokaci_Daraja 초과/Mai_fayyace_umani 복귀'.format(종류), flush=True)
            finally:
                try: na_ura_mai_kwakwalwa.Umarni('net', [])
                except Exception: pass
                (위치 / 'build/사용자통신-last.log').write_bytes(na_ura_mai_kwakwalwa.logu_naɗa)
                na_ura_mai_kwakwalwa.Rufe()
        na_ura_mai_kwakwalwa = Mai_alaka_da_aikin_na_ura_na_boye_na_ura_mai_kwakwalwa(위치 / 'build/kernel.elf', Hanyar_sadarwa_Daraja=False)
        try:
            na_ura_mai_kwakwalwa.Umarni('net', ['NET unavailable'])
            na_ura_mai_kwakwalwa.Umarni('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            na_ura_mai_kwakwalwa.Umarni('run hello', ['USER MODE ring 3', 'Exit: 0'])
            결과['no_nic'] = na_ura_mai_kwakwalwa.logu_naɗa.decode()
        finally: na_ura_mai_kwakwalwa.Rufe()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            na_ura_mai_kwakwalwa = Mai_alaka_da_aikin_na_ura_na_boye_na_ura_mai_kwakwalwa(보호커널(Path(임시)), Hanyar_sadarwa_Daraja=False)
            try:
                for Suna, Matsayi_Daraja in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    na_ura_mai_kwakwalwa.Umarni('run ' + Suna, ['Exit: ' + str(Matsayi_Daraja)])
                    na_ura_mai_kwakwalwa.Umarni('run hello', ['USER MODE ring 3', 'Exit: 0'])
                결과['protection'] = na_ura_mai_kwakwalwa.logu_naɗa.decode()
                print('PASS: Mai_anfani_da_kwamfuta Mahardatar_kwamfuta_Tarin_bayani/kayan_haɗi_na_kwamfuta_fot 격리, 잘못된 manuni/ELF, CPU banbanchi, 무한 sifirint_Daraja 제한', flush=True)
            finally:
                (위치 / 'build/보호시험-last.log').write_bytes(na_ura_mai_kwakwalwa.logu_naɗa)
                na_ura_mai_kwakwalwa.Rufe()
    finally:
        Mafita_Shiri.set()
        일꾼.join(timeout=2)
        Saba_Daraja.close()
    결과['host_udp_received'] = [{'length': len(Tarin_bayani), 'sha256': hashlib.sha256(Tarin_bayani).hexdigest()} for Tarin_bayani in 받은것]
    (위치 / 'build/사용자통신시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    gudanar_Umarni()
