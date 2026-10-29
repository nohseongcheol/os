#!/usr/bin/env python3
import hashlib,json,subprocess
from ausféieren_Befeel import projezéieren_Racinn

def Laf():
    Mooss_Daten=projezéieren_Racinn/'build/verification/stream';Mooss_Daten.mkdir(parents=True,exist_ok=True)
    Validatioun_mellen={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((projezéieren_Racinn/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(Mooss_Daten),str(projezéieren_Racinn/'시험/자바/흐름시험.java')])
        Daten_positionéieren=subprocess.run(['python3',str(projezéieren_Racinn/'Tools/ausféieren_Fichier.py'),str(Mooss_Daten/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (Mooss_Daten/'serial.log').write_bytes(Daten_positionéieren.stdout);assert Daten_positionéieren.returncode==0,Daten_positionéieren.stdout.decode('utf-8','replace')
        SMS=Daten_positionéieren.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in SMS,SMS
        Validatioun_mellen.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(Mooss_Daten/'report.json').write_text(json.dumps(Validatioun_mellen,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Laf()
