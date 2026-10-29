#!/usr/bin/env python3
import hashlib,json,subprocess
from executa_comandă import Project_rădăcină

def Pornește():
    KR_date=Project_rădăcină/'build/verification/stream';KR_date.mkdir(parents=True,exist_ok=True)
    validare_raport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_rădăcină/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_date),str(Project_rădăcină/'시험/자바/흐름시험.java')])
        date_poziție=subprocess.run(['python3',str(Project_rădăcină/'Instrumente/executa_Fișier.py'),str(KR_date/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (KR_date/'serial.log').write_bytes(date_poziție.stdout);assert date_poziție.returncode==0,date_poziție.stdout.decode('utf-8','replace')
        SMS=date_poziție.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in SMS,SMS
        validare_raport.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(KR_date/'report.json').write_text(json.dumps(validare_raport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Pornește()
