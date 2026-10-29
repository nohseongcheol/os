#!/usr/bin/env python3
import hashlib,json,subprocess
from ಪೂರೈಸು_ಆದೇಶ import ಬಿಂಬಿಸು_ಮೂಲ

def ಚಲಾಯಿಸು_2():
    ಮಾಪನ_ಡೇಟಾ=ಬಿಂಬಿಸು_ಮೂಲ/'build/verification/stream';ಮಾಪನ_ಡೇಟಾ.mkdir(parents=True,exist_ok=True)
    ದೃಢೀಕರಣ_ವರದಿ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ಬಿಂಬಿಸು_ಮೂಲ/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ಮಾಪನ_ಡೇಟಾ),str(ಬಿಂಬಿಸು_ಮೂಲ/'시험/자바/흐름시험.java')])
        ಡೇಟಾ_ಹುದ್ದೆ=subprocess.run(['python3',str(ಬಿಂಬಿಸು_ಮೂಲ/'ಪರಿಕರಗಳು/ಪೂರೈಸು_ಫೈಲ್.py'),str(ಮಾಪನ_ಡೇಟಾ/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (ಮಾಪನ_ಡೇಟಾ/'serial.log').write_bytes(ಡೇಟಾ_ಹುದ್ದೆ.stdout);assert ಡೇಟಾ_ಹುದ್ದೆ.returncode==0,ಡೇಟಾ_ಹುದ್ದೆ.stdout.decode('utf-8','replace')
        ಪಠ್ಯ=ಡೇಟಾ_ಹುದ್ದೆ.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in ಪಠ್ಯ,ಪಠ್ಯ
        ದೃಢೀಕರಣ_ವರದಿ.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(ಮಾಪನ_ಡೇಟಾ/'report.json').write_text(json.dumps(ದೃಢೀಕರಣ_ವರದಿ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ಚಲಾಯಿಸು_2()
