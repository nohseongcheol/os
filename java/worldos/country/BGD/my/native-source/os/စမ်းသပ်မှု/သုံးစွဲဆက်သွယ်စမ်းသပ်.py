#!/usr/bin/env python3
"""တကယ့်ဒေတာ ring 3 ELF/အိမ်ရှင် UDP 왕복/တန်ဖိုးကာကွယ် အမှား/အချိန်တန်ဖိုး ကန့်သတ်ချက်တန်ဖိုး/잘못된 ELF를 검증한다."""
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

နေရာ = Path(__file__).resolve().parents[1]


class စက်တု:
    def __init__(self, လမ်း, အမျိုးအစားတန်ဖိုး='elf', ကွန်ရက်တန်ဖိုး=True, 저장매체=None):
        self.ယာယီတန်ဖိုး = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        ဖိုင်တွဲတန်ဖိုး = Path(self.ယာယီတန်ဖိုး.name)
        self.မှတ်တမ်းမှတ်တမ်းတစ်ခု = bytearray()
        self.အစဉ်ဆက်တန်ဖိုး = socket.socket(socket.AF_UNIX)
        self.ကြီးကြပ်သူတန်ဖိုး = socket.socket(socket.AF_UNIX)
        အစဉ်ဆက်လမ်းကြောင်း, ကြီးကြပ်သူလမ်းကြောင်း = ဖိုင်တွဲတန်ဖိုး / 'serial.sock', ဖိုင်တွဲတန်ဖိုး / 'monitor.sock'
        အမိန့် = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(အစဉ်ဆက်လမ်းကြောင်း) + ',server,nowait',
                '-monitor', 'unix:' + str(ကြီးကြပ်သူလမ်းကြောင်း) + ',server,nowait']
        အမိန့် += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if ကွန်ရက်တန်ဖိုး else ['-net', 'none']
        အမိန့် += ['-kernel', str(လမ်း)] if အမျိုးအစားတန်ဖိုး == 'elf' else ['-cdrom', str(လမ်း), '-boot', 'd']
        if 저장매체 is not None:
            အမိန့် += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.လုပ်ငန်းစဉ် = subprocess.Popen(အမိန့်, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            အဆုံး = time.monotonic() + 10
            while not (အစဉ်ဆက်လမ်းကြောင်း.exists() and ကြီးကြပ်သူလမ်းကြောင်း.exists()):
                if self.လုပ်ငန်းစဉ်.poll() is not None:
                    raise AssertionError(self.လုပ်ငန်းစဉ်.stderr.read().decode())
                if time.monotonic() > အဆုံး: raise AssertionError('QEMU လုပ်ဆောင် အချိန်တန်ဖိုး 초과')
                time.sleep(0.03)
            self.အစဉ်ဆက်တန်ဖိုး.connect(str(အစဉ်ဆက်လမ်းကြောင်း))
            self.ကြီးကြပ်သူတန်ဖိုး.connect(str(ကြီးကြပ်သူလမ်းကြောင်း))
            self.အစဉ်ဆက်တန်ဖိုး.setblocking(False)
            self.ကြီးကြပ်သူတန်ဖိုး.sendall(b'cont\n')
            self.အခြေအနေစောင့်('jkoros> ')
        except BaseException:
            self.ပိတ်()
            raise

    def အခြေအနေစောင့်(self, စကားစု, လုပ်ဆောင်=0, ကန့်သတ်ချက်တန်ဖိုး=15):
        အဆုံး = time.monotonic() + ကန့်သတ်ချက်တန်ဖိုး
        while time.monotonic() < အဆုံး:
            if စကားစု.encode() in self.မှတ်တမ်းမှတ်တမ်းတစ်ခု[လုပ်ဆောင်:]:
                return self.မှတ်တမ်းမှတ်တမ်းတစ်ခု[လုပ်ဆောင်:].decode('utf-8', 'replace')
            ဖတ်, _, _ = select.select([self.အစဉ်ဆက်တန်ဖိုး], [], [], 0.1)
            if ဖတ်:
                ဒေတာ = self.အစဉ်ဆက်တန်ဖိုး.recv(65536)
                if not ဒေတာ: break
                self.မှတ်တမ်းမှတ်တမ်းတစ်ခု.extend(ဒေတာ)
            if self.လုပ်ငန်းစဉ်.poll() is not None: break
        raise AssertionError('တန်ဖိုးစောင့် မအောင်မြင်မှု: ' + စကားစု + '\n' + self.မှတ်တမ်းမှတ်တမ်းတစ်ခု.decode('utf-8', 'replace'))

    def အမိန့်(self, အက္ခရာစဉ်, မျှော်လင့်ချက်):
        လုပ်ဆောင် = len(self.မှတ်တမ်းမှတ်တမ်းတစ်ခု)
        self.အစဉ်ဆက်တန်ဖိုး.sendall((အက္ခရာစဉ် + '\n').encode())
        ရလဒ် = self.အခြေအနေစောင့်('jkoros> ', လုပ်ဆောင်)
        for စကားစု in မျှော်လင့်ချက်:
            assert စကားစု in ရလဒ်, (အက္ခရာစဉ်, စကားစု, ရလဒ်)
        assert 'PANIC' not in ရလဒ်, ရလဒ်
        return ရလဒ်

    def ပိတ်(self):
        self.အစဉ်ဆက်တန်ဖိုး.close()
        self.ကြီးကြပ်သူတန်ဖိုး.close()
        if self.လုပ်ငန်းစဉ်.poll() is None:
            self.လုပ်ငန်းစဉ်.terminate()
            try: self.လုပ်ငန်းစဉ်.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.လုပ်ငန်းစဉ်.kill()
                self.လုပ်ငန်းစဉ်.wait()
        self.လုပ်ငန်းစဉ်.communicate()
        self.ယာယီတန်ဖိုး.cleanup()


def 보호커널(ဖိုင်တွဲတန်ဖိုး):
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
    항목들 = ['hello=' + str(နေရာ / 'build/apps/hello.elf')]
    for အမည်, အကြောင်းအရာတန်ဖိုး in 사례들.items():
        မူရင်းကုဒ် = ဖိုင်တွဲတန်ဖိုး / (အမည် + '.s')
        မူရင်းကုဒ်.write_text('.code32\n.text\n.globl _start\n_start:\n' + အကြောင်းအရာတန်ဖိုး +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(ဖိုင်တွဲတန်ဖိုး / (အမည် + '.o')), str(မူရင်းကုဒ်)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(နေရာ.parent / 'compiler/သုံးစွဲသူချိတ်နေရာချပုံ.ld'),
                        '-o', str(ဖိုင်တွဲတန်ဖိုး / (အမည် + '.elf')), str(ဖိုင်တွဲတန်ဖိုး / (အမည် + '.o'))], check=True)
        항목들.append(အမည် + '=' + str(ဖိုင်တွဲတန်ဖိုး / (အမည် + '.elf')))
    ဖြစ်သောပုံမှန် = bytearray((နေရာ / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    မမှန်ကန်ရလဒ် = bytearray(ဖြစ်သောပုံမှန်); မမှန်ကန်ရလဒ်[0] = 0; 변형들['badelf'] = မမှန်ကန်ရလဒ်
    မမှန်ကန်ရလဒ် = bytearray(ဖြစ်သောပုံမှန်); struct.pack_into('<I', မမှန်ကန်ရလဒ်, 24, 0x00100000); 변형들['badentry'] = မမှန်ကန်ရလဒ်
    မမှန်ကန်ရလဒ် = bytearray(ဖြစ်သောပုံမှန်); struct.pack_into('<I', မမှန်ကန်ရလဒ်, 28, 0x7fffffff); 변형들['badtable'] = မမှန်ကန်ရလဒ်
    မမှန်ကန်ရလဒ် = bytearray(ဖြစ်သောပုံမှန်); ဇယား = struct.unpack_from('<I', မမှန်ကန်ရလဒ်, 28)[0]
    struct.pack_into('<I', မမှန်ကန်ရလဒ်, ဇယား + 20, 0x7fffffff); 변형들['badsize'] = မမှန်ကန်ရလဒ်
    for အမည်, ဒေတာ in 변형들.items():
        ဖိုင် = ဖိုင်တွဲတန်ဖိုး / (အမည် + '.elf'); ဖိုင်.write_bytes(ဒေတာ)
        항목들.append(အမည် + '=' + str(ဖိုင်))
    subprocess.run([sys.executable, str(နေရာ / 'ကိရိယာစု/စက်ဖိုင်ထုပ်ပိုး.py'), '-o', str(ဖိုင်တွဲတန်ဖိုး / 'apps.bin')] + 항목들, check=True)
    မူရင်းကုဒ် = ဖိုင်တွဲတန်ဖိုး / 'apps.s'
    မူရင်းကုဒ်.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(ဖိုင်တွဲတန်ဖိုး / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(ဖိုင်တွဲတန်ဖိုး / 'apps.o'), str(မူရင်းကုဒ်)], check=True)
    အူတိုင်တန်ဖိုး = ဖိုင်တွဲတန်ဖိုး / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(နေရာ / 'စက်တင်/နေရာချထားပုံ.ld'), '-o', str(အူတိုင်တန်ဖိုး),
                    str(နေရာ / 'build/boot.o'), str(နေရာ / 'build/java.o'), str(နေရာ / 'build/user.o'), str(ဖိုင်တွဲတန်ဖိုး / 'apps.o')], check=True)
    return အူတိုင်တန်ဖိုး


def စက်မောင်း():
    ရလဒ် = {}
    ဝန်ဆောင်စက်တန်ဖိုး = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ဝန်ဆောင်စက်တန်ဖိုး.bind(('127.0.0.1', 0))
    ဝန်ဆောင်စက်တန်ဖိုး.settimeout(0.1)
    ဆက်သွယ်ပေါက်တန်ဖိုး = ဝန်ဆောင်စက်တန်ဖိုး.getsockname()[1]
    ရရှိအချက် = []
    ထွက်ပရိုဂရမ် = threading.Event()
    def 되보내기():
        while not ထွက်ပရိုဂရမ်.is_set():
            try: ဒေတာ, တစ်ဖက်တန်ဖိုး = ဝန်ဆောင်စက်တန်ဖိုး.recvfrom(4096)
            except socket.timeout: continue
            ရရှိအချက်.append(ဒေတာ)
            if ဒေတာ != b'drop-me': ဝန်ဆောင်စက်တန်ဖိုး.sendto(ဒေတာ, တစ်ဖက်တန်ဖိုး)
    အလုပ်သမားတန်ဖိုး = threading.Thread(target=되보내기, daemon=True)
    အလုပ်သမားတန်ဖိုး.start()
    try:
        for အမျိုးအစားတန်ဖိုး in ('elf', 'iso'):
            စက် = စက်တု(နေရာ / ('build/kernel.elf' if အမျိုးအစားတန်ဖိုး == 'elf' else 'build/kernel.iso'), အမျိုးအစားတန်ဖိုး)
            try:
                စက်.အမိန့်('apps', ['hello', 'udp', 'netcheck', 'stress'])
                စက်.အမိန့်('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                စက်.အမိန့်('run missing', ['Exit: -2'])
                စက်.အမိန့်('net', ['NET RTL8139'])
                စက်.အမိန့်('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for အကြောင်းအရာတန်ဖိုး in ('hello-network', 'odd', 'even', 'repeat-123'):
                    စက်.အမိန့်('run udp 10.0.2.2 {} {}'.format(ဆက်သွယ်ပေါက်တန်ဖိုး, အကြောင်းအရာတန်ဖိုး), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert အကြောင်းအရာတန်ဖိုး.encode() in ရရှိအချက်, 'အိမ်ရှင် 서버에서 자료를 받지 못함'
                စက်.အမိန့်('run stress {}'.format(ဆက်သွယ်ပေါက်တန်ဖိုး), ['UDP STRESS PASS', 'Exit: 0'])
                စက်.အမိန့်('run udp 10.0.2.2 {} drop-me'.format(ဆက်သွယ်ပေါက်တန်ဖိုး), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                စက်.အမိန့်('run hello recovered', ['arg: recovered', 'Exit: 0'])
                ရလဒ်[အမျိုးအစားတန်ဖိုး] = စက်.မှတ်တမ်းမှတ်တမ်းတစ်ခု.decode('utf-8', 'replace')
                print('PASS: {} သုံးစွဲသူ ELF/ring 3/အချက်များ/UDP အိမ်ရှင် 왕복/အချိန်တန်ဖိုး 초과/အမိန့်ဝင်း 복귀'.format(အမျိုးအစားတန်ဖိုး), flush=True)
            finally:
                try: စက်.အမိန့်('net', [])
                except Exception: pass
                (နေရာ / 'build/사용자통신-last.log').write_bytes(စက်.မှတ်တမ်းမှတ်တမ်းတစ်ခု)
                စက်.ပိတ်()
        စက် = စက်တု(နေရာ / 'build/kernel.elf', ကွန်ရက်တန်ဖိုး=False)
        try:
            စက်.အမိန့်('net', ['NET unavailable'])
            စက်.အမိန့်('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            စက်.အမိန့်('run hello', ['USER MODE ring 3', 'Exit: 0'])
            ရလဒ်['no_nic'] = စက်.မှတ်တမ်းမှတ်တမ်းတစ်ခု.decode()
        finally: စက်.ပိတ်()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as ယာယီတန်ဖိုး:
            စက် = စက်တု(보호커널(Path(ယာယီတန်ဖိုး)), ကွန်ရက်တန်ဖိုး=False)
            try:
                for အမည်, အခြေအနေတန်ဖိုး in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    စက်.အမိန့်('run ' + အမည်, ['Exit: ' + str(အခြေအနေတန်ဖိုး)])
                    စက်.အမိန့်('run hello', ['USER MODE ring 3', 'Exit: 0'])
                ရလဒ်['protection'] = စက်.မှတ်တမ်းမှတ်တမ်းတစ်ခု.decode()
                print('PASS: သုံးစွဲသူ မှတ်ဉာဏ်ဒေတာ/စက်ပစ္စည်းဆက်သွယ်ပေါက် 격리, 잘못된 ညွှန်တံ/ELF, CPU ခြွင်းချက်, 무한 반복 ကန့်သတ်ချက်တန်ဖိုး', flush=True)
            finally:
                (နေရာ / 'build/ကာကွယ်မှုစမ်းသပ်-last.log').write_bytes(စက်.မှတ်တမ်းမှတ်တမ်းတစ်ခု)
                စက်.ပိတ်()
    finally:
        ထွက်ပရိုဂရမ်.set()
        အလုပ်သမားတန်ဖိုး.join(timeout=2)
        ဝန်ဆောင်စက်တန်ဖိုး.close()
    ရလဒ်['host_udp_received'] = [{'length': len(ဒေတာ), 'sha256': hashlib.sha256(ဒေတာ).hexdigest()} for ဒေတာ in ရရှိအချက်]
    (နေရာ / 'build/သုံးစွဲဆက်သွယ်စမ်းသပ်.json').write_text(json.dumps(ရလဒ်, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    စက်မောင်း()
