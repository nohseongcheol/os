#!/usr/bin/env python3
import hashlib,json,subprocess
from uitvoer_bevel import Project_wortel

def Loop():
    maatreël_data=Project_wortel/'build/verification/stream';maatreël_data.mkdir(parents=True,exist_ok=True)
    validering_verslag={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_wortel/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(maatreël_data),str(Project_wortel/'시험/자바/흐름시험.java')])
        data_plaas=subprocess.run(['python3',str(Project_wortel/'Nutsmiddels/uitvoer_lêer.py'),str(maatreël_data/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (maatreël_data/'serial.log').write_bytes(data_plaas.stdout);assert data_plaas.returncode==0,data_plaas.stdout.decode('utf-8','replace')
        Teks=data_plaas.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in Teks,Teks
        validering_verslag.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(maatreël_data/'report.json').write_text(json.dumps(validering_verslag,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Loop()
