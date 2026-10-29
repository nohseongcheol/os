#!/usr/bin/env python3
import hashlib,json,subprocess
from befehlAusführen import projektWurzel

def ausführenVorgang():
    ergebnisDaten=projektWurzel/'build/verification/stream';ergebnisDaten.mkdir(parents=True,exist_ok=True)
    validierungBericht={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((projektWurzel/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ergebnisDaten),str(projektWurzel/'Prüfungen/Java/datenstromPrüfung.java')])
        datenPosition=subprocess.run(['python3',str(projektWurzel/'Werkzeuge/dateiAusführen.py'),str(ergebnisDaten/'datenstromPrüfung.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (ergebnisDaten/'serial.log').write_bytes(datenPosition.stdout);assert datenPosition.returncode==0,datenPosition.stdout.decode('utf-8','replace')
        Text=datenPosition.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 grenzwertWert\nDNS istNichtUnterstützt\nSTREAM PASS\nexit 0\n' in Text,Text
        validierungBericht.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(ergebnisDaten/'report.json').write_text(json.dumps(validierungBericht,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ausführenVorgang()
