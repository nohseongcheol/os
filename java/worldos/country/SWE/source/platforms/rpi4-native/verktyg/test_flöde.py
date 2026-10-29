#!/usr/bin/env python3
import hashlib,json,subprocess
from köra_kommando import åtgärd_rot

def Kör():
    KR_data=åtgärd_rot/'build/verification/stream';KR_data.mkdir(parents=True,exist_ok=True)
    validering_Rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((åtgärd_rot/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_data),str(åtgärd_rot/'tester/자바/test_flöde.java')])
        data_placera=subprocess.run(['python3',str(åtgärd_rot/'verktyg/köra_fil.py'),str(KR_data/'test_flöde.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (KR_data/'serial.log').write_bytes(data_placera.stdout);assert data_placera.returncode==0,data_placera.stdout.decode('utf-8','replace')
        text=data_placera.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in text,text
        validering_Rapport.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(KR_data/'report.json').write_text(json.dumps(validering_Rapport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Kör()
