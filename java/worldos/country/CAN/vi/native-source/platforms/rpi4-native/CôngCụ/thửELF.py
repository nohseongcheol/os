#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from thựcThiLệnh import gốcCâyDựÁn


def víDụLinux(dữLiệuKếtQuả):
    dữLiệuKếtQuả.mkdir(parents=True, exist_ok=True)
    for dữLiệuNguyênBản, tên in [('chạy.S', 'start.o'), ('LờiChào.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(gốcCâyDựÁn/'VíDụ/ABILinux'/dữLiệuNguyênBản), '-o', str(dữLiệuKếtQuả/tên)])
    ảnhTệpThựcThi = dữLiệuKếtQuả/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(ảnhTệpThựcThi), str(dữLiệuKếtQuả/'start.o'), str(dữLiệuKếtQuả/'hello.o')])
    giáTrịNộiDung = ảnhTệpThựcThi.read_bytes()
    assert len(giáTrịNộiDung) <= 16384 and giáTrịNộiDung[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', giáTrịNộiDung, 16) == (2, 183) and b'JKOROS\0' not in giáTrịNộiDung
    dựKiến = 'LINUX ARM64 ELF PASS\n한글인수\n'
    mốcCơSởPhépSoSánh = subprocess.check_output(['qemu-aarch64', str(ảnhTệpThựcThi), '한글인수'], cwd=str(dữLiệuKếtQuả)).decode()
    assert mốcCơSởPhépSoSánh == dựKiến, mốcCơSởPhépSoSánh
    (dữLiệuKếtQuả/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(ảnhTệpThựcThi)]))
    return ảnhTệpThựcThi, dựKiến


def chạy():
    dữLiệuKếtQuả = gốcCâyDựÁn/'build/verification/elf'
    dữLiệuKếtQuả.mkdir(parents=True, exist_ok=True)
    (dữLiệuKếtQuả/'report.json').write_text('{"passed": false}\n')
    ảnhTệpThựcThi, dựKiến = víDụLinux(dữLiệuKếtQuả)
    kếtQuả = subprocess.check_output(['python3', str(gốcCâyDựÁn/'CôngCụ/thựcThiTệp.py'), '--linux', str(ảnhTệpThựcThi), '한글인수']).decode().replace('\r\n', '\n')
    assert dựKiến+'exit 0' in kếtQuả, kếtQuả
    (dữLiệuKếtQuả/'serial.log').write_text(kếtQuả)
    nguyênBản=ảnhTệpThựcThi.read_bytes()
    độLệchĐầuMụcChươngTrình=struct.unpack_from('<Q',nguyênBản,32)[0]
    for tên,giáTrịĐộLệch,chọnĐịnhDạng,giáTrị in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',độLệchĐầuMụcChươngTrình+4,'I',7),('kernel-address',độLệchĐầuMụcChươngTrình+16,'Q',0x400000)]:
        dữLiệuKhôngHợpLệ=bytearray(nguyênBản);struct.pack_into('<'+chọnĐịnhDạng,dữLiệuKhôngHợpLệ,giáTrịĐộLệch,giáTrị)
        đườngDẫn=dữLiệuKếtQuả/tên;đườngDẫn.write_bytes(dữLiệuKhôngHợpLệ)
        kếtQuảSựTừChối=subprocess.run(['python3',str(gốcCâyDựÁn/'CôngCụ/thựcThiTệp.py'),'--linux',str(đườngDẫn)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert kếtQuảSựTừChối.returncode==1 and b'exit -8' in kếtQuảSựTừChối.stdout,(tên,kếtQuảSựTừChối.stdout)
    báoCáoViệcThẩmĐịnh = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((gốcCâyDựÁn/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(ảnhTệpThựcThi.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (dữLiệuKếtQuả/'report.json').write_text(json.dumps(báoCáoViệcThẩmĐịnh, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': chạy()
