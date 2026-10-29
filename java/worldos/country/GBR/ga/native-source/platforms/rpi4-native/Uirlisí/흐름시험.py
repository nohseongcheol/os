#!/usr/bin/env python3
import hashlib,json,subprocess
from Rith_ordú import teilgean_fréamh

def Rith_2():
    tomhas_sonraí=teilgean_fréamh/'build/verification/stream';tomhas_sonraí.mkdir(parents=True,exist_ok=True)
    bailíochtú_tuairisc={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((teilgean_fréamh/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(tomhas_sonraí),str(teilgean_fréamh/'시험/자바/흐름시험.java')])
        sonraí_suíomh=subprocess.run(['python3',str(teilgean_fréamh/'Uirlisí/Rith_comhad.py'),str(tomhas_sonraí/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (tomhas_sonraí/'serial.log').write_bytes(sonraí_suíomh.stdout);assert sonraí_suíomh.returncode==0,sonraí_suíomh.stdout.decode('utf-8','replace')
        Téacs=sonraí_suíomh.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in Téacs,Téacs
        bailíochtú_tuairisc.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(tomhas_sonraí/'report.json').write_text(json.dumps(bailíochtú_tuairisc,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Rith_2()
