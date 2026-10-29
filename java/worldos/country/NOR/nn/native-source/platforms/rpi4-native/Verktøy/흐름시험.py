#!/usr/bin/env python3
import hashlib,json,subprocess
from Utfør_kommando import spegle_rot

def Køyr_2():
    forretningsmål_data=spegle_rot/'build/verification/stream';forretningsmål_data.mkdir(parents=True,exist_ok=True)
    validering_rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((spegle_rot/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(forretningsmål_data),str(spegle_rot/'시험/자바/흐름시험.java')])
        data_plassere=subprocess.run(['python3',str(spegle_rot/'Verktøy/Utfør_fil.py'),str(forretningsmål_data/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (forretningsmål_data/'serial.log').write_bytes(data_plassere.stdout);assert data_plassere.returncode==0,data_plassere.stdout.decode('utf-8','replace')
        Tekst=data_plassere.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in Tekst,Tekst
        validering_rapport.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(forretningsmål_data/'report.json').write_text(json.dumps(validering_rapport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Køyr_2()
