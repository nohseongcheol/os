#!/usr/bin/env python3
import hashlib,json,subprocess
from అమలు_చేయి_ఆదేశం import ప్రొజెక్ట్_మూలం

def నడుపుము():
    ప్రమాణం_డేటా=ప్రొజెక్ట్_మూలం/'build/verification/stream';ప్రమాణం_డేటా.mkdir(parents=True,exist_ok=True)
    నిర్ధారణ_నివేదిక={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ప్రొజెక్ట్_మూలం/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ప్రమాణం_డేటా),str(ప్రొజెక్ట్_మూలం/'시험/자바/흐름시험.java')])
        డేటా_స్థాయి=subprocess.run(['python3',str(ప్రొజెక్ట్_మూలం/'ఉపకరణాలు/అమలు_చేయి_ఫైలు.py'),str(ప్రమాణం_డేటా/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (ప్రమాణం_డేటా/'serial.log').write_bytes(డేటా_స్థాయి.stdout);assert డేటా_స్థాయి.returncode==0,డేటా_స్థాయి.stdout.decode('utf-8','replace')
        పాఠ్యము=డేటా_స్థాయి.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in పాఠ్యము,పాఠ్యము
        నిర్ధారణ_నివేదిక.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(ప్రమాణం_డేటా/'report.json').write_text(json.dumps(నిర్ధారణ_నివేదిక,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':నడుపుము()
