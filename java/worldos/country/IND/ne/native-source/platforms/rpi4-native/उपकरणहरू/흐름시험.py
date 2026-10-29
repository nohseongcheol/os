#!/usr/bin/env python3
import hashlib,json,subprocess
from कार्यान्वयन_गर्नुहोस्_आदेश import परियोजना_रूट

def चलाउनुहोस्():
    मापन_लगत=परियोजना_रूट/'build/verification/stream';मापन_लगत.mkdir(parents=True,exist_ok=True)
    वैधानिकता_रिपोर्ट={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((परियोजना_रूट/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(मापन_लगत),str(परियोजना_रूट/'시험/자바/흐름시험.java')])
        लगत_राख्नुहोस्=subprocess.run(['python3',str(परियोजना_रूट/'उपकरणहरू/कार्यान्वयन_गर्नुहोस्_फाइल.py'),str(मापन_लगत/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (मापन_लगत/'serial.log').write_bytes(लगत_राख्नुहोस्.stdout);assert लगत_राख्नुहोस्.returncode==0,लगत_राख्नुहोस्.stdout.decode('utf-8','replace')
        पाठ=लगत_राख्नुहोस्.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in पाठ,पाठ
        वैधानिकता_रिपोर्ट.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(मापन_लगत/'report.json').write_text(json.dumps(वैधानिकता_रिपोर्ट,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':चलाउनुहोस्()
