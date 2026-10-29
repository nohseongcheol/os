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
    def __init__(자신, داده_ها):
        자신.داده_ها = داده_ها
        자신.مرتب_کردن = 0

    def خواندن(자신, طول_مقدار):
        if طول_مقدار < 0 or 자신.مرتب_کردن + طول_مقدار > len(자신.داده_ها):
            raise 컴파일오류('잘린 کلاس_مقدار 또는 فرمان داده_ها')
        سنجش = 자신.داده_ها[자신.مرتب_کردن:자신.مرتب_کردن + طول_مقدار]
        자신.مرتب_کردن += طول_مقدار
        return سنجش

    def 수(자신, قالب_مقدار):
        return struct.unpack('>' + قالب_مقدار, 자신.خواندن(struct.calcsize('>' + قالب_مقدار)))[0]


def 수정유티에프해독(داده_ها):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    رشته_مقدار_6ca8363c = داده_ها.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return رشته_مقدار_6ca8363c.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class کلاس_مقدار:
    def __init__(자신, مسیر):
        자신.مسیر = مسیر
        خواننده_مقدار = 자료읽기(مسیر.read_bytes())
        if خواننده_مقدار.수('I') != 0xcafebabe:
            raise 컴파일오류('Java کلاس_مقدار 표식이 아님')
        خواننده_مقدار.خواندن(4)
        개수 = خواننده_مقدار.수('H')
        자신.ثابت_مقدار = [None] * 개수
        فهرست = 1
        while فهرست < 개수:
            종류 = خواننده_مقدار.수('B')
            if 종류 == 1:
                مقدار = 수정유티에프해독(خواننده_مقدار.خواندن(خواننده_مقدار.수('H')))
            elif 종류 == 3:
                مقدار = خواننده_مقدار.수('i')
            elif 종류 == 4:
                مقدار = خواننده_مقدار.خواندن(4)
            elif 종류 in (5, 6):
                مقدار = خواننده_مقدار.خواندن(8)
            elif 종류 in (7, 8, 16):
                مقدار = خواننده_مقدار.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                مقدار = (خواننده_مقدار.수('H'), خواننده_مقدار.수('H'))
            elif 종류 == 15:
                مقدار = (خواننده_مقدار.수('B'), خواننده_مقدار.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 ثابت_مقدار 종류: {}'.format(종류))
            자신.ثابت_مقدار[فهرست] = (종류, مقدار)
            فهرست += 2 if 종류 in (5, 6) else 1
        자신.دسترسی_ورودی = خواننده_مقدار.수('H')
        자신.نام = 자신.کلاس_نام(خواننده_مقدار.수('H'))
        부모 = خواننده_مقدار.수('H')
        if 자신.کلاس_نام(부모) != 'java/lang/Object' or خواننده_مقدار.수('H') != 0:
            raise 컴파일오류(자신.نام + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.فیلد_مقدار = 자신.멤버읽기(خواننده_مقدار)
        자신.عملکرد_مقدار = 자신.멤버읽기(خواننده_مقدار)
        자신.속성읽기(خواننده_مقدار)

    def 문자(자신, فهرست):
        if 자신.ثابت_مقدار[فهرست][0] != 1:
            raise 컴파일오류('رشته_مقدار_6ca8363c ثابت_مقدار قالب_مقدار خطا')
        return 자신.ثابت_مقدار[فهرست][1]

    def کلاس_نام(자신, فهرست):
        return 자신.문자(자신.ثابت_مقدار[فهرست][1])

    def مرجع(자신, فهرست):
        مالک_مقدار, نام_قالب = 자신.ثابت_مقدار[فهرست][1]
        نام, قالب_مقدار = 자신.ثابت_مقدار[نام_قالب][1]
        return 자신.کلاس_نام(مالک_مقدار), 자신.문자(نام), 자신.문자(قالب_مقدار)

    def 속성읽기(자신, خواننده_مقدار):
        سنجش = {}
        for _ in range(خواننده_مقدار.수('H')):
            نام = 자신.문자(خواننده_مقدار.수('H'))
            سنجش[نام] = خواننده_مقدار.خواندن(خواننده_مقدار.수('I'))
        return سنجش

    def 멤버읽기(자신, خواننده_مقدار):
        سنجش = []
        for _ in range(خواننده_مقدار.수('H')):
            دسترسی_ورودی = خواننده_مقدار.수('H')
            نام = 자신.문자(خواننده_مقدار.수('H'))
            قالب_مقدار = 자신.문자(خواننده_مقدار.수('H'))
            سنجش.append((دسترسی_ورودی, نام, قالب_مقدار, 자신.속성읽기(خواننده_مقدار)))
        return سنجش


def 형식읽기(رشته_مقدار_6ca8363c):
    سنجش = []
    مرتب_کردن = 0
    while مرتب_کردن < len(رشته_مقدار_6ca8363c):
        for قالب_مقدار in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if رشته_مقدار_6ca8363c.startswith(قالب_مقدار, مرتب_کردن):
                سنجش.append(قالب_مقدار)
                مرتب_کردن += len(قالب_مقدار)
                break
        else:
            raise 컴파일오류('지원하지 않는 نوع_داده_ها: ' + رشته_مقدار_6ca8363c)
    return سنجش


def 함수형식(서술):
    نشانوندها, بازگرداندن_سنجش = 서술[1:].split(')')
    نشانوندها = 형식읽기(نشانوندها)
    بازگرداندن_تایپ_کردن = 형식읽기(بازگرداندن_سنجش)
    if 'V' in نشانوندها or len(بازگرداندن_تایپ_کردن) != 1:
        raise 컴파일오류('عملکرد_مقدار 서술 قالب_مقدار خطا: ' + 서술)
    return نشانوندها, بازگرداندن_سنجش


def نماد(종류, *부분):
    مبداء = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(مبداء).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 عملکرد_مقدار 서술에 대해서만 허용한다.
def اجرا_فرمان(نشانوندها=None):
    مفسر_48ee4b1b = argparse.ArgumentParser(description='بومی Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK منبع_درخت ساخت_سیستم')
    مفسر_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    مفسر_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/کلاس_مقدار 디렉터리')
    مفسر_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 ساخت_سیستم JDK 또는 openjdk-build의 부트 JDK مسیر')
    مفسر_48ee4b1b.add_argument('--bundle-runtime', help='اجرا_فرمان 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    مفسر_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK برنامه_راه_انداز/منبع_درخت 빌드의 C 컴파일러')
    مفسر_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    مفسر_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 ساخت_سیستم 작업 수')
    مفسر_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 ساخت_سیستم هدف (예: aarch64-linux-gnu)')
    مفسر_48ee4b1b.add_argument('--sysroot', help='교차 ساخت_سیستم 대상의 libc/헤더/کتابخانه 루트')
    مفسر_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 قالب_مقدار')
    مفسر_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=کلاس_مقدار.عملکرد_مقدار (بومی 스택 ABI)')
    مفسر_48ee4b1b.add_argument('--entry', help='예: 계산.اجرا_2 (openjdk-build 이외 대상에서 필수)')
    مفسر_48ee4b1b.add_argument('-o', '--output', required=True, help='اجرا_فرمان ELF/.o خروجی; openjdk-build는 전용 ساخت_سیستم 디렉터리')
    مفسر_48ee4b1b.add_argument('sources', nargs='+')
    پارامتر_آرگومان = مفسر_48ee4b1b.parse_args(نشانوندها)
    if پارامتر_آرگومان.target == 'openjdk-build':
        if len(پارامتر_آرگومان.sources) != 1 or not پارامتر_آرگومان.java_home or پارامتر_آرگومان.entry or پارامتر_آرگومان.export or پارامتر_آرگومان.classpath or پارامتر_آرگومان.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK منبع_درخت 디렉터리 하나와 --java-home 부트 JDK, -o ساخت_سیستم 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(پارامتر_آرگومان.sources[0], پارامتر_آرگومان.output, پارامتر_آرگومان.java_home, پارامتر_آرگومان.jobs, پارامتر_آرگومان.openjdk_target,
                  پارامتر_آرگومان.sysroot, None if پارامتر_آرگومان.cc == 'cc' else پارامتر_آرگومان.cc, پارامتر_آرگومان.cxx, پارامتر_آرگومان.configure_arg)
        except BuildError as خطا:
            raise 컴파일오류(str(خطا))
        return
    if not پارامتر_آرگومان.entry:
        مفسر_48ee4b1b.error('--entry is required for this target')
    if پارامتر_آرگومان.cxx or پارامتر_آرگومان.openjdk_target or پارامتر_آرگومان.sysroot or پارامتر_آرگومان.configure_arg or پارامتر_آرگومان.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build هدف 전용')
    if پارامتر_آرگومان.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import ایجاد_ورودی
        ایجاد_ورودی(پارامتر_آرگومان)
        return
    if پارامتر_آرگومان.classpath or پارامتر_آرگومان.java_home or پارامتر_آرگومان.bundle_runtime or پارامتر_آرگومان.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk هدف 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', پارامتر_آرگومان.target, '--entry', پارامتر_آرگومان.entry, '-o', پارامتر_آرگومان.output]
    for اختصاص_مقدار in پارامتر_آرگومان.export: 자바명령.extend(['--export', اختصاص_مقدار])
    subprocess.run(자바명령+پارامتر_آرگومان.sources, check=True)
    return


if __name__ == '__main__':
    try:
        اجرا_فرمان()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as خطا:
        print('ساختن_منبع خطا: ' + str(خطا), file=sys.stderr)
        sys.exit(1)
