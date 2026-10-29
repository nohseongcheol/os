#!/usr/bin/env python3
import hashlib,json,subprocess
from icra_etmək_əmr import Project_kök

def İcra_Et():
    ölçü_verilənlər=Project_kök/'build/verification/stream';ölçü_verilənlər.mkdir(parents=True,exist_ok=True)
    yoxlama_hesabat={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_kök/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ölçü_verilənlər),str(Project_kök/'시험/자바/흐름시험.java')])
        verilənlər_yerinə_qoymaq=subprocess.run(['python3',str(Project_kök/'Alətlər/icra_etmək_fayl.py'),str(ölçü_verilənlər/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (ölçü_verilənlər/'serial.log').write_bytes(verilənlər_yerinə_qoymaq.stdout);assert verilənlər_yerinə_qoymaq.returncode==0,verilənlər_yerinə_qoymaq.stdout.decode('utf-8','replace')
        Mətn=verilənlər_yerinə_qoymaq.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in Mətn,Mətn
        yoxlama_hesabat.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(ölçü_verilənlər/'report.json').write_text(json.dumps(yoxlama_hesabat,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':İcra_Et()
