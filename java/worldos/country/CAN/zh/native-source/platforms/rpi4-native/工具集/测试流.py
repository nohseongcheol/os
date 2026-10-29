#!/usr/bin/env python3
import hashlib,json,subprocess
from 执行命令 import 项目根

def 运行():
    结果数据=项目根/'build/verification/stream';结果数据.mkdir(parents=True,exist_ok=True)
    有效性验证报告={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((项目根/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(结果数据),str(项目根/'测试/Java/测试流.java')])
        数据位置=subprocess.run(['python3',str(项目根/'工具集/执行文件.py'),str(结果数据/'测试流.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (结果数据/'serial.log').write_bytes(数据位置.stdout);assert 数据位置.returncode==0,数据位置.stdout.decode('utf-8','replace')
        文本=数据位置.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 限制值\nDNS 是否不支持\nSTREAM PASS\nexit 0\n' in 文本,文本
        有效性验证报告.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(结果数据/'report.json').write_text(json.dumps(有效性验证报告,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':运行()
