#!/usr/bin/env python3
"""ໂຮສ libc 없이 연결한 한국어 C 프로그램을 ຕົວ_ຈິງ_ຂໍ້ມູນ ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 사용자통신시험 import ຈໍາລອງ_ເຄື່ອງຈັກ

ຈັດຕໍາແຫນ່ງ = Path(__file__).resolve().parents[1]

def ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ():
    ມາດຕະການ = {}
    서버 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    서버.bind(('127.0.0.1', 0))
    서버.settimeout(0.1)
    ຫມາຍເລກພອດ = 서버.getsockname()[1]
    받은자료 = []
    끝냄 = threading.Event()
    def 되보내기():
        while not 끝냄.is_set():
            try:
                ຂໍ້ມູນ, ອີເມວ = 서버.recvfrom(4096)
            except socket.timeout:
                continue
            받은자료.append(ຂໍ້ມູນ)
            서버.sendto(ຂໍ້ມູນ, ອີເມວ)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            ເຄື່ອງຈັກ = ຈໍາລອງ_ເຄື່ອງຈັກ(ຈັດຕໍາແຫນ່ງ / ('build/kernel.' + 종류), 종류)
            try:
                for ສະປຣິນ_ຄ່າ in range(2):
                    ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('run posixudp ' + str(ຫມາຍເລກພອດ), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                ແລ່ນ = len(ເຄື່ອງຈັກ.ບັນທຶກ_ແຖວ)
                ເຄື່ອງຈັກ.직렬.sendall(b'run posixinput\n')
                ເຄື່ອງຈັກ.ລໍຖ້າ_ສະຖານະ('POSIX INPUT READY', ແລ່ນ)
                ເຄື່ອງຈັກ.직렬.sendall(b'abcdef')
                출력 = ເຄື່ອງຈັກ.ລໍຖ້າ_ສະຖານະ('jkoros> ', ແລ່ນ)
                assert 'POSIX INPUT PASS' in 출력 and 'Exit: 0' in 출력, 출력
                ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('javac Hello.java', ['Exit: 0'])
                ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('run hello recovered', ['arg: recovered', 'Exit: 0'])
                ມາດຕະການ[종류] = ເຄື່ອງຈັກ.ບັນທຶກ_ແຖວ.decode('utf-8', 'replace')
                print('PASS:', 종류, 'POSIX ຟາຍ/공유 ຈັດຕໍາແຫນ່ງ/삭제 수명/ອີເມວ ປົກປ້ອງ_ຄ່າ/UDP/표준 입력/기존 Java', flush=True)
            finally:
                ເຄື່ອງຈັກ.ປິດ()
        assert b'posix-udp' in 받은자료 and b'truncate' in 받은자료 and b'' in 받은자료
    finally:
        끝냄.set(); 일꾼.join(timeout=2); 서버.close()
    ມາດຕະການ['host_datagrams'] = [ຂໍ້ມູນ.decode() for ຂໍ້ມູນ in 받은자료]
    (ຈັດຕໍາແຫນ່ງ / 'build/규약시험.json').write_text(json.dumps(ມາດຕະການ, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ()
