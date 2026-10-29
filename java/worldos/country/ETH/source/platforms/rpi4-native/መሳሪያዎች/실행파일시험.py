#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from ፈጽም_ትእዛዝ import አሳይ_ስር


def 리눅스예제(ልኬት_ውሂብ):
    ልኬት_ውሂብ.mkdir(parents=True, exist_ok=True)
    for 원본자료, ስም in [('ማስኬጃ.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(አሳይ_ስር/'예제/리눅스ABI'/원본자료), '-o', str(ልኬት_ውሂብ/ስም)])
    실행가능파일 = ልኬት_ውሂብ/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(ልኬት_ውሂብ/'start.o'), str(ልኬት_ውሂብ/'hello.o')])
    ይዘት_እሴት = 실행가능파일.read_bytes()
    assert len(ይዘት_እሴት) <= 16384 and ይዘት_እሴት[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', ይዘት_እሴት, 16) == (2, 183) and b'JKOROS\0' not in ይዘት_እሴት
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    ንጽጽር_መነሻ = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(ልኬት_ውሂብ)).decode()
    assert ንጽጽር_መነሻ == 예상결과, ንጽጽር_መነሻ
    (ልኬት_ውሂብ/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def ማስኬጃ():
    ልኬት_ውሂብ = አሳይ_ስር/'build/verification/elf'
    ልኬት_ውሂብ.mkdir(parents=True, exist_ok=True)
    (ልኬት_ውሂብ/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(ልኬት_ውሂብ)
    ልኬት = subprocess.check_output(['python3', str(አሳይ_ስር/'መሳሪያዎች/ፈጽም_ፋይል.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in ልኬት, ልኬት
    (ልኬት_ውሂብ/'serial.log').write_text(ልኬት)
    원본=실행가능파일.read_bytes()
    ፕሮግራም_ርእስ_ዝንፍ=struct.unpack_from('<Q',원본,32)[0]
    for ስም,ዝንፍ_እሴት,ቅርጸት_b87fd068,እሴት in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',ፕሮግራም_ርእስ_ዝንፍ+4,'I',7),('kernel-address',ፕሮግራም_ርእስ_ዝንፍ+16,'Q',0x400000)]:
        ልክ_ያልኾነ_ውሂብ=bytearray(원본);struct.pack_into('<'+ቅርጸት_b87fd068,ልክ_ያልኾነ_ውሂብ,ዝንፍ_እሴት,እሴት)
        መተላለፊያ=ልኬት_ውሂብ/ስም;መተላለፊያ.write_bytes(ልክ_ያልኾነ_ውሂብ)
        거부결과=subprocess.run(['python3',str(አሳይ_ስር/'መሳሪያዎች/ፈጽም_ፋይል.py'),'--linux',str(መተላለፊያ)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(ስም,거부결과.stdout)
    ማረጋገጥ_ዘገባ = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((አሳይ_ስር/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (ልኬት_ውሂብ/'report.json').write_text(json.dumps(ማረጋገጥ_ዘገባ, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': ማስኬጃ()
