#!/usr/bin/env python3
import hashlib,json,subprocess
from Izvedi_ukaz import pobuda_koren

def Zaženi():
    KR_podatki=pobuda_koren/'build/verification/stream';KR_podatki.mkdir(parents=True,exist_ok=True)
    preverjanje_veljavnosti_prijavi={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((pobuda_koren/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_podatki),str(pobuda_koren/'시험/자바/preskusiti_tok.java')])
        podatki_položaj=subprocess.run(['python3',str(pobuda_koren/'Orodja/Izvedi_Datoteka.py'),str(KR_podatki/'preskusiti_tok.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (KR_podatki/'serial.log').write_bytes(podatki_položaj.stdout);assert podatki_položaj.returncode==0,podatki_položaj.stdout.decode('utf-8','replace')
        Besedilo=podatki_položaj.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in Besedilo,Besedilo
        preverjanje_veljavnosti_prijavi.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(KR_podatki/'report.json').write_text(json.dumps(preverjanje_veljavnosti_prijavi,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Zaženi()
