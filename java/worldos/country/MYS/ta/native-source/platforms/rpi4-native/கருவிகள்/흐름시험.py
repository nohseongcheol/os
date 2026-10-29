#!/usr/bin/env python3
import hashlib,json,subprocess
from இயக்கு_கட்டளை import திட்டப்பணி_மூலம்

def செயல்படுத்துக():
    அளவிடக்கூடியது_தரவு=திட்டப்பணி_மூலம்/'build/verification/stream';அளவிடக்கூடியது_தரவு.mkdir(parents=True,exist_ok=True)
    செல்லுபடியாக்கம்_அறிக்கை={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((திட்டப்பணி_மூலம்/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(அளவிடக்கூடியது_தரவு),str(திட்டப்பணி_மூலம்/'시험/자바/흐름시험.java')])
        தரவு_நிலை=subprocess.run(['python3',str(திட்டப்பணி_மூலம்/'கருவிகள்/இயக்கு_கோப்பு.py'),str(அளவிடக்கூடியது_தரவு/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (அளவிடக்கூடியது_தரவு/'serial.log').write_bytes(தரவு_நிலை.stdout);assert தரவு_நிலை.returncode==0,தரவு_நிலை.stdout.decode('utf-8','replace')
        உரை=தரவு_நிலை.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in உரை,உரை
        செல்லுபடியாக்கம்_அறிக்கை.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(அளவிடக்கூடியது_தரவு/'report.json').write_text(json.dumps(செல்லுபடியாக்கம்_அறிக்கை,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':செயல்படுத்துக()
