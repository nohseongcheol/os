#!/usr/bin/env python3
import hashlib,json,subprocess
from Vykonať_príkaz import akcia_koreň

def Spustiť_2():
    KR_údaje=akcia_koreň/'build/verification/stream';KR_údaje.mkdir(parents=True,exist_ok=True)
    overenie_správa={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((akcia_koreň/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_údaje),str(akcia_koreň/'시험/자바/test_Stream.java')])
        údaje_pozícia=subprocess.run(['python3',str(akcia_koreň/'Nástroje/Vykonať_Súbor.py'),str(KR_údaje/'test_Stream.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (KR_údaje/'serial.log').write_bytes(údaje_pozícia.stdout);assert údaje_pozícia.returncode==0,údaje_pozícia.stdout.decode('utf-8','replace')
        Spracovanie_textu=údaje_pozícia.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in Spracovanie_textu,Spracovanie_textu
        overenie_správa.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(KR_údaje/'report.json').write_text(json.dumps(overenie_správa,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Spustiť_2()
