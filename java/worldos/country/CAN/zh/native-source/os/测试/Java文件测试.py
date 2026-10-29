#!/usr/bin/env python3
"""게스트 작성 표준 FileStream 바이트코드를 독립 OpenJDK 실행과 대조한다."""
import json
from pathlib import Path
import re
import subprocess
import tempfile
from 测试用户网络 import 虚拟机, 位置
from Java测试 import 编辑值, 客户机文件

def 执行命令():
    结果 = {}
    源代码 = (位置.parent / 'posix-kor/Java示例/FileDemo.java').read_text()
    for 种类值 in ('elf', 'iso'):
        计算机 = 虚拟机(位置 / ('build/kernel.' + 种类值), 种类值, 网络值=False)
        try:
            编辑值(计算机, 'FileDemo.java', 源代码)
            计算机.命令('javac FileDemo.java', ['Compiled: FileDemo.class', 'Exit: 0'])
            for 迭代值 in range(2):
                输出 = 计算机.命令('java FileDemo', ['65\r\n255\r\n66\r\n-1\r\n', 'JAVA FILE IO PASS', 'Exit: 0'])
            条目列表 = 计算机.命令('ls', ['java.txt  3 bytes'])
            大小 = int(re.search(r'FileDemo.class\s+(\d+) bytes', 条目列表)[1])
            with tempfile.TemporaryDirectory(prefix='jkoros-stream-class-') as 临时值:
                目录值 = Path(临时值)
                客户机文件(计算机, 2, 大小, 目录值 / 'FileDemo.class')
                宿主 = subprocess.check_output(['java', '-Xverify:all', '-cp', str(目录值), 'FileDemo'], cwd=str(目录值), universal_newlines=True)
                assert 宿主 == '65\n255\n66\n-1\nJAVA FILE IO PASS\n', 宿主
                assert (目录值 / 'java.txt').read_bytes() == b'A\xffB'
            编辑值(计算机, 'FileDemo.java', 源代码.replace('output.write(65);', 'output.close(); output.write(65);'))
            计算机.命令('javac FileDemo.java', ['Exit: 0'])
            计算机.命令('java FileDemo', ['IOException: stream closed', 'Exit: 1'])
            编辑值(计算机, 'FileDemo.java', '''import java.io.FileInputStream;
public class FileDemo {
 public static void main(String[] args) throws Exception {
  FileInputStream input = new FileInputStream("missing.dat");
 }
}''')
            计算机.命令('javac FileDemo.java', ['Exit: 0'])
            计算机.命令('java FileDemo', ['FileNotFoundException', 'Exit: 1'])
            计算机.命令('run hello recovered', ['Exit: 0'])
            结果[种类值] = 计算机.日志记录.decode('utf-8', 'replace')
        finally:
            计算机.关闭()
        print('PASS:', 种类值, '게스트 Java 文件 生成/追加继续状态/字节值/EOF/是否已关闭/失败值/OpenJDK 교차 执行命令', flush=True)
    (位置 / 'build/Java文件测试.json').write_text(json.dumps(结果, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    执行命令()
