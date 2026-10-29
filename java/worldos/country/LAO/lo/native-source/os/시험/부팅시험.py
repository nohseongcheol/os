#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 직렬/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

ຈັດຕໍາແຫນ່ງ = Path(__file__).resolve().parents[1]


def 기다리기(검사, 설명, 제한=15):
    끝 = time.monotonic() + 제한
    while time.monotonic() < 끝:
        ມາດຕະການ = 검사()
        if ມາດຕະການ:
            return ມາດຕະການ
        time.sleep(0.05)
    raise AssertionError('ເວລາ_ຄ່າ 초과: ' + 설명)


def 시험(종류):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 임시:
        임시 = Path(임시)
        직렬경로 = 임시 / 'serial.sock'
        ຫນ້າຈໍ_ທາງໂຄຈອນ = 임시 / 'monitor.sock'
        ຄໍາສັ່ງ_1f12b8e2 = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(ຫນ້າຈໍ_ທາງໂຄຈອນ) + ',server,nowait']
        ຄໍາສັ່ງ_1f12b8e2 += ['-kernel', str(ຈັດຕໍາແຫນ່ງ / 'build/kernel.elf')] if 종류 == 'elf' else [
            '-cdrom', str(ຈັດຕໍາແຫນ່ງ / 'build/kernel.iso'), '-boot', 'd']
        # 직렬 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        ຄໍາສັ່ງ_1f12b8e2 += ['-S']
        ຂະ_ບວນ_ການ_ຄ່າ = subprocess.Popen(ຄໍາສັ່ງ_1f12b8e2, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        직렬 = socket.socket(socket.AF_UNIX)
        ຫນ້າຈໍ_ຄ່າ = socket.socket(socket.AF_UNIX)
        ບັນທຶກ_ແຖວ = bytearray()
        try:
            def 소켓준비():
                if ຂະ_ບວນ_ການ_ຄ່າ.poll() is not None:
                    raise AssertionError(ຂະ_ບວນ_ການ_ຄ່າ.stderr.read().decode('utf-8', 'replace'))
                return 직렬경로.exists() and ຫນ້າຈໍ_ທາງໂຄຈອນ.exists()
            기다리기(소켓준비, 'QEMU 소켓')
            직렬.connect(str(직렬경로))
            ຫນ້າຈໍ_ຄ່າ.connect(str(ຫນ້າຈໍ_ທາງໂຄຈອນ))
            직렬.setblocking(False)
            ຫນ້າຈໍ_ຄ່າ.sendall(b'cont\n')

            def 포함(ສະຕຣິງ_ຄ່າ, ແລ່ນ=0):
                읽기, _, _ = select.select([직렬], [], [], 0.1)
                if 읽기:
                    ຂໍ້ມູນ = 직렬.recv(65536)
                    if not ຂໍ້ມູນ:
                        raise AssertionError('직렬 ເຊື່ອມຕໍ່ ອອກ_ແອັບ')
                    ບັນທຶກ_ແຖວ.extend(ຂໍ້ມູນ)
                if ຂະ_ບວນ_ການ_ຄ່າ.poll() is not None:
                    raise AssertionError('QEMU 비정상 ອອກ_ແອັບ: ' + str(ຂະ_ບວນ_ການ_ຄ່າ.returncode))
                return ສະຕຣິງ_ຄ່າ.encode('utf-8') in ບັນທຶກ_ແຖວ[ແລ່ນ:]

            def 명령시험(입력, 기대):
                ແລ່ນ = len(ບັນທຶກ_ແຖວ)
                직렬.sendall(입력.encode('ascii'))
                기다리기(lambda: 포함(기대, ແລ່ນ), 기대)
                기다리기(lambda: 포함('jkoros> ', ແລ່ນ), 'ຄໍາສັ່ງ_1f12b8e2 후 프롬프트')

            기다리기(lambda: 포함('READY'), 종류 + ' 부팅')
            assert b'JAVA SELFTEST PASS' in ບັນທຶກ_ແຖວ
            assert '자바 기계어 ແກນກາງ_ຄ່າ ແລ່ນ'.encode() in ບັນທຶກ_ແຖວ
            명령시험('info\r\n', 'embedded subset JVM / polling kernel')
            명령시험('help\n', 'free N | echo TEXT')
            명령시험('mem\n', ' / 8 (각 4096바이트)')
            명령시험('echo natix\bve\n', 'native\r\n')
            for ດັດຊະນີ in range(8):
                명령시험('alloc\n', 'ຕອນ_ຄ່າ ດັດຊະນີ: ' + str(ດັດຊະນີ))
            명령시험('alloc\n', 'ຕອນ_ຄ່າ ດັດຊະນີ: -1')
            명령시험('free 3\n', '반환됨')
            명령시험('free 3\n', '할당되지 않은 ຕອນ_ຄ່າ')
            명령시험('free 99\n', '사용법: free 0..7')
            명령시험('alloc\n', 'ຕອນ_ຄ່າ ດັດຊະນີ: 3')
            명령시험('free 0\n', '반환됨')
            명령시험('test\n', 'JAVA SELFTEST PASS')
            명령시험('unknown\n', '알 수 없는 명령입니다')
            명령시험('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            ແລ່ນ = len(ບັນທຶກ_ແຖວ)
            for ກະແຈ_ຄ່າ in ('i', 'n', 'f', 'o', 'ret'):
                ຫນ້າຈໍ_ຄ່າ.sendall(('sendkey ' + ກະແຈ_ຄ່າ + ' 30\n').encode())
                time.sleep(0.09)
            기다리기(lambda: 포함('embedded subset JVM / polling kernel', ແລ່ນ), 'PS/2 info 입력')
            명령시험('echo ' + 'a' * 150 + '\n', 'a' * 123)
            직렬.sendall(b'halt\n')
            기다리기(lambda: 포함('HALTED'), '정지 ຄໍາສັ່ງ_1f12b8e2')
            assert b'PANIC' not in ບັນທຶກ_ແຖວ and b'SELFTEST FAIL' not in ບັນທຶກ_ແຖວ
            print('PASS: {} 부팅, Java 자체 시험, 직렬 ຄໍາສັ່ງ_1f12b8e2, PS/2 입력, ຈັດສັນ_ບ່ອນເກັບຂໍ້ມູນ/반환, 정지'.format(종류))
            return ບັນທຶກ_ແຖວ.decode('utf-8', 'replace')
        finally:
            직렬.close()
            ຫນ້າຈໍ_ຄ່າ.close()
            ຂະ_ບວນ_ການ_ຄ່າ.terminate()
            try:
                ຂະ_ບວນ_ການ_ຄ່າ.wait(timeout=3)
            except subprocess.TimeoutExpired:
                ຂະ_ບວນ_ການ_ຄ່າ.kill()
                ຂະ_ບວນ_ການ_ຄ່າ.wait()


if __name__ == '__main__':
    ມາດຕະການ = {종류: 시험(종류) for 종류 in ('elf', 'iso')}
    (ຈັດຕໍາແຫນ່ງ / 'build/부팅시험.json').write_text(json.dumps(ມາດຕະການ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
