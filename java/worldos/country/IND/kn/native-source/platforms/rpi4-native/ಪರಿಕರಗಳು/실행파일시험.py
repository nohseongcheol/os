#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from ಪೂರೈಸು_ಆದೇಶ import ಬಿಂಬಿಸು_ಮೂಲ


def 리눅스예제(ಮಾಪನ_ಡೇಟಾ):
    ಮಾಪನ_ಡೇಟಾ.mkdir(parents=True, exist_ok=True)
    for 원본자료, ಹೆಸರು in [('ಚಲಾಯಿಸು_2.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(ಬಿಂಬಿಸು_ಮೂಲ/'예제/리눅스ABI'/원본자료), '-o', str(ಮಾಪನ_ಡೇಟಾ/ಹೆಸರು)])
    실행가능파일 = ಮಾಪನ_ಡೇಟಾ/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(ಮಾಪನ_ಡೇಟಾ/'start.o'), str(ಮಾಪನ_ಡೇಟಾ/'hello.o')])
    ವಿಷಯ_ಮೌಲ್ಯ = 실행가능파일.read_bytes()
    assert len(ವಿಷಯ_ಮೌಲ್ಯ) <= 16384 and ವಿಷಯ_ಮೌಲ್ಯ[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', ವಿಷಯ_ಮೌಲ್ಯ, 16) == (2, 183) and b'JKOROS\0' not in ವಿಷಯ_ಮೌಲ್ಯ
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    ಹೋಲಿಕೆ_ಆಧಾರರೇಖೆ = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(ಮಾಪನ_ಡೇಟಾ)).decode()
    assert ಹೋಲಿಕೆ_ಆಧಾರರೇಖೆ == 예상결과, ಹೋಲಿಕೆ_ಆಧಾರರೇಖೆ
    (ಮಾಪನ_ಡೇಟಾ/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def ಚಲಾಯಿಸು_2():
    ಮಾಪನ_ಡೇಟಾ = ಬಿಂಬಿಸು_ಮೂಲ/'build/verification/elf'
    ಮಾಪನ_ಡೇಟಾ.mkdir(parents=True, exist_ok=True)
    (ಮಾಪನ_ಡೇಟಾ/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(ಮಾಪನ_ಡೇಟಾ)
    ಮಾಪನ = subprocess.check_output(['python3', str(ಬಿಂಬಿಸು_ಮೂಲ/'ಪರಿಕರಗಳು/ಪೂರೈಸು_ಫೈಲ್.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in ಮಾಪನ, ಮಾಪನ
    (ಮಾಪನ_ಡೇಟಾ/'serial.log').write_text(ಮಾಪನ)
    원본=실행가능파일.read_bytes()
    ಅಪ್ಲಿ_ಶಿರೋಲೇಖ_ಆಫ್_ಸೆಟ್=struct.unpack_from('<Q',원본,32)[0]
    for ಹೆಸರು,ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ,ಸ್ವರೂಪ_b87fd068,ಮೌಲ್ಯ in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',ಅಪ್ಲಿ_ಶಿರೋಲೇಖ_ಆಫ್_ಸೆಟ್+4,'I',7),('kernel-address',ಅಪ್ಲಿ_ಶಿರೋಲೇಖ_ಆಫ್_ಸೆಟ್+16,'Q',0x400000)]:
        ಅಮಾನ್ಯ_ಡೇಟಾ=bytearray(원본);struct.pack_into('<'+ಸ್ವರೂಪ_b87fd068,ಅಮಾನ್ಯ_ಡೇಟಾ,ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ,ಮೌಲ್ಯ)
        ಮಾರ್ಗ=ಮಾಪನ_ಡೇಟಾ/ಹೆಸರು;ಮಾರ್ಗ.write_bytes(ಅಮಾನ್ಯ_ಡೇಟಾ)
        거부결과=subprocess.run(['python3',str(ಬಿಂಬಿಸು_ಮೂಲ/'ಪರಿಕರಗಳು/ಪೂರೈಸು_ಫೈಲ್.py'),'--linux',str(ಮಾರ್ಗ)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(ಹೆಸರು,거부결과.stdout)
    ದೃಢೀಕರಣ_ವರದಿ = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((ಬಿಂಬಿಸು_ಮೂಲ/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (ಮಾಪನ_ಡೇಟಾ/'report.json').write_text(json.dumps(ದೃಢೀಕರಣ_ವರದಿ, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': ಚಲಾಯಿಸು_2()
