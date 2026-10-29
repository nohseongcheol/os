#!/usr/bin/env python3
import hashlib,json,subprocess
from ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ import ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍

def ଚଳାନ୍ତୁ():
    ମାପ_ଡାଟା=ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/verification/stream';ମାପ_ଡାଟା.mkdir(parents=True,exist_ok=True)
    ବୈଧକରଣ_ରିପୋର୍ଟ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ମାପ_ଡାଟା),str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'시험/자바/흐름시험.java')])
        ଡାଟା_ସ୍ଥିତି=subprocess.run(['python3',str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'ଉପକରଣସମୂହ/ନିର୍ବାହ_କରିବା_ଫାଇଲ୍.py'),str(ମାପ_ଡାଟା/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (ମାପ_ଡାଟା/'serial.log').write_bytes(ଡାଟା_ସ୍ଥିତି.stdout);assert ଡାଟା_ସ୍ଥିତି.returncode==0,ଡାଟା_ସ୍ଥିତି.stdout.decode('utf-8','replace')
        ପାଠ୍ଯ=ଡାଟା_ସ୍ଥିତି.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in ପାଠ୍ଯ,ପାଠ୍ଯ
        ବୈଧକରଣ_ରିପୋର୍ଟ.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(ମାପ_ଡାଟା/'report.json').write_text(json.dumps(ବୈଧକରଣ_ରିପୋର୍ଟ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ଚଳାନ୍ତୁ()
