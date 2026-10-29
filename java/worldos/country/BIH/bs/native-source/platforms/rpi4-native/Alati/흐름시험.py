#!/usr/bin/env python3
import hashlib,json,subprocess
from Izvrši_komanda import projicirati_koijen

def Pokreni():
    mjera_podaci=projicirati_koijen/'build/verification/stream';mjera_podaci.mkdir(parents=True,exist_ok=True)
    provjera_izvještaj={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((projicirati_koijen/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(mjera_podaci),str(projicirati_koijen/'시험/자바/흐름시험.java')])
        podaci_položaj=subprocess.run(['python3',str(projicirati_koijen/'Alati/Izvrši_fajl.py'),str(mjera_podaci/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (mjera_podaci/'serial.log').write_bytes(podaci_položaj.stdout);assert podaci_položaj.returncode==0,podaci_položaj.stdout.decode('utf-8','replace')
        Tekst=podaci_položaj.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in Tekst,Tekst
        provjera_izvještaj.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(mjera_podaci/'report.json').write_text(json.dumps(provjera_izvještaj,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Pokreni()
