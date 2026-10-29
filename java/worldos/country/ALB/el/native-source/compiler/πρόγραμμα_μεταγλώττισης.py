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


class σφάλμα_μεταγλώττισης(Exception):
    pass


class 자료읽기:
    def __init__(자신, δεδομένα):
        자신.δεδομένα = δεδομένα
        자신.Θέση = 0

    def Ανάγνωση(자신, διάρκεια_τιμή):
        if διάρκεια_τιμή < 0 or 자신.Θέση + διάρκεια_τιμή > len(자신.δεδομένα):
            raise σφάλμα_μεταγλώττισης('잘린 Τάξη_τιμή 또는 Εντολή δεδομένα')
        μέτρηση = 자신.δεδομένα[자신.Θέση:자신.Θέση + διάρκεια_τιμή]
        자신.Θέση += διάρκεια_τιμή
        return μέτρηση

    def 수(자신, μορφή_τιμή):
        return struct.unpack('>' + μορφή_τιμή, 자신.Ανάγνωση(struct.calcsize('>' + μορφή_τιμή)))[0]


def 수정유티에프해독(δεδομένα):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    συμβολοσειρά_τιμή = δεδομένα.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return συμβολοσειρά_τιμή.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class Τάξη_τιμή:
    def __init__(자신, ΔΙΑΔΡΟΜΗ):
        자신.ΔΙΑΔΡΟΜΗ = ΔΙΑΔΡΟΜΗ
        Αναγνώστης_τιμή = 자료읽기(ΔΙΑΔΡΟΜΗ.read_bytes())
        if Αναγνώστης_τιμή.수('I') != 0xcafebabe:
            raise σφάλμα_μεταγλώττισης('Java Τάξη_τιμή 표식이 아님')
        Αναγνώστης_τιμή.Ανάγνωση(4)
        개수 = Αναγνώστης_τιμή.수('H')
        자신.σταθερά_τιμή = [None] * 개수
        Ευρετήριο = 1
        while Ευρετήριο < 개수:
            종류 = Αναγνώστης_τιμή.수('B')
            if 종류 == 1:
                τιμή = 수정유티에프해독(Αναγνώστης_τιμή.Ανάγνωση(Αναγνώστης_τιμή.수('H')))
            elif 종류 == 3:
                τιμή = Αναγνώστης_τιμή.수('i')
            elif 종류 == 4:
                τιμή = Αναγνώστης_τιμή.Ανάγνωση(4)
            elif 종류 in (5, 6):
                τιμή = Αναγνώστης_τιμή.Ανάγνωση(8)
            elif 종류 in (7, 8, 16):
                τιμή = Αναγνώστης_τιμή.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                τιμή = (Αναγνώστης_τιμή.수('H'), Αναγνώστης_τιμή.수('H'))
            elif 종류 == 15:
                τιμή = (Αναγνώστης_τιμή.수('B'), Αναγνώστης_τιμή.수('H'))
            else:
                raise σφάλμα_μεταγλώττισης('지원하지 않는 σταθερά_τιμή 종류: {}'.format(종류))
            자신.σταθερά_τιμή[Ευρετήριο] = (종류, τιμή)
            Ευρετήριο += 2 if 종류 in (5, 6) else 1
        자신.πρόσβαση_καταχώρηση = Αναγνώστης_τιμή.수('H')
        자신.Όνομα = 자신.όνομα_κλάσης(Αναγνώστης_τιμή.수('H'))
        γονικός_τιμή = Αναγνώστης_τιμή.수('H')
        if 자신.όνομα_κλάσης(γονικός_τιμή) != 'java/lang/Object' or Αναγνώστης_τιμή.수('H') != 0:
            raise σφάλμα_μεταγλώττισης(자신.Όνομα + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.τιμή_πεδίου = 자신.멤버읽기(Αναγνώστης_τιμή)
        자신.συνάρτηση_τιμή = 자신.멤버읽기(Αναγνώστης_τιμή)
        자신.속성읽기(Αναγνώστης_τιμή)

    def 문자(자신, Ευρετήριο):
        if 자신.σταθερά_τιμή[Ευρετήριο][0] != 1:
            raise σφάλμα_μεταγλώττισης('συμβολοσειρά_τιμή σταθερά_τιμή μορφή_τιμή ΣΦΑΛΜΑ')
        return 자신.σταθερά_τιμή[Ευρετήριο][1]

    def όνομα_κλάσης(자신, Ευρετήριο):
        return 자신.문자(자신.σταθερά_τιμή[Ευρετήριο][1])

    def Αναφορά(자신, Ευρετήριο):
        κάτοχος_τιμή, όνομα_μορφή = 자신.σταθερά_τιμή[Ευρετήριο][1]
        Όνομα, μορφή_τιμή = 자신.σταθερά_τιμή[όνομα_μορφή][1]
        return 자신.όνομα_κλάσης(κάτοχος_τιμή), 자신.문자(Όνομα), 자신.문자(μορφή_τιμή)

    def 속성읽기(자신, Αναγνώστης_τιμή):
        μέτρηση = {}
        for _ in range(Αναγνώστης_τιμή.수('H')):
            Όνομα = 자신.문자(Αναγνώστης_τιμή.수('H'))
            μέτρηση[Όνομα] = Αναγνώστης_τιμή.Ανάγνωση(Αναγνώστης_τιμή.수('I'))
        return μέτρηση

    def 멤버읽기(자신, Αναγνώστης_τιμή):
        μέτρηση = []
        for _ in range(Αναγνώστης_τιμή.수('H')):
            πρόσβαση_καταχώρηση = Αναγνώστης_τιμή.수('H')
            Όνομα = 자신.문자(Αναγνώστης_τιμή.수('H'))
            μορφή_τιμή = 자신.문자(Αναγνώστης_τιμή.수('H'))
            μέτρηση.append((πρόσβαση_καταχώρηση, Όνομα, μορφή_τιμή, 자신.속성읽기(Αναγνώστης_τιμή)))
        return μέτρηση


def 형식읽기(συμβολοσειρά_τιμή):
    μέτρηση = []
    Θέση = 0
    while Θέση < len(συμβολοσειρά_τιμή):
        for μορφή_τιμή in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if συμβολοσειρά_τιμή.startswith(μορφή_τιμή, Θέση):
                μέτρηση.append(μορφή_τιμή)
                Θέση += len(μορφή_τιμή)
                break
        else:
            raise σφάλμα_μεταγλώττισης('지원하지 않는 τύπος_δεδομένων: ' + συμβολοσειρά_τιμή)
    return μέτρηση


def 함수형식(서술):
    Παράμετροι, επιστρέφω_μέτρηση = 서술[1:].split(')')
    Παράμετροι = 형식읽기(Παράμετροι)
    επιστρέφω_Τύπος = 형식읽기(επιστρέφω_μέτρηση)
    if 'V' in Παράμετροι or len(επιστρέφω_Τύπος) != 1:
        raise σφάλμα_μεταγλώττισης('συνάρτηση_τιμή 서술 μορφή_τιμή ΣΦΑΛΜΑ: ' + 서술)
    return Παράμετροι, επιστρέφω_μέτρηση


def σύμβολο(종류, *부분):
    ΠΗΓΗ = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(ΠΗΓΗ).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 συνάρτηση_τιμή 서술에 대해서만 허용한다.
def εκτελώ_εντολή(Παράμετροι=None):
    ανάλυση_48ee4b1b = argparse.ArgumentParser(description='ίδιο Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK προέλευση_δέντρο δομή_Σύστημα')
    ανάλυση_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    ανάλυση_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 προσαρτώ_καταχώρηση JAR/Τάξη_τιμή 디렉터리')
    ανάλυση_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 δομή_Σύστημα JDK 또는 openjdk-build의 부트 JDK ΔΙΑΔΡΟΜΗ')
    ανάλυση_48ee4b1b.add_argument('--bundle-runtime', help='εκτελώ_εντολή 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    ανάλυση_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK εφαρμογή_εκκίνηση/προέλευση_δέντρο 빌드의 C πρόγραμμα_μεταγλώττισης')
    ανάλυση_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ πρόγραμμα_μεταγλώττισης')
    ανάλυση_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 δομή_Σύστημα 작업 수')
    ανάλυση_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 δομή_Σύστημα τιμή_στόχος (예: aarch64-linux-gnu)')
    ανάλυση_48ee4b1b.add_argument('--sysroot', help='교차 δομή_Σύστημα 대상의 libc/헤더/βιβλιοθήκη 루트')
    ανάλυση_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 μορφή_τιμή')
    ανάλυση_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=Τάξη_τιμή.συνάρτηση_τιμή (ίδιο τελεστέος_δέσμη ABI)')
    ανάλυση_48ee4b1b.add_argument('--entry', help='예: 계산.Εκτέλεση_2 (openjdk-build 이외 대상에서 필수)')
    ανάλυση_48ee4b1b.add_argument('-o', '--output', required=True, help='εκτελώ_εντολή ELF/.o Έξοδος; openjdk-build는 전용 δομή_Σύστημα 디렉터리')
    ανάλυση_48ee4b1b.add_argument('sources', nargs='+')
    παράμετρος_όρισμα = ανάλυση_48ee4b1b.parse_args(Παράμετροι)
    if παράμετρος_όρισμα.target == 'openjdk-build':
        if len(παράμετρος_όρισμα.sources) != 1 or not παράμετρος_όρισμα.java_home or παράμετρος_όρισμα.entry or παράμετρος_όρισμα.export or παράμετρος_όρισμα.classpath or παράμετρος_όρισμα.bundle_runtime:
            raise σφάλμα_μεταγλώττισης('openjdk-build: OpenJDK προέλευση_δέντρο 디렉터리 하나와 --java-home 부트 JDK, -o δομή_Σύστημα 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(παράμετρος_όρισμα.sources[0], παράμετρος_όρισμα.output, παράμετρος_όρισμα.java_home, παράμετρος_όρισμα.jobs, παράμετρος_όρισμα.openjdk_target,
                  παράμετρος_όρισμα.sysroot, None if παράμετρος_όρισμα.cc == 'cc' else παράμετρος_όρισμα.cc, παράμετρος_όρισμα.cxx, παράμετρος_όρισμα.configure_arg)
        except BuildError as ΣΦΑΛΜΑ:
            raise σφάλμα_μεταγλώττισης(str(ΣΦΑΛΜΑ))
        return
    if not παράμετρος_όρισμα.entry:
        ανάλυση_48ee4b1b.error('--entry is required for this target')
    if παράμετρος_όρισμα.cxx or παράμετρος_όρισμα.openjdk_target or παράμετρος_όρισμα.sysroot or παράμετρος_όρισμα.configure_arg or παράμετρος_όρισμα.jobs != 2:
        raise σφάλμα_μεταγλώττισης('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build τιμή_στόχος 전용')
    if παράμετρος_όρισμα.target == 'openjdk':
        sys.modules.setdefault('πρόγραμμα_μεταγλώττισης', sys.modules[__name__])
        from εκτελέσιμο import ανοίγω_καταχώρηση
        ανοίγω_καταχώρηση(παράμετρος_όρισμα)
        return
    if παράμετρος_όρισμα.classpath or παράμετρος_όρισμα.java_home or παράμετρος_όρισμα.bundle_runtime or παράμετρος_όρισμα.cc != 'cc':
        raise σφάλμα_μεταγλώττισης('classpath/java-home/bundle-runtime/cc 옵션은 openjdk τιμή_στόχος 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', παράμετρος_όρισμα.target, '--entry', παράμετρος_όρισμα.entry, '-o', παράμετρος_όρισμα.output]
    for εκχωρώ_τιμή in παράμετρος_όρισμα.export: 자바명령.extend(['--export', εκχωρώ_τιμή])
    subprocess.run(자바명령+παράμετρος_όρισμα.sources, check=True)
    return


if __name__ == '__main__':
    try:
        εκτελώ_εντολή()
    except (σφάλμα_μεταγλώττισης, OSError, ValueError, subprocess.CalledProcessError) as ΣΦΑΛΜΑ:
        print('δόμηση_προέλευση ΣΦΑΛΜΑ: ' + str(ΣΦΑΛΜΑ), file=sys.stderr)
        sys.exit(1)
