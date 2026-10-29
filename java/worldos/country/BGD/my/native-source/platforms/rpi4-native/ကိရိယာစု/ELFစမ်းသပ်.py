#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from စက်မောင်း import စီမံကိန်းအမြစ်


def 리눅스예제(ရလဒ်ဒေတာ):
    ရလဒ်ဒေတာ.mkdir(parents=True, exist_ok=True)
    for မူရင်းဒေတာ, အမည် in [('လုပ်ဆောင်.S', 'start.o'), ('နှုတ်ဆက်.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(စီမံကိန်းအမြစ်/'ဥပမာ/리눅스ABI'/မူရင်းဒေတာ), '-o', str(ရလဒ်ဒေတာ/အမည်)])
    စက်ဖိုင်စက်ပုံရိပ် = ရလဒ်ဒေတာ/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(စက်ဖိုင်စက်ပုံရိပ်), str(ရလဒ်ဒေတာ/'start.o'), str(ရလဒ်ဒေတာ/'hello.o')])
    အကြောင်းအရာတန်ဖိုး = စက်ဖိုင်စက်ပုံရိပ်.read_bytes()
    assert len(အကြောင်းအရာတန်ဖိုး) <= 16384 and အကြောင်းအရာတန်ဖိုး[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', အကြောင်းအရာတန်ဖိုး, 16) == (2, 183) and b'JKOROS\0' not in အကြောင်းအရာတန်ဖိုး
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    비교기준 = subprocess.check_output(['qemu-aarch64', str(စက်ဖိုင်စက်ပုံရိပ်), '한글인수'], cwd=str(ရလဒ်ဒေတာ)).decode()
    assert 비교기준 == 예상결과, 비교기준
    (ရလဒ်ဒေတာ/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(စက်ဖိုင်စက်ပုံရိပ်)]))
    return စက်ဖိုင်စက်ပုံရိပ်, 예상결과


def လုပ်ဆောင်():
    ရလဒ်ဒေတာ = စီမံကိန်းအမြစ်/'build/verification/elf'
    ရလဒ်ဒေတာ.mkdir(parents=True, exist_ok=True)
    (ရလဒ်ဒေတာ/'report.json').write_text('{"passed": false}\n')
    စက်ဖိုင်စက်ပုံရိပ်, 예상결과 = 리눅스예제(ရလဒ်ဒေတာ)
    ရလဒ် = subprocess.check_output(['python3', str(စီမံကိန်းအမြစ်/'ကိရိယာစု/ဖိုင်လုပ်ဆောင်.py'), '--linux', str(စက်ဖိုင်စက်ပုံရိပ်), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in ရလဒ်, ရလဒ်
    (ရလဒ်ဒေတာ/'serial.log').write_text(ရလဒ်)
    မူရင်း=စက်ဖိုင်စက်ပုံရိပ်.read_bytes()
    ပရိုဂရမ်ခေါင်းစီးအရွေ့=struct.unpack_from('<Q',မူရင်း,32)[0]
    for အမည်,အရွေ့တန်ဖိုး,형식지정,တန်ဖိုး in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',ပရိုဂရမ်ခေါင်းစီးအရွေ့+4,'I',7),('kernel-address',ပရိုဂရမ်ခေါင်းစီးအရွေ့+16,'Q',0x400000)]:
        မမှန်ကန်ဒေတာ=bytearray(မူရင်း);struct.pack_into('<'+형식지정,မမှန်ကန်ဒေတာ,အရွေ့တန်ဖိုး,တန်ဖိုး)
        လမ်း=ရလဒ်ဒေတာ/အမည်;လမ်း.write_bytes(မမှန်ကန်ဒေတာ)
        거부결과=subprocess.run(['python3',str(စီမံကိန်းအမြစ်/'ကိရိယာစု/ဖိုင်လုပ်ဆောင်.py'),'--linux',str(လမ်း)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(အမည်,거부결과.stdout)
    검증기록 = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((စီမံကိန်းအမြစ်/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(စက်ဖိုင်စက်ပုံရိပ်.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (ရလဒ်ဒေတာ/'report.json').write_text(json.dumps(검증기록, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': လုပ်ဆောင်()
