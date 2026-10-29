#!/usr/bin/env python3
import hashlib,json,subprocess
from Udfør_kommando import To_do_rod

def Kør_2():
    KR_data=To_do_rod/'build/verification/stream';KR_data.mkdir(parents=True,exist_ok=True)
    validering_rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((To_do_rod/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_data),str(To_do_rod/'시험/자바/test_strøm.java')])
        data_placere=subprocess.run(['python3',str(To_do_rod/'Værktøjer/Udfør_fil.py'),str(KR_data/'test_strøm.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (KR_data/'serial.log').write_bytes(data_placere.stdout);assert data_placere.returncode==0,data_placere.stdout.decode('utf-8','replace')
        Tekst=data_placere.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in Tekst,Tekst
        validering_rapport.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(KR_data/'report.json').write_text(json.dumps(validering_rapport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Kør_2()
