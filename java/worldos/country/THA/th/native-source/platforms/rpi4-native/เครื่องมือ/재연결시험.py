#!/usr/bin/env python3
"""การกระจาย_ค่า 자료만으로 LGPL 재연결과 수정한 TinyCC의 ค่าจริง_ข้อมูล 게스트 실행을 검사한다."""
import argparse
import hashlib
import json
from pathlib import Path
import selectors
import subprocess
import tarfile
import tempfile
import time
from ดําเนินการ_คําสั่ง import แสดง_ราก, คําสั่ง


def เรียกใช้งาน():
    ตัวแยกวิเคราะห์_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--sdk', type=Path, default=แสดง_ราก.parent / 'rpi4/build/rootfs')
    อาร์กิวเมนต์ = ตัวแยกวิเคราะห์_48ee4b1b.parse_args()
    ข้อความออก = แสดง_ราก / 'build/verification/cosl-relink'
    ข้อความออก.mkdir(parents=True, exist_ok=True)
    รายงาน_ค่า = {'passed': False, 'physical_board_tested': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((แสดง_ราก / 'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-relink-') as 임시:
            เส้นทาง = Path(임시)
            with tarfile.open(str(แสดง_ราก / 'dist/jkoros-native-relink.tar.gz')) as กลุ่ม_ค่า:
                for รายการ_ค่า in กลุ่ม_ค่า.getmembers():
                    if เส้นทาง not in (เส้นทาง / รายการ_ค่า.name).resolve().parents or รายการ_ค่า.issym() or รายการ_ค่า.islnk():
                        raise AssertionError('Unsafe relink archive member: ' + รายการ_ค่า.name)
                กลุ่ม_ค่า.extractall(str(เส้นทาง))
            รหัสต้นฉบับ = เส้นทาง / 'jkoros-native-relink'
            def 재연결(ชื่อ, 인수들):
                with (ข้อความออก / ชื่อ).open('wb') as บันทึก_สถิติ:
                    subprocess.run(['python3', 'relink.py'] + 인수들, cwd=str(รหัสต้นฉบับ),
                                   stdout=บันทึก_สถิติ, stderr=subprocess.STDOUT, check=True, timeout=180)
            재연결('original.log', ['--verify'])
            รายงาน_ค่า['checks'].append('Recompiled libassh and reproduced original kernel SHA256 outside source tree')
            # Only the extracted test copy is modified. The actual vendored source stays unchanged.
            คอมไพเลอร์_เครื่องมือ = รหัสต้นฉบับ / 'vendor/tinycc/libtcc.c'
            เนื้อความ = คอมไพเลอร์_เครื่องมือ.read_text()
            ตําแหน่ง = '    tcc_set_lib_path(s, CONFIG_TCCDIR);'
            assert เนื้อความ.count(ตําแหน่ง) == 1
            คอมไพเลอร์_เครื่องมือ.write_text(เนื้อความ.replace(ตําแหน่ง, ตําแหน่ง + '\n    tcc_define_symbol(s, "JKOROS_RELINK_TEST", "2026");'))
            재연결('modified-tinycc.log', ['--tinycc', '--sdk', str(อาร์กิวเมนต์.sdk.resolve()),
                                         '--libassh-archive', 'build/relinked/libassh.a'])
            รูป_ค่า = รหัสต้นฉบับ / 'build/relinked/kernel8.img'
            รายงาน_ค่า['modified_kernel_sha256'] = hashlib.sha256(รูป_ค่า.read_bytes()).hexdigest()
            assert รายงาน_ค่า['modified_kernel_sha256'] != รายงาน_ค่า['kernel_sha256']
            รายงาน_ค่า['checks'].append('Modified TinyCC source rebuilt and replaced embedded cc ELF with updated size table')
            인수들 = คําสั่ง()
            인수들[인수들.index('-kernel') + 1] = str(รูป_ค่า)
            กระบวนการ_ค่า = subprocess.Popen(인수들 + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            บันทึก_สถิติ = bytearray()
            การเลือก_ค่า = selectors.DefaultSelector()
            การเลือก_ค่า.register(กระบวนการ_ค่า.stdout, selectors.EVENT_READ)
            def ภาวะรอ(แสดง_ค่า=b'jkoros-native> ', 처음=0):
                끝 = time.monotonic() + 40
                while แสดง_ค่า not in บันทึก_สถิติ[처음:]:
                    if time.monotonic() > 끝 or กระบวนการ_ค่า.poll() is not None:
                        raise AssertionError('Missing ' + repr(แสดง_ค่า) + '\n' + บันทึก_สถิติ[처음:].decode('utf-8', 'replace'))
                    for รายการ_ค่า, _ in การเลือก_ค่า.select(.1):
                        ข้อมูล = รายการ_ค่า.fileobj.read(65536)
                        if ข้อมูล:
                            บันทึก_สถิติ.extend(ข้อมูล)
                return bytes(บันทึก_สถิติ[처음:])
            def ส่ง(คํา_ข้อความ, แสดง_ค่า=b'jkoros-native> '):
                처음 = len(บันทึก_สถิติ)
                กระบวนการ_ค่า.stdin.write(คํา_ข้อความ.encode() + b'\n')
                กระบวนการ_ค่า.stdin.flush()
                return ภาวะรอ(แสดง_ค่า, 처음)
            try:
                ภาวะรอ()
                시험 = '#include <파일규약.h>\n#if JKOROS_RELINK_TEST != 2026\n#error Modified_TinyCC_required\n#endif\nint main(void){const char s[]="LGPL_RELINKED_TINYCC_2026\\n";return 파일자료쓰기(1,s,sizeof(s)-1)==sizeof(s)-1?0:1;}\n'.encode()
                ส่ง('load /relink.c', b'hex> ')
                for ดัชนีชี้ตําแหน่ง in range(0, len(시험), 64):
                    ส่ง(시험[ดัชนีชี้ตําแหน่ง:ดัชนีชี้ตําแหน่ง+64].hex(), b'hex> ')
                assert b'LOADED' in ส่ง('.')
                ผลลัพธ์ = ส่ง('cc /relink.c -o /relink')
                assert b'Compiled native ARM64 ELF' in ผลลัพธ์, ผลลัพธ์
                ผลลัพธ์ = ส่ง('run /relink')
                assert b'LGPL_RELINKED_TINYCC_2026' in ผลลัพธ์ and b'exit 0' in ผลลัพธ์, ผลลัพธ์
                รายงาน_ค่า['checks'].append('Booted modified kernel; guest cc compiled source requiring new macro; resulting ELF executed')
            finally:
                การเลือก_ค่า.close()
                if กระบวนการ_ค่า.poll() is None:
                    กระบวนการ_ค่า.terminate()
                    try:
                        กระบวนการ_ค่า.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        กระบวนการ_ค่า.kill()
                        กระบวนการ_ค่า.wait()
                (ข้อความออก / 'guest.log').write_bytes(บันทึก_สถิติ)
        รายงาน_ค่า['passed'] = True
        print(json.dumps(รายงาน_ค่า, ensure_ascii=False, indent=2))
    finally:
        (ข้อความออก / 'report.json').write_text(json.dumps(รายงาน_ค่า, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    เรียกใช้งาน()
