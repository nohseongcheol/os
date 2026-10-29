#!/usr/bin/env python3
import hashlib,json,subprocess
from ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ import ਪ੍ਰੋਜੈਕਟ_ਰੂਟ

def ਚਲਾਓ_2():
    ਮਾਪ_ਸਮੱਗਰੀ=ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/verification/stream';ਮਾਪ_ਸਮੱਗਰੀ.mkdir(parents=True,exist_ok=True)
    ਮਾਨਤਾ_ਵਿਵਰਨ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ਮਾਪ_ਸਮੱਗਰੀ),str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'시험/자바/흐름시험.java')])
        ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ=subprocess.run(['python3',str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'ਸਾਧਨ/ਅਮਲ_ਕਰੋ_ਲਿਖਤ_ਪੱਤਰ.py'),str(ਮਾਪ_ਸਮੱਗਰੀ/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (ਮਾਪ_ਸਮੱਗਰੀ/'serial.log').write_bytes(ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.stdout);assert ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.returncode==0,ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.stdout.decode('utf-8','replace')
        ਟੈਕਸਟ=ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in ਟੈਕਸਟ,ਟੈਕਸਟ
        ਮਾਨਤਾ_ਵਿਵਰਨ.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(ਮਾਪ_ਸਮੱਗਰੀ/'report.json').write_text(json.dumps(ਮਾਨਤਾ_ਵਿਵਰਨ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ਚਲਾਓ_2()
