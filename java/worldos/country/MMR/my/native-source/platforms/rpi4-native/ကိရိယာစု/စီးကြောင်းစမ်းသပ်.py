#!/usr/bin/env python3
import hashlib,json,subprocess
from စက်မောင်း import စီမံကိန်းအမြစ်

def လုပ်ဆောင်():
    ရလဒ်ဒေတာ=စီမံကိန်းအမြစ်/'build/verification/stream';ရလဒ်ဒေတာ.mkdir(parents=True,exist_ok=True)
    검증기록={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((စီမံကိန်းအမြစ်/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ရလဒ်ဒေတာ),str(စီမံကိန်းအမြစ်/'စမ်းသပ်မှု/Java/စီးကြောင်းစမ်းသပ်.java')])
        ဒေတာနေရာ=subprocess.run(['python3',str(စီမံကိန်းအမြစ်/'ကိရိယာစု/ဖိုင်လုပ်ဆောင်.py'),str(ရလဒ်ဒေတာ/'စီးကြောင်းစမ်းသပ်.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (ရလဒ်ဒေတာ/'serial.log').write_bytes(ဒေတာနေရာ.stdout);assert ဒေတာနေရာ.returncode==0,ဒေတာနေရာ.stdout.decode('utf-8','replace')
        စာသား=ဒေတာနေရာ.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 ကန့်သတ်ချက်တန်ဖိုး\nDNS 미지원\nSTREAM PASS\nexit 0\n' in စာသား,စာသား
        검증기록.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(ရလဒ်ဒေတာ/'report.json').write_text(json.dumps(검증기록,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':လုပ်ဆောင်()
