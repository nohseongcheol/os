#!/usr/bin/env python3
import hashlib,json,subprocess
from Esegui_comando import azione_radice

def avvia():
    KR_dati=azione_radice/'build/verification/stream';KR_dati.mkdir(parents=True,exist_ok=True)
    convalida_Report={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((azione_radice/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_dati),str(azione_radice/'prove/자바/test_Stream.java')])
        dati_funzione=subprocess.run(['python3',str(azione_radice/'strumenti/Esegui_File.py'),str(KR_dati/'test_Stream.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (KR_dati/'serial.log').write_bytes(dati_funzione.stdout);assert dati_funzione.returncode==0,dati_funzione.stdout.decode('utf-8','replace')
        testo=dati_funzione.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in testo,testo
        convalida_Report.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(KR_dati/'report.json').write_text(json.dumps(convalida_Report,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':avvia()
