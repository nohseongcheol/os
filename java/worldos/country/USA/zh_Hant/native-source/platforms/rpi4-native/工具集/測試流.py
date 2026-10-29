#!/usr/bin/env python3
import hashlib,json,subprocess
from 執行命令 import 項目根

def 運行():
    結果資料=項目根/'build/verification/stream';結果資料.mkdir(parents=True,exist_ok=True)
    有效性驗證報告={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((項目根/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(結果資料),str(項目根/'測試/Java/測試流.java')])
        資料位置=subprocess.run(['python3',str(項目根/'工具集/執行檔案.py'),str(結果資料/'測試流.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (結果資料/'serial.log').write_bytes(資料位置.stdout);assert 資料位置.returncode==0,資料位置.stdout.decode('utf-8','replace')
        文本=資料位置.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 限制值\nDNS 是否不支持\nSTREAM PASS\nexit 0\n' in 文本,文本
        有效性驗證報告.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(結果資料/'report.json').write_text(json.dumps(有效性驗證報告,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':運行()
