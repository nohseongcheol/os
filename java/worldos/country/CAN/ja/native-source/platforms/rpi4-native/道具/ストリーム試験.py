#!/usr/bin/env python3
import hashlib,json,subprocess
from 命令実行 import 計画根

def 起動処理():
    結果データ=計画根/'build/verification/stream';結果データ.mkdir(parents=True,exist_ok=True)
    妥当性報告={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((計画根/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(結果データ),str(計画根/'試験/Java/ストリーム試験.java')])
        データ位置=subprocess.run(['python3',str(計画根/'道具/ファイル実行.py'),str(結果データ/'ストリーム試験.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (結果データ/'serial.log').write_bytes(データ位置.stdout);assert データ位置.returncode==0,データ位置.stdout.decode('utf-8','replace')
        文=データ位置.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 上限値\nDNS 判定未対応\nSTREAM PASS\nexit 0\n' in 文,文
        妥当性報告.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(結果データ/'report.json').write_text(json.dumps(妥当性報告,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':起動処理()
