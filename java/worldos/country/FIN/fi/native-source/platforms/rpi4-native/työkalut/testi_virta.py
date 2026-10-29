#!/usr/bin/env python3
import hashlib,json,subprocess
from Suorita_komento import aloite_juuri

def Suorita_2():
    KR_data=aloite_juuri/'build/verification/stream';KR_data.mkdir(parents=True,exist_ok=True)
    vahvistus_raportti={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((aloite_juuri/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_data),str(aloite_juuri/'testit/자바/testi_virta.java')])
        data_toimi=subprocess.run(['python3',str(aloite_juuri/'työkalut/Suorita_Tiedosto.py'),str(KR_data/'testi_virta.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (KR_data/'serial.log').write_bytes(data_toimi.stdout);assert data_toimi.returncode==0,data_toimi.stdout.decode('utf-8','replace')
        teksti=data_toimi.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in teksti,teksti
        vahvistus_raportti.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(KR_data/'report.json').write_text(json.dumps(vahvistus_raportti,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Suorita_2()
