#!/usr/bin/env python3
import hashlib,json,subprocess
from ئىجرا_قىلىش_بۇيرۇق import كۆرسىتىش_يىلتىز

def ئىجرا_قىل_2():
    ئۆلچەم_مەلۇمات=كۆرسىتىش_يىلتىز/'build/verification/stream';ئۆلچەم_مەلۇمات.mkdir(parents=True,exist_ok=True)
    دەلىللەش_خەۋەر={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((كۆرسىتىش_يىلتىز/'build/kernel8.img').read_bytes()).hexdigest()}
    try:
        subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ئۆلچەم_مەلۇمات),str(كۆرسىتىش_يىلتىز/'시험/자바/흐름시험.java')])
        مەلۇمات_ئورۇنلاشتۇرۇش=subprocess.run(['python3',str(كۆرسىتىش_يىلتىز/'قوراللار/ئىجرا_قىلىش_ھۆججەت.py'),str(ئۆلچەم_مەلۇمات/'흐름시험.class')],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        (ئۆلچەم_مەلۇمات/'serial.log').write_bytes(مەلۇمات_ئورۇنلاشتۇرۇش.stdout);assert مەلۇمات_ئورۇنلاشتۇرۇش.returncode==0,مەلۇمات_ئورۇنلاشتۇرۇش.stdout.decode('utf-8','replace')
        تېكىست=مەلۇمات_ئورۇنلاشتۇرۇش.stdout.decode('utf-8').replace('\r\n','\n');assert '\ntrue\n42\n-1\n시간 제한\nDNS 미지원\nSTREAM PASS\nexit 0\n' in تېكىست,تېكىست
        دەلىللەش_خەۋەر.update(passed=True,checks=['Socket/ServerSocket connect/accept and local/peer ports','UTF-8 byte array slice I/O and bidirectional reply','EOF after peer close','accept timeout and listener port reuse','unsupported DNS name throws an exception'])
        print('PASS: own JVM stream sockets, UTF-8, EOF, timeout, port reuse')
    finally:(ئۆلچەم_مەلۇمات/'report.json').write_text(json.dumps(دەلىللەش_خەۋەر,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ئىجرا_قىل_2()
