#!/usr/bin/env python3
import hashlib,json,subprocess
from અમલ_કરો_આદેશ import પ્રોજેક્ટ_રૂટ

def ચલાવો_2():
    પરિમાણ_ડેટા=પ્રોજેક્ટ_રૂટ/'build/verification/stream';પરિમાણ_ડેટા.mkdir(parents=True,exist_ok=True)
    માન્યતા_અહેવાલ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((પ્રોજેક્ટ_રૂટ/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(પરિમાણ_ડેટા),str(પ્રોજેક્ટ_રૂટ/'시험/자바/흐름시험.java')])
        ડેટા_સ્થિતિ=subprocess.run(['python3',str(પ્રોજેક્ટ_રૂટ/'ઉપકરણો/અમલ_કરો_ફાઇલ.py'),str(પરિમાણ_ડેટા/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (પરિમાણ_ડેટા/'serial.log').write_bytes(ડેટા_સ્થિતિ.stdout);assert ડેટા_સ્થિતિ.returncode==0,ડેટા_સ્થિતિ.stdout.decode('utf-8','replace')
        લખાણ=ડેટા_સ્થિતિ.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in લખાણ,લખાણ
        માન્યતા_અહેવાલ.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(પરિમાણ_ડેટા/'report.json').write_text(json.dumps(માન્યતા_અહેવાલ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ચલાવો_2()
