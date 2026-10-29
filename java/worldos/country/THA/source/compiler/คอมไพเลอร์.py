#!/usr/bin/env python3
"""제한형 Java의 검증된 javac 바이트코드를 x86 ELF32 네이티브 코드로 변환한다."""
import argparse
import hashlib
import json
import re
from pathlib import Path
import struct
import subprocess
import sys
import tempfile


class 컴파일오류(Exception):
    pass


class 자료읽기:
    def __init__(자신, ข้อมูล):
        자신.ข้อมูล = ข้อมูล
        자신.ตําแหน่ง = 0

    def อ่าน(자신, 길이):
        if 길이 < 0 or 자신.ตําแหน่ง + 길이 > len(자신.ข้อมูล):
            raise 컴파일오류('잘린 คลาส_ค่า 또는 คําสั่ง ข้อมูล')
        ผลลัพธ์ = 자신.ข้อมูล[자신.ตําแหน่ง:자신.ตําแหน่ง + 길이]
        자신.ตําแหน่ง += 길이
        return ผลลัพธ์

    def หมายเลข(자신, รูปแบบ_ค่า_d1a42ea5):
        return struct.unpack('>' + รูปแบบ_ค่า_d1a42ea5, 자신.อ่าน(struct.calcsize('>' + รูปแบบ_ค่า_d1a42ea5)))[0]


def 수정유티에프해독(ข้อมูล):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    สตริง_ค่า = ข้อมูล.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return สตริง_ค่า.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class คลาส_ค่า:
    def __init__(자신, เส้นทาง):
        자신.เส้นทาง = เส้นทาง
        ผู้อ่าน_ค่า = 자료읽기(เส้นทาง.read_bytes())
        if ผู้อ่าน_ค่า.หมายเลข('I') != 0xcafebabe:
            raise 컴파일오류('Java คลาส_ค่า 표식이 아님')
        ผู้อ่าน_ค่า.อ่าน(4)
        개수 = ผู้อ่าน_ค่า.หมายเลข('H')
        자신.ค่าคงที่_ค่า = [None] * 개수
        ดัชนี = 1
        while ดัชนี < 개수:
            종류 = ผู้อ่าน_ค่า.หมายเลข('B')
            if 종류 == 1:
                ค่า = 수정유티에프해독(ผู้อ่าน_ค่า.อ่าน(ผู้อ่าน_ค่า.หมายเลข('H')))
            elif 종류 == 3:
                ค่า = ผู้อ่าน_ค่า.หมายเลข('i')
            elif 종류 == 4:
                ค่า = ผู้อ่าน_ค่า.อ่าน(4)
            elif 종류 in (5, 6):
                ค่า = ผู้อ่าน_ค่า.อ่าน(8)
            elif 종류 in (7, 8, 16):
                ค่า = ผู้อ่าน_ค่า.หมายเลข('H')
            elif 종류 in (9, 10, 11, 12, 18):
                ค่า = (ผู้อ่าน_ค่า.หมายเลข('H'), ผู้อ่าน_ค่า.หมายเลข('H'))
            elif 종류 == 15:
                ค่า = (ผู้อ่าน_ค่า.หมายเลข('B'), ผู้อ่าน_ค่า.หมายเลข('H'))
            else:
                raise 컴파일오류('지원하지 않는 ค่าคงที่_ค่า 종류: {}'.format(종류))
            자신.ค่าคงที่_ค่า[ดัชนี] = (종류, ค่า)
            ดัชนี += 2 if 종류 in (5, 6) else 1
        자신.เข้าถึง_รายการ = ผู้อ่าน_ค่า.หมายเลข('H')
        자신.ชื่อ = 자신.ชื่อคลาส(ผู้อ่าน_ค่า.หมายเลข('H'))
        แม่_ค่า = ผู้อ่าน_ค่า.หมายเลข('H')
        if 자신.ชื่อคลาส(แม่_ค่า) != 'java/lang/Object' or ผู้อ่าน_ค่า.หมายเลข('H') != 0:
            raise 컴파일오류(자신.ชื่อ + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.ค่าเขตข้อมูล = 자신.멤버읽기(ผู้อ่าน_ค่า)
        자신.ฟังก์ชัน_ค่า = 자신.멤버읽기(ผู้อ่าน_ค่า)
        자신.속성읽기(ผู้อ่าน_ค่า)

    def 문자(자신, ดัชนี):
        if 자신.ค่าคงที่_ค่า[ดัชนี][0] != 1:
            raise 컴파일오류('สตริง_ค่า ค่าคงที่_ค่า รูปแบบ_ค่า_d1a42ea5 ข้อผิดพลาด')
        return 자신.ค่าคงที่_ค่า[ดัชนี][1]

    def ชื่อคลาส(자신, ดัชนี):
        return 자신.문자(자신.ค่าคงที่_ค่า[ดัชนี][1])

    def อ้างอิง(자신, ดัชนี):
        เจ้าของ_ค่า, ชื่อ_รูปแบบ = 자신.ค่าคงที่_ค่า[ดัชนี][1]
        ชื่อ, รูปแบบ_ค่า_d1a42ea5 = 자신.ค่าคงที่_ค่า[ชื่อ_รูปแบบ][1]
        return 자신.ชื่อคลาส(เจ้าของ_ค่า), 자신.문자(ชื่อ), 자신.문자(รูปแบบ_ค่า_d1a42ea5)

    def 속성읽기(자신, ผู้อ่าน_ค่า):
        ผลลัพธ์ = {}
        for _ in range(ผู้อ่าน_ค่า.หมายเลข('H')):
            ชื่อ = 자신.문자(ผู้อ่าน_ค่า.หมายเลข('H'))
            ผลลัพธ์[ชื่อ] = ผู้อ่าน_ค่า.อ่าน(ผู้อ่าน_ค่า.หมายเลข('I'))
        return ผลลัพธ์

    def 멤버읽기(자신, ผู้อ่าน_ค่า):
        ผลลัพธ์ = []
        for _ in range(ผู้อ่าน_ค่า.หมายเลข('H')):
            เข้าถึง_รายการ = ผู้อ่าน_ค่า.หมายเลข('H')
            ชื่อ = 자신.문자(ผู้อ่าน_ค่า.หมายเลข('H'))
            รูปแบบ_ค่า_d1a42ea5 = 자신.문자(ผู้อ่าน_ค่า.หมายเลข('H'))
            ผลลัพธ์.append((เข้าถึง_รายการ, ชื่อ, รูปแบบ_ค่า_d1a42ea5, 자신.속성읽기(ผู้อ่าน_ค่า)))
        return ผลลัพธ์


def 형식읽기(สตริง_ค่า):
    ผลลัพธ์ = []
    ตําแหน่ง = 0
    while ตําแหน่ง < len(สตริง_ค่า):
        for รูปแบบ_ค่า_d1a42ea5 in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if สตริง_ค่า.startswith(รูปแบบ_ค่า_d1a42ea5, ตําแหน่ง):
                ผลลัพธ์.append(รูปแบบ_ค่า_d1a42ea5)
                ตําแหน่ง += len(รูปแบบ_ค่า_d1a42ea5)
                break
        else:
            raise 컴파일오류('지원하지 않는 ชนิดข้อมูล: ' + สตริง_ค่า)
    return ผลลัพธ์


def 함수형식(서술):
    อาร์กิวเมนต์, ส่งคืน_เมตริก = 서술[1:].split(')')
    อาร์กิวเมนต์ = 형식읽기(อาร์กิวเมนต์)
    ส่งคืน_ชนิด = 형식읽기(ส่งคืน_เมตริก)
    if 'V' in อาร์กิวเมนต์ or len(ส่งคืน_ชนิด) != 1:
        raise 컴파일오류('ฟังก์ชัน_ค่า 서술 รูปแบบ_ค่า_d1a42ea5 ข้อผิดพลาด: ' + 서술)
    return อาร์กิวเมนต์, ส่งคืน_เมตริก


def สัญลักษณ์(종류, *부분):
    รหัสต้นฉบับ = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(รหัสต้นฉบับ).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 ฟังก์ชัน_ค่า 서술에 대해서만 허용한다.
def ดําเนินการ_คําสั่ง(อาร์กิวเมนต์=None):
    ตัวแยกวิเคราะห์_48ee4b1b = argparse.ArgumentParser(description='เอง Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK แหล่ง_ทรี สร้าง')
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 ผนวก_รายการ JAR/คลาส_ค่า 디렉터리')
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 สร้าง JDK 또는 openjdk-build의 부트 JDK เส้นทาง')
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--bundle-runtime', help='ดําเนินการ_คําสั่ง 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK แอป_ลิ้นชักแอป/แหล่ง_ทรี 빌드의 C คอมไพเลอร์')
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ คอมไพเลอร์')
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 สร้าง 작업 หมายเลข')
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 สร้าง เป้าหมาย (예: aarch64-linux-gnu)')
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--sysroot', help='교차 สร้าง 대상의 libc/헤더/ไลบรารี 루트')
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 รูปแบบ_ค่า_d1a42ea5')
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=คลาส_ค่า.ฟังก์ชัน_ค่า (เอง ตัวถูกดําเนินการ_สแตก ABI)')
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('--entry', help='예: 계산.เรียกใช้งาน (openjdk-build 이외 대상에서 필수)')
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('-o', '--output', required=True, help='ดําเนินการ_คําสั่ง ELF/.o ข้อความออก; openjdk-build는 전용 สร้าง 디렉터리')
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('sources', nargs='+')
    พารามิเตอร์_อาร์กิวเมนต์ = ตัวแยกวิเคราะห์_48ee4b1b.parse_args(อาร์กิวเมนต์)
    if พารามิเตอร์_อาร์กิวเมนต์.target == 'openjdk-build':
        if len(พารามิเตอร์_อาร์กิวเมนต์.sources) != 1 or not พารามิเตอร์_อาร์กิวเมนต์.java_home or พารามิเตอร์_อาร์กิวเมนต์.entry or พารามิเตอร์_อาร์กิวเมนต์.export or พารามิเตอร์_อาร์กิวเมนต์.classpath or พารามิเตอร์_อาร์กิวเมนต์.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK แหล่ง_ทรี 디렉터리 하나와 --java-home 부트 JDK, -o สร้าง 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(พารามิเตอร์_อาร์กิวเมนต์.sources[0], พารามิเตอร์_อาร์กิวเมนต์.output, พารามิเตอร์_อาร์กิวเมนต์.java_home, พารามิเตอร์_อาร์กิวเมนต์.jobs, พารามิเตอร์_อาร์กิวเมนต์.openjdk_target,
                  พารามิเตอร์_อาร์กิวเมนต์.sysroot, None if พารามิเตอร์_อาร์กิวเมนต์.cc == 'cc' else พารามิเตอร์_อาร์กิวเมนต์.cc, พารามิเตอร์_อาร์กิวเมนต์.cxx, พารามิเตอร์_อาร์กิวเมนต์.configure_arg)
        except BuildError as ข้อผิดพลาด:
            raise 컴파일오류(str(ข้อผิดพลาด))
        return
    if not พารามิเตอร์_อาร์กิวเมนต์.entry:
        ตัวแยกวิเคราะห์_48ee4b1b.error('--entry is required for this target')
    if พารามิเตอร์_อาร์กิวเมนต์.cxx or พารามิเตอร์_อาร์กิวเมนต์.openjdk_target or พารามิเตอร์_อาร์กิวเมนต์.sysroot or พารามิเตอร์_อาร์กิวเมนต์.configure_arg or พารามิเตอร์_อาร์กิวเมนต์.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build เป้าหมาย 전용')
    if พารามิเตอร์_อาร์กิวเมนต์.target == 'openjdk':
        sys.modules.setdefault('คอมไพเลอร์', sys.modules[__name__])
        from แฟ้มปฏิบัติการ import เปิด_รายการ
        เปิด_รายการ(พารามิเตอร์_อาร์กิวเมนต์)
        return
    if พารามิเตอร์_อาร์กิวเมนต์.classpath or พารามิเตอร์_อาร์กิวเมนต์.java_home or พารามิเตอร์_อาร์กิวเมนต์.bundle_runtime or พารามิเตอร์_อาร์กิวเมนต์.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk เป้าหมาย 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', พารามิเตอร์_อาร์กิวเมนต์.target, '--entry', พารามิเตอร์_อาร์กิวเมนต์.entry, '-o', พารามิเตอร์_อาร์กิวเมนต์.output]
    for กําหนด_ค่า in พารามิเตอร์_อาร์กิวเมนต์.export: 자바명령.extend(['--export', กําหนด_ค่า])
    subprocess.run(자바명령+พารามิเตอร์_อาร์กิวเมนต์.sources, check=True)
    return


if __name__ == '__main__':
    try:
        ดําเนินการ_คําสั่ง()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as ข้อผิดพลาด:
        print('คอมไพล์_แหล่ง ข้อผิดพลาด: ' + str(ข้อผิดพลาด), file=sys.stderr)
        sys.exit(1)
