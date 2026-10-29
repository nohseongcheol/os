#!/usr/bin/env python3
"""배포 자료만으로 LGPL 재연결과 수정한 TinyCC의 ຕົວ_ຈິງ_ຂໍ້ມູນ 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ import ໂຄງ_ການ_ເລກຮາກ, ຄໍາສັ່ງ_1f12b8e2


def ແລ່ນ():
    ຕົວແຍກວິເຄາະ_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('--sdk', type=Path, default=ໂຄງ_ການ_ເລກຮາກ.parent / 'rpi4/build/rootfs')
    인수 = ຕົວແຍກວິເຄາະ_48ee4b1b.parse_args()
    출력 = ໂຄງ_ການ_ເລກຮາກ / 'build/verification/cosl-relink'
    출력.mkdir(parents=True, exist_ok=True)
    ລາຍງານ_ຄ່າ = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((ໂຄງ_ການ_ເລກຮາກ / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            ທາງໂຄຈອນ = Path(임시)
            with tarfile.open(str(ໂຄງ_ການ_ເລກຮາກ / 'dist/jkoros-native-relink.tar.gz')) as ກຸ່ມ_ຄ່າ:
                for ເຂົ້າໃນ_ຄ່າ in ກຸ່ມ_ຄ່າ.getmembers():
                    if ທາງໂຄຈອນ not in (ທາງໂຄຈອນ / ເຂົ້າໃນ_ຄ່າ.name).resolve().parents or ເຂົ້າໃນ_ຄ່າ.issym() or ເຂົ້າໃນ_ຄ່າ.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + ເຂົ້າໃນ_ຄ່າ.name)
                ກຸ່ມ_ຄ່າ.extractall(str(ທາງໂຄຈອນ))
            ແຫຼ່ງທີ່ມາ = ທາງໂຄຈອນ / 'jkoros-native-relink'
            def 재연결(ຊື່, 인수들):
                with (출력 / ຊື່).open('wb') as ບັນທຶກ_ແຖວ:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(ແຫຼ່ງທີ່ມາ),
                                   stdout=ບັນທຶກ_ແຖວ, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            ລາຍງານ_ຄ່າ['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            번역기 = ແຫຼ່ງທີ່ມາ / 'vendor/tinycc/libtcc.c'
            ເນື້ອໃນເອກະສານ = 번역기.read_text()
            ຈັດຕໍາແຫນ່ງ = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert ເນື້ອໃນເອກະສານ.count(ຈັດຕໍາແຫນ່ງ) == 1
            번역기.write_text(ເນື້ອໃນເອກະສານ.replace(ຈັດຕໍາແຫນ່ງ, ຈັດຕໍາແຫນ່ງ + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(인수.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            ຮູບ_ຄ່າ = ແຫຼ່ງທີ່ມາ / 'build/relinked/kernel8.img'
            ລາຍງານ_ຄ່າ['modified_kernel_sha256'] = hashlib.sha256(ຮູບ_ຄ່າ.read_bytes()).hexdigest()
            assert ລາຍງານ_ຄ່າ['modified_kernel_sha256'] != ລາຍງານ_ຄ່າ['kernel_sha256']
            ລາຍງານ_ຄ່າ['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = ຄໍາສັ່ງ_1f12b8e2()
            인수들[인수들.index('-kernel') + 1] = str(ຮູບ_ຄ່າ)
            ຂະ_ບວນ_ການ_ຄ່າ = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            ບັນທຶກ_ແຖວ = bytearray()
            ການ_ເລືອກ_ຄ່າ = selectors.DefaultSelector()
            ການ_ເລືອກ_ຄ່າ.register(ຂະ_ບວນ_ການ_ຄ່າ.stdout, selectors.EVENT_READ)
            def ລໍຖ້າ_ສະຖານະ(ລາຍການ_ຄ່າ=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while ລາຍການ_ຄ່າ not in ບັນທຶກ_ແຖວ[처음:]:
                    if time.monotonic() > 끝 or ຂະ_ບວນ_ການ_ຄ່າ.poll() is not None:
                        raise AssertionError('Missing ' + repr(ລາຍການ_ຄ່າ) + '\n' + ບັນທຶກ_ແຖວ[처음:].decode('utf-8', 'replace'))
                    for ເຂົ້າໃນ_ຄ່າ, _ in ການ_ເລືອກ_ຄ່າ.select(.1):
                        ຂໍ້ມູນ = ເຂົ້າໃນ_ຄ່າ.fileobj.read(65536)
                        if ຂໍ້ມູນ:
                            ບັນທຶກ_ແຖວ.extend(ຂໍ້ມູນ)
                return bytes(ບັນທຶກ_ແຖວ[처음:])
            def ສົ່ງ(ຄໍາ_ເວົ້າ_ຂໍ້ຄວາມ, ລາຍການ_ຄ່າ=b'jkoros-native> '):
                처음 = len(ບັນທຶກ_ແຖວ)
                ຂະ_ບວນ_ການ_ຄ່າ.stdin.write(ຄໍາ_ເວົ້າ_ຂໍ້ຄວາມ.encode() + b'\n')
                ຂະ_ບວນ_ການ_ຄ່າ.stdin.flush()
                return ລໍຖ້າ_ສະຖານະ(ລາຍການ_ຄ່າ, 처음)
            try:
                ລໍຖ້າ_ສະຖານະ()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return ຂຽນ_ຟາຍ_ຂໍ້ມູນ(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                ສົ່ງ('load /relink.c', b'hex> ')
                for ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ in range(0, len(시험), 64):
                    ສົ່ງ(시험[ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ:ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ+64].hex(), b'hex> ')
                assert b'LOADED' in ສົ່ງ('.')
                ມາດຕະການ = ສົ່ງ('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in ມາດຕະການ, ມາດຕະການ
                ມາດຕະການ = ສົ່ງ('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in ມາດຕະການ and b'exit 0' in ມາດຕະການ, ມາດຕະການ
                ລາຍງານ_ຄ່າ['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                ການ_ເລືອກ_ຄ່າ.close()
                if ຂະ_ບວນ_ການ_ຄ່າ.poll() is None:
                    ຂະ_ບວນ_ການ_ຄ່າ.terminate()
                    try:
                        ຂະ_ບວນ_ການ_ຄ່າ.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        ຂະ_ບວນ_ການ_ຄ່າ.kill()
                        ຂະ_ບວນ_ການ_ຄ່າ.wait()
                (출력 / 'guest.log').write_bytes(ບັນທຶກ_ແຖວ)
        ລາຍງານ_ຄ່າ['passed'] = True
        print(json.dumps(ລາຍງານ_ຄ່າ, ensure_ascii=False, indent=2))
    finally:
        (출력 / 'report.json').write_text(json.dumps(ລາຍງານ_ຄ່າ, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    ແລ່ນ()
