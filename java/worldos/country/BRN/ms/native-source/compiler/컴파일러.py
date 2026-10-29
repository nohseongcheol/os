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


class ralat_kompilasi(Exception):
    pass


class 자료읽기:
    def __init__(자신, data):
        자신.data = data
        자신.Kedudukan = 0

    def Baca(자신, kepanjangan_VALUE):
        if kepanjangan_VALUE < 0 or 자신.Kedudukan + kepanjangan_VALUE > len(자신.data):
            raise ralat_kompilasi('잘린 Kelas_VALUE 또는 Perintah data')
        ukuran = 자신.data[자신.Kedudukan:자신.Kedudukan + kepanjangan_VALUE]
        자신.Kedudukan += kepanjangan_VALUE
        return ukuran

    def 수(자신, format_VALUE):
        return struct.unpack('>' + format_VALUE, 자신.Baca(struct.calcsize('>' + format_VALUE)))[0]


def 수정유티에프해독(data):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    rentetan_VALUE = data.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return rentetan_VALUE.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class Kelas_VALUE:
    def __init__(자신, LALUAN):
        자신.LALUAN = LALUAN
        Pembaca_VALUE = 자료읽기(LALUAN.read_bytes())
        if Pembaca_VALUE.수('I') != 0xcafebabe:
            raise ralat_kompilasi('Java Kelas_VALUE 표식이 아님')
        Pembaca_VALUE.Baca(4)
        item_COUNT = Pembaca_VALUE.수('H')
        자신.pemalar_VALUE = [None] * item_COUNT
        INDEX = 1
        while INDEX < item_COUNT:
            종류 = Pembaca_VALUE.수('B')
            if 종류 == 1:
                VALUE = 수정유티에프해독(Pembaca_VALUE.Baca(Pembaca_VALUE.수('H')))
            elif 종류 == 3:
                VALUE = Pembaca_VALUE.수('i')
            elif 종류 == 4:
                VALUE = Pembaca_VALUE.Baca(4)
            elif 종류 in (5, 6):
                VALUE = Pembaca_VALUE.Baca(8)
            elif 종류 in (7, 8, 16):
                VALUE = Pembaca_VALUE.수('H')
            elif 종류 in (9, 10, 11, 12, 18):
                VALUE = (Pembaca_VALUE.수('H'), Pembaca_VALUE.수('H'))
            elif 종류 == 15:
                VALUE = (Pembaca_VALUE.수('B'), Pembaca_VALUE.수('H'))
            else:
                raise ralat_kompilasi('지원하지 않는 pemalar_VALUE 종류: {}'.format(종류))
            자신.pemalar_VALUE[INDEX] = (종류, VALUE)
            INDEX += 2 if 종류 in (5, 6) else 1
        자신.capai_pemasukan = Pembaca_VALUE.수('H')
        자신.Nama = 자신.nama_kelas(Pembaca_VALUE.수('H'))
        부모 = Pembaca_VALUE.수('H')
        if 자신.nama_kelas(부모) != 'java/lang/Object' or Pembaca_VALUE.수('H') != 0:
            raise ralat_kompilasi(자신.Nama + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.medan_VALUE = 자신.멤버읽기(Pembaca_VALUE)
        자신.fungsi_VALUE = 자신.멤버읽기(Pembaca_VALUE)
        자신.속성읽기(Pembaca_VALUE)

    def 문자(자신, INDEX):
        if 자신.pemalar_VALUE[INDEX][0] != 1:
            raise ralat_kompilasi('rentetan_VALUE pemalar_VALUE format_VALUE RALAT')
        return 자신.pemalar_VALUE[INDEX][1]

    def nama_kelas(자신, INDEX):
        return 자신.문자(자신.pemalar_VALUE[INDEX][1])

    def Rujukan(자신, INDEX):
        pemilik_VALUE, nama_format = 자신.pemalar_VALUE[INDEX][1]
        Nama, format_VALUE = 자신.pemalar_VALUE[nama_format][1]
        return 자신.nama_kelas(pemilik_VALUE), 자신.문자(Nama), 자신.문자(format_VALUE)

    def 속성읽기(자신, Pembaca_VALUE):
        ukuran = {}
        for _ in range(Pembaca_VALUE.수('H')):
            Nama = 자신.문자(Pembaca_VALUE.수('H'))
            ukuran[Nama] = Pembaca_VALUE.Baca(Pembaca_VALUE.수('I'))
        return ukuran

    def 멤버읽기(자신, Pembaca_VALUE):
        ukuran = []
        for _ in range(Pembaca_VALUE.수('H')):
            capai_pemasukan = Pembaca_VALUE.수('H')
            Nama = 자신.문자(Pembaca_VALUE.수('H'))
            format_VALUE = 자신.문자(Pembaca_VALUE.수('H'))
            ukuran.append((capai_pemasukan, Nama, format_VALUE, 자신.속성읽기(Pembaca_VALUE)))
        return ukuran


def 형식읽기(rentetan_VALUE):
    ukuran = []
    Kedudukan = 0
    while Kedudukan < len(rentetan_VALUE):
        for format_VALUE in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if rentetan_VALUE.startswith(format_VALUE, Kedudukan):
                ukuran.append(format_VALUE)
                Kedudukan += len(format_VALUE)
                break
        else:
            raise ralat_kompilasi('지원하지 않는 jenis_data: ' + rentetan_VALUE)
    return ukuran


def 함수형식(서술):
    인수, kembalikan_ukuran = 서술[1:].split(')')
    인수 = 형식읽기(인수)
    kembalikan_TYPE = 형식읽기(kembalikan_ukuran)
    if 'V' in 인수 or len(kembalikan_TYPE) != 1:
        raise ralat_kompilasi('fungsi_VALUE 서술 format_VALUE RALAT: ' + 서술)
    return 인수, kembalikan_ukuran


def simbol(종류, *부분):
    SUMBER = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(종류, hashlib.sha256(SUMBER).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 fungsi_VALUE 서술에 대해서만 허용한다.
def laksanakan_perintah(인수=None):
    penghurai_48ee4b1b = argparse.ArgumentParser(description='Asli Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK sumber_pepohon bina_sistem')
    penghurai_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    penghurai_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 Tambah_pemasukan JAR/Kelas_VALUE 디렉터리')
    penghurai_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 bina_sistem JDK 또는 openjdk-build의 부트 JDK LALUAN')
    penghurai_48ee4b1b.add_argument('--bundle-runtime', help='laksanakan_perintah 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    penghurai_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK aplikasi_pelancar/sumber_pepohon 빌드의 C 컴파일러')
    penghurai_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ 컴파일러')
    penghurai_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 bina_sistem 작업 수')
    penghurai_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 bina_sistem sasaran (예: aarch64-linux-gnu)')
    penghurai_48ee4b1b.add_argument('--sysroot', help='교차 bina_sistem 대상의 libc/헤더/pustaka 루트')
    penghurai_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 format_VALUE')
    penghurai_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=Kelas_VALUE.fungsi_VALUE (Asli 스택 ABI)')
    penghurai_48ee4b1b.add_argument('--entry', help='예: 계산.Jalan (openjdk-build 이외 대상에서 필수)')
    penghurai_48ee4b1b.add_argument('-o', '--output', required=True, help='laksanakan_perintah ELF/.o 출력; openjdk-build는 전용 bina_sistem 디렉터리')
    penghurai_48ee4b1b.add_argument('sources', nargs='+')
    parameter_argumen = penghurai_48ee4b1b.parse_args(인수)
    if parameter_argumen.target == 'openjdk-build':
        if len(parameter_argumen.sources) != 1 or not parameter_argumen.java_home or parameter_argumen.entry or parameter_argumen.export or parameter_argumen.classpath or parameter_argumen.bundle_runtime:
            raise ralat_kompilasi('openjdk-build: OpenJDK sumber_pepohon 디렉터리 하나와 --java-home 부트 JDK, -o bina_sistem 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(parameter_argumen.sources[0], parameter_argumen.output, parameter_argumen.java_home, parameter_argumen.jobs, parameter_argumen.openjdk_target,
                  parameter_argumen.sysroot, None if parameter_argumen.cc == 'cc' else parameter_argumen.cc, parameter_argumen.cxx, parameter_argumen.configure_arg)
        except BuildError as RALAT:
            raise ralat_kompilasi(str(RALAT))
        return
    if not parameter_argumen.entry:
        penghurai_48ee4b1b.error('--entry is required for this target')
    if parameter_argumen.cxx or parameter_argumen.openjdk_target or parameter_argumen.sysroot or parameter_argumen.configure_arg or parameter_argumen.jobs != 2:
        raise ralat_kompilasi('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build sasaran 전용')
    if parameter_argumen.target == 'openjdk':
        sys.modules.setdefault('컴파일러', sys.modules[__name__])
        from fail_boleh_laku import cipta_pemasukan
        cipta_pemasukan(parameter_argumen)
        return
    if parameter_argumen.classpath or parameter_argumen.java_home or parameter_argumen.bundle_runtime or parameter_argumen.cc != 'cc':
        raise ralat_kompilasi('classpath/java-home/bundle-runtime/cc 옵션은 openjdk sasaran 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', parameter_argumen.target, '--entry', parameter_argumen.entry, '-o', parameter_argumen.output]
    for Tugaskan_VALUE in parameter_argumen.export: 자바명령.extend(['--export', Tugaskan_VALUE])
    subprocess.run(자바명령+parameter_argumen.sources, check=True)
    return


if __name__ == '__main__':
    try:
        laksanakan_perintah()
    except (ralat_kompilasi, OSError, ValueError, subprocess.CalledProcessError) as RALAT:
        print('bina_sumber RALAT: ' + str(RALAT), file=sys.stderr)
        sys.exit(1)
