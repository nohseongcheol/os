#!/usr/bin/env python3
import hashlib,json,subprocess
from Izpildīt_komanda import Project_sakne

def Palaist():
    mērs_dati=Project_sakne/'build/verification/stream';mērs_dati.mkdir(parents=True,exist_ok=True)
    validācija_ziņot={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_sakne/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(mērs_dati),str(Project_sakne/'시험/자바/흐름시험.java')])
        dati_amats=subprocess.run(['python3',str(Project_sakne/'Rīki/Izpildīt_Fails.py'),str(mērs_dati/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (mērs_dati/'serial.log').write_bytes(dati_amats.stdout);assert dati_amats.returncode==0,dati_amats.stdout.decode('utf-8','replace')
        Teksts=dati_amats.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in Teksts,Teksts
        validācija_ziņot.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(mērs_dati/'report.json').write_text(json.dumps(validācija_ziņot,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Palaist()
