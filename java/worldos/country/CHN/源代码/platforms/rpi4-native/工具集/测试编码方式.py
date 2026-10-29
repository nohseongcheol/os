#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from 执行命令 import 项目根

def 运行():
    结果数据=项目根/'build/verification/coding';结果数据.mkdir(parents=True,exist_ok=True)
    有效性验证报告={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((项目根/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(项目根/'工具集/导出SDK.py')])
        with tarfile.open(str(项目根/'dist/jkoros-native-aarch64-sdk.tar.gz')) as 已压缩捆绑:已压缩捆绑.extractall(str(结果数据))
        开发工具套件=结果数据/'jkoros-native-sdk'
        符号列列表=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(开发工具套件/'lib/libposix-kor-user.a')]).decode()
        for 名称 in ('创建端点','绑定地址','发送数据报数据','接收数据报数据','打开文件','读取文件数据','写入文件数据'):
            assert ' T '+名称+'\n' in 符号列列表, 名称
        (结果数据/'korean-function-symbols.txt').write_text(符号列列表)
        有效性验证报告['checks'].append('real-korean-c-function-symbols')
        def 执行命令(名称,路径,参数数组,预期):
            数据位置=subprocess.run(['python3',str(项目根/'工具集/执行文件.py'),str(路径)]+参数数组,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (结果数据/(名称+'.log')).write_bytes(数据位置.stdout);assert 数据位置.returncode==0,数据位置.stdout.decode('utf-8','replace')
            assert 预期.encode() in 数据位置.stdout,数据位置.stdout;有效性验证报告['checks'].append(名称)
        for 后缀值 in ('c','cpp'):
            可执行文件文件=结果数据/('问候例-'+后缀值+'.elf')
            subprocess.check_call(['python3',str(开发工具套件/'compile.py'),str(开发工具套件/'examples'/('问候例.'+后缀值)),'-o',str(可执行文件文件)])
            执行命令('korean-'+后缀值,可执行文件文件,[],'posix-kor 调用')
        可执行文件文件=结果数据/'流值.elf'
        subprocess.check_call(['python3',str(开发工具套件/'compile.py'),str(开发工具套件/'examples/流值.c'),'-o',str(可执行文件文件)])
        执行命令('c-stream-queues',可执行文件文件,[],'C posix-kor 연결형 通信 PASS')
        执行命令('korean-python',项目根/'用例/韩文字母编码方式/问候例.py',['--include',str(项目根/'用例/韩文字母编码方式/中文.py')],'안녕하세요 누리')
        执行命令('guest-korean-javac',项目根/'用例/韩文字母编码方式/问候例.java',[],'안녕하세요 · 总计值=42')
        有效性验证报告['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(结果数据/'report.json').write_text(json.dumps(有效性验证报告,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':运行()
