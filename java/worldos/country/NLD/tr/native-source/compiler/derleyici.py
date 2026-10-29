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


class derleme_hatası(Exception):
    pass


class 자료읽기:
    def __init__(자신, veri):
        자신.veri = veri
        자신.konum = 0

    def Okuma(자신, süre_değer):
        if süre_değer < 0 or 자신.konum + süre_değer > len(자신.veri):
            raise derleme_hatası('잘린 Sınıf_değer 또는 komut veri')
        sonuç = 자신.veri[자신.konum:자신.konum + süre_değer]
        자신.konum += süre_değer
        return sonuç

    def 수(자신, biçim_değer):
        return struct.unpack('>' + biçim_değer, 자신.Okuma(struct.calcsize('>' + biçim_değer)))[0]


def 수정유티에프해독(veri):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    dize_değer = veri.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return dize_değer.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class Sınıf_değer:
    def __init__(자신, yol):
        자신.yol = yol
        Okuyucu_değer = 자료읽기(yol.read_bytes())
        if Okuyucu_değer.수('I') != 0xcafebabe:
            raise derleme_hatası('Java Sınıf_değer 표식이 아님')
        Okuyucu_değer.Okuma(4)
        öğe_BAĞ_DEĞ_SAY = Okuyucu_değer.수('H')
        자신.sabit_değer = [None] * öğe_BAĞ_DEĞ_SAY
        Dizin = 1
        while Dizin < öğe_BAĞ_DEĞ_SAY:
            Tip_değer = Okuyucu_değer.수('B')
            if Tip_değer == 1:
                değer = 수정유티에프해독(Okuyucu_değer.Okuma(Okuyucu_değer.수('H')))
            elif Tip_değer == 3:
                değer = Okuyucu_değer.수('i')
            elif Tip_değer == 4:
                değer = Okuyucu_değer.Okuma(4)
            elif Tip_değer in (5, 6):
                değer = Okuyucu_değer.Okuma(8)
            elif Tip_değer in (7, 8, 16):
                değer = Okuyucu_değer.수('H')
            elif Tip_değer in (9, 10, 11, 12, 18):
                değer = (Okuyucu_değer.수('H'), Okuyucu_değer.수('H'))
            elif Tip_değer == 15:
                değer = (Okuyucu_değer.수('B'), Okuyucu_değer.수('H'))
            else:
                raise derleme_hatası('지원하지 않는 sabit_değer Tip_değer: {}'.format(Tip_değer))
            자신.sabit_değer[Dizin] = (Tip_değer, değer)
            Dizin += 2 if Tip_değer in (5, 6) else 1
        자신.erişim_girdi = Okuyucu_değer.수('H')
        자신.İsim = 자신.sınıf_adı(Okuyucu_değer.수('H'))
        ana_değer = Okuyucu_değer.수('H')
        if 자신.sınıf_adı(ana_değer) != 'java/lang/Object' or Okuyucu_değer.수('H') != 0:
            raise derleme_hatası(자신.İsim + ': 상속 및 인터페이스는 아직 지원하지 않음')
        자신.alan_değeri = 자신.멤버읽기(Okuyucu_değer)
        자신.işlev_değer = 자신.멤버읽기(Okuyucu_değer)
        자신.속성읽기(Okuyucu_değer)

    def 문자(자신, Dizin):
        if 자신.sabit_değer[Dizin][0] != 1:
            raise derleme_hatası('dize_değer sabit_değer biçim_değer hata')
        return 자신.sabit_değer[Dizin][1]

    def sınıf_adı(자신, Dizin):
        return 자신.문자(자신.sabit_değer[Dizin][1])

    def Başvuru(자신, Dizin):
        sahip_değer, ad_biçim = 자신.sabit_değer[Dizin][1]
        İsim, biçim_değer = 자신.sabit_değer[ad_biçim][1]
        return 자신.sınıf_adı(sahip_değer), 자신.문자(İsim), 자신.문자(biçim_değer)

    def 속성읽기(자신, Okuyucu_değer):
        sonuç = {}
        for _ in range(Okuyucu_değer.수('H')):
            İsim = 자신.문자(Okuyucu_değer.수('H'))
            sonuç[İsim] = Okuyucu_değer.Okuma(Okuyucu_değer.수('I'))
        return sonuç

    def 멤버읽기(자신, Okuyucu_değer):
        sonuç = []
        for _ in range(Okuyucu_değer.수('H')):
            erişim_girdi = Okuyucu_değer.수('H')
            İsim = 자신.문자(Okuyucu_değer.수('H'))
            biçim_değer = 자신.문자(Okuyucu_değer.수('H'))
            sonuç.append((erişim_girdi, İsim, biçim_değer, 자신.속성읽기(Okuyucu_değer)))
        return sonuç


def 형식읽기(dize_değer):
    sonuç = []
    konum = 0
    while konum < len(dize_değer):
        for biçim_değer in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if dize_değer.startswith(biçim_değer, konum):
                sonuç.append(biçim_değer)
                konum += len(biçim_değer)
                break
        else:
            raise derleme_hatası('지원하지 않는 veri_türü: ' + dize_değer)
    return sonuç


def metot_tanımlayıcı(서술):
    bağımsız_değişkenler, İade_KR = 서술[1:].split(')')
    bağımsız_değişkenler = 형식읽기(bağımsız_değişkenler)
    dönüş_türü = 형식읽기(İade_KR)
    if 'V' in bağımsız_değişkenler or len(dönüş_türü) != 1:
        raise derleme_hatası('işlev_değer 서술 biçim_değer hata: ' + 서술)
    return bağımsız_değişkenler, İade_KR


def simge(Tip_değer, *부분):
    kaynakKod = '\x00'.join(부분).encode('utf-8')
    return 'j_{}_{}'.format(Tip_değer, hashlib.sha256(kaynakKod).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 işlev_değer 서술에 대해서만 허용한다.
def yürütmek_komut(bağımsız_değişkenler=None):
    ayrıştırıcı_48ee4b1b = argparse.ArgumentParser(description='Öz Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK kaynak_ağaç oluştur')
    ayrıştırıcı_48ee4b1b.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    ayrıştırıcı_48ee4b1b.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 Ekleme_girdi JAR/Sınıf_değer 디렉터리')
    ayrıştırıcı_48ee4b1b.add_argument('--java-home', help='openjdk 앱의 oluştur JDK 또는 openjdk-build의 부트 JDK yol')
    ayrıştırıcı_48ee4b1b.add_argument('--bundle-runtime', help='yürütmek_komut 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    ayrıştırıcı_48ee4b1b.add_argument('--cc', default='cc', help='OpenJDK program_Launcher/kaynak_ağaç 빌드의 C derleyici')
    ayrıştırıcı_48ee4b1b.add_argument('--cxx', help='openjdk-build의 C++ derleyici')
    ayrıştırıcı_48ee4b1b.add_argument('--jobs', type=int, default=2, help='openjdk-build의 oluştur 작업 수')
    ayrıştırıcı_48ee4b1b.add_argument('--openjdk-target', help='공식 OpenJDK 교차 oluştur hedef (예: aarch64-linux-gnu)')
    ayrıştırıcı_48ee4b1b.add_argument('--sysroot', help='교차 oluştur 대상의 libc/헤더/kitaplık 루트')
    ayrıştırıcı_48ee4b1b.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 biçim_değer')
    ayrıştırıcı_48ee4b1b.add_argument('--export', action='append', default=[], help='외부기호=Sınıf_değer.işlev_değer (Öz işlenen_Yığın ABI)')
    ayrıştırıcı_48ee4b1b.add_argument('--entry', help='예: 계산.çalıştır (openjdk-build 이외 대상에서 필수)')
    ayrıştırıcı_48ee4b1b.add_argument('-o', '--output', required=True, help='yürütmek_komut ELF/.o metinÇıktısı; openjdk-build는 전용 oluştur 디렉터리')
    ayrıştırıcı_48ee4b1b.add_argument('sources', nargs='+')
    parametre_bağımsız_değişken = ayrıştırıcı_48ee4b1b.parse_args(bağımsız_değişkenler)
    if parametre_bağımsız_değişken.target == 'openjdk-build':
        if len(parametre_bağımsız_değişken.sources) != 1 or not parametre_bağımsız_değişken.java_home or parametre_bağımsız_değişken.entry or parametre_bağımsız_değişken.export or parametre_bağımsız_değişken.classpath or parametre_bağımsız_değişken.bundle_runtime:
            raise derleme_hatası('openjdk-build: OpenJDK kaynak_ağaç 디렉터리 하나와 --java-home 부트 JDK, -o oluştur 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(parametre_bağımsız_değişken.sources[0], parametre_bağımsız_değişken.output, parametre_bağımsız_değişken.java_home, parametre_bağımsız_değişken.jobs, parametre_bağımsız_değişken.openjdk_target,
                  parametre_bağımsız_değişken.sysroot, None if parametre_bağımsız_değişken.cc == 'cc' else parametre_bağımsız_değişken.cc, parametre_bağımsız_değişken.cxx, parametre_bağımsız_değişken.configure_arg)
        except BuildError as hata:
            raise derleme_hatası(str(hata))
        return
    if not parametre_bağımsız_değişken.entry:
        ayrıştırıcı_48ee4b1b.error('--entry is required for this target')
    if parametre_bağımsız_değişken.cxx or parametre_bağımsız_değişken.openjdk_target or parametre_bağımsız_değişken.sysroot or parametre_bağımsız_değişken.configure_arg or parametre_bağımsız_değişken.jobs != 2:
        raise derleme_hatası('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build hedef 전용')
    if parametre_bağımsız_değişken.target == 'openjdk':
        sys.modules.setdefault('derleyici', sys.modules[__name__])
        from çalıştırılabilir import açmak_girdi
        açmak_girdi(parametre_bağımsız_değişken)
        return
    if parametre_bağımsız_değişken.classpath or parametre_bağımsız_değişken.java_home or parametre_bağımsız_değişken.bundle_runtime or parametre_bağımsız_değişken.cc != 'cc':
        raise derleme_hatası('classpath/java-home/bundle-runtime/cc 옵션은 openjdk hedef 전용')
    자바명령 = ['sh', str(Path(__file__).resolve().parent/'미리번역.sh'),
                '--target', parametre_bağımsız_değişken.target, '--entry', parametre_bağımsız_değişken.entry, '-o', parametre_bağımsız_değişken.output]
    for Ata_değer in parametre_bağımsız_değişken.export: 자바명령.extend(['--export', Ata_değer])
    subprocess.run(자바명령+parametre_bağımsız_değişken.sources, check=True)
    return


if __name__ == '__main__':
    try:
        yürütmek_komut()
    except (derleme_hatası, OSError, ValueError, subprocess.CalledProcessError) as hata:
        print('derlemek_kaynak hata: ' + str(hata), file=sys.stderr)
        sys.exit(1)
