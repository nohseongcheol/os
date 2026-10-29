#!/usr/bin/env python3
import hashlib,json,subprocess
from изпълнявам_команда import проект_корен

def Стартиране():
    мярка_данни=проект_корен/'build/verification/stream';мярка_данни.mkdir(parents=True,exist_ok=True)
    проверка_отчет={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((проект_корен/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(мярка_данни),str(проект_корен/'시험/자바/흐름시험.java')])
        данни_позиция=subprocess.run(['python3',str(проект_корен/'Инструменти/изпълнявам_Файл.py'),str(мярка_данни/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (мярка_данни/'serial.log').write_bytes(данни_позиция.stdout);assert данни_позиция.returncode==0,данни_позиция.stdout.decode('utf-8','replace')
        Текст=данни_позиция.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in Текст,Текст
        проверка_отчет.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(мярка_данни/'report.json').write_text(json.dumps(проверка_отчет,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Стартиране()
