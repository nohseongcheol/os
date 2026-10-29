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


class يقرأ_بيانات:
    def __init__(자신, بيانات):
        자신.بيانات = بيانات
        자신.موضع = 0

    def قراءة(자신, 길이):
        if 길이 < 0 or 자신.موضع + 길이 > len(자신.بيانات):
            raise 컴파일오류('잘린 فئة_قيمة_55654bf1 또는 أمر بيانات')
        نتيجة = 자신.بيانات[자신.موضع:자신.موضع + 길이]
        자신.موضع += 길이
        return نتيجة

    def رقم(자신, ينسق_قيمة):
        return struct.unpack('>' + ينسق_قيمة, 자신.قراءة(struct.calcsize('>' + ينسق_قيمة)))[0]


def 수정유티에프해독(بيانات):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    سلسلة_قيمة = بيانات.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return سلسلة_قيمة.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class فئة_قيمة_55654bf1:
    def __init__(자신, مسار):
        자신.مسار = مسار
        قارئ_قيمة = يقرأ_بيانات(مسار.read_bytes())
        if قارئ_قيمة.رقم('I') != 0xcafebabe:
            raise 컴파일오류('Java فئة_قيمة_55654bf1 표식이 아님')
        قارئ_قيمة.قراءة(4)
        개수 = قارئ_قيمة.رقم('H')
        자신.ثابت_قيمة = [None] * 개수
        فهرس = 1
        while فهرس < 개수:
            종류 = قارئ_قيمة.رقم('B')
            if 종류 == 1:
                قيمة = 수정유티에프해독(قارئ_قيمة.قراءة(قارئ_قيمة.رقم('H')))
            elif 종류 == 3:
                قيمة = قارئ_قيمة.رقم('i')
            elif 종류 == 4:
                قيمة = قارئ_قيمة.قراءة(4)
            elif 종류 in (5, 6):
                قيمة = قارئ_قيمة.قراءة(8)
            elif 종류 in (7, 8, 16):
                قيمة = قارئ_قيمة.رقم('H')
            elif 종류 in (9, 10, 11, 12, 18):
                قيمة = (قارئ_قيمة.رقم('H'), قارئ_قيمة.رقم('H'))
            elif 종류 == 15:
                قيمة = (قارئ_قيمة.رقم('B'), قارئ_قيمة.رقم('H'))
            else:
                raise 컴파일오류('지원하지 않는 ثابت_قيمة 종류: {}'.format(종류))
            자신.ثابت_قيمة[فهرس] = (종류, قيمة)
            فهرس += 2 if 종류 in (5, 6) else 1
        자신.يصل_إدخال = قارئ_قيمة.رقم('H')
        자신.اسم = 자신.اسم_الفئة(قارئ_قيمة.رقم('H'))
        أصل_قيمة = قارئ_قيمة.رقم('H')
        if 자신.اسم_الفئة(أصل_قيمة) != 'java/lang/Object' or قارئ_قيمة.رقم('H') != 0:
            raise 컴파일오류(자신.اسم + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.قيمة_الحقل = 자신.멤버읽기(قارئ_قيمة)
        자신.دالة_قيمة = 자신.멤버읽기(قارئ_قيمة)
        자신.يقرأ_السمات(قارئ_قيمة)

    def 문자(자신, فهرس):
        if 자신.ثابت_قيمة[فهرس][0] != 1:
            raise 컴파일오류('سلسلة_قيمة ثابت_قيمة ينسق_قيمة خطأ')
        return 자신.ثابت_قيمة[فهرس][1]

    def اسم_الفئة(자신, فهرس):
        return 자신.문자(자신.ثابت_قيمة[فهرس][1])

    def مرجع(자신, فهرس):
        مالك_قيمة, اسم_ينسق = 자신.ثابت_قيمة[فهرس][1]
        اسم, ينسق_قيمة = 자신.ثابت_قيمة[اسم_ينسق][1]
        return 자신.اسم_الفئة(مالك_قيمة), 자신.문자(اسم), 자신.문자(ينسق_قيمة)

    def يقرأ_السمات(자신, قارئ_قيمة):
        نتيجة = {}
        for _ in range(قارئ_قيمة.رقم('H')):
            اسم = 자신.문자(قارئ_قيمة.رقم('H'))
            نتيجة[اسم] = قارئ_قيمة.قراءة(قارئ_قيمة.رقم('I'))
        return نتيجة

    def 멤버읽기(자신, قارئ_قيمة):
        نتيجة = []
        for _ in range(قارئ_قيمة.رقم('H')):
            يصل_إدخال = قارئ_قيمة.رقم('H')
            اسم = 자신.문자(قارئ_قيمة.رقم('H'))
            ينسق_قيمة = 자신.문자(قارئ_قيمة.رقم('H'))
            نتيجة.append((يصل_إدخال, اسم, ينسق_قيمة, 자신.يقرأ_السمات(قارئ_قيمة)))
        return نتيجة


def 형식읽기(سلسلة_قيمة):
    نتيجة = []
    موضع = 0
    while موضع < len(سلسلة_قيمة):
        for ينسق_قيمة in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if سلسلة_قيمة.startswith(ينسق_قيمة, موضع):
                نتيجة.append(ينسق_قيمة)
                موضع += len(ينسق_قيمة)
                break
        else:
            raise 컴파일오류('지원하지 않는 نوع_البيانات: ' + سلسلة_قيمة)
    return نتيجة


def 함수형식(서술):
    وسائط, إرجاع_مقياس = 서술[1:].split(')')
    وسائط = 형식읽기(وسائط)
    إرجاع_نوع = 형식읽기(إرجاع_مقياس)
    if 'V' in وسائط or len(إرجاع_نوع) != 1:
        raise 컴파일오류('دالة_قيمة 서술 ينسق_قيمة خطأ: ' + 서술)
    return وسائط, إرجاع_مقياس


def رمز(종류, *부분):
    مصدر = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(مصدر).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 دالة_قيمة 서술에 대해서만 허용한다.
def ينفذ_أمر(وسائط=None):
    المحلل_48ee4b1b = argparse.ArgumentParser(description='ذاتي Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK مصدر_شجرة بنية_نظام')
    المحلل_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    المحلل_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 إلحاق_إدخال JAR/فئة_قيمة_55654bf1 디렉터리')
    المحلل_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 بنية_نظام JDK 또는 openjdk-build의 부트 JDK مسار')
    المحلل_48ee4b1b.add_argument('--bundle-runtime', help='ينفذ_أمر 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    المحلل_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK تطبيق_مشغّل/مصدر_شجرة 빌드의 C محول_برمجي')
    المحلل_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ محول_برمجي')
    المحلل_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 بنية_نظام 작업 رقم')
    المحلل_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 بنية_نظام الهدف (예: aarch64-linux-gnu)')
    المحلل_48ee4b1b.add_argument('--sysroot', help='교차 بنية_نظام 대상의 libc/헤더/مكتبة 루트')
    المحلل_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 ينسق_قيمة')
    المحلل_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=فئة_قيمة_55654bf1.دالة_قيمة (ذاتي مُعامل_رمز ABI)')
    المحلل_48ee4b1b.add_argument('--entry', help='예: 계산.تشغيل (openjdk-build 이외 대상에서 필수)')
    المحلل_48ee4b1b.add_argument('-o', '--output', required=True, help='ينفذ_أمر ELF/.o مخرجات; openjdk-build는 전용 بنية_نظام 디렉터리')
    المحلل_48ee4b1b.add_argument('sources', nargs='+')
    معلمة_وسيطة = المحلل_48ee4b1b.parse_args(وسائط)
    if معلمة_وسيطة.target == 'openjdk-build':
        if len(معلمة_وسيطة.sources) != 1 or not معلمة_وسيطة.java_home or معلمة_وسيطة.entry or معلمة_وسيطة.export or معلمة_وسيطة.classpath or معلمة_وسيطة.bundle_runtime:
            raise 컴파일오류('openjdk-build: OpenJDK مصدر_شجرة 디렉터리 하나와 --java-home 부트 JDK, -o بنية_نظام 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(معلمة_وسيطة.sources[0], معلمة_وسيطة.output, معلمة_وسيطة.java_home, معلمة_وسيطة.jobs, معلمة_وسيطة.openjdk_target,
                  معلمة_وسيطة.sysroot, None if معلمة_وسيطة.cc == 'cc' else معلمة_وسيطة.cc, معلمة_وسيطة.cxx, معلمة_وسيطة.configure_arg)
        except BuildError as خطأ:
            raise 컴파일오류(str(خطأ))
        return
    if not معلمة_وسيطة.entry:
        المحلل_48ee4b1b.error('--entry is required for this target')
    if معلمة_وسيطة.cxx or معلمة_وسيطة.openjdk_target or معلمة_وسيطة.sysroot or معلمة_وسيطة.configure_arg or معلمة_وسيطة.jobs != 2:
        raise 컴파일오류('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build الهدف 전용')
    if معلمة_وسيطة.target == 'openjdk':
        sys.modules.setdefault('محول_برمجي', sys.modules[__name__])
        from 실행파일 import فتح_إدخال
        فتح_إدخال(معلمة_وسيطة)
        return
    if معلمة_وسيطة.classpath or معلمة_وسيطة.java_home or معلمة_وسيطة.bundle_runtime or معلمة_وسيطة.cc != 'cc':
        raise 컴파일오류('classpath/java-home/bundle-runtime/cc 옵션은 openjdk الهدف 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', معلمة_وسيطة.target, '--entry', معلمة_وسيطة.entry, '-o', معلمة_وسيطة.output]
    for تعيين_قيمة in معلمة_وسيطة.export: 자바명령.extend(['--export', تعيين_قيمة])
    subprocess.run(자바명령+معلمة_وسيطة.sources, check=True)
    return


if __name__ == '__main__':
    try:
        ينفذ_أمر()
    except (컴파일오류, OSError, ValueError, subprocess.CalledProcessError) as خطأ:
        print('يحول_برمجياً_مصدر خطأ: ' + str(خطأ), file=sys.stderr)
        sys.exit(1)
