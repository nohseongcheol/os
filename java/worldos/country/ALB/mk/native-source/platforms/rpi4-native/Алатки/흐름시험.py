#!/usr/bin/env python3
import hashlib,json,subprocess
from Изврши_наредба import Project_корен

def Изврши_2():
    мерка_податоци=Project_корен/'build/verification/stream';мерка_податоци.mkdir(parents=True,exist_ok=True)
    проверка_извештај={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_корен/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(мерка_податоци),str(Project_корен/'시험/자바/흐름시험.java')])
        податоци_позиционирање=subprocess.run(['python3',str(Project_корен/'Алатки/Изврши_датотека.py'),str(мерка_податоци/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (мерка_податоци/'serial.log').write_bytes(податоци_позиционирање.stdout);assert податоци_позиционирање.returncode==0,податоци_позиционирање.stdout.decode('utf-8','replace')
        Текст=податоци_позиционирање.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in Текст,Текст
        проверка_извештај.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(мерка_податоци/'report.json').write_text(json.dumps(проверка_извештај,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Изврши_2()
