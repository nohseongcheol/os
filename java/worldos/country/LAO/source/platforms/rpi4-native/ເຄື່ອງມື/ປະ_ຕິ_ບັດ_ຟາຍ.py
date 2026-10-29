#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. ໂຮສ 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ import ຄໍາສັ່ງ_1f12b8e2


def ແລ່ນ():
    ຕົວແຍກວິເຄາະ = argparse.ArgumentParser(description=__doc__)
    ຕົວແຍກວິເຄາະ.add_argument('file', type=Path)
    ຕົວແຍກວິເຄາະ.add_argument('arguments', nargs='*')
    ຕົວແຍກວິເຄາະ.add_argument('--class-name', help='패키지가 있는 .class의 전체 ຊື່(예: ຮັບ_ຮອງ.꾸러미시험)')
    ຕົວແຍກວິເຄາະ.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 호출 ABI 사용')
    ຕົວແຍກວິເຄາະ.add_argument('--vnc', help='예: 127.0.0.1:2')
    ຕົວແຍກວິເຄາະ.add_argument('--include', action='append', type=Path, default=[], help='추가 class ຟາຍ 또는 class 디렉터리(패키지 ຊື່ 유지)')
    ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ = ຕົວແຍກວິເຄາະ.parse_args()
    ຂໍ້ມູນ = ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.file.read_bytes()
    if ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.class_name and ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.file.suffix != '.class': ຕົວແຍກວິເຄາະ.error('--class-name은 .class 입력에서 사용합니다.')
    ຊື່ = ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.class_name + '.class' if ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.class_name else ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.file.name
    if len(ຂໍ້ມູນ) > 16384 or not 1 <= len(ຊື່.encode('utf-8')) <= 63 or '\n' in ຊື່ or '\r' in ຊື່:
        ຕົວແຍກວິເຄາະ.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    ຫມວດ_ຄ່າ = '.elf' if ຂໍ້ມູນ[:4] == b'\x7fELF' else ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.file.suffix
    if ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.linux and ຫມວດ_ຄ່າ != '.elf': ຕົວແຍກວິເຄາະ.error('--linux는 ELF 바이너리에만 사용합니다.')
    if ຫມວດ_ຄ່າ not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        ຕົວແຍກວິເຄາະ.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.arguments) > 7 or any(len(ສະຕຣິງ_ຂໍ້ມູນ.encode('utf-8')) > 255 or '\n' in ສະຕຣິງ_ຂໍ້ມູນ or '\r' in ສະຕຣິງ_ຂໍ້ມູນ for ສະຕຣິງ_ຂໍ້ມູນ in ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.arguments):
        ຕົວແຍກວິເຄາະ.error('인수는 최대 7개, 각각 UTF-8 255바이트 이하입니다.')
    ຕົວເລືອກ = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.vnc: ຕົວເລືອກ += ['-vnc', ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.vnc]
    ຂະ_ບວນ_ການ = subprocess.Popen(ຄໍາສັ່ງ_1f12b8e2() + ຕົວເລືອກ, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ຕົວ_ໃຊ້_ເລືອກ = selectors.DefaultSelector(); ຕົວ_ໃຊ້_ເລືອກ.register(ຂະ_ບວນ_ການ.stdout, selectors.EVENT_READ)
    def 수신하기(확인표시, 시간제한=45):
        출력결과 = bytearray(); ຈົບ_ອອບເຊັດ = time.monotonic() + 시간제한
        while 확인표시 not in 출력결과:
            if time.monotonic() > ຈົບ_ອອບເຊັດ: raise RuntimeError('UART timeout: ' + 출력결과.decode('utf-8', 'replace'))
            for 누름값, _ in ຕົວ_ໃຊ້_ເລືອກ.select(0.1):
                조각 = 누름값.fileobj.read(4096)
                if 조각: 출력결과.extend(조각)
            if b'PANIC:' in 출력결과 or b'FAIL ' in 출력결과: raise RuntimeError(출력결과.decode('utf-8', 'replace'))
            if ຂະ_ບວນ_ການ.poll() is not None: raise RuntimeError('QEMU exited: ' + 출력결과.decode('utf-8', 'replace'))
        return bytes(출력결과)
    def ສົ່ງ(ສາຍ, 확인표시=b'jkoros-native> '):
        ຂະ_ບວນ_ການ.stdin.write(ສາຍ.encode('utf-8') + b'\n'); ຂະ_ບວນ_ການ.stdin.flush()
        return 수신하기(확인표시)
    def ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ສາຍ):
        출력결과 = ສົ່ງ(ສາຍ); sys.stdout.buffer.write(출력결과); sys.stdout.buffer.flush()
        일치 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 출력결과)
        if not 일치: raise RuntimeError('guest did not report exit status')
        return int(일치.group(1))
    try:
        수신하기(b'jkoros-native> ')
        ຟາຍ_ລາຍຊື່ = []
        for 포함항목 in ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.include:
            if 포함항목.is_dir():
                ຟາຍ_ລາຍຊື່ += [(str(ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.relative_to(포함항목).with_suffix('')).replace('/', '.') + '.class', ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ.read_bytes()) for ຂໍ້ມູນ_ຈັດຕໍາແຫນ່ງ in sorted(포함항목.rglob('*.class'))]
            else:
                ຟາຍ_ລາຍຊື່.append((포함항목.name, 포함항목.read_bytes()))
        ຟາຍ_ລາຍຊື່ = [(개수, ປາຍທາງ_ຂໍ້ມູນ) for 개수, ປາຍທາງ_ຂໍ້ມູນ in ຟາຍ_ລາຍຊື່ if 개수 != ຊື່] + [(ຊື່, ຂໍ້ມູນ)]
        for ໂອນອອກ_ຊື່, ໂອນອອກ_ຂໍ້ມູນ in ຟາຍ_ລາຍຊື່:
            if len(ໂອນອອກ_ຂໍ້ມູນ) > 16384 or len(ໂອນອອກ_ຊື່.encode('utf-8')) > 63 or '\n' in ໂອນອອກ_ຊື່ or '\r' in ໂອນອອກ_ຊື່:
                raise ValueError('추가 파일의 ຊື່/ຂະ_ຫນາດ 제한 초과: ' + ໂອນອອກ_ຊື່)
            ສົ່ງ('load ' + shlex.quote(ໂອນອອກ_ຊື່), b'hex> ')
            for 순번 in range(0, len(ໂອນອອກ_ຂໍ້ມູນ), 64): ສົ່ງ(ໂອນອອກ_ຂໍ້ມູນ[순번:순번+64].hex(), b'hex> ')
            if b'LOADED' not in ສົ່ງ('.'): raise RuntimeError('upload failed: ' + ໂອນອອກ_ຊື່)
            갈무리자료 = ສົ່ງ('hex ' + shlex.quote(ໂອນອອກ_ຊື່))
            일치 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 갈무리자료, re.S)
            if not 일치 or bytes.fromhex(''.join(일치.group(2).decode().split())) != ໂອນອອກ_ຂໍ້ມູນ: raise RuntimeError('upload verification failed')
        if ຫມວດ_ຄ່າ == '.java' and ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ('javac ' + shlex.quote(ຊື່)) != 0: return 1
        실행가능파일 = ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.file.stem + '.elf'
        if ຫມວດ_ຄ່າ == '.c' and ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ('cc ' + shlex.quote(ຊື່) + ' -o ' + shlex.quote(실행가능파일)) != 0: return 1
        ແອັບ = 'java ' + shlex.quote(ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.class_name or ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.file.stem) if ຫມວດ_ຄ່າ in ('.java', '.class') else ('python ' if ຫມວດ_ຄ່າ == '.py' else 'run ') + shlex.quote(ຊື່)
        if ຫມວດ_ຄ່າ == '.jar': ແອັບ = 'java -jar ' + shlex.quote(ຊື່)
        if ຫມວດ_ຄ່າ == '.c': ແອັບ = 'run ' + shlex.quote(실행가능파일)
        if ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.linux: ແອັບ = 'run --linux ' + shlex.quote(ຊື່)
        if ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.arguments: ແອັບ += ' ' + ' '.join(shlex.quote(ສະຕຣິງ_ຂໍ້ມູນ) for ສະຕຣິງ_ຂໍ້ມູນ in ຂໍ້ພິສູດ_ການຈັດຄ່າຮອບວຽນ.arguments)
        return 0 if ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ແອັບ) == 0 else 1
    finally:
        if ຂະ_ບວນ_ການ.poll() is None:
            ຂະ_ບວນ_ການ.terminate()
            try: ຂະ_ບວນ_ການ.wait(timeout=5)
            except subprocess.TimeoutExpired: ຂະ_ບວນ_ການ.kill(); ຂະ_ບວນ_ການ.wait(timeout=5)
        ຕົວ_ໃຊ້_ເລືອກ.close(); ຂະ_ບວນ_ການ.stdin.close(); ຂະ_ບວນ_ການ.stdout.close()


if __name__ == '__main__':
    raise SystemExit(ແລ່ນ())
