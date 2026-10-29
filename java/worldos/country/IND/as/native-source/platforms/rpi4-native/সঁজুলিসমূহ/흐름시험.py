#!/usr/bin/env python3
import hashlib,json,subprocess
from নিষ্পাদন_আদেশ import 기준

def সঞ্চালন():
    পৰিমাপ_ডাটা=기준/'build/verification/stream';পৰিমাপ_ডাটা.mkdir(parents=True,exist_ok=True)
    বৈধতা_ৰিপ_ৰ্ট={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(পৰিমাপ_ডাটা),str(기준/'시험/자바/흐름시험.java')])
        ডাটা_স্থান_সলনি_কৰক=subprocess.run(['python3',str(기준/'সঁজুলিসমূহ/নিষ্পাদন_ফাইল.py'),str(পৰিমাপ_ডাটা/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (পৰিমাপ_ডাটা/'serial.log').write_bytes(ডাটা_স্থান_সলনি_কৰক.stdout);assert ডাটা_স্থান_সলনি_কৰক.returncode==0,ডাটা_স্থান_সলনি_কৰক.stdout.decode('utf-8','replace')
        টেক্সট=ডাটা_স্থান_সলনি_কৰক.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in টেক্সট,টেক্সট
        বৈধতা_ৰিপ_ৰ্ট.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(পৰিমাপ_ডাটা/'report.json').write_text(json.dumps(বৈধতা_ৰিপ_ৰ্ট,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':সঞ্চালন()
