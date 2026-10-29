#!/usr/bin/env python3
import hashlib,json,subprocess
from Изврши_команда import пројектовати_корен

def Покрени():
    мера_подаци=пројектовати_корен/'build/verification/stream';мера_подаци.mkdir(parents=True,exist_ok=True)
    провјера_извештај={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((пројектовати_корен/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(мера_подаци),str(пројектовати_корен/'시험/자바/흐름시험.java')])
        подаци_позиција=subprocess.run(['python3',str(пројектовати_корен/'Алатке/Изврши_фајл.py'),str(мера_подаци/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (мера_подаци/'serial.log').write_bytes(подаци_позиција.stdout);assert подаци_позиција.returncode==0,подаци_позиција.stdout.decode('utf-8','replace')
        Текст=подаци_позиција.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in Текст,Текст
        провјера_извештај.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(мера_подаци/'report.json').write_text(json.dumps(провјера_извештај,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Покрени()
