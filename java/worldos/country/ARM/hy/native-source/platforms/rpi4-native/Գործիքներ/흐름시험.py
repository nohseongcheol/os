#!/usr/bin/env python3
import hashlib,json,subprocess
from կատարել_հրաման import արձակել_արմատ

def Գործարկել():
    չափ_տվյալ=արձակել_արմատ/'build/verification/stream';չափ_տվյալ.mkdir(parents=True,exist_ok=True)
    վավերացում_զեկույց={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((արձակել_արմատ/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(չափ_տվյալ),str(արձակել_արմատ/'시험/자바/흐름시험.java')])
        տվյալ_դիրք=subprocess.run(['python3',str(արձակել_արմատ/'Գործիքներ/կատարել_նիշք.py'),str(չափ_տվյալ/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (չափ_տվյալ/'serial.log').write_bytes(տվյալ_դիրք.stdout);assert տվյալ_դիրք.returncode==0,տվյալ_դիրք.stdout.decode('utf-8','replace')
        Տեքստ=տվյալ_դիրք.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in Տեքստ,Տեքստ
        վավերացում_զեկույց.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(չափ_տվյալ/'report.json').write_text(json.dumps(վավերացում_զեկույց,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Գործարկել()
