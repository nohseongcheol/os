#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from இயக்கு_கட்டளை import திட்டப்பணி_மூலம்


def 리눅스예제(அளவிடக்கூடியது_தரவு):
    அளவிடக்கூடியது_தரவு.mkdir(parents=True, exist_ok=True)
    for 원본자료, பெயர் in [('செயல்படுத்துக.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(திட்டப்பணி_மூலம்/'예제/리눅스ABI'/원본자료), '-o', str(அளவிடக்கூடியது_தரவு/பெயர்)])
    செயல்படுத்தக்கூடிய_கோப்பு_படம் = அளவிடக்கூடியது_தரவு/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(செயல்படுத்தக்கூடிய_கோப்பு_படம்), str(அளவிடக்கூடியது_தரவு/'start.o'), str(அளவிடக்கூடியது_தரவு/'hello.o')])
    உள்ளடக்கம்_மதிப்பு = செயல்படுத்தக்கூடிய_கோப்பு_படம்.read_bytes()
    assert len(உள்ளடக்கம்_மதிப்பு) <= 16384 and உள்ளடக்கம்_மதிப்பு[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', உள்ளடக்கம்_மதிப்பு, 16) == (2, 183) and b'JKOROS\0' not in உள்ளடக்கம்_மதிப்பு
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    ஒப்பிடுதல்_அடிப்படைக்_கோடு = subprocess.check_output(['qemu-aarch64', str(செயல்படுத்தக்கூடிய_கோப்பு_படம்), '한글인수'], cwd=str(அளவிடக்கூடியது_தரவு)).decode()
    assert ஒப்பிடுதல்_அடிப்படைக்_கோடு == 예상결과, ஒப்பிடுதல்_அடிப்படைக்_கோடு
    (அளவிடக்கூடியது_தரவு/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(செயல்படுத்தக்கூடிய_கோப்பு_படம்)]))
    return செயல்படுத்தக்கூடிய_கோப்பு_படம், 예상결과


def செயல்படுத்துக():
    அளவிடக்கூடியது_தரவு = திட்டப்பணி_மூலம்/'build/verification/elf'
    அளவிடக்கூடியது_தரவு.mkdir(parents=True, exist_ok=True)
    (அளவிடக்கூடியது_தரவு/'report.json').write_text('{"passed": false}\n')
    செயல்படுத்தக்கூடிய_கோப்பு_படம், 예상결과 = 리눅스예제(அளவிடக்கூடியது_தரவு)
    அளவிடக்கூடியது = subprocess.check_output(['python3', str(திட்டப்பணி_மூலம்/'கருவிகள்/இயக்கு_கோப்பு.py'), '--linux', str(செயல்படுத்தக்கூடிய_கோப்பு_படம்), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in அளவிடக்கூடியது, அளவிடக்கூடியது
    (அளவிடக்கூடியது_தரவு/'serial.log').write_text(அளவிடக்கூடியது)
    원본=செயல்படுத்தக்கூடிய_கோப்பு_படம்.read_bytes()
    நிரல்_மேற்குறிப்பு_ஆஃப்செட்=struct.unpack_from('<Q',원본,32)[0]
    for பெயர்,ஆஃப்செட்_மதிப்பு,வடிவமை_b87fd068,மதிப்பு in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',நிரல்_மேற்குறிப்பு_ஆஃப்செட்+4,'I',7),('kernel-address',நிரல்_மேற்குறிப்பு_ஆஃப்செட்+16,'Q',0x400000)]:
        செல்லுபடியாகாத_தரவு=bytearray(원본);struct.pack_into('<'+வடிவமை_b87fd068,செல்லுபடியாகாத_தரவு,ஆஃப்செட்_மதிப்பு,மதிப்பு)
        பாதை_2=அளவிடக்கூடியது_தரவு/பெயர்;பாதை_2.write_bytes(செல்லுபடியாகாத_தரவு)
        거부결과=subprocess.run(['python3',str(திட்டப்பணி_மூலம்/'கருவிகள்/இயக்கு_கோப்பு.py'),'--linux',str(பாதை_2)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(பெயர்,거부결과.stdout)
    செல்லுபடியாக்கம்_அறிக்கை = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((திட்டப்பணி_மூலம்/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(செயல்படுத்தக்கூடிய_கோப்பு_படம்.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (அளவிடக்கூடியது_தரவு/'report.json').write_text(json.dumps(செல்லுபடியாக்கம்_அறிக்கை, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': செயல்படுத்துக()
