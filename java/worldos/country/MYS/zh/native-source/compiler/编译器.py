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


class 编译过程错误(Exception):
    pass


class 读取数据:
    def __init__(自身值, 数据):
        自身值.数据 = 数据
        自身值.位置 = 0

    def 读取(自身值, 长度):
        if 长度 < 0 or 自身值.位置 + 长度 > len(自身值.数据):
            raise 编译过程错误('已裁剪值 类值 또는 命令 数据')
        结果 = 自身值.数据[自身值.位置:自身值.位置 + 长度]
        自身值.位置 += 长度
        return 结果

    def 数(自身值, 格式值):
        return struct.unpack('>' + 格式值, 自身值.读取(struct.calcsize('>' + 格式值)))[0]


def 解码已修改UTF8(数据):
    # CONSTANT_Utf8은 NUL 및 UTF-16 대리쌍을 사용하는 modified UTF-8이다.
    字符串 = 数据.replace(b'\xc0\x80', b'\x00').decode('utf-8', 'surrogatepass')
    return 字符串.encode('utf-16-le', 'surrogatepass').decode('utf-16-le', 'surrogatepass')


class 类值:
    def __init__(自身值, 路径):
        自身值.路径 = 路径
        读取器值 = 读取数据(路径.read_bytes())
        if 读取器值.数('I') != 0xcafebabe:
            raise 编译过程错误('Java 类值 표식이 아님')
        读取器值.读取(4)
        项目个数 = 读取器值.数('H')
        自身值.常量值 = [None] * 项目个数
        编号 = 1
        while 编号 < 项目个数:
            种类值 = 读取器值.数('B')
            if 种类值 == 1:
                值 = 解码已修改UTF8(读取器值.读取(读取器值.数('H')))
            elif 种类值 == 3:
                值 = 读取器值.数('i')
            elif 种类值 == 4:
                值 = 读取器值.读取(4)
            elif 种类值 in (5, 6):
                值 = 读取器值.读取(8)
            elif 种类值 in (7, 8, 16):
                值 = 读取器值.数('H')
            elif 种类值 in (9, 10, 11, 12, 18):
                值 = (读取器值.数('H'), 读取器值.数('H'))
            elif 种类值 == 15:
                值 = (读取器值.数('B'), 读取器值.数('H'))
            else:
                raise 编译过程错误('지원하지 않는 常量值 种类值: {}'.format(种类值))
            自身值.常量值[编号] = (种类值, 值)
            编号 += 2 if 种类值 in (5, 6) else 1
        自身值.存取条目 = 读取器值.数('H')
        自身值.名称 = 自身值.类名称(读取器值.数('H'))
        父值 = 读取器值.数('H')
        if 自身值.类名称(父值) != 'java/lang/Object' or 读取器值.数('H') != 0:
            raise 编译过程错误(自身值.名称 + ': 상속 및 인터페이스는 아직 지원하지 않음')
        自身值.字段值 = 自身值.读取成员列(读取器值)
        自身值.函数 = 自身值.读取成员列(读取器值)
        自身值.读取属性集(读取器值)

    def 字符(自身值, 编号):
        if 自身值.常量值[编号][0] != 1:
            raise 编译过程错误('字符串 常量值 格式值 错误')
        return 自身值.常量值[编号][1]

    def 类名称(自身值, 编号):
        return 自身值.字符(自身值.常量值[编号][1])

    def 引用(自身值, 编号):
        所有者值, 名称格式 = 自身值.常量值[编号][1]
        名称, 格式值 = 自身值.常量值[名称格式][1]
        return 自身值.类名称(所有者值), 自身值.字符(名称), 自身值.字符(格式值)

    def 读取属性集(自身值, 读取器值):
        结果 = {}
        for _ in range(读取器值.数('H')):
            名称 = 自身值.字符(读取器值.数('H'))
            结果[名称] = 读取器值.读取(读取器值.数('I'))
        return 结果

    def 读取成员列(自身值, 读取器值):
        结果 = []
        for _ in range(读取器值.数('H')):
            存取条目 = 读取器值.数('H')
            名称 = 自身值.字符(读取器值.数('H'))
            格式值 = 自身值.字符(读取器值.数('H'))
            结果.append((存取条目, 名称, 格式值, 自身值.读取属性集(读取器值)))
        return 结果


def 解析类型列(字符串):
    结果 = []
    位置 = 0
    while 位置 < len(字符串):
        for 格式值 in ('Ljava/lang/String;', '[I', 'I', 'Z', 'B', 'C', 'S', 'V'):
            if 字符串.startswith(格式值, 位置):
                结果.append(格式值)
                位置 += len(格式值)
                break
        else:
            raise 编译过程错误('지원하지 않는 数据类型: ' + 字符串)
    return 结果


def 方法描述符(说明值):
    实参, 发回结果 = 说明值[1:].split(')')
    实参 = 解析类型列(实参)
    发回类型 = 解析类型列(发回结果)
    if 'V' in 实参 or len(发回类型) != 1:
        raise 编译过程错误('函数 说明值 格式值 错误: ' + 说明值)
    return 实参, 发回结果


def 符号(种类值, *子部分值):
    源代码 = '\x00'.join(子部分值).encode('utf-8')
    return 'j_{}_{}'.format(种类值, hashlib.sha256(源代码).hexdigest()[:24])


# CPU 경계는 이 클래스와 정확한 函数 서술에 대해서만 허용한다.
def 执行命令(实参=None):
    解析器 = argparse.ArgumentParser(description='内置 Java AOT, OpenJDK 앱 포장 또는 공식 OpenJDK 源代码树 构建系统')
    解析器.add_argument('--target', choices=['linux', 'kernel', 'user', 'openjdk', 'openjdk-build'], default='linux')
    解析器.add_argument('--classpath', action='append', default=[], help='openjdk 대상의 追加条目 JAR/类值 디렉터리')
    解析器.add_argument('--java-home', help='openjdk 앱의 构建系统 JDK 또는 openjdk-build의 부트 JDK 路径')
    解析器.add_argument('--bundle-runtime', help='执行命令 파일과 함께 제공할 같은 CPU/OS용 JDK/JRE 디렉터리')
    解析器.add_argument('--cc', default='cc', help='OpenJDK 运行器/源代码树 빌드의 C 编译器')
    解析器.add_argument('--cxx', help='openjdk-build의 C++ 编译器')
    解析器.add_argument('--jobs', type=int, default=2, help='openjdk-build의 构建系统 任务 数')
    解析器.add_argument('--openjdk-target', help='공식 OpenJDK 교차 构建系统 目标值 (예: aarch64-linux-gnu)')
    解析器.add_argument('--sysroot', help='교차 构建系统 대상의 libc/헤더/库 루트')
    解析器.add_argument('--configure-arg', action='append', default=[], help='공식 configure에 전달할 옵션; --configure-arg=--옵션 格式值')
    解析器.add_argument('--export', action='append', default=[], help='외부기호=类值.函数 (内置 操作数栈 ABI)')
    解析器.add_argument('--entry', help='예: 计算结果.运行 (openjdk-build 이외 대상에서 是否必需)')
    解析器.add_argument('-o', '--output', required=True, help='执行命令 ELF/.o 输出; openjdk-build는 전용 构建系统 디렉터리')
    解析器.add_argument('sources', nargs='+')
    形参参数 = 解析器.parse_args(实参)
    if 形参参数.target == 'openjdk-build':
        if len(形参参数.sources) != 1 or not 形参参数.java_home or 形参参数.entry or 形参参数.export or 形参参数.classpath or 形参参数.bundle_runtime:
            raise 编译过程错误('openjdk-build: OpenJDK 源代码树 디렉터리 하나와 --java-home 부트 JDK, -o 构建系统 디렉터리를 지정하세요')
        from openjdk_build import build, BuildError
        try:
            build(形参参数.sources[0], 形参参数.output, 形参参数.java_home, 形参参数.jobs, 形参参数.openjdk_target,
                  形参参数.sysroot, None if 形参参数.cc == 'cc' else 形参参数.cc, 形参参数.cxx, 形参参数.configure_arg)
        except BuildError as 错误:
            raise 编译过程错误(str(错误))
        return
    if not 形参参数.entry:
        解析器.error('--entry is required for this target')
    if 形参参数.cxx or 形参参数.openjdk_target or 形参参数.sysroot or 形参参数.configure_arg or 形参参数.jobs != 2:
        raise 编译过程错误('cxx/jobs/openjdk-target/sysroot/configure-arg 옵션은 openjdk-build 目标值 전용')
    if 形参参数.target == 'openjdk':
        sys.modules.setdefault('编译器', sys.modules[__name__])
        from 可执行文件文件 import 创建条目
        创建条目(形参参数)
        return
    if 形参参数.classpath or 形参参数.java_home or 形参参数.bundle_runtime or 形参参数.cc != 'cc':
        raise 编译过程错误('classpath/java-home/bundle-runtime/cc 옵션은 openjdk 目标值 전용')
    Java命令 = ['sh', str(Path(__file__).resolve().parent/'提前所属时间.sh'),
                '--target', 形参参数.target, '--entry', 形参参数.entry, '-o', 形参参数.output]
    for 赋值值 in 形参参数.export: Java命令.extend(['--export', 赋值值])
    subprocess.run(Java命令+形参参数.sources, check=True)
    return


if __name__ == '__main__':
    try:
        执行命令()
    except (编译过程错误, OSError, ValueError, subprocess.CalledProcessError) as 错误:
        print('编译源代码 错误: ' + str(错误), file=sys.stderr)
        sys.exit(1)
