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
        자신.위치 = 0

    def 읽기(자신, لمبائی_قدر):
        if لمبائی_قدر < 0 or 자신.위치 + لمبائی_قدر > len(자신.کوائف):
            raise 컴파일오류('잘린 درجہ_قدر 또는 حکم کوائف')
        결과 = 자신.کوائف[자신.위치:자신.위치 + لمبائی_قدر]
        자신.위치 += لمبائی_قدر
        return 결과

    def 수(자신, وضع_قدر):
        return struct.unpack('>' + وضع_قدر, 자신.읽기(struct.calcsize('>' + وضع_قدر)))[0]


def 수정유티에프해독(کوائف):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    سٹرنگ_قدر = کوائف.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return سٹرنگ_قدر.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class درجہ_قدر:
    def __init__(자신, راہ):
        자신.راہ = راہ
        پڑھن_والا_قدر = 자료읽기(راہ.read_bytes())
        if پڑھن_والا_قدر.수('I') != 0xcafebabe:
            raise 컴파일오류('Java درجہ_قدر 표식이 아님')
        پڑھن_والا_قدر.읽기(4)
        개수 = پڑھن_والا_قدر.수('H')
        자신.مستقل_قدر = [None] * 개수
        اشاریہ = 1
        while اشاریہ < 개수:
            종류 = پڑھن_والا_قدر.수('B')
            if 종류 == 1:
                قدر = 수정유티에프해독(پڑھن_والا_قدر.읽기(پڑھن_والا_قدر.수('H')))
            elif 종류 == 3:
                قدر = پڑھن_والا_قدر.수('i')
            elif 종류 == 4:
                قدر = پڑھن_والا_قدر.읽기(4)
            elif 종류 in (5, 6):
                قدر = پڑھن_والا_قدر.읽기(8)
            elif 종류 in (7, 8, 16):
                قدر = پڑھن_والا_قدر.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                قدر = (پڑھن_والا_قدر.수('H'), پڑھن_والا_قدر.수('H'))
            elif 종류 == 15:
                قدر = (پڑھن_والا_قدر.수('B'), پڑھن_والا_قدر.수('H'))
            else:
                raise 컴파일오류('지원하지 않는 مستقل_قدر 종류: {}'.format(종류))
            자신.مستقل_قدر[اشاریہ] = (종류, قدر)
            اشاریہ += 2 if 종류 in (5, 6) else 1
        자신.پہنچ_داخلہ = پڑھن_والا_قدر.수('H')
        자신.ناں = 자신.درجہ_ناں(پڑھن_والا_قدر.수('H'))
        부모 = پڑھن_والا_قدر.수('H')
        if 자신.درجہ_ناں(부모) != 'java/lang/Object' or پڑھن_والا_قدر.수('H') != 0:
            raise 컴파일오류(자신.ناں + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.قطعہ_قدر = 자신.멤버읽기(پڑھن_والا_قدر)
        자신.فعل_قدر = 자신.멤버읽기(پڑھن_والا_قدر)
        자신.속성읽기(پڑھن_والا_قدر)

    def 문자(자신, اشاریہ):
        if 자신.مستقل_قدر[اشاریہ][0] != 1:
            raise 컴파일오류('سٹرنگ_قدر مستقل_قدر وضع_قدر نقص')
        return 자신.مستقل_قدر[اشاریہ][1]

    def درجہ_ناں(자신, اشاریہ):
        return 자신.문자(자신.مستقل_قدر[اشاریہ][1])

    def حوالہ(자신, اشاریہ):
        مالک_قدر, ناں_وضع = 자신.مستقل_قدر[اشاریہ][1]
        ناں, وضع_قدر = 자신.مستقل_قدر[ناں_وضع][1]
        return 자신.درجہ_ناں(مالک_قدر), 자신.문자(ناں), 자신.문자(وضع_قدر)

    def 속성읽기(자신, پڑھن_والا_قدر):
        결과 = {}
        for _ in range(پڑھن_والا_قدر.수('H')):
            ناں = 자신.문자(پڑھن_والا_قدر.수('H'))
            결과[ناں] = پڑھن_والا_قدر.읽기(پڑھن_والا_قدر.수('I'))
        return 결과

    def 멤버읽기(자신, پڑھن_والا_قدر):
        결과 = []
        for _ in range(پڑھن_والا_قدر.수('H')):
            پہنچ_داخلہ = پڑھن_والا_قدر.수('H')
            ناں = 자신.문자(پڑھن_والا_قدر.수('H'))
            وضع_قدر = 자신.문자(پڑھن_والا_قدر.수('H'))
            결과.append((پہنچ_داخلہ, ناں, وضع_قدر, 자신.속성읽기(پڑھن_والا_قدر)))
        return 결과


def 형식읽기(سٹرنگ_قدر):
    결과 = []
    위치 = 0
    while 위치 < len(سٹرنگ_قدر):
        for وضع_قدر in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if سٹرنگ_قدر.startswith(وضع_قدر, 위치):
                결과.append(وضع_قدر)
                위치 += len(وضع_قدر)
                break
        else:
            raise 컴파일오류('지원하지 않는 ڈیٹا_قسم: ' + سٹرنگ_قدر)
    return 결과


def 함수형식(서술):
    인수, 반환 = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    반환형 = 형식읽기(반환)
    if 'V' in 인수 or len(반환형) != 1:
        raise 컴파일오류('فعل_قدر 서술 وضع_قدر نقص: ' + 서술)
    return 인수, 반환


def علامت(종류, *부분):
    ماخذ = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(ماخذ).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 فعل_قدر 서술에 대해서만 허용한다.
def نفاذ_کرو_حکم(인수=None):
    해석기 = argparse.ArgumentParser(description='자체 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK ماخذ_شجرہ بلڈ_نظام')
    해석기.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    해석기.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 추가 JAR/درجہ_قدر 디렉터리')
    해석기.add_argument('--java-home', help='openjdk 앱의 بلڈ_نظام JDK 또는 openjdk-build의 부트 JDK راہ')
    해석기.add_argument('--bundle-runtime', help='نفاذ_کرو_حکم 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    해석기.add_argument('--cc', default='cc', help='OpenJDK ایپ_عملے_دا_رکن/ماخذ_شجرہ 빌드의 C 컴파일러')
    해석기.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    해석기.add_argument('--jobs', type=int, default=2, help='openjdk-build의 بلڈ_نظام 작업 수')
    해석기.add_argument('--openjdk-target', help='공식 OpenJDK 교차 بلڈ_نظام ہدف (예: aarch64-linux-gnu)')
    해석기.add_argument('--sysroot', help='교차 بلڈ_نظام 대상의 libc/헤더/لائبریری 루트')
    해석기.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 وضع_قدر')
    해석기.add_argument('--export', action='append', default=[], help='외부기호=درجہ_قدر.فعل_قدر (자체 스택 ABI)')
    해석기.add_argument('--entry', help='예: 계산.چلاؤ (openjdk-build 이외 대상에서 필수)')
    해석기.add_argument('-o', '--output', required=True, help='نفاذ_کرو_حکم ELF/.o 출력; openjdk-build는 전용 بلڈ_نظام 디렉터리')
    해석기.add_argument('sources', nargs='+')
    인자 = 해석기.parse_args(인수)
    if 인자.target == 'openjdk-build':
        if len(인자.sources) != 1 or not 인자.java_home or 인자.entry or 인자.export or 인자.classpath or 인자.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK ماخذ_شجرہ 디렉터리 하나와 --java-home 부트 JDK, -o بلڈ_نظام 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(인자.sources[0], 인자.output, 인자.java_home, 인자.jobs, 인자.openjdk_target,
                  인자.sysroot, None if 인자.cc == 'cc' else 인자.cc, 인자.cxx, 인자.configure_arg)
        except BuildError as نقص:
            raise 컴파일오류(str(نقص))
        return
    if not 인자.entry:
        해석기.error('--entry is required for this target')
    if 인자.cxx or 인자.openjdk_target or 인자.sysroot or 인자.configure_arg or 인자.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build ہدف 전용')
    if 인자.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from 실행파일 import بنڑاؤ_داخلہ
        بنڑاؤ_داخلہ(인자)
        return
    if 인자.classpath or 인자.java_home or 인자.bundle_runtime or 인자.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk ہدف 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', 인자.target, '--entry', 인자.entry, '-o', 인자.output]
    for 지정 in 인자.export: 자바명령.extend(['--export', 지정])
    subprocess.run(자바명령+인자.sources, check=True)
    return


if __name__ == '__main__':
    try:
        نفاذ_کرو_حکم()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as نقص:
        print('تیار_کرو_ماخذ نقص: ' + str(نقص), file=sys.stderr)
        sys.exit(1)
