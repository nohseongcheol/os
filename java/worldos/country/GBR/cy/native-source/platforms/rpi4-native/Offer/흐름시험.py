#!/usr/bin/env python3
import hashlib,json,subprocess
from Gweithredu_gorchymyn import prosiect_gwraidd

def Gweithredu_2():
    mesur_data=prosiect_gwraidd/'build/verification/stream';mesur_data.mkdir(parents=True,exist_ok=True)
    dilysu_adrodd={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((prosiect_gwraidd/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(mesur_data),str(prosiect_gwraidd/'시험/자바/흐름시험.java')])
        data_safle=subprocess.run(['python3',str(prosiect_gwraidd/'Offer/Gweithredu_ffeil.py'),str(mesur_data/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (mesur_data/'serial.log').write_bytes(data_safle.stdout);assert data_safle.returncode==0,data_safle.stdout.decode('utf-8','replace')
        Testun=data_safle.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in Testun,Testun
        dilysu_adrodd.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(mesur_data/'report.json').write_text(json.dumps(dilysu_adrodd,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Gweithredu_2()
