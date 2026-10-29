#!/usr/bin/env python3
import hashlib,json,subprocess
from Uitvoeren_opdracht import Taken_wortel

def starten():
    HR_gegevens=Taken_wortel/'build/verification/stream';HR_gegevens.mkdir(parents=True,exist_ok=True)
    validatie_Rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Taken_wortel/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(HR_gegevens),str(Taken_wortel/'tests/자바/test_Stream.java')])
        gegevens_functie=subprocess.run(['python3',str(Taken_wortel/'hulpmiddelen/Uitvoeren_Bestand.py'),str(HR_gegevens/'test_Stream.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (HR_gegevens/'serial.log').write_bytes(gegevens_functie.stdout);assert gegevens_functie.returncode==0,gegevens_functie.stdout.decode('utf-8','replace')
        tekst=gegevens_functie.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in tekst,tekst
        validatie_Rapport.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(HR_gegevens/'report.json').write_text(json.dumps(validatie_Rapport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':starten()
