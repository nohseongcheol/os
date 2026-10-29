#!/usr/bin/env python3
"""OpenJDK와 内置 ARM64 커널에서 동일 class 파일을 실행하여 출력을 비교한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 执行命令 import 项目根


def 运行():
    输出结果 = 项目根 / 'build/verification/jvm'
    类路径 = 输出结果 / 'classes'; 类路径.mkdir(parents=True, exist_ok=True)
    Java捆绑 = 项目根 / 'dist/jkoros-native-korean.jar'
    源代码列表 = sorted((项目根 / '测试/Java').rglob('*.java'))
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Java捆绑), '-d', str(类路径)] + [str(字符串数据) for 字符串数据 in 源代码列表])
    测试列表 = [('测试对象集', ['背景值', '分支值', '能够计算']), ('测试异常列', []), ('集合测试', []),
             ('测试线程集', ['计数器值', '任务动作', '线程值']), ('测试韩文字母', []), ('测试联网', []), ('测试韩语联网', []), ('测试韩语异常列', []), ('韩文字母源代码', []), ('测试边界列', []), ('有效性校验.测试捆绑', []), ('条目兼容性测试', [])]
    有效性验证报告 = {'passed': False, 'linux_loaded': False, 'machine': 'raspi4b',
              'kernel_sha256': hashlib.sha256((项目根 / 'build/kernel8.img').read_bytes()).hexdigest(),
              'korean_library_sha256': hashlib.sha256(Java捆绑.read_bytes()).hexdigest(), 'tests': []}
    try:
        for 名称, 包含项 in 测试列表:
            with tempfile.TemporaryDirectory(prefix='jkoros-reference-') as 临时路径:
                预期 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(类路径) + ':' + str(Java捆绑), 名称], cwd=临时路径, timeout=15).decode('utf-8')
            命令参数列 = ['python3', str(项目根 / '工具集/执行文件.py'), str(类路径 / (名称.replace('.', '/') + '.class'))]
            if '.' in 名称: 命令参数列 += ['--class-name', 名称]
            for 包含条目 in 包含项: 命令参数列 += ['--include', str(类路径 / (包含条目 + '.class'))]
            if 名称 == '韩文字母源代码': 命令参数列[2] = str(项目根 / '测试/Java/韩文字母源代码.java')
            已完成总量 = subprocess.run(命令参数列, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            实际结果 = 已完成总量.stdout.decode('utf-8').replace('\r\n', '\n')
            (输出结果 / (名称 + '.log')).write_text(实际结果, encoding='utf-8')
            是否相等 = re.search(r"(?:^|\n)jkoros-native> java [^\n]+\n(.*?)\nexit 0\n|^java [^\n]+\n(.*?)\nexit 0\n", 实际结果, re.S)
            assert 已完成总量.returncode == 0 and 是否相等, (名称, 实际结果)
            结果 = next(字符串数据 for 字符串数据 in 是否相等.groups() if 字符串数据 is not None) + '\n'
            assert 结果 == 预期, (名称, 预期, 结果)
            有效性验证报告['tests'].append({'name': 名称, 'passed': True, 'openjdk_output_equal': True})
            print('PASS:', 名称, flush=True)
        # 内置 JVM에 직접 연결한 中文 线程值/진입점은 OpenJDK용 래퍼가 아니다.
        已完成总量 = subprocess.run(['python3', str(项目根/'工具集/执行文件.py'), str(类路径/'测试韩语线程集.class')],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        结果 = 已完成总量.stdout.decode('utf-8').replace('\r\n', '\n')
        (输出结果/'测试韩语线程集.log').write_text(结果)
        assert 已完成总量.returncode == 0 and '中文 직접 线程值 通过值\n' in 结果 and '\nexit 0\n' in 结果, 结果
        有效性验证报告['direct_korean_thread_and_entry'] = True
        print('PASS: 中文 직접 线程值·执行任务·运行 条目分', flush=True)
        有效 = (类路径 / '测试对象集.class').read_bytes()
        测试情况 = [('판거부', 有效[:6] + b'\x00\x35' + 有效[8:], 'supported class versions'),
                 ('잘린클래스', 有效[:24], 'truncated class file')]
        有效性验证报告['rejection_tests'] = []
        for 名称, 载荷数据数据, 通知文本 in 测试情况:
            测试数据 = 输出结果 / (名称 + '.class'); 测试数据.write_bytes(载荷数据数据)
            已完成总量 = subprocess.run(['python3', str(项目根 / '工具集/执行文件.py'), str(测试数据)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
            文本 = 已完成总量.stdout.decode('utf-8').replace('\r\n', '\n')
            (输出结果 / (名称 + '.log')).write_text(文本, encoding='utf-8')
            assert 已完成总量.returncode == 1 and 通知文本 in 文本 and 'exit 1\n' in 文本, (名称, 文本)
            有效性验证报告['rejection_tests'].append({'name': 名称, 'passed': True})
            print('PASS (rejected):', 名称, flush=True)
        有效性验证报告['passed'] = True
    finally:
        (输出结果 / 'report.json').write_text(json.dumps(有效性验证报告, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    运行()
