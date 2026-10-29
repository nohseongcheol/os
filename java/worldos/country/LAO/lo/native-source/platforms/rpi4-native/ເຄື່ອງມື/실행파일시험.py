#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ import ໂຄງ_ການ_ເລກຮາກ


def 리눅스예제(ມາດຕະການ_ຂໍ້ມູນ):
    ມາດຕະການ_ຂໍ້ມູນ.mkdir(parents=True, exist_ok=True)
    for 원본자료, ຊື່ in [('ແລ່ນ.S', 'start.o'), ('인사.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(ໂຄງ_ການ_ເລກຮາກ/'예제/리눅스ABI'/원본자료), '-o', str(ມາດຕະການ_ຂໍ້ມູນ/ຊື່)])
    실행가능파일 = ມາດຕະການ_ຂໍ້ມູນ/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(실행가능파일), str(ມາດຕະການ_ຂໍ້ມູນ/'start.o'), str(ມາດຕະການ_ຂໍ້ມູນ/'hello.o')])
    ເນື້ອໃນ_ຄ່າ_cb0f2404 = 실행가능파일.read_bytes()
    assert len(ເນື້ອໃນ_ຄ່າ_cb0f2404) <= 16384 and ເນື້ອໃນ_ຄ່າ_cb0f2404[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', ເນື້ອໃນ_ຄ່າ_cb0f2404, 16) == (2, 183) and b'JKOROS\0' not in ເນື້ອໃນ_ຄ່າ_cb0f2404
    예상결과 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    ການປຽບທຽບ_ຖານເສັ້ນ = subprocess.check_output(['qemu-aarch64', str(실행가능파일), '한글인수'], cwd=str(ມາດຕະການ_ຂໍ້ມູນ)).decode()
    assert ການປຽບທຽບ_ຖານເສັ້ນ == 예상결과, ການປຽບທຽບ_ຖານເສັ້ນ
    (ມາດຕະການ_ຂໍ້ມູນ/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(실행가능파일)]))
    return 실행가능파일, 예상결과


def ແລ່ນ():
    ມາດຕະການ_ຂໍ້ມູນ = ໂຄງ_ການ_ເລກຮາກ/'build/verification/elf'
    ມາດຕະການ_ຂໍ້ມູນ.mkdir(parents=True, exist_ok=True)
    (ມາດຕະການ_ຂໍ້ມູນ/'report.json').write_text('{"passed": false}\n')
    실행가능파일, 예상결과 = 리눅스예제(ມາດຕະການ_ຂໍ້ມູນ)
    ມາດຕະການ = subprocess.check_output(['python3', str(ໂຄງ_ການ_ເລກຮາກ/'ເຄື່ອງມື/ປະ_ຕິ_ບັດ_ຟາຍ.py'), '--linux', str(실행가능파일), '한글인수']).decode().replace('\r\n', '\n')
    assert 예상결과+'exit 0' in ມາດຕະການ, ມາດຕະການ
    (ມາດຕະການ_ຂໍ້ມູນ/'serial.log').write_text(ມາດຕະການ)
    원본=실행가능파일.read_bytes()
    ແອັບ_ສ່ວນຫົວ_ອອບເຊັດ=struct.unpack_from('<Q',원본,32)[0]
    for ຊື່,ອອບເຊັດ_ຄ່າ,ຮູບແບບ_b87fd068,ຄ່າ in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',ແອັບ_ສ່ວນຫົວ_ອອບເຊັດ+4,'I',7),('kernel-address',ແອັບ_ສ່ວນຫົວ_ອອບເຊັດ+16,'Q',0x400000)]:
        ໃຊ້ບໍ່ໄດ້_ຂໍ້ມູນ=bytearray(원본);struct.pack_into('<'+ຮູບແບບ_b87fd068,ໃຊ້ບໍ່ໄດ້_ຂໍ້ມູນ,ອອບເຊັດ_ຄ່າ,ຄ່າ)
        ທາງໂຄຈອນ=ມາດຕະການ_ຂໍ້ມູນ/ຊື່;ທາງໂຄຈອນ.write_bytes(ໃຊ້ບໍ່ໄດ້_ຂໍ້ມູນ)
        거부결과=subprocess.run(['python3',str(ໂຄງ_ການ_ເລກຮາກ/'ເຄື່ອງມື/ປະ_ຕິ_ບັດ_ຟາຍ.py'),'--linux',str(ທາງໂຄຈອນ)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 거부결과.returncode==1 and b'exit -8' in 거부결과.stdout,(ຊື່,거부결과.stdout)
    ໃຊ້ໄດ້_ລາຍງານ = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((ໂຄງ_ການ_ເລກຮາກ/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(실행가능파일.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (ມາດຕະການ_ຂໍ້ມູນ/'report.json').write_text(json.dumps(ໃຊ້ໄດ້_ລາຍງານ, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': ແລ່ນ()
