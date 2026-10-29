#!/usr/bin/env python3
import hashlib,json,subprocess
from Wykonaj_polecenie import Project_korzeń

def Uruchom_2():
    KR_dane=Project_korzeń/'build/verification/stream';KR_dane.mkdir(parents=True,exist_ok=True)
    walidacja_Raport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_korzeń/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_dane),str(Project_korzeń/'testy/자바/test_Stream.java')])
        dane_stanowisko=subprocess.run(['python3',str(Project_korzeń/'narzędzia/Wykonaj_Plik.py'),str(KR_dane/'test_Stream.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (KR_dane/'serial.log').write_bytes(dane_stanowisko.stdout);assert dane_stanowisko.returncode==0,dane_stanowisko.stdout.decode('utf-8','replace')
        tekst=dane_stanowisko.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in tekst,tekst
        walidacja_Raport.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(KR_dane/'report.json').write_text(json.dumps(walidacja_Raport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Uruchom_2()
