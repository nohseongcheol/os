#!/usr/bin/env python3
import hashlib,json,subprocess
from gnìomhaich_àithne import tilg_freumh

def ruith():
    tomhas_dàta=tilg_freumh/'build/verification/stream';tomhas_dàta.mkdir(parents=True,exist_ok=True)
    dearbhadh_aithisg={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((tilg_freumh/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(tomhas_dàta),str(tilg_freumh/'시험/자바/흐름시험.java')])
        dàta_suidhich=subprocess.run(['python3',str(tilg_freumh/'innealan/gnìomhaich_faidhle.py'),str(tomhas_dàta/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (tomhas_dàta/'serial.log').write_bytes(dàta_suidhich.stdout);assert dàta_suidhich.returncode==0,dàta_suidhich.stdout.decode('utf-8','replace')
        SMS=dàta_suidhich.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in SMS,SMS
        dearbhadh_aithisg.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(tomhas_dàta/'report.json').write_text(json.dumps(dearbhadh_aithisg,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ruith()
