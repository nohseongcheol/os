#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from לבצע_פקודה import לשקף_בסיס


def 리눅스예제(תוצאה_נתונים):
    תוצאה_נתונים.mkdir(parents=True, exist_ok=True)
    for 원본자료, שם in [('הפעלה.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(לשקף_בסיס/'예제/리눅스ABI'/원본자료), '-o', str(תוצאה_נתונים/שם)])
    실행가능파일 = תוצאה_נתונים/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(תוצאה_נתונים/'start.o'), str(תוצאה_נתונים/'hello.o')])
    תוכן_ערך = 실행가능파일.read_bytes()
    assert len(תוכן_ערך) <= 16384 and תוכן_ערך[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', תוכן_ערך, 16) == (2, 183) and b'JKOROS\0' not in תוכן_ערך
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    השוואה_בסיס = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(תוצאה_נתונים)).decode()
    assert השוואה_בסיס == 예상결과, השוואה_בסיס
    (תוצאה_נתונים/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def הפעלה():
    תוצאה_נתונים = לשקף_בסיס/'build/verification/elf'
    תוצאה_נתונים.mkdir(parents=True, exist_ok=True)
    (תוצאה_נתונים/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(תוצאה_נתונים)
    תוצאה = subprocess.check_output(['python3', str(לשקף_בסיס/'כלים/לבצע_קובץ.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in תוצאה, תוצאה
    (תוצאה_נתונים/'serial.log').write_text(תוצאה)
    원본=실행가능파일.read_bytes()
    תוכנית_כותרת_היסט=struct.unpack_from('<Q',원본,32)[0]
    for שם,היסט_ערך,לעצב_b87fd068,ערך in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',תוכנית_כותרת_היסט+4,'I',7),('kernel-address',תוכנית_כותרת_היסט+16,'Q',0x400000)]:
        לא_חוקי_נתונים=bytearray(원본);struct.pack_into('<'+לעצב_b87fd068,לא_חוקי_נתונים,היסט_ערך,ערך)
        נתיב=תוצאה_נתונים/שם;נתיב.write_bytes(לא_חוקי_נתונים)
        거부결과=subprocess.run(['python3',str(לשקף_בסיס/'כלים/לבצע_קובץ.py'),'--linux',str(נתיב)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(שם,거부결과.stdout)
    אימות_דוח = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((לשקף_בסיס/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (תוצאה_נתונים/'report.json').write_text(json.dumps(אימות_דוח, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': הפעלה()
