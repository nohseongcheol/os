#!/usr/bin/env python3
import hashlib,json,subprocess
from Provést_příkaz import akce_kořen

def Spustit_2():
    KV_data=akce_kořen/'build/verification/stream';KV_data.mkdir(parents=True,exist_ok=True)
    ověření_Zpráva={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((akce_kořen/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KV_data),str(akce_kořen/'zkoušky/자바/test_tok.java')])
        data_pozice=subprocess.run(['python3',str(akce_kořen/'nástroje/Provést_Soubor.py'),str(KV_data/'test_tok.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (KV_data/'serial.log').write_bytes(data_pozice.stdout);assert data_pozice.returncode==0,data_pozice.stdout.decode('utf-8','replace')
        text=data_pozice.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in text,text
        ověření_Zpráva.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(KV_data/'report.json').write_text(json.dumps(ověření_Zpráva,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Spustit_2()
