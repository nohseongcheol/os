#!/usr/bin/env python3
import hashlib,json,subprocess
from Täida_käsk import Project_juur

def Käivita_2():
    näitaja_andmed=Project_juur/'build/verification/stream';näitaja_andmed.mkdir(parents=True,exist_ok=True)
    kinnitamine_aruanne={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_juur/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(näitaja_andmed),str(Project_juur/'시험/자바/흐름시험.java')])
        andmed_ametikoht=subprocess.run(['python3',str(Project_juur/'Tööriistad/Täida_Fail.py'),str(näitaja_andmed/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (näitaja_andmed/'serial.log').write_bytes(andmed_ametikoht.stdout);assert andmed_ametikoht.returncode==0,andmed_ametikoht.stdout.decode('utf-8','replace')
        Tekst=andmed_ametikoht.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in Tekst,Tekst
        kinnitamine_aruanne.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(näitaja_andmed/'report.json').write_text(json.dumps(kinnitamine_aruanne,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Käivita_2()
