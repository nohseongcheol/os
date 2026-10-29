#!/usr/bin/env python3
import hashlib,json,subprocess
from কার্যকর_করুন_আদেশ import প্রকল্প_মূল

def চালনা():
    পরিমাপ_ডাটা=প্রকল্প_মূল/'build/verification/stream';পরিমাপ_ডাটা.mkdir(parents=True,exist_ok=True)
    বৈধকরণ_রিপোর্ট={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((প্রকল্প_মূল/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(পরিমাপ_ডাটা),str(প্রকল্প_মূল/'시험/자바/흐름시험.java')])
        ডাটা_পদ=subprocess.run(['python3',str(প্রকল্প_মূল/'সরঞ্জামগুলি/কার্যকর_করুন_ফাইল.py'),str(পরিমাপ_ডাটা/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (পরিমাপ_ডাটা/'serial.log').write_bytes(ডাটা_পদ.stdout);assert ডাটা_পদ.returncode==0,ডাটা_পদ.stdout.decode('utf-8','replace')
        পাঠ=ডাটা_পদ.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in পাঠ,পাঠ
        বৈধকরণ_রিপোর্ট.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(পরিমাপ_ডাটা/'report.json').write_text(json.dumps(বৈধকরণ_রিপোর্ট,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':চালনা()
