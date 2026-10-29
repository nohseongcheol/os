#!/usr/bin/env python3
import hashlib,json,subprocess
from kawe_tono import whakaatu_pūtake

def whakahaere():
    mēhua_raraunga=whakaatu_pūtake/'build/verification/stream';mēhua_raraunga.mkdir(parents=True,exist_ok=True)
    whakamana_pūrongo={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((whakaatu_pūtake/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(mēhua_raraunga),str(whakaatu_pūtake/'시험/자바/흐름시험.java')])
        raraunga_tūranga=subprocess.run(['python3',str(whakaatu_pūtake/'Ngā_Utauta/kawe_kōnae.py'),str(mēhua_raraunga/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (mēhua_raraunga/'serial.log').write_bytes(raraunga_tūranga.stdout);assert raraunga_tūranga.returncode==0,raraunga_tūranga.stdout.decode('utf-8','replace')
        Ngā_kupu=raraunga_tūranga.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in Ngā_kupu,Ngā_kupu
        whakamana_pūrongo.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(mēhua_raraunga/'report.json').write_text(json.dumps(whakamana_pūrongo,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':whakahaere()
