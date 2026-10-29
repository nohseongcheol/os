#!/usr/bin/env python3
import hashlib,json,subprocess
from Vykdyti_komanda import Project_šaknis

def Paleisti():
    KR_duomenys=Project_šaknis/'build/verification/stream';KR_duomenys.mkdir(parents=True,exist_ok=True)
    tikrinimas_pranešti={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_šaknis/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_duomenys),str(Project_šaknis/'시험/자바/흐름시험.java')])
        duomenys_padėtis=subprocess.run(['python3',str(Project_šaknis/'Įrankiai/Vykdyti_Failas.py'),str(KR_duomenys/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (KR_duomenys/'serial.log').write_bytes(duomenys_padėtis.stdout);assert duomenys_padėtis.returncode==0,duomenys_padėtis.stdout.decode('utf-8','replace')
        Tekstas=duomenys_padėtis.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in Tekstas,Tekstas
        tikrinimas_pranešti.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(KR_duomenys/'report.json').write_text(json.dumps(tikrinimas_pranešti,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Paleisti()
