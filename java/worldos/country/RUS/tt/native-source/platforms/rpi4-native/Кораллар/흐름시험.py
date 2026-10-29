#!/usr/bin/env python3
import hashlib,json,subprocess
from үтәргә_команда import экранга_җибәрү_тамыр

def эшләтү():
    үлчәм_мәгълүмат=экранга_җибәрү_тамыр/'build/verification/stream';үлчәм_мәгълүмат.mkdir(parents=True,exist_ok=True)
    раслау_отчет={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((экранга_җибәрү_тамыр/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(үлчәм_мәгълүмат),str(экранга_җибәрү_тамыр/'시험/자바/흐름시험.java')])
        мәгълүмат_урнаштыру=subprocess.run(['python3',str(экранга_җибәрү_тамыр/'Кораллар/үтәргә_файл.py'),str(үлчәм_мәгълүмат/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (үлчәм_мәгълүмат/'serial.log').write_bytes(мәгълүмат_урнаштыру.stdout);assert мәгълүмат_урнаштыру.returncode==0,мәгълүмат_урнаштыру.stdout.decode('utf-8','replace')
        Mäten=мәгълүмат_урнаштыру.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in Mäten,Mäten
        раслау_отчет.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(үлчәм_мәгълүмат/'report.json').write_text(json.dumps(раслау_отчет,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':эшләтү()
