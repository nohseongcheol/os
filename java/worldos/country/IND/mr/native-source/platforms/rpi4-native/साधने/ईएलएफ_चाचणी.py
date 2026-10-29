#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from आज्ञा_कार्यवाही_करा import प्रोजेक्ट_मूळ


def लिनक्स_उदाहरण(मोजमाप_डेटा):
    मोजमाप_डेटा.mkdir(parents=True, exist_ok=True)
    for मूळ_डेटा, नाव in [('सुरू_करा.S', 'start.o'), ('अभिवादन_ae353e94.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(प्रोजेक्ट_मूळ/'उदाहरणे/लिनक्स_द्विमानजोडणी_02c60c12'/मूळ_डेटा), '-o', str(मोजमाप_डेटा/नाव)])
    निष्पादनीय_चित्र = मोजमाप_डेटा/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(निष्पादनीय_चित्र), str(मोजमाप_डेटा/'start.o'), str(मोजमाप_डेटा/'hello.o')])
    सामुग्री_मूल्य = निष्पादनीय_चित्र.read_bytes()
    assert len(सामुग्री_मूल्य) <= 16384 and सामुग्री_मूल्य[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', सामुग्री_मूल्य, 16) == (2, 183) and b'JKOROS\0' not in सामुग्री_मूल्य
    अपेक्षित = 'LINUX ARM64 ELF PASS\n한글인수\n'
    तुलना_आधाररेखा = subprocess.check_output(['qemu-aarch64', str(निष्पादनीय_चित्र), '한글인수'], cwd=str(मोजमाप_डेटा)).decode()
    assert तुलना_आधाररेखा == अपेक्षित, तुलना_आधाररेखा
    (मोजमाप_डेटा/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(निष्पादनीय_चित्र)]))
    return निष्पादनीय_चित्र, अपेक्षित


def सुरू_करा():
    मोजमाप_डेटा = प्रोजेक्ट_मूळ/'build/verification/elf'
    मोजमाप_डेटा.mkdir(parents=True, exist_ok=True)
    (मोजमाप_डेटा/'report.json').write_text('{"passed": false}\n')
    निष्पादनीय_चित्र, अपेक्षित = लिनक्स_उदाहरण(मोजमाप_डेटा)
    मोजमाप = subprocess.check_output(['python3', str(प्रोजेक्ट_मूळ/'साधने/संचिका_कार्यवाही_करा.py'), '--linux', str(निष्पादनीय_चित्र), '한글인수']).decode().replace('\r\n', '\n')
    assert अपेक्षित+'exit 0' in मोजमाप, मोजमाप
    (मोजमाप_डेटा/'serial.log').write_text(मोजमाप)
    मूळ=निष्पादनीय_चित्र.read_bytes()
    अनुप्रयोग_शीर्षलेख_ऑफसेट=struct.unpack_from('<Q',मूळ,32)[0]
    for नाव,ऑफसेट_मूल्य,स्वरूप_b87fd068,मूल्य in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',अनुप्रयोग_शीर्षलेख_ऑफसेट+4,'I',7),('kernel-address',अनुप्रयोग_शीर्षलेख_ऑफसेट+16,'Q',0x400000)]:
        अवैध_डेटा=bytearray(मूळ);struct.pack_into('<'+स्वरूप_b87fd068,अवैध_डेटा,ऑफसेट_मूल्य,मूल्य)
        मार्ग=मोजमाप_डेटा/नाव;मार्ग.write_bytes(अवैध_डेटा)
        नकार_मोजमाप=subprocess.run(['python3',str(प्रोजेक्ट_मूळ/'साधने/संचिका_कार्यवाही_करा.py'),'--linux',str(मार्ग)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert नकार_मोजमाप.returncode==1 and b'exit -8' in नकार_मोजमाप.stdout,(नाव,नकार_मोजमाप.stdout)
    पडताळणी_अहवाल = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((प्रोजेक्ट_मूळ/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(निष्पादनीय_चित्र.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (मोजमाप_डेटा/'report.json').write_text(json.dumps(पडताळणी_अहवाल, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': सुरू_करा()
