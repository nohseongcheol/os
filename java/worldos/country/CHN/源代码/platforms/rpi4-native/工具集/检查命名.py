#!/usr/bin/env python3
"""命名 裁剪·异常·경로를 검사한다. --시언어는 libclang 声明 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

项目根 = Path(__file__).resolve().parents[1]
代码库根 = 项目根.parents[1]

def 运行():
    解析器 = argparse.ArgumentParser(description=__doc__)
    解析器.add_argument('--C语言', action='store_true')
    实参 = 解析器.parse_args()
    失败列 = []
    契约值 = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    文件个数 = 0
    形参表 = {}
    可变参数函数 = set()
    AST节点列 = {}
    共享编译器集 = [代码库根/'compiler/编译器.py', 代码库根/'compiler/提前所属时间编译器.py']
    for 路径 in list((项目根/'工具集').glob('*.py')) + list((项目根/'用例').rglob('*.py')) + 共享编译器集:
        if 路径.name.endswith(('이름반영.py', '이름분석.py')): continue
        文件个数 += 1
        AST节点 = ast.parse(路径.read_text()); AST节点列[路径] = AST节点
        for 条目值 in ast.walk(AST节点):
            if isinstance(条目值, ast.FunctionDef):
                形参表.setdefault(条目值.name, set()).update(形参参数.arg for 形参参数 in 条目值.args.args + 条目值.args.kwonlyargs)
                if 条目值.args.kwarg: 可变参数函数.add(条目值.name)
            if isinstance(条目值, ast.ClassDef):
                for 函数 in 条目值.body:
                    if isinstance(函数, ast.FunctionDef) and 函数.name == '__init__':
                        形参表.setdefault(条目值.name, set()).update(形参参数.arg for 形参参数 in 函数.args.args + 函数.args.kwonlyargs)
            名称 = ''
            if isinstance(条目值, (ast.FunctionDef, ast.ClassDef)): 名称 = 条目值.name
            elif isinstance(条目值, ast.Name) and isinstance(条目值.ctx, ast.Store): 名称 = 条目值.id
            elif isinstance(条目值, ast.arg): 名称 = 条目值.arg
            if 名称 and 名称 not in 契约值 and all(ord(字符值)<128 for 字符值 in 名称):
                失败列.append('{}:{}: {}'.format(路径.relative_to(代码库根), 条目值.lineno, 名称))
    for 路径, AST节点 in AST节点列.items():
        for 调用 in ast.walk(AST节点):
            if not isinstance(调用, ast.Call): continue
            名称 = 调用.func.id if isinstance(调用.func, ast.Name) else 调用.func.attr if isinstance(调用.func, ast.Attribute) else ''
            if 名称 not in 形参表 or 名称 in 可变参数函数 or not any(ord(字符值)>127 for 字符值 in 名称): continue
            for 形参参数 in 调用.keywords:
                if 形参参数.arg and 形参参数.arg not in 形参表[名称]:
                    失败列.append('{}:{}: {}의 매개변수 {}'.format(路径.relative_to(代码库根), 调用.lineno, 名称, 形参参数.arg))
    for 行 in (项目根/'命名/文件名称映射.tsv').read_text().splitlines()[1:]:
        上一个项目, 当前项目, 进程值条目 = 行.split('\t')
        if not (项目根/当前项目).is_file(): 失败列.append('移动值 文件 缺失方法: '+当前项目)
        if 进程值条目 == '호환진입점유지' and not (项目根/上一个项目).is_file(): 失败列.append('호환 条目分 缺失方法: '+上一个项目)
    用例 = (项目根.parents[1]/'example/java/网络例.java').read_text()
    for 禁止调用列 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 禁止调用列 in 用例: 失败列.append('네트워크 예제에 남은 표준 직접 调用: '+禁止调用列)
    # 사용자가 읽는 Java 예제는 已保留位单词列/리터럴을 제외한 식별자도 构建全部 한국어다.
    已保留位单词列 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for 路径 in sorted((项目根.parents[1]/'example/java').glob('*.java')):
        源代码 = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', 路径.read_text())
        for 名称 in re.findall(r'\b[^\W\d]\w*\b', 源代码, re.UNICODE):
            if 名称 not in 已保留位单词列 and all(ord(字符值)<128 for 字符值 in 名称):
                失败列.append('{}: 예제의 영어 标识符值 {}'.format(路径.name, 名称))
    for 名称 in ('窗口', '按钮', '标签', '文本字段', '屏幕元素', '事件排队', '后台任务', '可运行任务任务', '动作接收者', '动作通知', '任务'):
        源代码 = (项目根/'中文Java/中文/内置'/(名称+'.java')).read_text()
        源代码 = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', 源代码)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', 源代码):
            失败列.append(名称+': 中文 직접 구현에 표준 对象值 래퍼가 남았습니다.')
    C示例 = (项目根.parents[1]/'example/c/网络例.c').read_text()
    for 名称 in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if 名称 in C示例: 失败列.append('C 通信 예제에 남은 표준 名称: '+名称)
    Python示例 = (项目根.parents[1]/'example/python/网络例.py').read_text()
    if 'OSError' in Python示例 or '.args' in Python示例: 失败列.append('Python 通信 예제에 남은 표준 异常 직접 使用值')
    头值 = (项目根.parents[1]/'posix-kor/arm64-native/头文件/网络ABI.h').read_text()
    for 名称 in ('互联网族', '数据报套接字', '数据报协议', '套接字地址', '互联网套接字地址', '创建端点', '发送数据报数据'):
        if re.search(r'^#define\s+'+名称+r'\b', 头值, re.M): 失败列.append('C 직접 实现 대신 宏值 使用值: '+名称)
    Java文件个数 = 0
    for 根值 in ('源代码', '用户/Java', '中文Java'):
        for 路径 in (项目根/根值).rglob('*.java'):
            Java文件个数 += 1
            源代码 = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', 路径.read_text())
            for 是否已匹配 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', 源代码):
                失败列.append('{}: 한국어화되지 않은 声明 {}'.format(路径.relative_to(项目根), 是否已匹配[1]))
            if 根值 == '中文Java' and re.search(r'\bthrows\s+[A-Za-z]', 源代码):
                失败列.append('{}: 공개 异常 声明'.format(路径.relative_to(项目根)))
    x86Java文件数 = 0
    标准Java名称列 = {'String', 'length', 'charAt'}
    for 路径 in sorted((代码库根/'os/源代码').glob('*.java')):
        x86Java文件数 += 1
        源代码 = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', 路径.read_text())
        for 名称 in re.findall(r'\b[^\W\d]\w*\b', 源代码, re.UNICODE):
            if 名称 not in 已保留位单词列 | 标准Java名称列 and all(ord(字符值)<128 for 字符值 in 名称):
                失败列.append('{}: 内置 영어 标识符值 {}'.format(路径.relative_to(代码库根), 名称))
    日志记录 = {'passed': False, 'python_files': 文件个数, 'java_files': Java文件个数,
          'x86_java_files': x86Java文件数, 'host_compiler_python_files': len(共享编译器集), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 实参.C语言:
        subprocess.check_call(['python3', str(项目根/'工具集/分析C名称列.py')])
        分析值 = json.loads((项目根/'build/한국어화/시언어분석.json').read_text())
        失败列.extend(str(错误) for 错误 in 分析值['错误'])
        导出ABI = set(json.loads((项目根/'命名/标准名称列.json').read_text()))
        for 条目值 in 分析值['声明'].values():
            名称 = 条目值['名称']; 路径 = Path(条目值['文件'])
            源代码 = 路径.read_bytes()
            # 中文 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if 源代码[条目值['偏移值']:条目值['偏移值']+len(名称)] == 名称.encode() and 名称 not in 导出ABI:
                失败列.append('{}:{}: {}'.format(路径.relative_to(项目根), 条目值['行'], 名称))
        日志记录['c_semantic_checked'] = True
        日志记录['c_source_sha256'] = {str(Path(文件).relative_to(项目根)):哈希文件 for 文件,哈希文件 in 分析值['원문해시'].items()}
    日志记录['passed'] = not 失败列; 日志记录['failures'] = 失败列
    目的地址值 = 项目根/'build/verification/naming'; 目的地址值.mkdir(parents=True, exist_ok=True)
    (目的地址值/'report.json').write_text(json.dumps(日志记录, ensure_ascii=False, indent=2)+'\n')
    if 失败列: raise SystemExit('\n'.join(失败列))
    print('PASS: 中文 声明·文件 路径·호환 条目分·通信 用例')

if __name__ == '__main__': 运行()
