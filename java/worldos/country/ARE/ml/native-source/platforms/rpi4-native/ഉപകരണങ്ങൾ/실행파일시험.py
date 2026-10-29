#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from നടപ്പാക്കുക_കമാന്_ഡ് import പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം


def 리눅스예제(അളവ്_ഡാറ്റാ):
    അളവ്_ഡാറ്റാ.mkdir(parents=True, exist_ok=True)
    for 원본자료, പേരു് in [('നടപ്പിലാക്കുക.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'예제/리눅스ABI'/원본자료), '-o', str(അളവ്_ഡാറ്റാ/പേരു്)])
    നിര്_വ്വഹണക്ഷമമായ_ഫയല്_ഇമേജ് = അളവ്_ഡാറ്റാ/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(നിര്_വ്വഹണക്ഷമമായ_ഫയല്_ഇമേജ്), str(അളവ്_ഡാറ്റാ/'start.o'), str(അളവ്_ഡാറ്റാ/'hello.o')])
    ഉള്ളടക്കം_മൂല്യം = നിര്_വ്വഹണക്ഷമമായ_ഫയല്_ഇമേജ്.read_bytes()
    assert len(ഉള്ളടക്കം_മൂല്യം) <= 16384 and ഉള്ളടക്കം_മൂല്യം[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', ഉള്ളടക്കം_മൂല്യം, 16) == (2, 183) and b'JKOROS\0' not in ഉള്ളടക്കം_മൂല്യം
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    താരതമ്യം_ఆధారరేఖ = subprocess.check_output(['qemu-aarch64', str(നിര്_വ്വഹണക്ഷമമായ_ഫയല്_ഇമേജ്), '한글인수'], cwd=str(അളവ്_ഡാറ്റാ)).decode()
    assert താരതമ്യം_ఆధారరేఖ == 예상결과, താരതമ്യം_ఆధారరేఖ
    (അളവ്_ഡാറ്റാ/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(നിര്_വ്വഹണക്ഷമമായ_ഫയല്_ഇമേജ്)]))
    return നിര്_വ്വഹണക്ഷമമായ_ഫയല്_ഇമേജ്, 예상결과


def നടപ്പിലാക്കുക():
    അളവ്_ഡാറ്റാ = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/verification/elf'
    അളവ്_ഡാറ്റാ.mkdir(parents=True, exist_ok=True)
    (അളവ്_ഡാറ്റാ/'report.json').write_text('{"passed": false}\n')
    നിര്_വ്വഹണക്ഷമമായ_ഫയല്_ഇമേജ്, 예상결과 = 리눅스예제(അളവ്_ഡാറ്റാ)
    അളവ് = subprocess.check_output(['python3', str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'ഉപകരണങ്ങൾ/നടപ്പാക്കുക_ഫയല്.py'), '--linux', str(നിര്_വ്വഹണക്ഷമമായ_ഫയല്_ഇമേജ്), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in അളവ്, അളവ്
    (അളവ്_ഡാറ്റാ/'serial.log').write_text(അളവ്)
    원본=നിര്_വ്വഹണക്ഷമമായ_ഫയല്_ഇമേജ്.read_bytes()
    പ്രോഗ്രാം_ശീർഷകം_ഓഫ്_സെറ്റ്=struct.unpack_from('<Q',원본,32)[0]
    for പേരു്,ഓഫ്_സെറ്റ്_മൂല്യം,ఫార్మాట్_b87fd068,മൂല്യം in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',പ്രോഗ്രാം_ശീർഷകം_ഓഫ്_സെറ്റ്+4,'I',7),('kernel-address',പ്രോഗ്രാം_ശീർഷകം_ഓഫ്_സെറ്റ്+16,'Q',0x400000)]:
        അസാധുവായ_ഡാറ്റാ=bytearray(원본);struct.pack_into('<'+ఫార్మాట్_b87fd068,അസാധുവായ_ഡാറ്റാ,ഓഫ്_സെറ്റ്_മൂല്യം,മൂല്യം)
        വഴി=അളവ്_ഡാറ്റാ/പേരു്;വഴി.write_bytes(അസാധുവായ_ഡാറ്റാ)
        거부결과=subprocess.run(['python3',str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'ഉപകരണങ്ങൾ/നടപ്പാക്കുക_ഫയല്.py'),'--linux',str(വഴി)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(പേരു്,거부결과.stdout)
    నిర్ధారణ_నివేదిక = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(നിര്_വ്വഹണക്ഷമമായ_ഫയല്_ഇമേജ്.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (അളവ്_ഡാറ്റാ/'report.json').write_text(json.dumps(నిర్ధారణ_నివేదిక, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': നടപ്പിലാക്കുക()
