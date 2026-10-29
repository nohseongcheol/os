"""内置 JVM용 中文 class/JAR와 EL0에 넣을 读取 전용 class 자료를 만든다."""
from pathlib import Path
import json
import zipfile


def 创建Java库(根路径, 执行命令):
    (根路径 / 'build/user').mkdir(parents=True, exist_ok=True)
    输出结果 = 根路径 / 'build/java-library'
    类路径 = 输出结果 / 'classes'
    类路径.mkdir(parents=True, exist_ok=True)
    源代码列表 = sorted((根路径 / '中文Java').rglob('*.java'))
    执行命令(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', 类路径] + 源代码列表)
    条目列列表 = []
    for 原始地址 in 源代码列表:
        相对路径 = 原始地址.relative_to(根路径 / '中文Java').with_suffix('.class')
        载荷数据数据 = (类路径 / 相对路径).read_bytes()
        名称 = str(相对路径).replace('/', '.')
        if len(载荷数据数据) > 16384 or len(名称.encode('utf-8')) > 511:
            raise ValueError('JVM class/name limit: ' + 名称)
        条目列列表.append((相对路径, 名称, 载荷数据数据))
    头部值 = ['/* Generated class resources; accessed only within the EL0 JVM. */',
              'typedef struct { const char *名称; const unsigned char *数据; unsigned 大小; } Java类资源;']
    for 序数索引, (_, 名称, 载荷数据数据) in enumerate(条目列列表):
        头部值.append('static const unsigned char Java类数据%d[] = {%s};' % (序数索引, ','.join(str(第二值) for 第二值 in 载荷数据数据)))
    头部值.append('static const Java类资源 Java类列表[] = {')
    for 序数索引, (_, 名称, 载荷数据数据) in enumerate(条目列列表):
        头部值.append('{%s, Java类数据%d, %d},' % (json.dumps(名称, ensure_ascii=False), 序数索引, len(载荷数据数据)))
    头部值.append('};')
    (根路径 / 'build/user/java-resources.h').write_text('\n'.join(头部值) + '\n', encoding='utf-8')
    分发路径 = 根路径 / 'dist'; 分发路径.mkdir(exist_ok=True)
    with zipfile.ZipFile(str(分发路径 / 'jkoros-native-korean.jar'), 'w', compression=zipfile.ZIP_DEFLATED) as Java捆绑:
        for 相对路径, _, 载荷数据数据 in 条目列列表:
            系统信息 = zipfile.ZipInfo(str(相对路径), date_time=(1980, 1, 1, 0, 0, 0)); 系统信息.compress_type = zipfile.ZIP_DEFLATED
            Java捆绑.writestr(系统信息, 载荷数据数据)
    with zipfile.ZipFile(str(分发路径 / 'jkoros-native-korean-sources.zip'), 'w', compression=zipfile.ZIP_DEFLATED) as 存档:
        for 原始地址 in 源代码列表:
            系统信息 = zipfile.ZipInfo(str(原始地址.relative_to(根路径 / '中文Java')), date_time=(1980, 1, 1, 0, 0, 0)); 系统信息.compress_type = zipfile.ZIP_DEFLATED
            存档.writestr(系统信息, 原始地址.read_bytes())
