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


class 翻訳工程エラー(Exception):
    pass


class データ読取:
    def __init__(自身値, データ):
        自身値.データ = データ
        自身値.位置 = 0

    def 読取(自身値, 長さ):
        if 長さ < 0 or 自身値.位置 + 長さ > len(自身値.データ):
            raise 翻訳工程エラー('切抜き済み値 クラス値 또는 命令 データ')
        結果 = 自身値.データ[自身値.位置:自身値.位置 + 長さ]
        自身値.位置 += 長さ
        return 結果

    def 数(自身値, 書式値):
        return struct.unpack('>' + 書式値, 自身値.読取(struct.calcsize('>' + 書式値)))[0]


def 改変済みUTF8復号(データ):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    文字列 = データ.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return 文字列.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class クラス値:
    def __init__(自身値, 経路):
        自身値.経路 = 経路
        読取器値 = データ読取(経路.read_bytes())
        if 読取器値.数('I') != 0xcafebabe:
            raise 翻訳工程エラー('Java クラス値 표식이 아님')
        読取器値.読取(4)
        項目個数 = 読取器値.数('H')
        自身値.定数値 = [None] * 項目個数
        番号 = 1
        while 番号 < 項目個数:
            種別値 = 読取器値.数('B')
            if 種別値 == 1:
                値 = 改変済みUTF8復号(読取器値.読取(読取器値.数('H')))
            elif 種別値 == 3:
                値 = 読取器値.数('i')
            elif 種別値 == 4:
                値 = 読取器値.読取(4)
            elif 種別値 in (5, 6):
                値 = 読取器値.読取(8)
            elif 種別値 in (7, 8, 16):
                値 = 読取器値.数('H')
            elif 種別値 in (9, 10, 11, 12, 18):
                値 = (読取器値.数('H'), 読取器値.数('H'))
            elif 種別値 == 15:
                値 = (読取器値.数('B'), 読取器値.数('H'))
            else:
                raise 翻訳工程エラー('지원하지 않는 定数値 種別値: {}'.format(種別値))
            自身値.定数値[番号] = (種別値, 値)
            番号 += 2 if 種別値 in (5, 6) else 1
        自身値.アクセス入口 = 読取器値.数('H')
        自身値.名前 = 自身値.クラス名前(読取器値.数('H'))
        親値 = 読取器値.数('H')
        if 自身値.クラス名前(親値) != 'java/lang/Object' or 読取器値.数('H') != 0:
            raise 翻訳工程エラー(自身値.名前 + ': 상속 및 인터페이스는 아직 지원하지 않음')
        自身値.フィールド値 = 自身値.成員一覧読取(読取器値)
        自身値.関数 = 自身値.成員一覧読取(読取器値)
        自身値.属性一覧読取(読取器値)

    def 文字(自身値, 番号):
        if 自身値.定数値[番号][0] != 1:
            raise 翻訳工程エラー('文字列 定数値 書式値 エラー')
        return 自身値.定数値[番号][1]

    def クラス名前(自身値, 番号):
        return 自身値.文字(自身値.定数値[番号][1])

    def 参照(自身値, 番号):
        所有者値, 名前書式 = 自身値.定数値[番号][1]
        名前, 書式値 = 自身値.定数値[名前書式][1]
        return 自身値.クラス名前(所有者値), 自身値.文字(名前), 自身値.文字(書式値)

    def 属性一覧読取(自身値, 読取器値):
        結果 = {}
        for _ in range(読取器値.数('H')):
            名前 = 自身値.文字(読取器値.数('H'))
            結果[名前] = 読取器値.読取(読取器値.数('I'))
        return 結果

    def 成員一覧読取(自身値, 読取器値):
        結果 = []
        for _ in range(読取器値.数('H')):
            アクセス入口 = 読取器値.数('H')
            名前 = 自身値.文字(読取器値.数('H'))
            書式値 = 自身値.文字(読取器値.数('H'))
            結果.append((アクセス入口, 名前, 書式値, 自身値.属性一覧読取(読取器値)))
        return 結果


def 型一覧解析(文字列):
    結果 = []
    位置 = 0
    while 位置 < len(文字列):
        for 書式値 in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if 文字列.startswith(書式値, 位置):
                結果.append(書式値)
                位置 += len(書式値)
                break
        else:
            raise 翻訳工程エラー('지원하지 않는 データ型: ' + 文字列)
    return 結果


def メソッド記述子(説明値):
    引数, 復帰結果 = 説明値[1:].split(')')
    引数 = 型一覧解析(引数)
    復帰型 = 型一覧解析(復帰結果)
    if 'V' in 引数 or len(復帰型) != 1:
        raise 翻訳工程エラー('関数 説明値 書式値 エラー: ' + 説明値)
    return 引数, 復帰結果


def 記号(種別値, *部分要素値):
    ソース = '\x00'.join(部分要素値).encode('utf-8')
    return 'j_{}_{}'.format(種別値, hashlib.sha256(ソース).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 関数 서술에 대해서만 허용한다.
def 命令実行(引数=None):
    構文解析器 = argparse.ArgumentParser(description='内蔵 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK ソース木 システム構築')
    構文解析器.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    構文解析器.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 入口追記 JAR/クラス値 디렉터리')
    構文解析器.add_argument('--java-home', help='openjdk 앱의 システム構築 JDK 또는 openjdk-build의 부트 JDK 経路')
    構文解析器.add_argument('--bundle-runtime', help='命令実行 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    構文解析器.add_argument('--cc', default='cc', help='OpenJDK プログラム実行器/ソース木 빌드의 C コンパイラ')
    構文解析器.add_argument('--cxx', help='openjdk-build의 C++ コンパイラ')
    構文解析器.add_argument('--jobs', type=int, default=2, help='openjdk-build의 システム構築 作業 数')
    構文解析器.add_argument('--openjdk-target', help='공식 OpenJDK 교차 システム構築 対象値 (예: aarch64-linux-gnu)')
    構文解析器.add_argument('--sysroot', help='교차 システム構築 대상의 libc/헤더/ライブラリ 루트')
    構文解析器.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 書式値')
    構文解析器.add_argument('--export', action='append', default=[], help='외부기호=クラス値.関数 (内蔵 被演算子スタック ABI)')
    構文解析器.add_argument('--entry', help='예: 計算結果.起動処理 (openjdk-build 이외 대상에서 判定必須)')
    構文解析器.add_argument('-o', '--output', required=True, help='命令実行 ELF/.o 出力; openjdk-build는 전용 システム構築 디렉터리')
    構文解析器.add_argument('sources', nargs='+')
    仮引数引数 = 構文解析器.parse_args(引数)
    if 仮引数引数.target == 'openjdk-build':
        if len(仮引数引数.sources) != 1 or not 仮引数引数.java_home or 仮引数引数.entry or 仮引数引数.export or 仮引数引数.classpath or 仮引数引数.bundle_runtime:
            raise 翻訳工程エラー('openjdk-build: OpenJDK ソース木 디렉터리 하나와 --java-home 부트 JDK, -o システム構築 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(仮引数引数.sources[0], 仮引数引数.output, 仮引数引数.java_home, 仮引数引数.jobs, 仮引数引数.openjdk_target,
                  仮引数引数.sysroot, None if 仮引数引数.cc == 'cc' else 仮引数引数.cc, 仮引数引数.cxx, 仮引数引数.configure_arg)
        except BuildError as エラー:
            raise 翻訳工程エラー(str(エラー))
        return
    if not 仮引数引数.entry:
        構文解析器.error('--entry is required for this target')
    if 仮引数引数.cxx or 仮引数引数.openjdk_target or 仮引数引数.sysroot or 仮引数引数.configure_arg or 仮引数引数.jobs != 2:
        raise 翻訳工程エラー('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build 対象値 전용')
    if 仮引数引数.target == 'openjdk':
        sys.modules.setdefault('コンパイラ', sys.modules[__name__])
        from 実行形式ファイル import 入口作成
        入口作成(仮引数引数)
        return
    if 仮引数引数.classpath or 仮引数引数.java_home or 仮引数引数.bundle_runtime or 仮引数引数.cc != 'cc':
        raise 翻訳工程エラー('classpath/java-home/bundle-runtime/cc 옵션은 openjdk 対象値 전용')
    Java命令 = ['sh', str(Path(__file__).resolve().parent/'事前用時間.sh'),
                '--target', 仮引数引数.target, '--entry', 仮引数引数.entry, '-o', 仮引数引数.output]
    for 代入値 in 仮引数引数.export: Java命令.extend(['--export', 代入値])
    subprocess.run(Java命令+仮引数引数.sources, check=True)
    return


if __name__ == '__main__':
    try:
        命令実行()
    except (翻訳工程エラー, OSError, ValueError, subprocess.CalledProcessError) as エラー:
        print('ソースコンパイル エラー: ' + str(エラー), file=sys.stderr)
        sys.exit(1)
