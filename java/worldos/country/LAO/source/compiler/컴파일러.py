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
    def __init__(자신, ຂໍ້ມູນ):
        자신.ຂໍ້ມູນ = ຂໍ້ມູນ
        자신.ຈັດຕໍາແຫນ່ງ = 0

    def 읽기(자신, ຄວາມຍາວ_ຄ່າ):
        if ຄວາມຍາວ_ຄ່າ < 0 or 자신.ຈັດຕໍາແຫນ່ງ + ຄວາມຍາວ_ຄ່າ > len(자신.ຂໍ້ມູນ):
            raise 컴파일오류('잘린 ປະເພດສິ່ງຂອງ_ຄ່າ 또는 ຄໍາສັ່ງ_1f12b8e2 ຂໍ້ມູນ')
        ມາດຕະການ = 자신.ຂໍ້ມູນ[자신.ຈັດຕໍາແຫນ່ງ:자신.ຈັດຕໍາແຫນ່ງ + ຄວາມຍາວ_ຄ່າ]
        자신.ຈັດຕໍາແຫນ່ງ += ຄວາມຍາວ_ຄ່າ
        return ມາດຕະການ

    def 수(자신, ຮູບແບບ_ຄ່າ_d1a42ea5):
        return struct.unpack('>' + ຮູບແບບ_ຄ່າ_d1a42ea5, 자신.읽기(struct.calcsize('>' + ຮູບແບບ_ຄ່າ_d1a42ea5)))[0]


def 수정유티에프해독(ຂໍ້ມູນ):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    ສະຕຣິງ_ຄ່າ = ຂໍ້ມູນ.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return ສະຕຣິງ_ຄ່າ.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class ປະເພດສິ່ງຂອງ_ຄ່າ:
    def __init__(자신, ທາງໂຄຈອນ):
        자신.ທາງໂຄຈອນ = ທາງໂຄຈອນ
        ຜູ້ອ່ານ_ຄ່າ = 자료읽기(ທາງໂຄຈອນ.read_bytes())
        if ຜູ້ອ່ານ_ຄ່າ.수('I') != 0xcafebabe:
            raise 컴파일오류('Java ປະເພດສິ່ງຂອງ_ຄ່າ 표식이 아님')
        ຜູ້ອ່ານ_ຄ່າ.읽기(4)
        개수 = ຜູ້ອ່ານ_ຄ່າ.수('H')
        자신.ຄ່າຄົງທີ່_ຄ່າ = [None] * 개수
        ດັດຊະນີ = 1
        while ດັດຊະນີ < 개수:
            종류 = ຜູ້ອ່ານ_ຄ່າ.수('B')
            if 종류 == 1:
                ຄ່າ = 수정유티에프해독(ຜູ້ອ່ານ_ຄ່າ.읽기(ຜູ້ອ່ານ_ຄ່າ.수('H')))
            elif 종류 == 3:
                ຄ່າ = ຜູ້ອ່ານ_ຄ່າ.수('i')
            elif 종류 == 4:
                ຄ່າ = ຜູ້ອ່ານ_ຄ່າ.읽기(4)
            elif 종류 in (5, 6):
                ຄ່າ = ຜູ້ອ່ານ_ຄ່າ.읽기(8)
            elif 종류 in (7, 8, 16):
                ຄ່າ = ຜູ້ອ່ານ_ຄ່າ.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                ຄ່າ = (ຜູ້ອ່ານ_ຄ່າ.수('H'), ຜູ້ອ່ານ_ຄ່າ.수('H'))
            elif 종류 == 15:
                ຄ່າ = (ຜູ້ອ່ານ_ຄ່າ.수('B'), ຜູ້ອ່ານ_ຄ່າ.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 ຄ່າຄົງທີ່_ຄ່າ 종류: {}'.format(종류))
            자신.ຄ່າຄົງທີ່_ຄ່າ[ດັດຊະນີ] = (종류, ຄ່າ)
            ດັດຊະນີ += 2 if 종류 in (5, 6) else 1
        자신.ເຂົ້າຫາ_ເຂົ້າໃນ = ຜູ້ອ່ານ_ຄ່າ.수('H')
        자신.ຊື່ = 자신.ປະເພດສິ່ງຂອງ_ຊື່(ຜູ້ອ່ານ_ຄ່າ.수('H'))
        부모 = ຜູ້ອ່ານ_ຄ່າ.수('H')
        if 자신.ປະເພດສິ່ງຂອງ_ຊື່(부모) != 'java/lang/Object' or ຜູ້ອ່ານ_ຄ່າ.수('H') != 0:
            raise 컴파일오류(자신.ຊື່ + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.ຊ່ອງຂໍ້ມູນ_ຄ່າ = 자신.멤버읽기(ຜູ້ອ່ານ_ຄ່າ)
        자신.ຟັງ_ຄ໌_ຊັນ_ຄ່າ = 자신.멤버읽기(ຜູ້ອ່ານ_ຄ່າ)
        자신.속성읽기(ຜູ້ອ່ານ_ຄ່າ)

    def 문자(자신, ດັດຊະນີ):
        if 자신.ຄ່າຄົງທີ່_ຄ່າ[ດັດຊະນີ][0] != 1:
            raise 컴파일오류('ສະຕຣິງ_ຄ່າ ຄ່າຄົງທີ່_ຄ່າ ຮູບແບບ_ຄ່າ_d1a42ea5 ຂໍ້ຜິດພາດ')
        return 자신.ຄ່າຄົງທີ່_ຄ່າ[ດັດຊະນີ][1]

    def ປະເພດສິ່ງຂອງ_ຊື່(자신, ດັດຊະນີ):
        return 자신.문자(자신.ຄ່າຄົງທີ່_ຄ່າ[ດັດຊະນີ][1])

    def ການ_ອ້າງ_ອີງ(자신, ດັດຊະນີ):
        ເຈົ້າຂອງ_ຄ່າ, ຊື່_ຮູບແບບ = 자신.ຄ່າຄົງທີ່_ຄ່າ[ດັດຊະນີ][1]
        ຊື່, ຮູບແບບ_ຄ່າ_d1a42ea5 = 자신.ຄ່າຄົງທີ່_ຄ່າ[ຊື່_ຮູບແບບ][1]
        return 자신.ປະເພດສິ່ງຂອງ_ຊື່(ເຈົ້າຂອງ_ຄ່າ), 자신.문자(ຊື່), 자신.문자(ຮູບແບບ_ຄ່າ_d1a42ea5)

    def 속성읽기(자신, ຜູ້ອ່ານ_ຄ່າ):
        ມາດຕະການ = {}
        for _ in range(ຜູ້ອ່ານ_ຄ່າ.수('H')):
            ຊື່ = 자신.문자(ຜູ້ອ່ານ_ຄ່າ.수('H'))
            ມາດຕະການ[ຊື່] = ຜູ້ອ່ານ_ຄ່າ.읽기(ຜູ້ອ່ານ_ຄ່າ.수('I'))
        return ມາດຕະການ

    def 멤버읽기(자신, ຜູ້ອ່ານ_ຄ່າ):
        ມາດຕະການ = []
        for _ in range(ຜູ້ອ່ານ_ຄ່າ.수('H')):
            ເຂົ້າຫາ_ເຂົ້າໃນ = ຜູ້ອ່ານ_ຄ່າ.수('H')
            ຊື່ = 자신.문자(ຜູ້ອ່ານ_ຄ່າ.수('H'))
            ຮູບແບບ_ຄ່າ_d1a42ea5 = 자신.문자(ຜູ້ອ່ານ_ຄ່າ.수('H'))
            ມາດຕະການ.append((ເຂົ້າຫາ_ເຂົ້າໃນ, ຊື່, ຮູບແບບ_ຄ່າ_d1a42ea5, 자신.속성읽기(ຜູ້ອ່ານ_ຄ່າ)))
        return ມາດຕະການ


def 형식읽기(ສະຕຣິງ_ຄ່າ):
    ມາດຕະການ = []
    ຈັດຕໍາແຫນ່ງ = 0
    while ຈັດຕໍາແຫນ່ງ < len(ສະຕຣິງ_ຄ່າ):
        for ຮູບແບບ_ຄ່າ_d1a42ea5 in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if ສະຕຣິງ_ຄ່າ.startswith(ຮູບແບບ_ຄ່າ_d1a42ea5, ຈັດຕໍາແຫນ່ງ):
                ມາດຕະການ.append(ຮູບແບບ_ຄ່າ_d1a42ea5)
                ຈັດຕໍາແຫນ່ງ += len(ຮູບແບບ_ຄ່າ_d1a42ea5)
                break
        else:
            raise 컴파일오류('지원하지 않는 ປະ_ເພດ_ຂໍ້_ມູນ: ' + ສະຕຣິງ_ຄ່າ)
    return ມາດຕະການ


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('ຟັງ_ຄ໌_ຊັນ_ຄ່າ 서술 ຮູບແບບ_ຄ່າ_d1a42ea5 ຂໍ້ຜິດພາດ: ' + 서술)
    return 인수, 반환


def ສັນຍາລັກ(종류, *부분):
    ແຫຼ່ງທີ່ມາ = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(ແຫຼ່ງທີ່ມາ).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 ຟັງ_ຄ໌_ຊັນ_ຄ່າ 서술에 대해서만 허용한다.
def ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(인수=None):
    ຕົວແຍກວິເຄາະ_48ee4b1b = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK ແຫຼ່ງທີ່ມາ_ຕົ້ນໄມ້ ສ້າງ_ລະບົບ')
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/ປະເພດສິ່ງຂອງ_ຄ່າ 디렉터리')
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 ສ້າງ_ລະບົບ JDK 또는 openjdk-build의 부트 JDK ທາງໂຄຈອນ')
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('--bundle-runtime', help='ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK ແອັບ_ຕົວເປີດໃຊ້/ແຫຼ່ງທີ່ມາ_ຕົ້ນໄມ້ 빌드의 C 컴파일러')
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 ສ້າງ_ລະບົບ 작업 수')
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 ສ້າງ_ລະບົບ ເປົ້າ_ຫມາຍ (예: aarch64-linux-gnu)')
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('--sysroot', help='교차 ສ້າງ_ລະບົບ 대상의 libc/헤더/ຫໍສະຫມຸດ 루트')
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 ຮູບແບບ_ຄ່າ_d1a42ea5')
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=ປະເພດສິ່ງຂອງ_ຄ່າ.ຟັງ_ຄ໌_ຊັນ_ຄ່າ (자체 스택 ABI)')
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('--entry', help='예: 계산.ແລ່ນ (openjdk-build 이외 대상에서 필수)')
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('-o', '--output', required=True, help='ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ ELF/.o 출력; openjdk-build는 전용 ສ້າງ_ລະບົບ 디렉터리')
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('sources', nargs='+')
    ພາຣາມິເຕີ_ຂໍ້ພິສູດ = ຕົວແຍກວິເຄາະ_48ee4b1b.parse_args(인수)
    if ພາຣາມິເຕີ_ຂໍ້ພິສູດ.target == 'openjdk-build':
        if len(ພາຣາມິເຕີ_ຂໍ້ພິສູດ.sources) != 1 or not ພາຣາມິເຕີ_ຂໍ້ພິສູດ.java_home or ພາຣາມິເຕີ_ຂໍ້ພິສູດ.entry or ພາຣາມິເຕີ_ຂໍ້ພິສູດ.export or ພາຣາມິເຕີ_ຂໍ້ພິສູດ.classpath or ພາຣາມິເຕີ_ຂໍ້ພິສູດ.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK ແຫຼ່ງທີ່ມາ_ຕົ້ນໄມ້ 디렉터리 하나와 --java-home 부트 JDK, -o ສ້າງ_ລະບົບ 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(ພາຣາມິເຕີ_ຂໍ້ພິສູດ.sources[0], ພາຣາມິເຕີ_ຂໍ້ພິສູດ.output, ພາຣາມິເຕີ_ຂໍ້ພິສູດ.java_home, ພາຣາມິເຕີ_ຂໍ້ພິສູດ.jobs, ພາຣາມິເຕີ_ຂໍ້ພິສູດ.openjdk_target,
                  ພາຣາມິເຕີ_ຂໍ້ພິສູດ.sysroot, None if ພາຣາມິເຕີ_ຂໍ້ພິສູດ.cc == 'cc' else ພາຣາມິເຕີ_ຂໍ້ພິສູດ.cc, ພາຣາມິເຕີ_ຂໍ້ພິສູດ.cxx, ພາຣາມິເຕີ_ຂໍ້ພິສູດ.configure_arg)
        except BuildError as ຂໍ້ຜິດພາດ:
            raise 컴파일오류(str(ຂໍ້ຜິດພາດ))
        return
    if not ພາຣາມິເຕີ_ຂໍ້ພິສູດ.entry:
        ຕົວແຍກວິເຄາະ_48ee4b1b.error('--entry is required for this target')
    if ພາຣາມິເຕີ_ຂໍ້ພິສູດ.cxx or ພາຣາມິເຕີ_ຂໍ້ພິສູດ.openjdk_target or ພາຣາມິເຕີ_ຂໍ້ພິສູດ.sysroot or ພາຣາມິເຕີ_ຂໍ້ພິສູດ.configure_arg or ພາຣາມິເຕີ_ຂໍ້ພິສູດ.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build ເປົ້າ_ຫມາຍ 전용')
    if ພາຣາມິເຕີ_ຂໍ້ພິສູດ.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import ສ້າງ_ເຂົ້າໃນ
        ສ້າງ_ເຂົ້າໃນ(ພາຣາມິເຕີ_ຂໍ້ພິສູດ)
        return
    if ພາຣາມິເຕີ_ຂໍ້ພິສູດ.classpath or ພາຣາມິເຕີ_ຂໍ້ພິສູດ.java_home or ພາຣາມິເຕີ_ຂໍ້ພິສູດ.bundle_runtime or ພາຣາມິເຕີ_ຂໍ້ພິສູດ.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk ເປົ້າ_ຫມາຍ 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', ພາຣາມິເຕີ_ຂໍ້ພິສູດ.target, '--entry', ພາຣາມິເຕີ_ຂໍ້ພິສູດ.entry, '-o', ພາຣາມິເຕີ_ຂໍ້ພິສູດ.output]
    for ມອບຫມາຍ_ຄ່າ in ພາຣາມິເຕີ_ຂໍ້ພິສູດ.export: 자바명령.extend(['--export', ມອບຫມາຍ_ຄ່າ])
    subprocess.run(자바명령+ພາຣາມິເຕີ_ຂໍ້ພິສູດ.sources, check=True)
    return


if __name__ == '__main__':
    try:
        ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as ຂໍ້ຜິດພາດ:
        print('ສ້າງ_ແຫຼ່ງທີ່ມາ ຂໍ້ຜິດພາດ: ' + str(ຂໍ້ຜິດພາດ), file=sys.stderr)
        sys.exit(1)
