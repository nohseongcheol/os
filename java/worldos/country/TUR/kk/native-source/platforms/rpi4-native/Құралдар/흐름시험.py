#!/usr/bin/env python3
import hashlib,json,subprocess
from орындау_пәрмен import жоба_түбір

def Орындау_2():
    өлшем_деректер=жоба_түбір/'build/verification/stream';өлшем_деректер.mkdir(parents=True,exist_ok=True)
    тексерім_есеп={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((жоба_түбір/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(өлшем_деректер),str(жоба_түбір/'시험/자바/흐름시험.java')])
        деректер_лауазым=subprocess.run(['python3',str(жоба_түбір/'Құралдар/орындау_файл.py'),str(өлшем_деректер/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (өлшем_деректер/'serial.log').write_bytes(деректер_лауазым.stdout);assert деректер_лауазым.returncode==0,деректер_лауазым.stdout.decode('utf-8','replace')
        Мәтін=деректер_лауазым.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in Мәтін,Мәтін
        тексерім_есеп.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(өлшем_деректер/'report.json').write_text(json.dumps(тексерім_есеп,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Орындау_2()
