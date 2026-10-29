#!/usr/bin/env python3
import hashlib,json,subprocess
from Executa_ordre import Project_rel

def Executa_2():
    mesura_dades=Project_rel/'build/verification/stream';mesura_dades.mkdir(parents=True,exist_ok=True)
    validació_informe={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_rel/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(mesura_dades),str(Project_rel/'시험/자바/흐름시험.java')])
        dades_càrrec=subprocess.run(['python3',str(Project_rel/'Eines/Executa_arxiu.py'),str(mesura_dades/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (mesura_dades/'serial.log').write_bytes(dades_càrrec.stdout);assert dades_càrrec.returncode==0,dades_càrrec.stdout.decode('utf-8','replace')
        SMS=dades_càrrec.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in SMS,SMS
        validació_informe.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(mesura_dades/'report.json').write_text(json.dumps(validació_informe,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Executa_2()
