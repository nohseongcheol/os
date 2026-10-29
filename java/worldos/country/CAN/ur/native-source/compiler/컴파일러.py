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
    def __init__(자신, کوائف):
        자신.کوائف = کوائف
        자신.مقام = 0

    def پڑھیں(자신, لمبا_ئی_قدر):
        if لمبا_ئی_قدر < 0 or 자신.مقام + لمبا_ئی_قدر > len(자신.کوائف):
            raise 컴파일오류('잘린 صنف_قدر 또는 حکم کوائف')
        پیمائش = 자신.کوائف[자신.مقام:자신.مقام + لمبا_ئی_قدر]
        자신.مقام += لمبا_ئی_قدر
        return پیمائش

    def 수(자신, وضع_قدر):
        return struct.unpack('>' + وضع_قدر, 자신.پڑھیں(struct.calcsize('>' + وضع_قدر)))[0]


def 수정유티에프해독(کوائف):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    سلک_قدر = کوائف.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return سلک_قدر.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class صنف_قدر:
    def __init__(자신, راستہ_2):
        자신.راستہ_2 = راستہ_2
        ریڈر_قدر = 자료읽기(راستہ_2.read_bytes())
        if ریڈر_قدر.수('I') != 0xcafebabe:
            raise 컴파일오류('Java صنف_قدر 표식이 아님')
        ریڈر_قدر.پڑھیں(4)
        개수 = ریڈر_قدر.수('H')
        자신.مستقل_قدر = [None] * 개수
        اشاریہ = 1
        while اشاریہ < 개수:
            종류 = ریڈر_قدر.수('B')
            if 종류 == 1:
                قدر = 수정유티에프해독(ریڈر_قدر.پڑھیں(ریڈر_قدر.수('H')))
            elif 종류 == 3:
                قدر = ریڈر_قدر.수('i')
            elif 종류 == 4:
                قدر = ریڈر_قدر.پڑھیں(4)
            elif 종류 in (5, 6):
                قدر = ریڈر_قدر.پڑھیں(8)
            elif 종류 in (7, 8, 16):
                قدر = ریڈر_قدر.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                قدر = (ریڈر_قدر.수('H'), ریڈر_قدر.수('H'))
            elif 종류 == 15:
                قدر = (ریڈر_قدر.수('B'), ریڈر_قدر.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 مستقل_قدر 종류: {}'.format(종류))
            자신.مستقل_قدر[اشاریہ] = (종류, قدر)
            اشاریہ += 2 if 종류 in (5, 6) else 1
        자신.رسائی_اندراج = ریڈر_قدر.수('H')
        자신.نام = 자신.صنف_نام(ریڈر_قدر.수('H'))
        부모 = ریڈر_قدر.수('H')
        if 자신.صنف_نام(부모) != 'java/lang/Object' or ریڈر_قدر.수('H') != 0:
            raise 컴파일오류(자신.نام + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.قطعہ_قدر = 자신.멤버읽기(ریڈر_قدر)
        자신.فعل_قدر = 자신.멤버읽기(ریڈر_قدر)
        자신.속성읽기(ریڈر_قدر)

    def 문자(자신, اشاریہ):
        if 자신.مستقل_قدر[اشاریہ][0] != 1:
            raise 컴파일오류('سلک_قدر مستقل_قدر وضع_قدر غلطی')
        return 자신.مستقل_قدر[اشاریہ][1]

    def صنف_نام(자신, اشاریہ):
        return 자신.문자(자신.مستقل_قدر[اشاریہ][1])

    def حوالہ_جات(자신, اشاریہ):
        مالک_قدر, نام_وضع = 자신.مستقل_قدر[اشاریہ][1]
        نام, وضع_قدر = 자신.مستقل_قدر[نام_وضع][1]
        return 자신.صنف_نام(مالک_قدر), 자신.문자(نام), 자신.문자(وضع_قدر)

    def 속성읽기(자신, ریڈر_قدر):
        پیمائش = {}
        for _ in range(ریڈر_قدر.수('H')):
            نام = 자신.문자(ریڈر_قدر.수('H'))
            پیمائش[نام] = ریڈر_قدر.پڑھیں(ریڈر_قدر.수('I'))
        return پیمائش

    def 멤버읽기(자신, ریڈر_قدر):
        پیمائش = []
        for _ in range(ریڈر_قدر.수('H')):
            رسائی_اندراج = ریڈر_قدر.수('H')
            نام = 자신.문자(ریڈر_قدر.수('H'))
            وضع_قدر = 자신.문자(ریڈر_قدر.수('H'))
            پیمائش.append((رسائی_اندراج, نام, وضع_قدر, 자신.속성읽기(ریڈر_قدر)))
        return پیمائش


def 형식읽기(سلک_قدر):
    پیمائش = []
    مقام = 0
    while مقام < len(سلک_قدر):
        for وضع_قدر in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if سلک_قدر.startswith(وضع_قدر, مقام):
                پیمائش.append(وضع_قدر)
                مقام += len(وضع_قدر)
                break
        else:
            raise 컴파일오류('지원하지 않는 قسم_کوا_ئف: ' + سلک_قدر)
    return پیمائش


def 함수형식(서술):
    دلائل, 반환 = 서술[1:].split(')')
    دلائل = 형식읽기(دلائل)
    반환형 = 형식읽기(반환)
    if 'V' in دلائل or len(반환형) != 1:
        raise 컴파일오류('فعل_قدر 서술 وضع_قدر غلطی: ' + 서술)
    return دلائل, 반환


def علامت(종류, *부분):
    ماخذ_فائل = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(ماخذ_فائل).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 فعل_قدر 서술에 대해서만 허용한다.
def نفاذ_کریں_حکم(دلائل=None):
    해석기 = argparse.ArgumentParser(description='اپنا Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK ماخذ_شجر بلڈ_نظام')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/صنف_قدر 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 بلڈ_نظام JDK 또는 openjdk-build의 부트 JDK راستہ_2')
    해석기.add_argument('--bundle-runtime', help='نفاذ_کریں_حکم 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK ایپ_ایپ_دراز/ماخذ_شجر 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 بلڈ_نظام 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 بلڈ_نظام ہدف (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 بلڈ_نظام 대상의 libc/헤더/لائبریری 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 وضع_قدر')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=صنف_قدر.فعل_قدر (اپنا 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.چلائیں (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='نفاذ_کریں_حکم ELF/.o اخراج_کا_مقام; openjdk-build는 전용 بلڈ_نظام 디렉터리')
    해석기.add_argument('sources', nargs='+')
    پیرا_میٹر_دلائل = 해석기.parse_args(دلائل)
    if پیرا_میٹر_دلائل.target == 'openjdk-build':
        if len(پیرا_میٹر_دلائل.sources) != 1 or not پیرا_میٹر_دلائل.java_home or پیرا_میٹر_دلائل.entry or پیرا_میٹر_دلائل.export or پیرا_میٹر_دلائل.classpath or پیرا_میٹر_دلائل.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK ماخذ_شجر 디렉터리 하나와 --java-home 부트 JDK, -o بلڈ_نظام 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(پیرا_میٹر_دلائل.sources[0], پیرا_میٹر_دلائل.output, پیرا_میٹر_دلائل.java_home, پیرا_میٹر_دلائل.jobs, پیرا_میٹر_دلائل.openjdk_target,
                  پیرا_میٹر_دلائل.sysroot, None if پیرا_میٹر_دلائل.cc == 'cc' else پیرا_میٹر_دلائل.cc, پیرا_میٹر_دلائل.cxx, پیرا_میٹر_دلائل.configure_arg)
        except BuildError as غلطی:
            raise 컴파일오류(str(غلطی))
        return
    if not پیرا_میٹر_دلائل.entry:
        해석기.error('--entry is required for this target')
    if پیرا_میٹر_دلائل.cxx or پیرا_میٹر_دلائل.openjdk_target or پیرا_میٹر_دلائل.sysroot or پیرا_میٹر_دلائل.configure_arg or پیرا_میٹر_دلائل.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build ہدف 전용')
    if پیرا_میٹر_دلائل.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import بنائیں_اندراج
        بنائیں_اندراج(پیرا_میٹر_دلائل)
        return
    if پیرا_میٹر_دلائل.classpath or پیرا_میٹر_دلائل.java_home or پیرا_میٹر_دلائل.bundle_runtime or پیرا_میٹر_دلائل.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk ہدف 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', پیرا_میٹر_دلائل.target, '--entry', پیرا_میٹر_دلائل.entry, '-o', پیرا_میٹر_دلائل.output]
    for تفویض_کریں_قدر in پیرا_میٹر_دلائل.export: 자바명령.extend(['--export', تفویض_کریں_قدر])
    subprocess.run(자바명령+پیرا_میٹر_دلائل.sources, check=True)
    return


if __name__ == '__main__':
    try:
        نفاذ_کریں_حکم()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as غلطی:
        print('مرتب_کریں_ماخذ غلطی: ' + str(غلطی), file=sys.stderr)
        sys.exit(1)
