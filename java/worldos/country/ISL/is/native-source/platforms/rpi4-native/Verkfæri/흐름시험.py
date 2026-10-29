#!/usr/bin/env python3
import hashlib,json,subprocess
from keyra_skipun import verk_rót

def Keyra_2():
    mæld_stærð_gögn=verk_rót/'build/verification/stream';mæld_stærð_gögn.mkdir(parents=True,exist_ok=True)
    prófun_skrá={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((verk_rót/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(mæld_stærð_gögn),str(verk_rót/'시험/자바/흐름시험.java')])
        gögn_staða=subprocess.run(['python3',str(verk_rót/'Verkfæri/keyra_skrá.py'),str(mæld_stærð_gögn/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (mæld_stærð_gögn/'serial.log').write_bytes(gögn_staða.stdout);assert gögn_staða.returncode==0,gögn_staða.stdout.decode('utf-8','replace')
        Texti=gögn_staða.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in Texti,Texti
        prófun_skrá.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(mæld_stærð_gögn/'report.json').write_text(json.dumps(prófun_skrá,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Keyra_2()
