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


class 編譯過程錯誤(Exception):
    pass


class 讀取資料:
    def __init__(自身值, 資料):
        自身值.資料 = 資料
        自身值.位置 = 0

    def 讀取(自身值, 長度):
        if 長度 < 0 or 自身值.位置 + 長度 > len(自身值.資料):
            raise 編譯過程錯誤('已裁剪值 類別值 또는 命令 資料')
        結果 = 自身值.資料[自身值.位置:自身值.位置 + 長度]
        自身值.位置 += 長度
        return 結果

    def 數(自身值, 格式值):
        return struct.unpack('>' + 格式值, 自身值.讀取(struct.calcsize('>' + 格式值)))[0]


def 解碼已修改UTF8(資料):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    字符串 = 資料.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return 字符串.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class 類別值:
    def __init__(自身值, 路徑):
        自身值.路徑 = 路徑
        讀取器值 = 讀取資料(路徑.read_bytes())
        if 讀取器值.數('I') != 0xcafebabe:
            raise 編譯過程錯誤('Java 類別值 표식이 아님')
        讀取器值.讀取(4)
        項目個數 = 讀取器值.數('H')
        自身值.常量值 = [None] * 項目個數
        編號 = 1
        while 編號 < 項目個數:
            種類值 = 讀取器值.數('B')
            if 種類值 == 1:
                值 = 解碼已修改UTF8(讀取器值.讀取(讀取器值.數('H')))
            elif 種類值 == 3:
                值 = 讀取器值.數('i')
            elif 種類值 == 4:
                值 = 讀取器值.讀取(4)
            elif 種類值 in (5, 6):
                值 = 讀取器值.讀取(8)
            elif 種類值 in (7, 8, 16):
                值 = 讀取器值.數('H')
            elif 種類值 in (9, 10, 11, 12, 18):
                值 = (讀取器值.數('H'), 讀取器值.數('H'))
            elif 種類值 == 15:
                值 = (讀取器值.數('B'), 讀取器值.數('H'))
            else:
                raise 編譯過程錯誤('지원하지 않는 常量值 種類值: {}'.format(種類值))
            自身值.常量值[編號] = (種類值, 值)
            編號 += 2 if 種類值 in (5, 6) else 1
        自身值.存取條目 = 讀取器值.數('H')
        自身值.名稱 = 自身值.類別名稱(讀取器值.數('H'))
        父值 = 讀取器值.數('H')
        if 自身值.類別名稱(父值) != 'java/lang/Object' or 讀取器值.數('H') != 0:
            raise 編譯過程錯誤(自身值.名稱 + ': 상속 및 인터페이스는 아직 지원하지 않음')
        自身值.字段值 = 自身值.讀取成員列(讀取器值)
        自身值.函數 = 自身值.讀取成員列(讀取器值)
        自身值.讀取屬性集(讀取器值)

    def 字元(自身值, 編號):
        if 自身值.常量值[編號][0] != 1:
            raise 編譯過程錯誤('字符串 常量值 格式值 錯誤')
        return 自身值.常量值[編號][1]

    def 類別名稱(自身值, 編號):
        return 自身值.字元(自身值.常量值[編號][1])

    def 引用(自身值, 編號):
        所有者值, 名稱格式 = 自身值.常量值[編號][1]
        名稱, 格式值 = 自身值.常量值[名稱格式][1]
        return 自身值.類別名稱(所有者值), 自身值.字元(名稱), 自身值.字元(格式值)

    def 讀取屬性集(自身值, 讀取器值):
        結果 = {}
        for _ in range(讀取器值.數('H')):
            名稱 = 自身值.字元(讀取器值.數('H'))
            結果[名稱] = 讀取器值.讀取(讀取器值.數('I'))
        return 結果

    def 讀取成員列(自身值, 讀取器值):
        結果 = []
        for _ in range(讀取器值.數('H')):
            存取條目 = 讀取器值.數('H')
            名稱 = 自身值.字元(讀取器值.數('H'))
            格式值 = 自身值.字元(讀取器值.數('H'))
            結果.append((存取條目, 名稱, 格式值, 自身值.讀取屬性集(讀取器值)))
        return 結果


def 解析類型列(字符串):
    結果 = []
    位置 = 0
    while 位置 < len(字符串):
        for 格式值 in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if 字符串.startswith(格式值, 位置):
                結果.append(格式值)
                位置 += len(格式值)
                break
        else:
            raise 編譯過程錯誤('지원하지 않는 資料類型: ' + 字符串)
    return 結果


def 方法描述符(說明值):
    實參, 發回結果 = 說明值[1:].split(')')
    實參 = 解析類型列(實參)
    發回類型 = 解析類型列(發回結果)
    if 'V' in 實參 or len(發回類型) != 1:
        raise 編譯過程錯誤('函數 說明值 格式值 錯誤: ' + 說明值)
    return 實參, 發回結果


def 符號(種類值, *子部分值):
    原始碼 = '\x00'.join(子部分值).encode('utf-8')
    return 'j_{}_{}'.format(種類值, hashlib.sha256(原始碼).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 函數 서술에 대해서만 허용한다.
def 執行命令(實參=None):
    解析器 = argparse.ArgumentParser(description='內建 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK 原始碼樹 構建系統')
    解析器.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    解析器.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 追加條目 JAR/類別值 디렉터리')
    解析器.add_argument('--java-home', help='openjdk 앱의 構建系統 JDK 또는 openjdk-build의 부트 JDK 路徑')
    解析器.add_argument('--bundle-runtime', help='執行命令 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    解析器.add_argument('--cc', default='cc', help='OpenJDK 運行器/原始碼樹 빌드의 C 編譯器')
    解析器.add_argument('--cxx', help='openjdk-build의 C++ 編譯器')
    解析器.add_argument('--jobs', type=int, default=2, help='openjdk-build의 構建系統 任務 數')
    解析器.add_argument('--openjdk-target', help='공식 OpenJDK 교차 構建系統 目標值 (예: aarch64-linux-gnu)')
    解析器.add_argument('--sysroot', help='교차 構建系統 대상의 libc/헤더/庫 루트')
    解析器.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 格式值')
    解析器.add_argument('--export', action='append', default=[], help='외부기호=類別值.函數 (內建 操作數棧 ABI)')
    解析器.add_argument('--entry', help='예: 計算結果.運行 (openjdk-build 이외 대상에서 是否必需)')
    解析器.add_argument('-o', '--output', required=True, help='執行命令 ELF/.o 輸出; openjdk-build는 전용 構建系統 디렉터리')
    解析器.add_argument('sources', nargs='+')
    形式參數實際參數 = 解析器.parse_args(實參)
    if 形式參數實際參數.target == 'openjdk-build':
        if len(形式參數實際參數.sources) != 1 or not 形式參數實際參數.java_home or 形式參數實際參數.entry or 形式參數實際參數.export or 形式參數實際參數.classpath or 形式參數實際參數.bundle_runtime:
            raise 編譯過程錯誤('openjdk-build: OpenJDK 原始碼樹 디렉터리 하나와 --java-home 부트 JDK, -o 構建系統 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(形式參數實際參數.sources[0], 形式參數實際參數.output, 形式參數實際參數.java_home, 形式參數實際參數.jobs, 形式參數實際參數.openjdk_target,
                  形式參數實際參數.sysroot, None if 形式參數實際參數.cc == 'cc' else 形式參數實際參數.cc, 形式參數實際參數.cxx, 形式參數實際參數.configure_arg)
        except BuildError as 錯誤:
            raise 編譯過程錯誤(str(錯誤))
        return
    if not 形式參數實際參數.entry:
        解析器.error('--entry is required for this target')
    if 形式參數實際參數.cxx or 形式參數實際參數.openjdk_target or 形式參數實際參數.sysroot or 形式參數實際參數.configure_arg or 形式參數實際參數.jobs != 2:
        raise 編譯過程錯誤('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build 目標值 전용')
    if 形式參數實際參數.target == 'openjdk':
        sys.modules.setdefault('編譯器', sys.modules[__name__])
        from 可執行文件檔案 import 創建條目
        創建條目(形式參數實際參數)
        return
    if 形式參數實際參數.classpath or 形式參數實際參數.java_home or 形式參數實際參數.bundle_runtime or 形式參數實際參數.cc != 'cc':
        raise 編譯過程錯誤('classpath/java-home/bundle-runtime/cc 옵션은 openjdk 目標值 전용')
    Java命令 = ['sh', str(Path(__file__).resolve().parent/'提前所屬時間.sh'),
                '--target', 形式參數實際參數.target, '--entry', 形式參數實際參數.entry, '-o', 形式參數實際參數.output]
    for 賦值值 in 形式參數實際參數.export: Java命令.extend(['--export', 賦值值])
    subprocess.run(Java命令+形式參數實際參數.sources, check=True)
    return


if __name__ == '__main__':
    try:
        執行命令()
    except (編譯過程錯誤, OSError, ValueError, subprocess.CalledProcessError) as 錯誤:
        print('編譯原始碼 錯誤: ' + str(錯誤), file=sys.stderr)
        sys.exit(1)
