#!/usr/bin/env python3
import hashlib,json,subprocess
from 실행 import задача_корень

def запустить():
    KR_данные=задача_корень/'build/verification/stream';KR_данные.mkdir(parents=True,exist_ok=True)
    проверка_Отчет={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((задача_корень/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_данные),str(задача_корень/'испытания/자바/тест_поток.java')])
        данные_позиция=subprocess.run(['python3',str(задача_корень/'инструменты/Выполнить_файл.py'),str(KR_данные/'тест_поток.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (KR_данные/'serial.log').write_bytes(данные_позиция.stdout);assert данные_позиция.returncode==0,данные_позиция.stdout.decode('utf-8','replace')
        текст=данные_позиция.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in текст,текст
        проверка_Отчет.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(KR_данные/'report.json').write_text(json.dumps(проверка_Отчет,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':запустить()
