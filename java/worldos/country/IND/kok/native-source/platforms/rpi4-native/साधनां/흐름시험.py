#!/usr/bin/env python3
import hashlib,json,subprocess
from पाळो_दिवचो_आदेश import प्रॉजॅक्ट_रूट

def चलोवप():
    मेजप_डेटा=प्रॉजॅक्ट_रूट/'build/verification/stream';मेजप_डेटा.mkdir(parents=True,exist_ok=True)
    वैधताय_अहवाल={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((प्रॉजॅक्ट_रूट/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(मेजप_डेटा),str(प्रॉजॅक्ट_रूट/'시험/자바/흐름시험.java')])
        डेटा_स्थिती=subprocess.run(['python3',str(प्रॉजॅक्ट_रूट/'साधनां/पाळो_दिवचो_फायल.py'),str(मेजप_डेटा/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (मेजप_डेटा/'serial.log').write_bytes(डेटा_स्थिती.stdout);assert डेटा_स्थिती.returncode==0,डेटा_स्थिती.stdout.decode('utf-8','replace')
        SMS=डेटा_स्थिती.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in SMS,SMS
        वैधताय_अहवाल.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(मेजप_डेटा/'report.json').write_text(json.dumps(वैधताय_अहवाल,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':चलोवप()
