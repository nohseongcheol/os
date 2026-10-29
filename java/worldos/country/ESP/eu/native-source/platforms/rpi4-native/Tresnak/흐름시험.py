#!/usr/bin/env python3
import hashlib,json,subprocess
from exekutatu_komando import Project_erro

def Exekutatu_2():
    neurria_datuak=Project_erro/'build/verification/stream';neurria_datuak.mkdir(parents=True,exist_ok=True)
    balidazio_txosten={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_erro/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(neurria_datuak),str(Project_erro/'시험/자바/흐름시험.java')])
        datuak_kargu=subprocess.run(['python3',str(Project_erro/'Tresnak/exekutatu_fitxategi.py'),str(neurria_datuak/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (neurria_datuak/'serial.log').write_bytes(datuak_kargu.stdout);assert datuak_kargu.returncode==0,datuak_kargu.stdout.decode('utf-8','replace')
        Testua=datuak_kargu.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in Testua,Testua
        balidazio_txosten.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(neurria_datuak/'report.json').write_text(json.dumps(balidazio_txosten,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Exekutatu_2()
