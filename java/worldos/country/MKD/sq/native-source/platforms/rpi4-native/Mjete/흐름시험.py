#!/usr/bin/env python3
import hashlib,json,subprocess
from zbatoj_komandë import Project_rrënjë

def Ekzekuto():
    llogaritje_të_dhëna=Project_rrënjë/'build/verification/stream';llogaritje_të_dhëna.mkdir(parents=True,exist_ok=True)
    miratim_raport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_rrënjë/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(llogaritje_të_dhëna),str(Project_rrënjë/'시험/자바/흐름시험.java')])
        të_dhëna_pozicioni=subprocess.run(['python3',str(Project_rrënjë/'Mjete/zbatoj_skedar.py'),str(llogaritje_të_dhëna/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (llogaritje_të_dhëna/'serial.log').write_bytes(të_dhëna_pozicioni.stdout);assert të_dhëna_pozicioni.returncode==0,të_dhëna_pozicioni.stdout.decode('utf-8','replace')
        Teksti=të_dhëna_pozicioni.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in Teksti,Teksti
        miratim_raport.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(llogaritje_të_dhëna/'report.json').write_text(json.dumps(miratim_raport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Ekzekuto()
