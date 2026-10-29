#!/usr/bin/env python3
import hashlib,json,subprocess
from निष्पादित_करें_आदेश import प्रोजेक्ट_करें_मूल

def चलाएँ():
    परिणाम_डेटा=प्रोजेक्ट_करें_मूल/'build/verification/stream';परिणाम_डेटा.mkdir(parents=True,exist_ok=True)
    प्रमाणीकरण_रिपोर्ट={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((प्रोजेक्ट_करें_मूल/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(परिणाम_डेटा),str(प्रोजेक्ट_करें_मूल/'시험/자바/흐름시험.java')])
        डेटा_पद=subprocess.run(['python3',str(प्रोजेक्ट_करें_मूल/'उपकरण/निष्पादित_करें_फ़ाइल.py'),str(परिणाम_डेटा/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (परिणाम_डेटा/'serial.log').write_bytes(डेटा_पद.stdout);assert डेटा_पद.returncode==0,डेटा_पद.stdout.decode('utf-8','replace')
        पाठ=डेटा_पद.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in पाठ,पाठ
        प्रमाणीकरण_रिपोर्ट.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(परिणाम_डेटा/'report.json').write_text(json.dumps(प्रमाणीकरण_रिपोर्ट,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':चलाएँ()
