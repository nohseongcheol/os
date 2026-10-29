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


class LỗiViệcBiênDịch(Exception):
    pass


class đọcDữLiệu:
    def __init__(giáTrịBảnThân, DữLiệu):
        giáTrịBảnThân.DữLiệu = DữLiệu
        giáTrịBảnThân.vịTrí = 0

    def đọc(giáTrịBảnThân, độDài):
        if độDài < 0 or giáTrịBảnThân.vịTrí + độDài > len(giáTrịBảnThân.DữLiệu):
            raise LỗiViệcBiênDịch('giáTrịĐãCắtXén giáTrịLớp 또는 lệnh DữLiệu')
        kếtQuả = giáTrịBảnThân.DữLiệu[giáTrịBảnThân.vịTrí:giáTrịBảnThân.vịTrí + độDài]
        giáTrịBảnThân.vịTrí += độDài
        return kếtQuả

    def trịSố(giáTrịBảnThân, giáTrịĐịnhDạng):
        return struct.unpack('>' + giáTrịĐịnhDạng, giáTrịBảnThân.đọc(struct.calcsize('>' + giáTrịĐịnhDạng)))[0]


def giảiMã8UTFĐãChỉnhSửa(DữLiệu):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    ChuỗiKýTự = DữLiệu.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return ChuỗiKýTự.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class giáTrịLớp:
    def __init__(giáTrịBảnThân, đườngDẫn):
        giáTrịBảnThân.đườngDẫn = đườngDẫn
        giáTrịBộĐọc = đọcDữLiệu(đườngDẫn.read_bytes())
        if giáTrịBộĐọc.trịSố('I') != 0xcafebabe:
            raise LỗiViệcBiênDịch('Java giáTrịLớp 표식이 아님')
        giáTrịBộĐọc.đọc(4)
        sốLượngPhầnMục = giáTrịBộĐọc.trịSố('H')
        giáTrịBảnThân.giáTrịHằng = [None] * sốLượngPhầnMục
        sốHiệu = 1
        while sốHiệu < sốLượngPhầnMục:
            giáTrịLoại = giáTrịBộĐọc.trịSố('B')
            if giáTrịLoại == 1:
                giáTrị = giảiMã8UTFĐãChỉnhSửa(giáTrịBộĐọc.đọc(giáTrịBộĐọc.trịSố('H')))
            elif giáTrịLoại == 3:
                giáTrị = giáTrịBộĐọc.trịSố('i')
            elif giáTrịLoại == 4:
                giáTrị = giáTrịBộĐọc.đọc(4)
            elif giáTrịLoại in (5, 6):
                giáTrị = giáTrịBộĐọc.đọc(8)
            elif giáTrịLoại in (7, 8, 16):
                giáTrị = giáTrịBộĐọc.trịSố('H')
            elif giáTrịLoại in (9, 10, 11, 12, 18):
                giáTrị = (giáTrịBộĐọc.trịSố('H'), giáTrịBộĐọc.trịSố('H'))
            elif giáTrịLoại == 15:
                giáTrị = (giáTrịBộĐọc.trịSố('B'), giáTrịBộĐọc.trịSố('H'))
            else:
                raise LỗiViệcBiênDịch('지원하지 않는 giáTrịHằng giáTrịLoại: {}'.format(giáTrịLoại))
            giáTrịBảnThân.giáTrịHằng[sốHiệu] = (giáTrịLoại, giáTrị)
            sốHiệu += 2 if giáTrịLoại in (5, 6) else 1
        giáTrịBảnThân.mụcTruyCập = giáTrịBộĐọc.trịSố('H')
        giáTrịBảnThân.tên = giáTrịBảnThân.tênLớp(giáTrịBộĐọc.trịSố('H'))
        giáTrịCha = giáTrịBộĐọc.trịSố('H')
        if giáTrịBảnThân.tênLớp(giáTrịCha) != 'java/lang/Object' or giáTrịBộĐọc.trịSố('H') != 0:
            raise LỗiViệcBiênDịch(giáTrịBảnThân.tên + ': 상속 및 인터페이스는 아직 지원하지 않음')
        giáTrịBảnThân.giáTrịTrường = giáTrịBảnThân.đọcCácThànhViên(giáTrịBộĐọc)
        giáTrịBảnThân.Hàm = giáTrịBảnThân.đọcCácThànhViên(giáTrịBộĐọc)
        giáTrịBảnThân.đọcCácThuộcTính(giáTrịBộĐọc)

    def KýTự(giáTrịBảnThân, sốHiệu):
        if giáTrịBảnThân.giáTrịHằng[sốHiệu][0] != 1:
            raise LỗiViệcBiênDịch('ChuỗiKýTự giáTrịHằng giáTrịĐịnhDạng lỗi')
        return giáTrịBảnThân.giáTrịHằng[sốHiệu][1]

    def tênLớp(giáTrịBảnThân, sốHiệu):
        return giáTrịBảnThân.KýTự(giáTrịBảnThân.giáTrịHằng[sốHiệu][1])

    def thamChiếu(giáTrịBảnThân, sốHiệu):
        giáTrịChủSởHữu, địnhDạngTên = giáTrịBảnThân.giáTrịHằng[sốHiệu][1]
        tên, giáTrịĐịnhDạng = giáTrịBảnThân.giáTrịHằng[địnhDạngTên][1]
        return giáTrịBảnThân.tênLớp(giáTrịChủSởHữu), giáTrịBảnThân.KýTự(tên), giáTrịBảnThân.KýTự(giáTrịĐịnhDạng)

    def đọcCácThuộcTính(giáTrịBảnThân, giáTrịBộĐọc):
        kếtQuả = {}
        for _ in range(giáTrịBộĐọc.trịSố('H')):
            tên = giáTrịBảnThân.KýTự(giáTrịBộĐọc.trịSố('H'))
            kếtQuả[tên] = giáTrịBộĐọc.đọc(giáTrịBộĐọc.trịSố('I'))
        return kếtQuả

    def đọcCácThànhViên(giáTrịBảnThân, giáTrịBộĐọc):
        kếtQuả = []
        for _ in range(giáTrịBộĐọc.trịSố('H')):
            mụcTruyCập = giáTrịBộĐọc.trịSố('H')
            tên = giáTrịBảnThân.KýTự(giáTrịBộĐọc.trịSố('H'))
            giáTrịĐịnhDạng = giáTrịBảnThân.KýTự(giáTrịBộĐọc.trịSố('H'))
            kếtQuả.append((mụcTruyCập, tên, giáTrịĐịnhDạng, giáTrịBảnThân.đọcCácThuộcTính(giáTrịBộĐọc)))
        return kếtQuả


def phânTíchCúPhápCácKiểu(ChuỗiKýTự):
    kếtQuả = []
    vịTrí = 0
    while vịTrí < len(ChuỗiKýTự):
        for giáTrịĐịnhDạng in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if ChuỗiKýTự.startswith(giáTrịĐịnhDạng, vịTrí):
                kếtQuả.append(giáTrịĐịnhDạng)
                vịTrí += len(giáTrịĐịnhDạng)
                break
        else:
            raise LỗiViệcBiênDịch('지원하지 않는 kiểuDữLiệu: ' + ChuỗiKýTự)
    return kếtQuả


def BộMôTảPhươngThức(giáTrịMôTả):
    cácĐốiSố, kếtQuảTrảVề = giáTrịMôTả[1:].split(')')
    cácĐốiSố = phânTíchCúPhápCácKiểu(cácĐốiSố)
    kiểuTrảVề = phânTíchCúPhápCácKiểu(kếtQuảTrảVề)
    if 'V' in cácĐốiSố or len(kiểuTrảVề) != 1:
        raise LỗiViệcBiênDịch('Hàm giáTrịMôTả giáTrịĐịnhDạng lỗi: ' + giáTrịMôTả)
    return cácĐốiSố, kếtQuảTrảVề


def kýHiệu(giáTrịLoại, *giáTrịPhầnCon):
    mãNguồn = '\x00'.join(giáTrịPhầnCon).encode('utf-8')
    return 'j_{}_{}'.format(giáTrịLoại, hashlib.sha256(mãNguồn).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 Hàm 서술에 대해서만 허용한다.
def thựcThiLệnh(cácĐốiSố=None):
    BộPhânTích = argparse.ArgumentParser(description='tựThân Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK câyNguồn xâyDựngHệThống')
    BộPhânTích.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    BộPhânTích.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 thêmCuốiMục JAR/giáTrịLớp 디렉터리')
    BộPhânTích.add_argument('--java-home', help='openjdk 앱의 xâyDựngHệThống JDK 또는 openjdk-build의 부트 JDK đườngDẫn')
    BộPhânTích.add_argument('--bundle-runtime', help='thựcThiLệnh 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    BộPhânTích.add_argument('--cc', default='cc', help='OpenJDK TrìnhKhởiChạyChươngTrình/câyNguồn 빌드의 C TrìnhBiênDịch')
    BộPhânTích.add_argument('--cxx', help='openjdk-build의 C++ TrìnhBiênDịch')
    BộPhânTích.add_argument('--jobs', type=int, default=2, help='openjdk-build의 xâyDựngHệThống TácVụ trịSố')
    BộPhânTích.add_argument('--openjdk-target', help='공식 OpenJDK 교차 xâyDựngHệThống giáTrịĐốiĐích (예: aarch64-linux-gnu)')
    BộPhânTích.add_argument('--sysroot', help='교차 xâyDựngHệThống 대상의 libc/헤더/thưViện 루트')
    BộPhânTích.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 giáTrịĐịnhDạng')
    BộPhânTích.add_argument('--export', action='append', default=[], help='외부기호=giáTrịLớp.Hàm (tựThân ngănXếpToánHạng ABI)')
    BộPhânTích.add_argument('--entry', help='예: phépTính.chạy (openjdk-build 이외 대상에서 làBắtBuộc)')
    BộPhânTích.add_argument('-o', '--output', required=True, help='thựcThiLệnh ELF/.o ĐầuRa; openjdk-build는 전용 xâyDựngHệThống 디렉터리')
    BộPhânTích.add_argument('sources', nargs='+')
    đốiSốThamSố = BộPhânTích.parse_args(cácĐốiSố)
    if đốiSốThamSố.target == 'openjdk-build':
        if len(đốiSốThamSố.sources) != 1 or not đốiSốThamSố.java_home or đốiSốThamSố.entry or đốiSốThamSố.export or đốiSốThamSố.classpath or đốiSốThamSố.bundle_runtime:
            raise LỗiViệcBiênDịch('openjdk-build: OpenJDK câyNguồn 디렉터리 하나와 --java-home 부트 JDK, -o xâyDựngHệThống 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(đốiSốThamSố.sources[0], đốiSốThamSố.output, đốiSốThamSố.java_home, đốiSốThamSố.jobs, đốiSốThamSố.openjdk_target,
                  đốiSốThamSố.sysroot, None if đốiSốThamSố.cc == 'cc' else đốiSốThamSố.cc, đốiSốThamSố.cxx, đốiSốThamSố.configure_arg)
        except BuildError as lỗi:
            raise LỗiViệcBiênDịch(str(lỗi))
        return
    if not đốiSốThamSố.entry:
        BộPhânTích.error('--entry is required for this target')
    if đốiSốThamSố.cxx or đốiSốThamSố.openjdk_target or đốiSốThamSố.sysroot or đốiSốThamSố.configure_arg or đốiSốThamSố.jobs != 2:
        raise LỗiViệcBiênDịch('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build giáTrịĐốiĐích 전용')
    if đốiSốThamSố.target == 'openjdk':
        sys.modules.setdefault('TrìnhBiênDịch', sys.modules[__name__])
        from tệpTệpThựcThi import tạoMục
        tạoMục(đốiSốThamSố)
        return
    if đốiSốThamSố.classpath or đốiSốThamSố.java_home or đốiSốThamSố.bundle_runtime or đốiSốThamSố.cc != 'cc':
        raise LỗiViệcBiênDịch('classpath/java-home/bundle-runtime/cc 옵션은 openjdk giáTrịĐốiĐích 전용')
    lệnhJava = ['sh', str(Path(__file__).resolve().parent/'thờiGianCủaTrước.sh'),
                '--target', đốiSốThamSố.target, '--entry', đốiSốThamSố.entry, '-o', đốiSốThamSố.output]
    for giáTrịGán in đốiSốThamSố.export: lệnhJava.extend(['--export', giáTrịGán])
    subprocess.run(lệnhJava+đốiSốThamSố.sources, check=True)
    return


if __name__ == '__main__':
    try:
        thựcThiLệnh()
    except (LỗiViệcBiênDịch, OSError, ValueError, subprocess.CalledProcessError) as lỗi:
        print('biênDịchNguồn lỗi: ' + str(lỗi), file=sys.stderr)
        sys.exit(1)
