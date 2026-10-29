#!/usr/bin/env python3
import hashlib,json,subprocess
from 실행 import 기준

def Oetveure():
    결과자료=기준/'build/verification/stream';결과자료.mkdir(parents=True,exist_ok=True)
    검증기록={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(기준/'시험/자바/흐름시험.java')])
        자료위치=subprocess.run(['python3',str(기준/'도구/파일실행.py'),str(결과자료/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (결과자료/'serial.log').write_bytes(자료위치.stdout);assert 자료위치.returncode==0,자료위치.stdout.decode('utf-8','replace')
        Teks=자료위치.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in Teks,Teks
        검증기록.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(결과자료/'report.json').write_text(json.dumps(검증기록,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Oetveure()
