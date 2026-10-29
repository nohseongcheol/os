#!/usr/bin/env python3
import hashlib,json,subprocess
from eżegwixxa_kmand import pprojetta_għerq

def serje():
    miżura_data=pprojetta_għerq/'build/verification/stream';miżura_data.mkdir(parents=True,exist_ok=True)
    validazzjoni_rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((pprojetta_għerq/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(miżura_data),str(pprojetta_għerq/'시험/자바/흐름시험.java')])
        data_pożizzjoni=subprocess.run(['python3',str(pprojetta_għerq/'Għodod/eżegwixxa_fajl.py'),str(miżura_data/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (miżura_data/'serial.log').write_bytes(data_pożizzjoni.stdout);assert data_pożizzjoni.returncode==0,data_pożizzjoni.stdout.decode('utf-8','replace')
        SMS=data_pożizzjoni.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in SMS,SMS
        validazzjoni_rapport.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(miżura_data/'report.json').write_text(json.dumps(validazzjoni_rapport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':serje()
