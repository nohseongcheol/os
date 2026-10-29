#!/usr/bin/env python3
"""בפועל_נתונים ring 3 ELF/ארח UDP 왕복/הגן_ערך שגיאה/ערך_זמן 제한/잘못된 ELF를 검증한다."""
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

מיקום = Path(__file__).resolve().parents[1]


class מחשב_וירטואלי:
    def __init__(self, נתיב, 종류='elf', רשת_ערך=True, אחסון_אמצעי=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        מדריך_ערך = Path(self.임시.name)
        self.לרשום_שיא = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.צג_ערך = socket.socket(socket.AF_UNIX)
        직렬경로, צג_נתיב = מדריך_ערך / 'serial.sock', מדריך_ערך / 'monitor.sock'
        פקודה = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(צג_נתיב) + ',server,nowait']
        פקודה += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if רשת_ערך else ['-net', 'none']
        פקודה += ['-kernel', str(נתיב)] if 종류 == 'elf' else ['-cdrom', str(נתיב), '-boot', 'd']
        if אחסון_אמצעי is not None:
            פקודה += ['-drive', 'file=' + str(אחסון_אמצעי) + ',format=raw,if=ide,index=0']
        self.תהליך_ערך = subprocess.Popen(פקודה, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and צג_נתיב.exists()):
                if self.תהליך_ערך.poll() is not None:
                    raise AssertionError(self.תהליך_ערך.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU הפעלה ערך_זמן 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.צג_ערך.connect(str(צג_נתיב))
            self.직렬.setblocking(False)
            self.צג_ערך.sendall(b'cont\n')
            self.מצב_המתנה('jkoros> ')
        except BaseException:
            self.סגירה()
            raise

    def מצב_המתנה(self, 문구, הפעלה=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.לרשום_שיא[הפעלה:]:
                return self.לרשום_שיא[הפעלה:].decode('utf-8', 'replace')
            קרא, _, _ = select.select([self.직렬], [], [], 0.1)
            if קרא:
                נתונים = self.직렬.recv(65536)
                if not נתונים: break
                self.לרשום_שיא.extend(נתונים)
            if self.תהליך_ערך.poll() is not None: break
        raise AssertionError('רק_רגע_ערך כשל_ערך: ' + 문구 + '\n' + self.לרשום_שיא.decode('utf-8', 'replace'))

    def פקודה(self, מחרוזת_ערך, 기대):
        הפעלה = len(self.לרשום_שיא)
        self.직렬.sendall((מחרוזת_ערך + '\n').encode())
        תוצאה = self.מצב_המתנה('jkoros> ', הפעלה)
        for 문구 in 기대:
            assert 문구 in תוצאה, (מחרוזת_ערך, 문구, תוצאה)
        assert 'PANIC' not in תוצאה, תוצאה
        return תוצאה

    def סגירה(self):
        self.직렬.close()
        self.צג_ערך.close()
        if self.תהליך_ערך.poll() is None:
            self.תהליך_ערך.terminate()
            try: self.תהליך_ערך.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.תהליך_ערך.kill()
                self.תהליך_ערך.wait()
        self.תהליך_ערך.communicate()
        self.임시.cleanup()


def 보호커널(מדריך_ערך):
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
    항목들 = ['hello=' + str(מיקום / 'build/apps/hello.elf')]
    for שם, תוכן_ערך in 사례들.items():
        קודמקור = מדריך_ערך / (שם + '.s')
        קודמקור.write_text('.code32\n.text\n.globl _start\n_start:\n' + תוכן_ערך +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(מדריך_ערך / (שם + '.o')), str(קודמקור)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(מיקום.parent / 'compiler/משתמש_לקשר_ניווט.ld'),
                        '-o', str(מדריך_ערך / (שם + '.elf')), str(מדריך_ערך / (שם + '.o'))], check=True)
        항목들.append(שם + '=' + str(מדריך_ערך / (שם + '.elf')))
    מערכות_מידע_רגיל = bytearray((מיקום / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    לא_חוקי_תוצאה = bytearray(מערכות_מידע_רגיל); לא_חוקי_תוצאה[0] = 0; 변형들['badelf'] = לא_חוקי_תוצאה
    לא_חוקי_תוצאה = bytearray(מערכות_מידע_רגיל); struct.pack_into('<I', לא_חוקי_תוצאה, 24, 0x00100000); 변형들['badentry'] = לא_חוקי_תוצאה
    לא_חוקי_תוצאה = bytearray(מערכות_מידע_רגיל); struct.pack_into('<I', לא_חוקי_תוצאה, 28, 0x7fffffff); 변형들['badtable'] = לא_חוקי_תוצאה
    לא_חוקי_תוצאה = bytearray(מערכות_מידע_רגיל); טבלת_בדיקת_מידע = struct.unpack_from('<I', לא_חוקי_תוצאה, 28)[0]
    struct.pack_into('<I', לא_חוקי_תוצאה, טבלת_בדיקת_מידע + 20, 0x7fffffff); 변형들['badsize'] = לא_חוקי_תוצאה
    for שם, נתונים in 변형들.items():
        קובץ = מדריך_ערך / (שם + '.elf'); קובץ.write_bytes(נתונים)
        항목들.append(שם + '=' + str(קובץ))
    subprocess.run([sys.executable, str(מיקום / 'כלים/לאגד_משתתף.py'), '-o', str(מדריך_ערך / 'apps.bin')] + 항목들, check=True)
    קודמקור = מדריך_ערך / 'apps.s'
    קודמקור.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(מדריך_ערך / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(מדריך_ערך / 'apps.o'), str(קודמקור)], check=True)
    ליבה_ערך = מדריך_ערך / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(מיקום / '부팅/לקשר_ניווט.ld'), '-o', str(ליבה_ערך),
                    str(מיקום / 'build/boot.o'), str(מיקום / 'build/java.o'), str(מיקום / 'build/user.o'), str(מדריך_ערך / 'apps.o')], check=True)
    return ליבה_ערך


def לבצע_פקודה():
    תוצאה = {}
    שרת_ערך = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    שרת_ערך.bind(('127.0.0.1', 0))
    שרת_ערך.settimeout(0.1)
    הסב_ערך = שרת_ערך.getsockname()[1]
    받은것 = []
    יציאה_תוכנית = threading.Event()
    def הד_מענה():
        while not יציאה_תוכנית.is_set():
            try: נתונים, עמית_ערך = שרת_ערך.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(נתונים)
            if נתונים != b'drop-me': שרת_ערך.sendto(נתונים, עמית_ערך)
    עובד_ערך = threading.Thread(target=הד_מענה, daemon=True)
    עובד_ערך.start()
    try:
        for 종류 in ('elf', 'iso'):
            מחשב = מחשב_וירטואלי(מיקום / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                מחשב.פקודה('apps', ['hello', 'udp', 'netcheck', 'stress'])
                מחשב.פקודה('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                מחשב.פקודה('run missing', ['Exit: -2'])
                מחשב.פקודה('net', ['NET RTL8139'])
                מחשב.פקודה('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for תוכן_ערך in ('hello-network', 'odd', 'even', 'repeat-123'):
                    מחשב.פקודה('run udp 10.0.2.2 {} {}'.format(הסב_ערך, תוכן_ערך), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert תוכן_ערך.encode() in 받은것, 'ארח 서버에서 자료를 받지 못함'
                מחשב.פקודה('run stress {}'.format(הסב_ערך), ['UDP STRESS PASS', 'Exit: 0'])
                מחשב.פקודה('run udp 10.0.2.2 {} drop-me'.format(הסב_ערך), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                מחשב.פקודה('run hello recovered', ['arg: recovered', 'Exit: 0'])
                תוצאה[종류] = מחשב.לרשום_שיא.decode('utf-8', 'replace')
                print('PASS: {} משתמש ELF/ring 3/ארגומנטים/UDP ארח 왕복/ערך_זמן 초과/מעטפת 복귀'.format(종류), flush=True)
            finally:
                try: מחשב.פקודה('net', [])
                except Exception: pass
                (מיקום / 'build/사용자통신-last.log').write_bytes(מחשב.לרשום_שיא)
                מחשב.סגירה()
        מחשב = מחשב_וירטואלי(מיקום / 'build/kernel.elf', רשת_ערך=False)
        try:
            מחשב.פקודה('net', ['NET unavailable'])
            מחשב.פקודה('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            מחשב.פקודה('run hello', ['USER MODE ring 3', 'Exit: 0'])
            תוצאה['no_nic'] = מחשב.לרשום_שיא.decode()
        finally: מחשב.סגירה()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            מחשב = מחשב_וירטואלי(보호커널(Path(임시)), רשת_ערך=False)
            try:
                for שם, מצב_ערך in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    מחשב.פקודה('run ' + שם, ['Exit: ' + str(מצב_ערך)])
                    מחשב.פקודה('run hello', ['USER MODE ring 3', 'Exit: 0'])
                תוצאה['protection'] = מחשב.לרשום_שיא.decode()
                print('PASS: משתמש זיכרון_נתונים/חומרה_הסב 격리, 잘못된 מצביע/ELF, CPU חריגה, 무한 סבב_ערך 제한', flush=True)
            finally:
                (מיקום / 'build/הגנה_נסה-last.log').write_bytes(מחשב.לרשום_שיא)
                מחשב.סגירה()
    finally:
        יציאה_תוכנית.set()
        עובד_ערך.join(timeout=2)
        שרת_ערך.close()
    תוצאה['host_udp_received'] = [{'length': len(נתונים), 'sha256': hashlib.sha256(נתונים).hexdigest()} for נתונים in 받은것]
    (מיקום / 'build/נסה_משתמש_רשת.json').write_text(json.dumps(תוצאה, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    לבצע_פקודה()
